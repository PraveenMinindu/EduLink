# =============================================================
# EduLink — Shared Admin Authentication Helper
# Improvement 1: single verify_admin dependency used by all routes
# =============================================================

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth as firebase_auth
from google.cloud.firestore import SERVER_TIMESTAMP

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from firebase_bridge import get_db

security = HTTPBearer()


def verify_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    FastAPI dependency injected into every /admin/* route.

    Steps:
      1. Verify Firebase ID token from Authorization header
      2. Look up UID in admin_users collection
      3. Raise 403 if document not found
      4. Update lastLogin silently
      5. Return admin profile dict

    Usage:
      @router.get("/something")
      def handler(admin: dict = Depends(verify_admin)):
          ...
    """
    token = credentials.credentials

    # Step 1 — Verify token
    try:
        decoded = firebase_auth.verify_id_token(token)
    except firebase_auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=401,
            detail="Token expired. Please sign in again.",
        )
    except firebase_auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Authentication failed: {str(e)}",
        )

    uid = decoded.get("uid")
    if not uid:
        raise HTTPException(status_code=401, detail="Token missing UID.")

    # Step 2 — Check admin_users collection
    db  = get_db()
    doc = db.collection("admin_users").document(uid).get()

    if not doc.exists:
        raise HTTPException(
            status_code=403,
            detail=(
                "Access denied. "
                "This account does not have administrator privileges."
            ),
        )

    profile        = doc.to_dict()
    profile["uid"] = uid

    # Step 3 — Update lastLogin (non-critical)
    try:
        db.collection("admin_users").document(uid).update(
            {"lastLogin": SERVER_TIMESTAMP}
        )
    except Exception:
        pass

    return profile
