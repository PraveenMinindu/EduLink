# =============================================================
# EduLink — Admin Dashboard Route
# GET /admin/dashboard/stats
# =============================================================

from fastapi import APIRouter, Depends

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from firebase_bridge import get_db
from utils.auth import verify_admin

router = APIRouter()


@router.get("/stats", summary="Live dashboard statistics from Firestore")
def get_stats(admin: dict = Depends(verify_admin)):
    """
    Returns real counts — zero hardcoded values.
    Designed so adding more stat blocks later is straightforward.
    """
    db = get_db()

    uni_docs    = list(db.collection("universities").stream())
    total_unis  = len(uni_docs)
    active_unis = sum(1 for d in uni_docs if d.to_dict().get("status") == "Active")

    prog_docs      = list(db.collection("degree_programs").stream())
    total_progs    = len(prog_docs)
    active_progs   = sum(1 for d in prog_docs if d.to_dict().get("status") == "Active")
    inactive_progs = total_progs - active_progs
    active_pct     = round((active_progs / total_progs * 100) if total_progs else 0, 1)

    report_docs  = list(db.collection("career_reports").stream())
    total_reports = len(report_docs)

    # Recent activity — last 5 programs by updatedAt
    recent_raw = (
        db.collection("degree_programs")
        .order_by("updatedAt", direction="DESCENDING")
        .limit(5)
        .stream()
    )
    recent_activity = []
    for doc in recent_raw:
        data = doc.to_dict()
        recent_activity.append({
            "id":             doc.id,
            "degreeName":     data.get("degreeName", ""),
            "universityName": data.get("universityName", ""),
            "status":         data.get("status", ""),
            "updatedBy":      data.get("updatedBy", ""),
        })

    return {
        "status": "success",
        "data": {
            "universities": {
                "total":    total_unis,
                "active":   active_unis,
                "inactive": total_unis - active_unis,
            },
            "programs": {
                "total":         total_progs,
                "active":        active_progs,
                "inactive":      inactive_progs,
                "activePercent": active_pct,
            },
            "reports": {
                "total": total_reports,
            },
            "recentActivity": recent_activity,
        }
    }
