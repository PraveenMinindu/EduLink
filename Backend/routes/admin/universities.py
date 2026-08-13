# =============================================================
# EduLink — Admin Universities Routes
# GET    /admin/universities              list
# POST   /admin/universities              create
# GET    /admin/universities/{id}         single
# PATCH  /admin/universities/{id}         update + batch sync
# DELETE /admin/universities/{id}         blocked if programs exist
# =============================================================

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from google.cloud.firestore import SERVER_TIMESTAMP

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from firebase_bridge import get_db
from utils.auth     import verify_admin
from utils.firestore import serialize
from utils.enums    import UniversityType, RecordStatus

router = APIRouter()


# =============================================================
# MODELS — Improvement 3: Enums for constrained fields
# =============================================================

class UniversityCreate(BaseModel):
    name:             str
    type:             UniversityType           # "State" | "Private"
    location:         str
    website:          Optional[str]  = ""
    shortDescription: Optional[str] = ""
    fullDescription:  Optional[str] = ""
    logoUrl:          Optional[str] = ""
    status:           RecordStatus  = RecordStatus.active


class UniversityUpdate(BaseModel):
    name:             Optional[str]            = None
    type:             Optional[UniversityType] = None
    location:         Optional[str]            = None
    website:          Optional[str]            = None
    shortDescription: Optional[str]            = None
    fullDescription:  Optional[str]            = None
    logoUrl:          Optional[str]            = None
    status:           Optional[RecordStatus]   = None


# =============================================================
# HELPERS
# =============================================================

def _batch_sync_university_name(db, university_id: str, new_name: str) -> int:
    """
    Batch-update universityName in all linked degree_programs.
    Called silently when university name changes.
    Returns count of updated documents.
    """
    programs = (
        db.collection("degree_programs")
        .where("universityId", "==", university_id)
        .stream()
    )

    batch   = db.batch()
    updated = 0

    for prog in programs:
        batch.update(prog.reference, {
            "universityName": new_name,
            "updatedAt":      SERVER_TIMESTAMP,
        })
        updated += 1

    if updated > 0:
        batch.commit()

    return updated


# =============================================================
# ROUTES
# Improvement 5: list endpoint designed for future ?search= support
# =============================================================

@router.get("", summary="List universities — supports ?status filter, ready for ?search")
def list_universities(
    status: Optional[RecordStatus] = Query(None, description="Filter by status"),
    search: Optional[str]          = Query(None, description="[Future] Search by name or location"),
    admin:  dict                   = Depends(verify_admin),
):
    """
    Returns universities from Firestore.

    Current filters:
      ?status=Active | Inactive

    Future filter (schema ready, not yet implemented):
      ?search=moratuwa  → will filter by name/location
    """
    db    = get_db()
    query = db.collection("universities")

    if status:
        query = query.where("status", "==", status.value)

    docs = list(query.order_by("name").stream())
    universities = [serialize(d.id, d.to_dict()) for d in docs]

    # Future: client-side search filter placeholder
    # When Firestore full-text search is added, move this server-side
    if search:
        term = search.lower()
        universities = [
            u for u in universities
            if term in u.get("name", "").lower()
            or term in u.get("location", "").lower()
        ]

    return {
        "status": "success",
        "count":  len(universities),
        "data":   universities,
    }


@router.post("", summary="Create a new university", status_code=201)
def create_university(
    body:  UniversityCreate,
    admin: dict = Depends(verify_admin),
):
    db = get_db()

    existing = list(
        db.collection("universities")
        .where("name", "==", body.name)
        .limit(1)
        .stream()
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"A university named '{body.name}' already exists."
        )

    doc_data = {
        **body.model_dump(),
        "createdAt": SERVER_TIMESTAMP,
        "updatedAt": SERVER_TIMESTAMP,
        "createdBy": admin.get("email", ""),
        "updatedBy": admin.get("email", ""),
    }

    ref = db.collection("universities").document()
    ref.set(doc_data)

    return {
        "status":  "success",
        "message": "University created successfully.",
        "data":    serialize(ref.id, ref.get().to_dict()),
    }


@router.get("/{university_id}", summary="Get a single university by ID")
def get_university(
    university_id: str,
    admin:         dict = Depends(verify_admin),
):
    db  = get_db()
    doc = db.collection("universities").document(university_id).get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="University not found.")

    return {
        "status": "success",
        "data":   serialize(doc.id, doc.to_dict()),
    }


@router.patch("/{university_id}", summary="Update university — auto batch-syncs name to programs")
def update_university(
    university_id: str,
    body:          UniversityUpdate,
    admin:         dict = Depends(verify_admin),
):
    db  = get_db()
    ref = db.collection("universities").document(university_id)
    doc = ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="University not found.")

    old_data = doc.to_dict()

    updates = {
        k: (v.value if hasattr(v, "value") else v)
        for k, v in body.model_dump().items()
        if v is not None
    }

    if not updates:
        raise HTTPException(status_code=400, detail="No fields provided to update.")

    updates["updatedAt"] = SERVER_TIMESTAMP
    updates["updatedBy"] = admin.get("email", "")

    ref.update(updates)

    # Batch sync universityName to all linked programs if name changed
    batch_updated = 0
    new_name      = updates.get("name")
    if new_name and new_name != old_data.get("name"):
        batch_updated = _batch_sync_university_name(db, university_id, new_name)

    response = {
        "status":  "success",
        "message": "University updated successfully.",
        "data":    serialize(university_id, ref.get().to_dict()),
    }

    if batch_updated > 0:
        response["batchUpdated"] = (
            f"universityName synced in {batch_updated} degree program(s)."
        )

    return response


@router.delete("/{university_id}", summary="Delete university — blocked if linked programs exist")
def delete_university(
    university_id: str,
    admin:         dict = Depends(verify_admin),
):
    db  = get_db()
    ref = db.collection("universities").document(university_id)
    doc = ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="University not found.")

    linked = list(
        db.collection("degree_programs")
        .where("universityId", "==", university_id)
        .where("status", "==", "Active")
        .limit(1)
        .stream()
    )
    if linked:
        raise HTTPException(
            status_code=409,
            detail=(
                "Cannot delete this university because it has active degree programs. "
                "Deactivate or delete all programs first."
            )
        )

    name = doc.to_dict().get("name", "")
    ref.delete()

    return {
        "status":  "success",
        "message": f"University '{name}' deleted successfully.",
    }
