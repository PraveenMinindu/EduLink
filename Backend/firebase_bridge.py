# ============================================================
# EduLink — Firebase Bridge
# Reads and writes data to Firestore
# ============================================================

from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()

_db = None

def get_db():
    global _db
    if _db is None:
        if not firebase_admin._apps:
            key_path = os.getenv("FIREBASE_KEY_PATH", "serviceAccountKey.json")
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred)
        _db = firestore.client()
    return _db


# ── Students ─────────────────────────────────────────────────
def save_student(student_id: str, data: dict):
    get_db().collection("students").document(student_id).set({
        **data,
        "created_at": datetime.now().isoformat()
    })

def get_student(student_id: str):
    doc = get_db().collection("students").document(student_id).get()
    return doc.to_dict() if doc.exists else None


# ── MCQ ──────────────────────────────────────────────────────
def save_mcq(student_id: str, answers: dict, composites: dict):
    get_db().collection("mcq_responses").document(student_id).set({
        **answers,
        "composites":   composites,
        "submitted_at": datetime.now().isoformat()
    })

def get_mcq(student_id: str):
    doc = get_db().collection("mcq_responses").document(student_id).get()
    return doc.to_dict() if doc.exists else None


# ── Writing ──────────────────────────────────────────────────
def save_writing(student_id: str, text: str):
    get_db().collection("writing_samples").document(student_id).set({
        "text":         text,
        "word_count":   len(text.split()),
        "submitted_at": datetime.now().isoformat()
    })

def get_writing(student_id: str):
    doc = get_db().collection("writing_samples").document(student_id).get()
    return doc.to_dict() if doc.exists else None


# ── Report ───────────────────────────────────────────────────
def save_report(student_id: str, report: dict):
    get_db().collection("career_reports").document(student_id).set(report)

def get_report(student_id: str):
    doc = get_db().collection("career_reports").document(student_id).get()
    return doc.to_dict() if doc.exists else None


# ── Status ───────────────────────────────────────────────────
def update_status(student_id: str, status: str, message: str = ""):
    get_db().collection("report_status").document(student_id).set({
        "status":     status,
        "message":    message,
        "updated_at": datetime.now().isoformat()
    })

def get_status(student_id: str):
    doc = get_db().collection("report_status").document(student_id).get()
    return doc.to_dict() if doc.exists else {"status": "not_found"}


# ── Skill Cache ───────────────────────────────────────────────
def save_cached_skills(cluster: str, skills: dict):
    """Save skills to Firestore cache."""
    try:
        skills_clean = {
            k: v for k, v in skills.items()
            if k != "updated_at"
        }
        skills_clean["updated_at"] = datetime.now().isoformat()
        get_db().collection("career_skills").document(cluster).set(
            skills_clean
        )
    except Exception as e:
        print(f"save_cached_skills error: {e}")


def get_cached_skills(cluster: str):
    """Get cached skills from Firestore if fresh under 24 hours."""
    try:
        doc = get_db().collection("career_skills").document(cluster).get()
        if not doc.exists:
            return None

        data       = doc.to_dict()
        updated_at = data.get("updated_at")

        if updated_at:
            if hasattr(updated_at, "timestamp"):
                updated_dt = datetime.fromtimestamp(updated_at.timestamp())
            else:
                updated_dt = datetime.fromisoformat(str(updated_at))

            age = datetime.now() - updated_dt
            if age < timedelta(hours=24):
                return data

        return None
    except Exception as e:
        print(f"get_cached_skills error: {e}")
        return None


# ── Job Demand History ────────────────────────────────────────
def save_demand_datapoint(role: str, month: str,
                           count: int, source: str = "adzuna_live"):
    """
    Save one monthly job count to Firestore time series.
    Collection: job_demand_history
    Document:   Data_Scientist_2026-05
    """
    try:
        doc_id = f"{role.replace(' ', '_').replace('/', '_')}_{month}"
        get_db().collection("job_demand_history").document(doc_id).set({
            "role":         role,
            "month":        month,
            "count":        count,
            "source":       source,
            "collected_at": datetime.now().isoformat(),
        })
    except Exception as e:
        print(f"save_demand_datapoint error: {e}")


def get_demand_history(role: str, months_back: int = 18) -> list:
    """
    Get historical job counts for a role from Firestore.
    Returns list sorted oldest to newest.
    """
    try:
        cutoff = (datetime.now() - timedelta(days=months_back * 30)
                  ).strftime("%Y-%m")
        docs   = (get_db().collection("job_demand_history")
                  .where("role", "==", role)
                  .stream())
        history = []
        for doc in docs:
            data  = doc.to_dict()
            month = data.get("month", "")
            if month >= cutoff:
                history.append({
                    "month":  month,
                    "count":  int(data.get("count", 0)),
                    "source": data.get("source", "unknown"),
                })
        history.sort(key=lambda x: x["month"])
        return history
    except Exception as e:
        print(f"get_demand_history error: {e}")
        return []


def get_demand_trend(role: str) -> dict:
    """
    Get the latest computed trend for a role from Firestore.
    Updated by Job Demand Forecasting Colab notebook monthly.
    """
    try:
        doc_id = role.replace(" ", "_").replace("/", "_")
        doc    = get_db().collection("job_demand_trends").document(doc_id).get()
        if doc.exists:
            return doc.to_dict()
        return None
    except Exception as e:
        print(f"get_demand_trend error: {e}")
        return None