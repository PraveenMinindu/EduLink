# ============================================================
# EduLink — MCQ Routes
# POST /student/submit-mcq
# ============================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from firebase_bridge import save_mcq

router = APIRouter()

class MCQSubmission(BaseModel):
    student_id: str
    Q1: int;  Q2: int;  Q3: int;  Q4: int;  Q5: int
    Q6: int;  Q7: int;  Q8: int;  Q9: int;  Q10: int
    Q11: int; Q12: int; Q13: int; Q14: int; Q15: int
    Q16: int; Q17: int; Q18: int; Q19: int; Q20: int
    Q21: int; Q22: int; Q23: int; Q24: int; Q25: int
    Q26: int; Q27: int; Q28: int; Q29: int; Q30: int
    Q31: int; Q32: int; Q33: int; Q34: int; Q35: int
    Q36: int; Q37: int; Q38: int; Q39: int; Q40: int


def compute_composites(q: dict) -> dict:
    def n(v): return (float(v) - 1) / 4.0
    return {
        "Analytical_Thinking":          round((n(q["Q1"])+n(q["Q2"])+n(q["Q3"])+n(q["Q16"]))/4, 4),
        "Creativity_Index":             round((n(q["Q5"])+n(q["Q24"])+n(q["Q30"]))/3, 4),
        "Communication_Skill":          round((n(q["Q6"])+n(q["Q13"])+n(q["Q17"]))/3, 4),
        "Emotional_Stability":          round(n(q["Q9"]), 4),
        "Strategic_Vision":             round((n(q["Q8"])+n(q["Q20"])+n(q["Q32"]))/3, 4),
        "Innovation_Drive":             round((n(q["Q5"])+n(q["Q40"]))/2, 4),
        "Social_Intelligence":          round((n(q["Q10"])+n(q["Q27"]))/2, 4),
        "Data_Literacy":                round((n(q["Q11"])+n(q["Q18"])+n(q["Q28"]))/3, 4),
        "Tech_Adaptability":            round((n(q["Q9"])+n(q["Q12"])+n(q["Q22"]))/3, 4),
        "Technical_ProblemSolving":     round((n(q["Q14"])+n(q["Q21"]))/2, 4),
        "Leadership_Capability":        round((n(q["Q15"])+n(q["Q35"]))/2, 4),
        "Process_Optimization":         round((n(q["Q14"])+n(q["Q39"]))/2, 4),
        "Tech_Interest":                round((n(q["Q22"])+n(q["Q31"])+n(q["Q37"]))/3, 4),
        "Business_Economics_Interest":  round((n(q["Q23"])+n(q["Q25"])+n(q["Q34"]))/3, 4),
        "Social_Impact_Motivation":     round((n(q["Q21"])+n(q["Q27"]))/2, 4),
        "Future_Orientation":           round((n(q["Q8"])+n(q["Q33"])+n(q["Q39"]))/3, 4),
        "Career_Growth_Mindset":        round((n(q["Q33"])+n(q["Q38"]))/2, 4),
        "Entrepreneurship_Orientation": round(n(q["Q26"]), 4),
        "Global_Innovation_Alignment":  round((n(q["Q40"])+n(q["Q39"]))/2, 4),
        "Structure_Preference":         round((n(q["Q7"])+n(q["Q18"]))/2, 4),
    }


@router.post("/submit-mcq")
def submit_mcq(data: MCQSubmission):
    try:
        q = data.model_dump()
        student_id = q.pop("student_id")

        # ── Validation 1 — student_id not empty ──────────
        if not student_id or student_id.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="student_id cannot be empty"
            )

        # ── Validation 2 — all 40 answers must be 1-5 ───
        invalid_questions = []
        for i in range(1, 41):
            val = q.get(f"Q{i}")
            if val is None:
                invalid_questions.append(f"Q{i} is missing")
            elif not 1 <= int(val) <= 5:
                invalid_questions.append(
                    f"Q{i} must be between 1 and 5 (got {val})"
                )

        if invalid_questions:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Invalid MCQ answers detected",
                    "errors":  invalid_questions
                }
            )

        # ── Validation 3 — check not all same answer ─────
        # Detects students who clicked all 1s or all 5s
        # without reading questions
        values = [q[f"Q{i}"] for i in range(1, 41)]
        if len(set(values)) == 1:
            raise HTTPException(
                status_code=400,
                detail="All answers are identical. Please answer each question carefully."
            )

        # ── All valid — compute and save ──────────────────
        composites = compute_composites(q)
        save_mcq(student_id, q, composites)

        return {
            "status":     "success",
            "message":    "MCQ responses saved successfully",
            "student_id": student_id,
            "composites": composites,
            "questions_answered": 40
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))