# ============================================================
# EduLink — Report Routes
# POST /student/generate-report/{id}
# GET  /student/report/{id}
# GET  /student/report-status/{id}
# ============================================================

from fastapi import APIRouter, HTTPException, BackgroundTasks
from firebase_bridge import (
    get_mcq, get_writing, save_report,
    update_status, get_status, get_report,
    get_student, get_cached_skills, save_cached_skills
)
import sys
import os

ML_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "ML")
sys.path.insert(0, ML_PATH)

from main_pipeline import run_pipeline

router = APIRouter()


def process_report(student_id: str):
    try:
        update_status(student_id, "processing", "Running AI models...")

        mcq     = get_mcq(student_id)
        writing = get_writing(student_id)
        student = get_student(student_id)  # ADD THIS

        if not mcq:
            update_status(student_id, "error", "MCQ not found")
            return
        if not writing:
            update_status(student_id, "error", "Writing not found")
            return

        q_keys = {f"Q{i}": mcq[f"Q{i}"] for i in range(1, 41)}
        report = run_pipeline(q_keys, writing["text"])

        # ADD student name to report
        report["student_name"] = student.get("name", student_id) if student else student_id

        save_report(student_id, report)
        update_status(student_id, "done", "Report ready")

    except Exception as e:
        update_status(student_id, "error", str(e))


@router.post("/generate-report/{student_id}")
def generate_report(student_id: str,
                    background_tasks: BackgroundTasks):
    try:
        if not student_id or student_id.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="student_id cannot be empty"
            )

        # Pre-check MCQ exists BEFORE queuing background task
        mcq = get_mcq(student_id)
        if not mcq:
            raise HTTPException(
                status_code=400,
                detail="MCQ responses not found. Submit MCQ first."
            )

        # Pre-check writing exists BEFORE queuing background task
        writing = get_writing(student_id)
        if not writing:
            raise HTTPException(
                status_code=400,
                detail="Writing sample not found. Submit writing first."
            )

        update_status(student_id, "pending",
                      "Report generation queued")
        background_tasks.add_task(process_report, student_id)

        return {
            "status":     "success",
            "message":    "Report generation started",
            "student_id": student_id
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/report/{student_id}")
def get_career_report(student_id: str):
    try:
        if not student_id or student_id.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="student_id cannot be empty"
            )

        report = get_report(student_id)
        if not report:
            raise HTTPException(
                status_code=404,
                detail="Report not found. Generate it first."
            )

        return {"status": "success", "data": report}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/report-status/{student_id}")
def check_status(student_id: str):
    try:
        if not student_id or student_id.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="student_id cannot be empty"
            )

        status = get_status(student_id)
        return {"status": "success", "data": status}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/skills/{student_id}")
def get_career_skills(student_id: str):
    try:
        report = get_report(student_id)
        if not report:
            raise HTTPException(status_code=404,
                detail="Report not found")

        cluster = report.get("top1_cluster", "")
        role    = report.get("final_recommended_role", "")

        cached = get_cached_skills(cluster)
        if cached:
            return {"status": "success", "data": cached}

        import sys, os
        ml_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "ML"
        )
        if ml_path not in sys.path:
            sys.path.insert(0, ml_path)

        from models.skill_extractor import extract_skills
        skills = extract_skills(role, cluster)
        save_cached_skills(cluster, skills)

        return {"status": "success", "data": skills}

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print("SKILLS ERROR:", str(e))
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))