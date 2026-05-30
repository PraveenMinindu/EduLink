# ============================================================
# EduLink — Student Routes
# POST /student/register
# GET  /student/profile/{id}
# ============================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from firebase_bridge import save_student, get_student

router = APIRouter()

class StudentProfile(BaseModel):
    student_id: str
    name:       str
    age:        int
    grade:      str
    stream:     str
    school:     str
    district:   str
    gender:     str = ""   # Male / Female / Other

@router.post("/register")
def register_student(profile: StudentProfile):
    try:
        # Validation 1 — student_id not empty
        if not profile.student_id or profile.student_id.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="student_id cannot be empty"
            )

        # Validation 2 — name minimum length
        if not profile.name or len(profile.name.strip()) < 2:
            raise HTTPException(
                status_code=400,
                detail="Name must be at least 2 characters"
            )

        # Validation 3 — age range
        if not 10 <= profile.age <= 25:
            raise HTTPException(
                status_code=400,
                detail=f"Age must be between 10 and 25 (got {profile.age})"
            )

        # Validation 4 — grade
        if profile.grade not in ["OL", "AL"]:
            raise HTTPException(
                status_code=400,
                detail=f"Grade must be OL or AL (got {profile.grade})"
            )

        # Validation 5 — stream
        valid_streams = ["Technology", "Science", "Commerce", "Arts",'Mathematics','N/A']
        if profile.stream not in valid_streams:
            raise HTTPException(
                status_code=400,
                detail=f"Stream must be one of {valid_streams} (got {profile.stream})"
            )

        # Validation 6 — school not empty
        if not profile.school or len(profile.school.strip()) < 2:
            raise HTTPException(
                status_code=400,
                detail="School name cannot be empty"
            )

        # Validation 7 — district not empty
        if not profile.district or len(profile.district.strip()) < 2:
            raise HTTPException(
                status_code=400,
                detail="District cannot be empty"
            )

        save_student(profile.student_id, profile.model_dump())
        return {
            "status":     "success",
            "message":    "Student registered successfully",
            "student_id": profile.student_id
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profile/{student_id}")
def get_profile(student_id: str):
    try:
        if not student_id or student_id.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="student_id cannot be empty"
            )

        student = get_student(student_id)
        if not student:
            raise HTTPException(
                status_code=404,
                detail=f"Student {student_id} not found"
            )

        return {"status": "success", "data": student}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))