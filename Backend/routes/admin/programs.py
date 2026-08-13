# =============================================================
# EduLink — Admin Degree Programs Routes
# GET    /admin/degree-programs
# POST   /admin/degree-programs
# GET    /admin/degree-programs/{id}
# PATCH  /admin/degree-programs/{id}
# DELETE /admin/degree-programs/{id}  ← soft delete (status=Inactive)
# =============================================================

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from google.cloud.firestore import SERVER_TIMESTAMP

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from firebase_bridge import get_db
from utils.auth      import verify_admin
from utils.firestore  import serialize
from utils.enums     import (
    RecordStatus, FeeType, StudyMode,
    ApplicationStatus, Currency,
)

router = APIRouter()


# =============================================================
# MODELS — Improvement 3: Enums for constrained fields
# =============================================================

class ProgramCreate(BaseModel):
    # Reference
    universityId:           str
    universityName:         str

    # Basic
    degreeName:             str
    faculty:                str
    shortDescription:       Optional[str]              = ""
    fullDescription:        Optional[str]              = ""

    # Academic
    duration:               Optional[str]              = ""
    studyMode:              StudyMode                  = StudyMode.full_time
    medium:                 Optional[str]              = "English"
    qualification:          Optional[str]              = ""

    # Admission & Fees
    entryRequirements:      Optional[str]              = ""
    feeType:                FeeType                    = FeeType.free
    tuitionFee:             Optional[float]            = 0
    currency:               Currency                   = Currency.lkr
    registrationFee:        Optional[float]            = 0
    installmentAvailable:   Optional[bool]             = False

    # Campus
    campusName:             Optional[str]              = ""
    address:                Optional[str]              = ""
    latitude:               Optional[float]            = None
    longitude:              Optional[float]            = None

    # Intake & Contact
    nextIntake:             Optional[str]              = ""
    applicationStatus:      ApplicationStatus          = ApplicationStatus.coming_soon
    applicationDeadline:    Optional[str]              = ""
    phone:                  Optional[str]              = ""
    email:                  Optional[str]              = ""
    officialWebsite:        Optional[str]              = ""
    degreePageUrl:          Optional[str]              = ""
    applyNowUrl:            Optional[str]              = ""

    # Recognition
    ugcRecognized:          Optional[bool]             = False
    ministryRecognized:     Optional[bool]             = False
    accreditation:          Optional[str]              = ""

    # Scholarships
    scholarships:           Optional[str]              = ""
    financialAid:           Optional[str]              = ""
    paymentPlans:           Optional[str]              = ""

    # Resources
    logoUrl:                Optional[str]              = ""
    campusImageUrl:         Optional[str]              = ""
    virtualTourUrl:         Optional[str]              = ""
    brochureUrl:            Optional[str]              = ""

    # Status
    status:                 RecordStatus               = RecordStatus.active


class ProgramUpdate(BaseModel):
    degreeName:             Optional[str]              = None
    faculty:                Optional[str]              = None
    shortDescription:       Optional[str]              = None
    fullDescription:        Optional[str]              = None
    duration:               Optional[str]              = None
    studyMode:              Optional[StudyMode]        = None
    medium:                 Optional[str]              = None
    qualification:          Optional[str]              = None
    entryRequirements:      Optional[str]              = None
    feeType:                Optional[FeeType]          = None
    tuitionFee:             Optional[float]            = None
    currency:               Optional[Currency]         = None
    registrationFee:        Optional[float]            = None
    installmentAvailable:   Optional[bool]             = None
    campusName:             Optional[str]              = None
    address:                Optional[str]              = None
    latitude:               Optional[float]            = None
    longitude:              Optional[float]            = None
    nextIntake:             Optional[str]              = None
    applicationStatus:      Optional[ApplicationStatus] = None
    applicationDeadline:    Optional[str]              = None
    phone:                  Optional[str]              = None
    email:                  Optional[str]              = None
    officialWebsite:        Optional[str]              = None
    degreePageUrl:          Optional[str]              = None
    applyNowUrl:            Optional[str]              = None
    ugcRecognized:          Optional[bool]             = None
    ministryRecognized:     Optional[bool]             = None
    accreditation:          Optional[str]              = None
    scholarships:           Optional[str]              = None
    financialAid:           Optional[str]              = None
    paymentPlans:           Optional[str]              = None
    logoUrl:                Optional[str]              = None
    campusImageUrl:         Optional[str]              = None
    virtualTourUrl:         Optional[str]              = None
    brochureUrl:            Optional[str]              = None
    status:                 Optional[RecordStatus]     = None


# =============================================================
# ROUTES
# Improvement 5: list designed for future ?search= support
# =============================================================

@router.get("", summary="List degree programs — supports filters, ready for ?search")
def list_programs(
    universityId: Optional[str]          = Query(None, description="Filter by university ID"),
    status:       Optional[RecordStatus] = Query(None, description="Filter by status"),
    search:       Optional[str]          = Query(None, description="[Future] Search by degree name"),
    admin:        dict                   = Depends(verify_admin),
):
    """
    Returns degree programs from Firestore.

    Current filters:
      ?universityId={id}   → programs for one university (University Detail page)
      ?status=Active       → active programs only

    Future filter (schema ready):
      ?search=computer     → filter by degree name
    """
    db    = get_db()
    query = db.collection("degree_programs")

    if universityId:
        query = query.where("universityId", "==", universityId)

    if status:
        query = query.where("status", "==", status.value)

    docs     = list(query.order_by("degreeName").stream())
    programs = [serialize(d.id, d.to_dict()) for d in docs]

    # Future: server-side search will replace this
    if search:
        term     = search.lower()
        programs = [
            p for p in programs
            if term in p.get("degreeName", "").lower()
            or term in p.get("faculty", "").lower()
        ]

    return {
        "status": "success",
        "count":  len(programs),
        "data":   programs,
    }


@router.post("", summary="Create a new degree program", status_code=201)
def create_program(
    body:  ProgramCreate,
    admin: dict = Depends(verify_admin),
):
    db = get_db()

    # Verify university exists
    if not db.collection("universities").document(body.universityId).get().exists:
        raise HTTPException(
            status_code=404,
            detail=f"University with ID '{body.universityId}' not found."
        )

    # Duplicate check
    existing = list(
        db.collection("degree_programs")
        .where("universityId", "==", body.universityId)
        .where("degreeName",   "==", body.degreeName)
        .limit(1)
        .stream()
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"A program named '{body.degreeName}' already exists for this university."
        )

    # Convert enums to their string values for Firestore storage
    doc_data = {
        k: (v.value if hasattr(v, "value") else v)
        for k, v in body.model_dump().items()
    }
    doc_data.update({
        "createdAt": SERVER_TIMESTAMP,
        "updatedAt": SERVER_TIMESTAMP,
        "createdBy": admin.get("email", ""),
        "updatedBy": admin.get("email", ""),
    })

    ref = db.collection("degree_programs").document()
    ref.set(doc_data)

    return {
        "status":  "success",
        "message": "Degree program created successfully.",
        "data":    serialize(ref.id, ref.get().to_dict()),
    }


@router.get("/{program_id}", summary="Get a single degree program by ID")
def get_program(
    program_id: str,
    admin:      dict = Depends(verify_admin),
):
    db  = get_db()
    doc = db.collection("degree_programs").document(program_id).get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Degree program not found.")

    return {
        "status": "success",
        "data":   serialize(doc.id, doc.to_dict()),
    }


@router.patch("/{program_id}", summary="Update a degree program")
def update_program(
    program_id: str,
    body:       ProgramUpdate,
    admin:      dict = Depends(verify_admin),
):
    db  = get_db()
    ref = db.collection("degree_programs").document(program_id)
    doc = ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Degree program not found.")

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

    return {
        "status":  "success",
        "message": "Degree program updated successfully.",
        "data":    serialize(program_id, ref.get().to_dict()),
    }


@router.delete(
    "/{program_id}",
    summary="Soft delete — sets status=Inactive instead of removing document"
)
def delete_program(
    program_id: str,
    admin:      dict = Depends(verify_admin),
):
    """
    Improvement 4: Soft delete.
    Sets status='Inactive' rather than removing the Firestore document.
    Document is retained for audit trail and can be reactivated via PATCH.
    """
    db  = get_db()
    ref = db.collection("degree_programs").document(program_id)
    doc = ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Degree program not found.")

    data = doc.to_dict()

    if data.get("status") == RecordStatus.inactive.value:
        raise HTTPException(
            status_code=409,
            detail="Degree program is already inactive."
        )

    ref.update({
        "status":    RecordStatus.inactive.value,
        "updatedAt": SERVER_TIMESTAMP,
        "updatedBy": admin.get("email", ""),
    })

    return {
        "status":  "success",
        "message": (
            f"Degree program '{data.get('degreeName', '')}' "
            "has been deactivated (status set to Inactive). "
            "Use PATCH to reactivate."
        ),
    }
