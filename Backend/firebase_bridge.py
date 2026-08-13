# =============================================================
# EduLink — Firebase Bridge
# ALL existing functions preserved unchanged.
# New v2 functions added for assessment-based architecture.
# Updated: supports FIREBASE_KEY_JSON env var for Render deploy
# =============================================================

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
import os
import json

_db = None

def get_db():
    global _db
    if _db is None:
        if not firebase_admin._apps:
            # ── Render / production: key passed as JSON string env var
            key_json = os.getenv("FIREBASE_KEY_JSON")
            if key_json:
                key_dict = json.loads(key_json)
                cred = credentials.Certificate(key_dict)
            else:
                # ── Local development: key loaded from file
                key_path = os.getenv(
                    "FIREBASE_KEY_PATH",
                    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "serviceAccountKey.json")
                )
                cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred)
        _db = firestore.client()
    return _db


# =============================================================
# EXISTING FUNCTIONS — unchanged
# =============================================================

def save_student(student_id: str, profile: dict):
    get_db().collection("students").document(student_id).set({
        **profile,
        "created_at": datetime.now().isoformat()
    })

def save_mcq(student_id: str, answers: dict, composites: dict):
    get_db().collection("mcq_responses").document(student_id).set({
        **answers,
        "composites":   composites,
        "submitted_at": datetime.now().isoformat()
    })

def save_writing(student_id: str, text: str):
    get_db().collection("writing_samples").document(student_id).set({
        "text":         text,
        "word_count":   len(text.split()),
        "submitted_at": datetime.now().isoformat()
    })

def get_mcq(doc_id: str) -> dict:
    doc = get_db().collection("mcq_responses").document(doc_id).get()
    return doc.to_dict() if doc.exists else None

def get_writing(doc_id: str) -> dict:
    doc = get_db().collection("writing_samples").document(doc_id).get()
    return doc.to_dict() if doc.exists else None

def get_student(student_id: str) -> dict:
    doc = get_db().collection("students").document(student_id).get()
    return doc.to_dict() if doc.exists else None

def save_report(student_id: str, report: dict):
    get_db().collection("career_reports").document(student_id).set(report)

def get_report(student_id: str) -> dict:
    doc = get_db().collection("career_reports").document(student_id).get()
    return doc.to_dict() if doc.exists else None

def update_status(doc_id: str, status: str, message: str = ""):
    get_db().collection("report_status").document(doc_id).set({
        "status":     status,
        "message":    message,
        "updated_at": datetime.now().isoformat()
    })

def get_status(doc_id: str) -> dict:
    doc = get_db().collection("report_status").document(doc_id).get()
    return doc.to_dict() if doc.exists else {"status": "not_found"}


# =============================================================
# NEW V2 FUNCTIONS — assessment-based architecture
# =============================================================

def save_user_mapping(firebase_uid: str, student_id: str, name: str):
    get_db().collection("user_mappings").document(firebase_uid).set({
        "student_id": student_id,
        "name":       name,
        "created_at": datetime.now().isoformat()
    })


def get_student_id_from_uid(firebase_uid: str) -> str:
    doc = get_db().collection("user_mappings").document(firebase_uid).get()
    if doc.exists:
        return doc.to_dict().get("student_id")
    return None


def save_mcq_v2(assessment_id: str, answers: dict):
    get_db().collection("mcq_responses").document(assessment_id).set({
        **answers,
        "assessment_id": assessment_id,
        "submitted_at":  datetime.now().isoformat()
    })


def save_writing_v2(assessment_id: str, text: str):
    get_db().collection("writing_samples").document(assessment_id).set({
        "text":          text,
        "word_count":    len(text.split()),
        "assessment_id": assessment_id,
        "submitted_at":  datetime.now().isoformat()
    })


def save_assessment_report(assessment_id: str, report: dict):
    get_db().collection("career_reports").document(assessment_id).set({
        **report,
        "assessment_id": assessment_id
    })


def get_assessment_report(assessment_id: str) -> dict:
    doc = get_db().collection("career_reports").document(assessment_id).get()
    return doc.to_dict() if doc.exists else None


def save_assessment_history_entry(student_id: str, entry: dict):
    ref = get_db().collection("assessment_history").document(student_id)
    doc = ref.get()
    if doc.exists:
        data = doc.to_dict()
        assessments = data.get("assessments", [])
        assessments.append(entry)
        ref.update({"assessments": assessments})
    else:
        ref.set({"assessments": [entry], "student_id": student_id})


def get_assessment_history(student_id: str) -> list:
    doc = get_db().collection("assessment_history").document(student_id).get()
    if not doc.exists:
        return []
    assessments = doc.to_dict().get("assessments", [])
    return sorted(assessments, key=lambda x: x.get("date", ""), reverse=True)


# =============================================================
# EXISTING DEMAND / SKILLS FUNCTIONS — unchanged
# =============================================================

def save_demand_datapoint(role: str, month: str,
                           count: int, source: str = "adzuna_live"):
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
    try:
        cutoff = (datetime.now() - timedelta(days=months_back * 30)
                  ).strftime("%Y-%m")
        docs = (get_db().collection("job_demand_history")
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
    try:
        doc_id = role.replace(" ", "_").replace("/", "_")
        doc    = get_db().collection("job_demand_trends").document(doc_id).get()
        return doc.to_dict() if doc.exists else None
    except Exception as e:
        print(f"get_demand_trend error: {e}")
        return None


def save_cached_skills(cluster: str, skills: dict):
    try:
        skills_clean = {k: v for k, v in skills.items() if k != "updated_at"}
        skills_clean["updated_at"] = datetime.now().isoformat()
        get_db().collection("career_skills").document(cluster).set(skills_clean)
    except Exception as e:
        print(f"save_cached_skills error: {e}")


def get_cached_skills(cluster: str):
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
