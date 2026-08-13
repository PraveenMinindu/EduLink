# =============================================================
# EduLink — Admin Auth Routes
# POST /admin/auth/login
# GET  /admin/auth/me
# =============================================================
# verify_admin dependency lives in utils/auth.py
# and is imported by all admin route files.
# =============================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from firebase_admin import auth as firebase_auth
from google.cloud.firestore import SERVER_TIMESTAMP

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from firebase_bridge import get_db
from utils.auth import verify_admin
from fastapi import Depends

router = APIRouter()


class LoginRequest(BaseModel):
    idToken: str  # Firebase ID token from Flutter client


class ProfileUpdate(BaseModel):
    name: str


@router.post("/login", summary="Verify Firebase token and check admin role")
def login(body: LoginRequest):
    get_db()  # initialize Firebase Admin SDK before verify_id_token()
    try:
        decoded = firebase_auth.verify_id_token(body.idToken)
    except firebase_auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Token expired. Please sign in again.")
    except firebase_auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")

    uid = decoded.get("uid")
    if not uid:
        raise HTTPException(status_code=401, detail="Token missing UID.")

    db  = get_db()
    doc = db.collection("admin_users").document(uid).get()

    if not doc.exists:
        raise HTTPException(
            status_code=403,
            detail="Access denied. This account does not have administrator privileges."
        )

    profile = doc.to_dict()

    try:
        db.collection("admin_users").document(uid).update({"lastLogin": SERVER_TIMESTAMP})
    except Exception:
        pass

    return {
        "status": "success",
        "uid":    uid,
        "name":   profile.get("name", ""),
        "email":  profile.get("email", ""),
        "role":   profile.get("role", "admin"),
    }


@router.get("/me", summary="Get current admin profile")
def me(admin: dict = Depends(verify_admin)):
    """Returns the current admin profile from admin_users collection."""
    last_login = admin.get("lastLogin")
    return {
        "status": "success",
        "uid":    admin.get("uid", ""),
        "name":   admin.get("name", ""),
        "email":  admin.get("email", ""),
        "role":   admin.get("role", "admin"),
        "lastLogin": last_login.isoformat() if hasattr(last_login, "isoformat") else None,
    }


@router.patch("/me", summary="Update current admin's display name")
def update_me(body: ProfileUpdate, admin: dict = Depends(verify_admin)):
    """Updates the 'name' field on the caller's own admin_users document."""
    name = body.name.strip()
    if len(name) < 2:
        raise HTTPException(
            status_code=400,
            detail="Name must be at least 2 characters.",
        )

    uid = admin["uid"]
    db  = get_db()
    db.collection("admin_users").document(uid).update({"name": name})

    last_login = admin.get("lastLogin")
    return {
        "status": "success",
        "uid":    uid,
        "name":   name,
        "email":  admin.get("email", ""),
        "role":   admin.get("role", "admin"),
        "lastLogin": last_login.isoformat() if hasattr(last_login, "isoformat") else None,
    }
