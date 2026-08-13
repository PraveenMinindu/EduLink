# =============================================================
# EduLink — Phase 5 Integration Verification Script
# =============================================================
# Run from Backend/ directory:
#   cd C:\Users\Praveen\Desktop\EduLink\Backend
#   python scripts/verify_phase5.py
#
# Tests:
#   1. Seed verification
#   2. recommend() with real Firestore data
#   3. Report field presence
#   4a. Firestore failure — unit (behavior test)
#   4b. Firestore failure — pipeline integration (real run_pipeline() call)
#   5. edu_level() field name compatibility
# =============================================================

import sys
import os
import json

# ── Resolve paths ─────────────────────────────────────────────
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ML_DIR      = os.path.join(os.path.dirname(BACKEND_DIR), "ML")
sys.path.insert(0, BACKEND_DIR)
sys.path.insert(0, ML_DIR)

import firebase_admin
from firebase_admin import credentials, firestore

PASS = "✓ PASS"
FAIL = "✗ FAIL"
results = []


def check(name: str, condition: bool, detail: str = ""):
    status = PASS if condition else FAIL
    results.append((status, name, detail))
    print(f"  {status}  {name}" + (f"  [{detail}]" if detail else ""))


def init_firebase():
    if not firebase_admin._apps:
        key_path = os.path.join(BACKEND_DIR, "serviceAccountKey.json")
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred)
    return firestore.client()


# =============================================================
# TEST 1 — Seed Verification
# =============================================================

def test_seed_verification(db):
    print("\n── Test 1: Seed Verification ────────────────────────")

    expected_ids = [
        "uom_bsc_cse",
        "uom_bsc_it",
        "sliit_bsc_it",
        "sliit_bsc_se",
        "nsbm_bsc_computing",
        "apiit_bsc_computing",
        "ucsc_bsc_cs",
        "ucsc_bsc_is",
    ]

    docs = {d.id: d.to_dict()
            for d in db.collection("degree_programs").stream()}

    # 1a — All deterministic IDs exist
    for doc_id in expected_ids:
        check(
            f"Document exists: {doc_id}",
            doc_id in docs,
            f"found={doc_id in docs}",
        )

    # 1b — All have durationMonths as a number
    for doc_id in expected_ids:
        if doc_id in docs:
            dm = docs[doc_id].get("durationMonths")
            check(
                f"durationMonths is int: {doc_id}",
                isinstance(dm, (int, float)) and dm > 0,
                f"durationMonths={dm}",
            )

    # 1c — No document contains _doc_id field
    for doc_id, data in docs.items():
        if doc_id in expected_ids:
            check(
                f"_doc_id NOT stored in Firestore: {doc_id}",
                "_doc_id" not in data,
            )

    # 1d — status is Active for all seeded programs
    for doc_id in expected_ids:
        if doc_id in docs:
            status = docs[doc_id].get("status")
            check(
                f"status=Active: {doc_id}",
                status == "Active",
                f"status={status}",
            )


# =============================================================
# TEST 2 — recommend() with real Firestore data
# =============================================================

def test_recommend():
    print("\n── Test 2: recommend() — real Firestore data ────────")

    from models.education_path import recommend, _fetch_active_programs, _cache

    # Reset cache to force fresh Firestore fetch
    _cache["programs"]   = None
    _cache["fetched_at"] = None

    # 2a — Fetch active programs
    try:
        programs = _fetch_active_programs()
        check("_fetch_active_programs() succeeds", True)
        check(
            "At least 1 active program returned",
            len(programs) > 0,
            f"count={len(programs)}",
        )
    except Exception as e:
        check("_fetch_active_programs() succeeds", False, str(e))
        return

    # 2b — All returned programs have required keys
    required_keys = [
        "program_id", "institute", "program_cluster",
        "all_clusters", "program_level", "duration_months",
        "cost_level", "delivery_mode",
    ]
    for prog in programs:
        for key in required_keys:
            check(
                f"Key '{key}' in program {prog.get('program_id','')}",
                key in prog,
            )
        break  # check first program only for brevity

    # 2c — Cache hit on second call
    programs2 = _fetch_active_programs()
    check(
        "Second call returns same count (cache hit)",
        len(programs) == len(programs2),
        f"first={len(programs)} second={len(programs2)}",
    )
    check(
        "Cache is populated after first call",
        _cache["programs"] is not None,
    )

    # 2d — recommend() returns correct structure
    result = recommend(
        top1_cluster="Data_AI_Engineering",
        top2_cluster="Software_Web_Engineering",
        budget="Medium",
        mode="Mixed",
        level="AL",
        time_horizon="Normal",
    )
    check(
        "recommend() returns programs key",
        "programs" in result,
    )
    check(
        "recommend() returns path_steps key",
        "path_steps" in result,
    )
    check(
        "recommend() programs is a list",
        isinstance(result["programs"], list),
    )

    # 2e — Each program in output has correct keys
    if result["programs"]:
        prog = result["programs"][0]
        for key in ["rank", "program_id", "institute", "cluster",
                    "level", "duration_months", "cost_level", "mode", "display"]:
            check(
                f"Output program has key '{key}'",
                key in prog,
            )

    # 2f — Cluster filtering works
    for prog in result["programs"]:
        valid_clusters = ["Data_AI_Engineering", "Software_Web_Engineering"]
        check(
            f"Cluster filter correct: {prog.get('cluster')}",
            prog.get("cluster") in valid_clusters,
            f"cluster={prog.get('cluster')}",
        )


# =============================================================
# TEST 3 — Report field presence
# =============================================================

def test_report_fields():
    print("\n── Test 3: Report field presence ────────────────────")

    # We test the edu dict structure directly (not full pipeline)
    # because full pipeline requires all 7 models

    from models.education_path import recommend

    edu = recommend(
        top1_cluster="Software_Web_Engineering",
        top2_cluster="Data_AI_Engineering",
        budget="Low",
        mode="Full-time",
        level="AL",
        time_horizon="Normal",
    )

    # Simulate what main_pipeline.py builds
    education_status  = edu.get("status",  "ok")
    education_code    = edu.get("code",    "")
    education_message = edu.get("message", "")

    report_keys = {
        "education_programs":   edu["programs"],
        "education_path_steps": edu["path_steps"],
        "education_status":     education_status,
        "education_code":       education_code,
        "education_message":    education_message,
    }

    for key, val in report_keys.items():
        check(f"Report key present: {key}", val is not None)

    check(
        "education_status defaults to 'ok' on success",
        education_status == "ok",
        f"status={education_status}",
    )
    check(
        "education_code empty on success",
        education_code == "",
        f"code={education_code!r}",
    )
    check(
        "path_steps has 3 entries",
        len(edu["path_steps"]) == 3,
    )


# =============================================================
# TEST 4 — Firestore failure simulation
# =============================================================

def test_firestore_failure():
    print("\n── Test 4a: Firestore failure — unit test ───────────")

    # Patch get_db to raise
    import models.education_path as ep
    original_get_db = ep.get_db

    class FakeFirestoreError(Exception):
        pass

    def broken_get_db():
        raise FakeFirestoreError("Simulated Firestore unavailable")

    # Clear cache so _fetch_active_programs actually calls get_db
    ep._cache["programs"]   = None
    ep._cache["fetched_at"] = None
    ep.get_db = broken_get_db

    # 4a — _fetch_active_programs raises
    raised = False
    try:
        ep._fetch_active_programs()
    except FakeFirestoreError:
        raised = True
    check(
        "_fetch_active_programs() re-raises on Firestore failure",
        raised,
    )

    # 4b — Simulate what main_pipeline.py does in its except block
    from ML.main_pipeline import (
        EDU_STATUS_UNAVAILABLE,
        EDU_CODE_SERVICE_UNAVAILABLE,
        EDU_STATUS_OK,
    )

    try:
        ep._fetch_active_programs()
        edu = {"status": EDU_STATUS_OK, "programs": [], "path_steps": []}
    except Exception:
        edu = {
            "status":   EDU_STATUS_UNAVAILABLE,
            "code":     EDU_CODE_SERVICE_UNAVAILABLE,
            "message":  "Education recommendations are temporarily unavailable.",
            "programs": [],
            "path_steps": [
                "Step 1: Select one recommended program and enroll.",
                "Step 2: Follow the syllabus and complete all assessments.",
                "Step 3: Complete the qualification and progress to the next level.",
            ],
        }

    check(
        "education_status == 'unavailable' on failure",
        edu.get("status") == EDU_STATUS_UNAVAILABLE,
        f"status={edu.get('status')}",
    )
    check(
        "education_code == 'EDU_SERVICE_UNAVAILABLE'",
        edu.get("code") == EDU_CODE_SERVICE_UNAVAILABLE,
        f"code={edu.get('code')}",
    )
    check(
        "education_programs == [] on failure",
        edu.get("programs") == [],
        f"programs={edu.get('programs')}",
    )
    check(
        "path_steps still present on failure",
        len(edu.get("path_steps", [])) == 3,
    )
    check(
        "message field present on failure",
        bool(edu.get("message")),
    )

    # Restore get_db
    ep.get_db = original_get_db
    ep._cache["programs"]   = None
    ep._cache["fetched_at"] = None


# =============================================================
# TEST 5 — edu_level() field name compatibility
# =============================================================

def test_edu_level_compatibility():
    print("\n── Test 5: edu_level() field name compatibility ─────")

    from models.education_path import recommend

    result = recommend(
        top1_cluster="Data_AI_Engineering",
        top2_cluster="Software_Web_Engineering",
        budget="Medium",
        mode="Mixed",
        level="AL",
        time_horizon="Normal",
    )

    # edu_level() in main_pipeline reads prog.get("cluster") and prog.get("level")
    # Verify output programs use these exact keys
    if result["programs"]:
        for prog in result["programs"]:
            check(
                "Output program has 'cluster' key (not 'program_cluster')",
                "cluster" in prog and "program_cluster" not in prog,
                f"keys={list(prog.keys())}",
            )
            check(
                "Output program has 'level' key (not 'program_level')",
                "level" in prog and "program_level" not in prog,
                f"level={prog.get('level')}",
            )

        # Simulate edu_level() logic exactly as in main_pipeline.py
        def edu_level(cluster: str) -> str:
            for prog in result.get("programs", []):
                if prog.get("cluster") == cluster:
                    return prog.get("level", "Degree")
            return "Degree"

        top1 = result["programs"][0]["cluster"]
        level_result = edu_level(top1)
        check(
            f"edu_level('{top1}') returns valid level",
            level_result in ["Degree", "Diploma", "Short"],
            f"level={level_result}",
        )
        check(
            "edu_level() does not return default 'Degree' for matched cluster",
            level_result != "Degree" or result["programs"][0].get("level") == "Degree",
        )
    else:
        check("Programs returned for edu_level test", False, "No programs returned")



# =============================================================
# TEST 4b — Real pipeline integration: Firestore failure
# Calls run_pipeline() with _fetch_active_programs patched
# to raise. Verifies main_pipeline.py catches correctly and
# the final report is still produced with education_status set.
# =============================================================

def test_pipeline_firestore_failure():
    print("\n── Test 4b: Firestore failure — pipeline integration ─")

    import models.education_path as ep
    from main_pipeline import (
        run_pipeline,
        EDU_STATUS_UNAVAILABLE,
        EDU_CODE_SERVICE_UNAVAILABLE,
    )

    original_fetch = ep._fetch_active_programs

    class FakeFirestoreError(Exception):
        pass

    def broken_fetch():
        raise FakeFirestoreError("Simulated Firestore unavailable")

    # Clear cache then patch
    ep._cache["programs"]   = None
    ep._cache["fetched_at"] = None
    ep._fetch_active_programs = broken_fetch

    TEST_MCQ = {f"Q{i}": 3 for i in range(1, 41)}
    TEST_WRITING = (
        "I enjoy solving complex problems using technology. "
        "I recently built a small Python script to automate a task at school. "
        "Through this I learned that breaking problems into small steps is key."
    )

    report = None
    pipeline_raised = False
    try:
        report = run_pipeline(
            mcq=TEST_MCQ,
            writing_text=TEST_WRITING,
            budget="Medium",
            mode="Mixed",
            level="AL",
        )
    except Exception as e:
        pipeline_raised = True
        check(
            "run_pipeline() does NOT raise on Model 5 failure",
            False,
            f"Exception: {e}",
        )
    finally:
        # Always restore
        ep._fetch_active_programs = original_fetch
        ep._cache["programs"]     = None
        ep._cache["fetched_at"]   = None

    if pipeline_raised:
        return

    check(
        "run_pipeline() completes without raising",
        report is not None,
    )

    # Education fields
    check(
        "education_status == 'unavailable'",
        report.get("education_status") == EDU_STATUS_UNAVAILABLE,
        f"status={report.get('education_status')}",
    )
    check(
        "education_code == 'EDU_SERVICE_UNAVAILABLE'",
        report.get("education_code") == EDU_CODE_SERVICE_UNAVAILABLE,
        f"code={report.get('education_code')}",
    )
    check(
        "education_programs == []",
        report.get("education_programs") == [],
        f"programs={report.get('education_programs')}",
    )
    check(
        "education_message is non-empty string",
        bool(report.get("education_message")),
        f"message={report.get('education_message')!r}",
    )
    check(
        "education_path_steps still present",
        len(report.get("education_path_steps", [])) == 3,
    )

    # Other models still ran — verify key report fields exist
    for key in [
        "top1_cluster", "top2_cluster", "top3_cluster",
        "final_recommended_role", "confidence_label", "final_score",
        "salary_min", "salary_max",
        "demand_trend",
        "vacancy_matches",
        "overall_writing_score",
        "generated_at",
    ]:
        check(
            f"Report still contains '{key}' after Model 5 failure",
            key in report,
        )

# =============================================================
# MAIN
# =============================================================

def main():
    print("=" * 56)
    print("  EduLink Phase 5 — Integration Verification")
    print("=" * 56)

    try:
        db = init_firebase()
        print("\n  Firebase initialized OK")
    except Exception as e:
        print(f"\n  ERROR: Cannot initialize Firebase: {e}")
        sys.exit(1)

    test_seed_verification(db)
    test_recommend()
    test_report_fields()
    test_firestore_failure()
    test_pipeline_firestore_failure()
    test_edu_level_compatibility()

    # ── Summary ───────────────────────────────────────────────
    passed = sum(1 for r in results if r[0] == PASS)
    failed = sum(1 for r in results if r[0] == FAIL)
    total  = len(results)

    print("\n" + "=" * 56)
    print(f"  Results: {passed}/{total} passed")
    if failed:
        print(f"\n  FAILED ({failed}):")
        for status, name, detail in results:
            if status == FAIL:
                print(f"    ✗  {name}" + (f"  [{detail}]" if detail else ""))
    else:
        print("  All checks passed. Phase 5 integration verified.")
    print("=" * 56)

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
