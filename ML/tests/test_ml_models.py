# ============================================================
# EduLink — Unit Tests for All 7 ML Models
# Run: python -m pytest tests/test_ml_models.py -v
# ============================================================

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.career_fit_prediction  import predict        as career_predict
from models.career_fit_prediction  import compute_composites
from models.writing_analysis_model import analyze        as writing_analyze
from models.job_demand_forecasting  import get_trend     as demand_get
from models.salary_api              import predict_live  as salary_predict
from models.education_path          import recommend     as edu_recommend
from models.job_api                 import get_jobs      as job_match
from models.reasoning_layer         import run           as reasoning_run
from main_pipeline                  import run_pipeline

# ── Shared test data ─────────────────────────────────────────

SAMPLE_MCQ_HIGH = {
    "Q1":5,"Q2":5,"Q3":5,"Q4":5,"Q5":5,
    "Q6":5,"Q7":5,"Q8":5,"Q9":5,"Q10":5,
    "Q11":5,"Q12":5,"Q13":5,"Q14":5,"Q15":5,
    "Q16":5,"Q17":5,"Q18":5,"Q19":5,"Q20":5,
    "Q21":5,"Q22":5,"Q23":5,"Q24":5,"Q25":5,
    "Q26":5,"Q27":5,"Q28":5,"Q29":5,"Q30":5,
    "Q31":5,"Q32":5,"Q33":5,"Q34":5,"Q35":5,
    "Q36":5,"Q37":5,"Q38":5,"Q39":5,"Q40":5,
}

SAMPLE_MCQ_LOW = {
    "Q1":1,"Q2":1,"Q3":1,"Q4":1,"Q5":1,
    "Q6":1,"Q7":1,"Q8":1,"Q9":1,"Q10":1,
    "Q11":1,"Q12":1,"Q13":1,"Q14":1,"Q15":1,
    "Q16":1,"Q17":1,"Q18":1,"Q19":1,"Q20":1,
    "Q21":1,"Q22":1,"Q23":1,"Q24":1,"Q25":1,
    "Q26":1,"Q27":1,"Q28":1,"Q29":1,"Q30":1,
    "Q31":1,"Q32":1,"Q33":1,"Q34":1,"Q35":1,
    "Q36":1,"Q37":1,"Q38":1,"Q39":1,"Q40":1,
}

SAMPLE_MCQ_MIXED = {
    "Q1":4,"Q2":5,"Q3":3,"Q4":4,"Q5":3,
    "Q6":4,"Q7":5,"Q8":3,"Q9":4,"Q10":3,
    "Q11":5,"Q12":4,"Q13":3,"Q14":4,"Q15":3,
    "Q16":4,"Q17":5,"Q18":3,"Q19":4,"Q20":3,
    "Q21":4,"Q22":5,"Q23":3,"Q24":4,"Q25":3,
    "Q26":4,"Q27":5,"Q28":3,"Q29":4,"Q30":3,
    "Q31":4,"Q32":5,"Q33":3,"Q34":4,"Q35":3,
    "Q36":4,"Q37":5,"Q38":3,"Q39":4,"Q40":3,
}

SAMPLE_WRITING_GOOD = """
I recently faced a challenge when learning Python for my school project.
At first the syntax was confusing and I made many errors. I decided to
break the problem into smaller parts and practice each concept separately.
Through this systematic approach I learned that analytical thinking and
patience are essential for solving technical problems methodically.
"""

VALID_CLUSTERS = [
    "Data_AI_Engineering",
    "Software_Web_Engineering",
    "Network_Infrastructure",
    "IT_Operations_QA",
    "UX_Creative_Tech",
    "Business_IT_Management",
    "Digital_Marketing_Media",
    "Hardware_Systems",
]


# ============================================================
# MODEL 1 — CAREER FIT PREDICTION
# ============================================================

class TestCareerFitPrediction:

    def test_output_has_required_keys(self):
        result = career_predict(SAMPLE_MCQ_MIXED)
        assert "top1_cluster"   in result
        assert "top2_cluster"   in result
        assert "top3_cluster"   in result
        assert "roles"          in result
        assert "features"       in result
        assert "cluster_scores" in result

    def test_clusters_are_valid(self):
        result = career_predict(SAMPLE_MCQ_MIXED)
        assert result["top1_cluster"] in VALID_CLUSTERS
        assert result["top2_cluster"] in VALID_CLUSTERS
        assert result["top3_cluster"] in VALID_CLUSTERS

    def test_clusters_are_distinct(self):
        result   = career_predict(SAMPLE_MCQ_MIXED)
        clusters = [result["top1_cluster"],
                    result["top2_cluster"],
                    result["top3_cluster"]]
        assert len(set(clusters)) == 3

    def test_roles_count_is_10(self):
        result = career_predict(SAMPLE_MCQ_MIXED)
        assert len(result["roles"]) == 10

    def test_roles_are_unique(self):
        result = career_predict(SAMPLE_MCQ_MIXED)
        assert len(set(result["roles"])) == len(result["roles"])

    def test_high_vs_low_scores_differ(self):
        high = career_predict(SAMPLE_MCQ_HIGH)
        low  = career_predict(SAMPLE_MCQ_LOW)
        assert high["cluster_scores"] != low["cluster_scores"]

    def test_composites_range(self):
        features = compute_composites(SAMPLE_MCQ_MIXED)
        for key, val in features.items():
            if key not in ["R","I","A","S","E","C","interest_code"]:
                assert 0.0 <= val <= 1.0

    def test_missing_key_raises_error(self):
        bad_mcq = {"Q1": 3}
        try:
            career_predict(bad_mcq)
            assert False, "Should have raised error"
        except (KeyError, Exception):
            pass

    def test_cluster_scores_positive(self):
        result = career_predict(SAMPLE_MCQ_MIXED)
        for cluster, score in result["cluster_scores"].items():
            assert score > 0

    def test_deterministic(self):
        r1 = career_predict(SAMPLE_MCQ_MIXED)
        r2 = career_predict(SAMPLE_MCQ_MIXED)
        assert r1["top1_cluster"] == r2["top1_cluster"]
        assert r1["roles"]        == r2["roles"]


# ============================================================
# MODEL 2 — WRITING ANALYSIS
# ============================================================

class TestWritingAnalysis:

    def test_output_has_required_keys(self):
        result = writing_analyze(SAMPLE_WRITING_GOOD)
        for key in ["clarity","structure","confidence",
                    "analytical","creativity","overall","word_count"]:
            assert key in result

    def test_scores_in_valid_range(self):
        result = writing_analyze(SAMPLE_WRITING_GOOD)
        for key in ["clarity","structure","confidence",
                    "analytical","creativity","overall"]:
            assert 0.0 <= result[key] <= 100.0

    def test_word_count_correct(self):
        result   = writing_analyze(SAMPLE_WRITING_GOOD)
        expected = len(SAMPLE_WRITING_GOOD.split())
        assert result["word_count"] == expected

    def test_empty_text_returns_defaults(self):
        result = writing_analyze("")
        assert result["overall"] == 50.0

    def test_short_text_does_not_crash(self):
        result = writing_analyze("I like IT.")
        assert "overall" in result
        assert 0.0 <= result["overall"] <= 100.0

    def test_overall_is_average_of_traits(self):
        result = writing_analyze(SAMPLE_WRITING_GOOD)
        traits = ["clarity","structure","confidence",
                  "analytical","creativity"]
        expected = round(sum(result[t] for t in traits) / 5, 1)
        assert abs(result["overall"] - expected) < 0.5

    def test_deterministic(self):
        r1 = writing_analyze(SAMPLE_WRITING_GOOD)
        r2 = writing_analyze(SAMPLE_WRITING_GOOD)
        assert r1["overall"]  == r2["overall"]
        assert r1["clarity"]  == r2["clarity"]


# ============================================================
# MODEL 3 — JOB DEMAND FORECASTING
# ============================================================

class TestJobDemandForecasting:

    SAMPLE_ROLES = [
        "Data Scientist","ML Engineer","Data Engineer",
        "Software Engineer","Business Analyst","QA Engineer",
        "UI/UX Designer","Network Engineer","Digital Marketer",
        "Embedded Systems Engineer"
    ]

    def test_output_has_required_keys(self):
        result = salary_predict("Data Scientist",
                                cluster="Data_AI_Engineering")
        for key in ["salary_min","salary_max","salary_mid",
                    "currency","role",
                    "future_salary_min","future_salary_max",
                    "future_salary_mid"]:
            assert key in result

    def test_trend_is_valid_value(self):
        result = demand_get(self.SAMPLE_ROLES)
        valid  = {"Increasing","Stable","Decreasing","Unknown"}
        assert result["overall_trend"] in valid
        assert result["primary_trend"] in valid

    def test_demand_score_in_range(self):
        result = demand_get(self.SAMPLE_ROLES)
        assert 0.0 <= result["demand_score"]  <= 100.0
        assert 0.0 <= result["primary_score"] <= 100.0

    def test_all_roles_covered(self):
        result = demand_get(self.SAMPLE_ROLES)
        for role in self.SAMPLE_ROLES:
            assert role in result["role_trends"]

    def test_empty_roles_no_crash(self):
        result = demand_get([])
        assert "overall_trend" in result

    def test_unknown_role_no_crash(self):
        result = demand_get(["NonExistentRole999"])
        assert result["overall_trend"] in \
               {"Stable","Unknown","Increasing","Decreasing"}


# ============================================================
# MODEL 4 — SALARY PREDICTION
# ============================================================

class TestSalaryPrediction:

    def test_output_has_required_keys(self):
        result = salary_predict("Data Scientist",
                                cluster="Data_AI_Engineering")
        for key in ["salary_min","salary_max","salary_mid",
                    "currency","role","exchange_rate"]:
            assert key in result

    def test_currency_is_lkr(self):
        result = salary_predict("Software Engineer")
        assert result["currency"] == "LKR"

    def test_min_less_than_max(self):
        result = salary_predict("Data Scientist")
        assert result["salary_min"] < result["salary_max"]

    def test_mid_between_min_and_max(self):
        result = salary_predict("ML Engineer")
        assert result["salary_min"] <= result["salary_mid"] \
                                    <= result["salary_max"]

    def test_salaries_are_positive(self):
        result = salary_predict("Software Engineer")
        assert result["salary_min"] > 0
        assert result["salary_max"] > 0
        assert result["salary_mid"] > 0

    def test_future_salary_higher_than_current(self):
        result = salary_predict("Data Scientist")
        assert result["future_salary_mid"] > result["salary_mid"]

    def test_unknown_role_uses_fallback(self):
        result = salary_predict("NonExistentRole123",
                                cluster="Data_AI_Engineering")
        assert result["salary_mid"] > 0

    def test_increasing_demand_higher_salary(self):
        inc = salary_predict("Software Engineer",
                             demand_trend="Increasing")
        dec = salary_predict("Software Engineer",
                             demand_trend="Decreasing")
        assert inc["salary_mid"] > dec["salary_mid"]

    def test_future_salary_logical(self):
        result = salary_predict("Software Engineer")
        assert result["future_salary_min"] < result["future_salary_max"]
        assert result["future_salary_min"] <= result["future_salary_mid"] \
                                       <= result["future_salary_max"]
# ============================================================
# MODEL 5 — EDUCATION PATH RECOMMENDATION
# ============================================================

class TestEducationPath:

    def test_output_has_required_keys(self):
        result = edu_recommend("Data_AI_Engineering")
        assert "programs"   in result
        assert "path_steps" in result

    def test_returns_up_to_3_programs(self):
        result = edu_recommend("Data_AI_Engineering")
        assert 1 <= len(result["programs"]) <= 3

    def test_program_has_required_fields(self):
        result = edu_recommend("Data_AI_Engineering")
        for prog in result["programs"]:
            for field in ["rank","institute","level",
                          "duration_months","cost_level"]:
                assert field in prog

    def test_returns_3_path_steps(self):
        result = edu_recommend("Data_AI_Engineering")
        assert len(result["path_steps"]) == 3

    def test_budget_constraint_low(self):
        cost_rank = {"Low":1,"Medium":2,"High":3}
        result    = edu_recommend("Data_AI_Engineering",
                                   budget="Low")
        for prog in result["programs"]:
            assert cost_rank.get(prog["cost_level"],2) <= 2

    def test_unknown_cluster_no_crash(self):
        result = edu_recommend("Unknown_Cluster_XYZ")
        assert "programs" in result

    def test_ranks_are_sequential(self):
        result = edu_recommend("Data_AI_Engineering")
        for i, prog in enumerate(result["programs"]):
            assert prog["rank"] == i + 1


# ============================================================
# MODEL 6 — JOB RECOMMENDATION
# ============================================================

class TestJobRecommendation:

    SAMPLE_ROLES = [
        "Data Scientist","ML Engineer","Data Engineer",
        "AI Developer","Database Administrator",
        "Software Developer","Software Engineer","Web Developer",
        "Business Analyst","IT Project Manager"
    ]

    def test_output_has_required_keys(self):
        result = job_match(self.SAMPLE_ROLES)
        assert "matches"     in result
        assert "source"      in result
        assert "is_live"     in result
        assert "total_found" in result

    def test_returns_matches(self):
        result = job_match(self.SAMPLE_ROLES)
        assert len(result["matches"]) >= 1

    def test_returns_max_5_matches(self):
        result = job_match(self.SAMPLE_ROLES)
        assert len(result["matches"]) <= 5

    def test_match_has_required_fields(self):
        result = job_match(self.SAMPLE_ROLES)
        for match in result["matches"]:
            for field in ["company","title","location",
                          "url","match_score"]:
                assert field in match

    def test_source_is_valid(self):
        result = job_match(self.SAMPLE_ROLES)
        assert result["source"] in \
               {"adzuna_live","local_sri_lanka_it"}

    def test_empty_roles_no_crash(self):
        result = job_match([])
        assert "matches" in result

    def test_is_live_is_boolean(self):
        result = job_match(self.SAMPLE_ROLES)
        assert isinstance(result["is_live"], bool)


# ============================================================
# MODEL 7 — AI REASONING LAYER
# ============================================================

class TestReasoningLayer:

    def setup_method(self):
        self.career  = career_predict(SAMPLE_MCQ_MIXED)
        self.writing = writing_analyze(SAMPLE_WRITING_GOOD)
        self.demand  = demand_get(self.career["roles"])
        self.salary  = salary_predict(
            self.career["roles"][0],
            cluster=self.career["top1_cluster"]
        )

    def test_output_has_required_keys(self):
        result = reasoning_run(self.career, self.writing,
                               self.salary, self.demand)
        for key in ["final_recommended_role","confidence_label",
                    "final_score","final_explanation",
                    "evidence_scores"]:
            assert key in result

    def test_confidence_is_valid(self):
        result = reasoning_run(self.career, self.writing,
                               self.salary, self.demand)
        assert result["confidence_label"] in \
               {"High","Medium","Low"}

    def test_final_score_in_range(self):
        result = reasoning_run(self.career, self.writing,
                               self.salary, self.demand)
        assert 0.0 <= result["final_score"] <= 100.0

    def test_explanation_not_empty(self):
        result = reasoning_run(self.career, self.writing,
                               self.salary, self.demand)
        assert len(result["final_explanation"]) > 10

    def test_explanation_has_5_parts(self):
        result = reasoning_run(self.career, self.writing,
                               self.salary, self.demand)
        parts  = result["final_explanation"].split("|")
        assert len(parts) == 5

    def test_weights_sum_to_one(self):
        result = reasoning_run(self.career, self.writing,
                               self.salary, self.demand)
        total  = sum(result["weights"].values())
        assert abs(total - 1.0) < 1e-9

    def test_evidence_scores_count(self):
        result = reasoning_run(self.career, self.writing,
                               self.salary, self.demand)
        assert len(result["evidence_scores"]) == 3

    def test_deterministic(self):
        r1 = reasoning_run(self.career, self.writing,
                           self.salary, self.demand)
        r2 = reasoning_run(self.career, self.writing,
                           self.salary, self.demand)
        assert r1["final_score"]            == r2["final_score"]
        assert r1["final_recommended_role"] == r2["final_recommended_role"]


# ============================================================
# FULL PIPELINE INTEGRATION
# ============================================================

class TestFullPipeline:

    def test_pipeline_runs_without_error(self):
        result = run_pipeline(SAMPLE_MCQ_MIXED,
                              SAMPLE_WRITING_GOOD)
        assert result is not None

    def test_output_has_all_sections(self):
        result = run_pipeline(SAMPLE_MCQ_MIXED,
                              SAMPLE_WRITING_GOOD)
        required = [
            "top1_cluster","top2_cluster","top3_cluster",
            "recommended_roles","salary_min","salary_max",
            "writing_clarity","writing_analytical",
            "overall_writing_score","demand_trend",
            "education_programs","vacancy_matches",
            "final_recommended_role","confidence_label",
            "final_score","final_explanation","generated_at"
        ]
        for key in required:
            assert key in result

    def test_pipeline_returns_10_roles(self):
        result = run_pipeline(SAMPLE_MCQ_MIXED,
                              SAMPLE_WRITING_GOOD)
        assert len(result["recommended_roles"]) == 10

    def test_education_programs_returned(self):
        result = run_pipeline(SAMPLE_MCQ_MIXED,
                              SAMPLE_WRITING_GOOD)
        assert len(result["education_programs"]) >= 1

    def test_vacancy_matches_returned(self):
        result = run_pipeline(SAMPLE_MCQ_MIXED,
                              SAMPLE_WRITING_GOOD)
        assert len(result["vacancy_matches"]) >= 1

    def test_salary_range_logical(self):
        result = run_pipeline(SAMPLE_MCQ_MIXED,
                              SAMPLE_WRITING_GOOD)
        assert result["salary_min"] < result["salary_max"]

    def test_pipeline_all_ones_no_crash(self):
        result = run_pipeline(SAMPLE_MCQ_LOW,
                              SAMPLE_WRITING_GOOD)
        assert "final_recommended_role" in result

    def test_pipeline_all_fives_no_crash(self):
        result = run_pipeline(SAMPLE_MCQ_HIGH,
                              SAMPLE_WRITING_GOOD)
        assert "final_recommended_role" in result

    def test_timestamp_present(self):
        result = run_pipeline(SAMPLE_MCQ_MIXED,
                              SAMPLE_WRITING_GOOD)
        assert "generated_at" in result
        assert len(result["generated_at"]) > 0
        
# ============================================================
# MATHEMATICAL LAYER — Dedicated Tests
# ============================================================

class TestMathematicalLayer:

    def test_feature_map_q1_contributes_to_analytical(self):
        # Q1 is in Analytical_Thinking [1,2,3,4,16]
        mcq_high = {f"Q{i}": 1 for i in range(1, 41)}
        mcq_low  = {f"Q{i}": 1 for i in range(1, 41)}
        mcq_high["Q1"] = 5
        high = compute_composites(mcq_high)["Analytical_Thinking"]
        low  = compute_composites(mcq_low) ["Analytical_Thinking"]
        assert high > low

    def test_feature_map_q5_contributes_to_creativity(self):
        # Q5 is in Creativity_Index [5,24,30,40]
        mcq_high = {f"Q{i}": 1 for i in range(1, 41)}
        mcq_low  = {f"Q{i}": 1 for i in range(1, 41)}
        mcq_high["Q5"] = 5
        high = compute_composites(mcq_high)["Creativity_Index"]
        low  = compute_composites(mcq_low) ["Creativity_Index"]
        assert high > low

    def test_composite_formula_correct(self):
        # Analytical_Thinking = mean(Q1,Q2,Q3,Q4,Q16) / 5
        mcq = {f"Q{i}": 1 for i in range(1, 41)}
        mcq["Q1"]  = 5
        mcq["Q2"]  = 5
        mcq["Q3"]  = 5
        mcq["Q4"]  = 5
        mcq["Q16"] = 5
        features  = compute_composites(mcq)
        expected  = round(5.0 / 5.0, 4)   # mean=5, /5 = 1.0
        assert features["Analytical_Thinking"] == expected

    def test_riasec_i_high_when_analytical_high(self):
        # I uses Analytical_Thinking(1.0) + Data_Literacy(0.9)
        # + Strategic_Vision(0.5) + Tech_Interest(0.4)
        mcq = {f"Q{i}": 1 for i in range(1, 41)}
        # Set all I-related questions high
        for q in [1,2,3,4,16,11,18,28,8,20,32,39,22,30,31,34,40]:
            mcq[f"Q{q}"] = 5
        features = compute_composites(mcq)
        # I should be highest RIASEC score
        riasec = {l: features[l] for l in ["R","I","A","S","E","C"]}
        assert riasec["I"] == max(riasec.values())

    def test_riasec_a_high_when_creativity_high(self):
        # A uses Creativity_Index(1.0) + Innovation_Drive(0.8)
        mcq = {f"Q{i}": 1 for i in range(1, 41)}
        for q in [5,24,30,40,21]:
            mcq[f"Q{q}"] = 5
        features = compute_composites(mcq)
        riasec   = {l: features[l] for l in ["R","I","A","S","E","C"]}
        assert riasec["A"] > riasec["S"]
        assert riasec["A"] > riasec["C"]

    def test_interest_code_matches_top3_riasec(self):
        features = compute_composites(SAMPLE_MCQ_MIXED)
        code     = features["interest_code"]
        assert len(code) == 3
        # All letters should be valid RIASEC
        for letter in code:
            assert letter in ["R","I","A","S","E","C"]

    def test_interest_code_ordered_by_score(self):
        features = compute_composites(SAMPLE_MCQ_HIGH)
        code     = features["interest_code"]
        scores   = [features[l] for l in code]
        # First letter should have highest or equal score
        assert scores[0] >= scores[1] >= scores[2]

    def test_all_ones_gives_minimum_composites(self):
        features = compute_composites(SAMPLE_MCQ_LOW)
        for key, val in features.items():
            if key not in ["R","I","A","S","E","C","interest_code"]:
                assert val == round(1.0 / 5.0, 4)  # 0.2

    def test_all_fives_gives_maximum_composites(self):
        features = compute_composites(SAMPLE_MCQ_HIGH)
        for key, val in features.items():
            if key not in ["R","I","A","S","E","C","interest_code"]:
                assert val == round(5.0 / 5.0, 4)  # 1.0

    def test_high_i_profile_predicts_data_ai(self):
        # Set all I-related questions to 5
        mcq = {f"Q{i}": 1 for i in range(1, 41)}
        for q in [1,2,3,4,16,11,18,28,22,30,31,34,40]:
            mcq[f"Q{q}"] = 5
        result = career_predict(mcq)
        assert result["top1_cluster"] == "Data_AI_Engineering"

    def test_high_e_profile_predicts_business(self):
        # Set all E-related questions to 5
        mcq = {f"Q{i}": 1 for i in range(1, 41)}
        for q in [15,32,35,26,34,23,25,31,33,36,37,38]:
            mcq[f"Q{q}"] = 5
        result = career_predict(mcq)
        assert result["top1_cluster"] in [
            "Business_IT_Management",
            "Digital_Marketing_Media"
        ]

    def test_high_r_profile_predicts_technical(self):
        # Set all R-related questions to 5
        mcq = {f"Q{i}": 1 for i in range(1, 41)}
        for q in [14,16,19,21,38,20,12,22,31,37]:
            mcq[f"Q{q}"] = 5
        result = career_predict(mcq)
        assert result["top1_cluster"] in [
            "Network_Infrastructure",
            "Software_Web_Engineering",
            "Hardware_Systems",
            "IT_Operations_QA"
        ]
        
        
        
    