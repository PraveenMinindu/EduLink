# ============================================================
# EduLink — Backend Unit Tests
# Run: python -m pytest tests/test_backend.py -v
# ============================================================

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

# ── Mock Firebase so tests run without real Firebase ─────────
def mock_save_student(student_id, data): pass
def mock_save_mcq(student_id, answers, composites): pass
def mock_save_writing(student_id, text): pass
def mock_get_mcq(student_id):
    return {
        "Q1":4,"Q2":5,"Q3":3,"Q4":4,"Q5":3,
        "Q6":4,"Q7":5,"Q8":3,"Q9":4,"Q10":3,
        "Q11":5,"Q12":4,"Q13":3,"Q14":4,"Q15":3,
        "Q16":4,"Q17":5,"Q18":3,"Q19":4,"Q20":3,
        "Q21":4,"Q22":5,"Q23":3,"Q24":4,"Q25":3,
        "Q26":4,"Q27":5,"Q28":3,"Q29":4,"Q30":3,
        "Q31":4,"Q32":5,"Q33":3,"Q34":4,"Q35":3,
        "Q36":4,"Q37":5,"Q38":3,"Q39":4,"Q40":3,
    }
def mock_get_writing(student_id):
    return {
        "text": "I recently faced a challenge learning Python. I broke problems into smaller parts and practiced daily. I learned that systematic thinking is essential for solving technical problems analytically.",
        "word_count": 32
    }
def mock_get_student(student_id):
    return {"student_id": student_id, "name": "Test Student"}
def mock_save_report(student_id, report): pass
def mock_get_report(student_id):
    return {
        "top1_cluster":           "Data_AI_Engineering",
        "final_recommended_role": "Data Scientist",
        "confidence_label":       "High",
        "final_score":            84.2,
        "salary_min":             234508,
        "salary_max":             317275,
    }
def mock_update_status(student_id, status, message=""): pass
def mock_get_status(student_id):
    return {"status": "done", "updated_at": "2026-05-02T10:00:00"}

VALID_STUDENT = {
    "student_id": "TEST001",
    "name":       "Kasun Perera",
    "age":        17,
    "grade":      "AL",
    "stream":     "Technology",
    "school":     "Nalanda College",
    "district":   "Colombo"
}

VALID_MCQ = {
    "student_id": "TEST001",
    "Q1":4,"Q2":5,"Q3":3,"Q4":4,"Q5":3,
    "Q6":4,"Q7":5,"Q8":3,"Q9":4,"Q10":3,
    "Q11":5,"Q12":4,"Q13":3,"Q14":4,"Q15":3,
    "Q16":4,"Q17":5,"Q18":3,"Q19":4,"Q20":3,
    "Q21":4,"Q22":5,"Q23":3,"Q24":4,"Q25":3,
    "Q26":4,"Q27":5,"Q28":3,"Q29":4,"Q30":3,
    "Q31":4,"Q32":5,"Q33":3,"Q34":4,"Q35":3,
    "Q36":4,"Q37":5,"Q38":3,"Q39":4,"Q40":3,
}

VALID_WRITING = {
    "student_id": "TEST001",
    "text": "I recently faced a challenge when learning Python for my school project. At first the syntax was confusing and I made many errors. I decided to break the problem into smaller parts and practice each concept separately. I also watched tutorials and asked my teacher for help. Through this experience I learned that systematic thinking and patience are essential for solving technical problems analytically."
}


# ============================================================
# HEALTH CHECK TESTS
# ============================================================

class TestHealthCheck:

    def test_ping_returns_200(self):
        response = client.get("/ping")
        assert response.status_code == 200

    def test_ping_returns_correct_message(self):
        response = client.get("/ping")
        data = response.json()
        assert "status" in data
        assert "EduLink" in data["status"]

    def test_root_returns_200(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_docs_accessible(self):
        response = client.get("/docs")
        assert response.status_code == 200


# ============================================================
# STUDENT REGISTRATION TESTS
# ============================================================

class TestStudentRegistration:

    def test_register_valid_student_returns_200(self):
        with patch("routes.student.save_student", mock_save_student):
            response = client.post("/student/register",
                                   json=VALID_STUDENT)
            assert response.status_code == 200

    def test_register_returns_success_status(self):
        with patch("routes.student.save_student", mock_save_student):
            response = client.post("/student/register",
                                   json=VALID_STUDENT)
            assert response.json()["status"] == "success"

    def test_register_returns_student_id(self):
        with patch("routes.student.save_student", mock_save_student):
            response = client.post("/student/register",
                                   json=VALID_STUDENT)
            assert response.json()["student_id"] == "TEST001"

    def test_register_missing_name_returns_422(self):
        bad = {**VALID_STUDENT}
        del bad["name"]
        response = client.post("/student/register", json=bad)
        assert response.status_code == 422

    def test_register_invalid_age_returns_400(self):
        with patch("routes.student.save_student", mock_save_student):
            bad = {**VALID_STUDENT, "age": 99}
            response = client.post("/student/register", json=bad)
            assert response.status_code == 400

    def test_register_invalid_grade_returns_400(self):
        with patch("routes.student.save_student", mock_save_student):
            bad = {**VALID_STUDENT, "grade": "INVALID"}
            response = client.post("/student/register", json=bad)
            assert response.status_code == 400

    def test_register_invalid_stream_returns_400(self):
        with patch("routes.student.save_student", mock_save_student):
            bad = {**VALID_STUDENT, "stream": "Unknown"}
            response = client.post("/student/register", json=bad)
            assert response.status_code == 400

    def test_get_profile_existing_student_returns_200(self):
        with patch("routes.student.get_student", mock_get_student):
            response = client.get("/student/profile/TEST001")
            assert response.status_code == 200

    def test_get_profile_unknown_student_returns_404(self):
        with patch("routes.student.get_student", lambda x: None):
            response = client.get("/student/profile/UNKNOWN999")
            assert response.status_code == 404


# ============================================================
# MCQ SUBMISSION TESTS
# ============================================================

class TestMCQSubmission:

    def test_submit_valid_mcq_returns_200(self):
        with patch("routes.mcq.save_mcq", mock_save_mcq):
            response = client.post("/student/submit-mcq",
                                   json=VALID_MCQ)
            assert response.status_code == 200

    def test_submit_mcq_returns_composites(self):
        with patch("routes.mcq.save_mcq", mock_save_mcq):
            response = client.post("/student/submit-mcq",
                                   json=VALID_MCQ)
            assert "composites" in response.json()

    def test_submit_mcq_returns_success_status(self):
        with patch("routes.mcq.save_mcq", mock_save_mcq):
            response = client.post("/student/submit-mcq",
                                   json=VALID_MCQ)
            assert response.json()["status"] == "success"

    def test_submit_mcq_invalid_answer_returns_400(self):
        with patch("routes.mcq.save_mcq", mock_save_mcq):
            bad = {**VALID_MCQ, "Q1": 6}
            response = client.post("/student/submit-mcq", json=bad)
            assert response.status_code == 400

    def test_submit_mcq_answer_zero_returns_400(self):
        with patch("routes.mcq.save_mcq", mock_save_mcq):
            bad = {**VALID_MCQ, "Q1": 0}
            response = client.post("/student/submit-mcq", json=bad)
            assert response.status_code == 400

    def test_submit_mcq_missing_question_returns_422(self):
        bad = {**VALID_MCQ}
        del bad["Q40"]
        response = client.post("/student/submit-mcq", json=bad)
        assert response.status_code == 422

    def test_submit_mcq_all_same_returns_400(self):
        with patch("routes.mcq.save_mcq", mock_save_mcq):
            same = {f"Q{i}": 3 for i in range(1, 41)}
            same["student_id"] = "TEST001"
            response = client.post("/student/submit-mcq", json=same)
            assert response.status_code == 400

    def test_submit_mcq_composites_are_normalized(self):
        with patch("routes.mcq.save_mcq", mock_save_mcq):
            response = client.post("/student/submit-mcq",
                                   json=VALID_MCQ)
            composites = response.json()["composites"]
            for key, val in composites.items():
                assert 0.0 <= float(val) <= 1.0


# ============================================================
# WRITING SUBMISSION TESTS
# ============================================================

class TestWritingSubmission:

    def test_submit_valid_writing_returns_200(self):
        with patch("routes.writing.save_writing", mock_save_writing):
            response = client.post("/student/submit-writing",
                                   json=VALID_WRITING)
            assert response.status_code == 200

    def test_submit_writing_returns_word_count(self):
        with patch("routes.writing.save_writing", mock_save_writing):
            response = client.post("/student/submit-writing",
                                   json=VALID_WRITING)
            data = response.json()
            assert "word_count" in data
            assert data["word_count"] > 0

    def test_submit_writing_returns_success_status(self):
        with patch("routes.writing.save_writing", mock_save_writing):
            response = client.post("/student/submit-writing",
                                   json=VALID_WRITING)
            assert response.json()["status"] == "success"

    def test_submit_writing_too_short_returns_400(self):
        with patch("routes.writing.save_writing", mock_save_writing):
            short = {**VALID_WRITING, "text": "Too short."}
            response = client.post("/student/submit-writing",
                                   json=short)
            assert response.status_code == 400

    def test_submit_writing_empty_returns_400(self):
        with patch("routes.writing.save_writing", mock_save_writing):
            empty = {**VALID_WRITING, "text": ""}
            response = client.post("/student/submit-writing",
                                   json=empty)
            assert response.status_code == 400

    def test_submit_writing_too_long_returns_400(self):
        with patch("routes.writing.save_writing", mock_save_writing):
            long_text = "word " * 600
            long = {**VALID_WRITING, "text": long_text}
            response = client.post("/student/submit-writing",
                                   json=long)
            assert response.status_code == 400

    def test_submit_writing_gibberish_returns_400(self):
        with patch("routes.writing.save_writing", mock_save_writing):
            gibberish = {**VALID_WRITING,
                         "text": "asdfghjkl qwerty zxcvbnm " * 10}
            response = client.post("/student/submit-writing",
                                   json=gibberish)
            assert response.status_code == 400

    def test_submit_writing_missing_student_id_returns_422(self):
        bad = {"text": VALID_WRITING["text"]}
        response = client.post("/student/submit-writing", json=bad)
        assert response.status_code == 422


# ============================================================
# REPORT GENERATION TESTS
# ============================================================

class TestReportGeneration:

    def test_generate_report_returns_200(self):
        with patch("routes.report.get_mcq", mock_get_mcq), \
             patch("routes.report.get_writing", mock_get_writing), \
             patch("routes.report.update_status", mock_update_status):
            response = client.post(
                "/student/generate-report/TEST001")
            assert response.status_code == 200

    def test_generate_report_returns_success_status(self):
        with patch("routes.report.get_mcq", mock_get_mcq), \
             patch("routes.report.get_writing", mock_get_writing), \
             patch("routes.report.update_status", mock_update_status):
            response = client.post(
                "/student/generate-report/TEST001")
            assert response.json()["status"] == "success"

    def test_generate_report_no_mcq_returns_400(self):
        with patch("routes.report.get_mcq", lambda x: None), \
             patch("routes.report.get_writing", mock_get_writing), \
             patch("routes.report.update_status", mock_update_status):
            response = client.post(
                "/student/generate-report/TEST001")
            assert response.status_code == 400

    def test_generate_report_no_writing_returns_400(self):
        with patch("routes.report.get_mcq", mock_get_mcq), \
             patch("routes.report.get_writing", lambda x: None), \
             patch("routes.report.update_status", mock_update_status):
            response = client.post(
                "/student/generate-report/TEST001")
            assert response.status_code == 400

    def test_get_report_existing_returns_200(self):
        with patch("routes.report.get_report", mock_get_report):
            response = client.get("/student/report/TEST001")
            assert response.status_code == 200

    def test_get_report_not_found_returns_404(self):
        with patch("routes.report.get_report", lambda x: None):
            response = client.get("/student/report/UNKNOWN999")
            assert response.status_code == 404

    def test_get_report_has_required_fields(self):
        with patch("routes.report.get_report", mock_get_report):
            response = client.get("/student/report/TEST001")
            data = response.json()["data"]
            for field in ["top1_cluster",
                          "final_recommended_role",
                          "confidence_label",
                          "final_score"]:
                assert field in data

    def test_get_status_returns_200(self):
        with patch("routes.report.get_status", mock_get_status):
            response = client.get(
                "/student/report-status/TEST001")
            assert response.status_code == 200

    def test_get_status_returns_done(self):
        with patch("routes.report.get_status", mock_get_status):
            response = client.get(
                "/student/report-status/TEST001")
            data = response.json()["data"]
            assert data["status"] == "done"