# =============================================================
# EduLink — Report Routes V2
# Assessment-based routes alongside existing routes.
# ALL existing routes preserved and unchanged.
# =============================================================

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from firebase_bridge import (
    get_mcq, get_writing, save_report,
    update_status, get_status, get_report,
    get_student, get_cached_skills, save_cached_skills,
    save_assessment_report, get_assessment_report,
    save_assessment_history_entry, get_assessment_history,
    save_mcq_v2, save_writing_v2, get_student_id_from_uid
)
import sys
import os
from datetime import datetime

ML_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "ML")
sys.path.insert(0, ML_PATH)

# run_pipeline imported lazily inside process functions

router = APIRouter()


# =============================================================
# EXISTING ROUTES — unchanged
# =============================================================

def process_report(student_id: str):
    try:
        update_status(student_id, "processing", "Running AI models...")
        mcq     = get_mcq(student_id)
        writing = get_writing(student_id)
        student = get_student(student_id)
        if not mcq:
            update_status(student_id, "error", "MCQ not found")
            return
        if not writing:
            update_status(student_id, "error", "Writing not found")
            return
        q_keys = {f"Q{i}": mcq[f"Q{i}"] for i in range(1, 41)}
        from main_pipeline import run_pipeline
        report = run_pipeline(q_keys, writing["text"])
        report["student_name"] = (
            student.get("name", student_id) if student else student_id
        )
        save_report(student_id, report)
        update_status(student_id, "done", "Report ready")
    except Exception as e:
        update_status(student_id, "error", str(e))


@router.post("/generate-report/{student_id}")
def generate_report(student_id: str, background_tasks: BackgroundTasks):
    try:
        if not student_id or student_id.strip() == "":
            raise HTTPException(status_code=400,
                                detail="student_id cannot be empty")
        mcq = get_mcq(student_id)
        if not mcq:
            raise HTTPException(status_code=400,
                                detail="MCQ responses not found.")
        writing = get_writing(student_id)
        if not writing:
            raise HTTPException(status_code=400,
                                detail="Writing sample not found.")
        update_status(student_id, "pending", "Report generation queued")
        background_tasks.add_task(process_report, student_id)
        return {"status": "success", "message": "Report generation started",
                "student_id": student_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/report/{student_id}")
def get_career_report(student_id: str):
    try:
        report = get_report(student_id)
        if not report:
            # Also check v2 format
            report = get_assessment_report(student_id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found.")
        return {"status": "success", "data": report}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/report-status/{student_id}")
def check_status(student_id: str):
    try:
        status = get_status(student_id)
        return {"status": "success", "data": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/skills/{student_id}")
def get_career_skills(student_id: str):
    try:
        report = get_report(student_id)
        if not report:
            report = get_assessment_report(student_id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        cluster = report.get("top1_cluster", "")
        role    = report.get("final_recommended_role", "")
        cached  = get_cached_skills(cluster)
        if cached:
            return {"status": "success", "data": cached}
        ml_path = os.path.join(os.path.dirname(__file__), "..", "..", "ML")
        if ml_path not in sys.path:
            sys.path.insert(0, ml_path)
        from models.skill_extractor import extract_skills
        skills = extract_skills(role, cluster)
        save_cached_skills(cluster, skills)
        return {"status": "success", "data": skills}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================
# NEW V2 ROUTES — assessment-based
# =============================================================

class MCQv2Body(BaseModel):
    assessment_id: str
    Q1: int; Q2: int; Q3: int; Q4: int; Q5: int
    Q6: int; Q7: int; Q8: int; Q9: int; Q10: int
    Q11: int; Q12: int; Q13: int; Q14: int; Q15: int
    Q16: int; Q17: int; Q18: int; Q19: int; Q20: int
    Q21: int; Q22: int; Q23: int; Q24: int; Q25: int
    Q26: int; Q27: int; Q28: int; Q29: int; Q30: int
    Q31: int; Q32: int; Q33: int; Q34: int; Q35: int
    Q36: int; Q37: int; Q38: int; Q39: int; Q40: int


class WritingV2Body(BaseModel):
    assessment_id: str
    text: str


@router.post("/submit-mcq-v2")
def submit_mcq_v2(body: MCQv2Body):
    """Save MCQ under assessmentId — preserves history."""
    try:
        assessment_id = body.assessment_id
        if not assessment_id:
            raise HTTPException(status_code=400,
                                detail="assessment_id required")
        answers = {f"Q{i}": getattr(body, f"Q{i}") for i in range(1, 41)}
        save_mcq_v2(assessment_id, answers)
        return {"status": "success",
                "message": "MCQ saved",
                "assessment_id": assessment_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/submit-writing-v2")
def submit_writing_v2(body: WritingV2Body):
    """Save writing sample under assessmentId."""
    try:
        assessment_id = body.assessment_id
        text = body.text.strip()
        if not assessment_id:
            raise HTTPException(status_code=400,
                                detail="assessment_id required")
        if len(text.split()) < 10:
            raise HTTPException(status_code=400,
                                detail="Writing sample too short")
        save_writing_v2(assessment_id, text)
        return {"status": "success",
                "message": "Writing saved",
                "assessment_id": assessment_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _extract_student_id(assessment_id: str) -> str:
    """
    Extract studentId from assessmentId.
    assessmentId format: STUDENTID_YYYYMMDD_HHMMSS
    e.g. A3B7F2C1_20260811_143022 → A3B7F2C1
    """
    parts = assessment_id.split("_")
    return parts[0] if parts else assessment_id


def process_report_v2(assessment_id: str):
    """
    V2 pipeline: reads MCQ/writing from assessmentId,
    saves report under assessmentId,
    saves entry to assessment_history.
    """
    try:
        student_id = _extract_student_id(assessment_id)

        update_status(assessment_id, "processing", "Running AI models...")

        mcq     = get_mcq(assessment_id)
        writing = get_writing(assessment_id)
        student = get_student(student_id)

        if not mcq:
            update_status(assessment_id, "error", "MCQ not found")
            return
        if not writing:
            update_status(assessment_id, "error", "Writing not found")
            return

        q_keys = {f"Q{i}": mcq[f"Q{i}"] for i in range(1, 41)}
        from main_pipeline import run_pipeline
        report = run_pipeline(q_keys, writing["text"])

        report["student_name"]   = (
            student.get("name", student_id) if student else student_id
        )
        report["student_id"]     = student_id
        report["assessment_id"]  = assessment_id

        # Save report under assessmentId
        save_assessment_report(assessment_id, report)

        # Save to assessment history
        save_assessment_history_entry(student_id, {
            "assessment_id": assessment_id,
            "date":          datetime.now().strftime("%Y-%m-%d %H:%M"),
            "role":          report.get("final_recommended_role", ""),
            "score":         report.get("final_score", 0),
            "confidence":    report.get("confidence_label", ""),
            "cluster":       report.get("top1_cluster", ""),
        })

        update_status(assessment_id, "done", "Report ready")

    except Exception as e:
        update_status(assessment_id, "error", str(e))


@router.post("/generate-report-v2/{assessment_id}")
def generate_report_v2(assessment_id: str,
                        background_tasks: BackgroundTasks):
    """Generate report under assessmentId."""
    try:
        if not assessment_id:
            raise HTTPException(status_code=400,
                                detail="assessment_id required")
        mcq = get_mcq(assessment_id)
        if not mcq:
            raise HTTPException(status_code=400,
                                detail="MCQ not found for this assessment.")
        writing = get_writing(assessment_id)
        if not writing:
            raise HTTPException(status_code=400,
                                detail="Writing not found for this assessment.")
        update_status(assessment_id, "pending", "Report generation queued")
        background_tasks.add_task(process_report_v2, assessment_id)
        return {"status": "success",
                "message": "Report generation started",
                "assessment_id": assessment_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/report-v2/{assessment_id}")
def get_report_v2(assessment_id: str):
    """Get report by assessmentId."""
    try:
        report = get_assessment_report(assessment_id)
        if not report:
            raise HTTPException(status_code=404,
                                detail="Report not found.")
        return {"status": "success", "data": report}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/report-status-v2/{assessment_id}")
def check_status_v2(assessment_id: str):
    """Get report status by assessmentId."""
    try:
        status = get_status(assessment_id)
        return {"status": "success", "data": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{student_id}")
def get_history(student_id: str):
    """Get all assessment history for a student."""
    try:
        history = get_assessment_history(student_id)
        return {"status": "success", "data": history,
                "count": len(history)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))