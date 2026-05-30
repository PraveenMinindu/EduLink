# =============================================================
# EduLink — Main Pipeline
# Connects all 7 models end-to-end for one student
# =============================================================

import sys
import os
sys.path.append(os.path.dirname(__file__))

from models.career_fit_prediction  import predict        as career_predict
from models.career_fit_prediction  import CLUSTER_ROLES
from models.writing_analysis_model import analyze        as writing_analyze
from models.job_demand_forecasting  import get_trend     as demand_get
from models.salary_api              import predict_live  as salary_predict
from models.education_path          import recommend     as edu_recommend
from models.job_api                 import get_jobs      as job_match
from models.reasoning_layer         import run           as reasoning_run

from datetime import datetime


def _get_cluster_primary_role(cluster: str) -> str:
    """Get the primary role for a cluster."""
    roles = CLUSTER_ROLES.get(cluster, ["Software Engineer"])
    return roles[0] if roles else "Software Engineer"


def run_pipeline(mcq: dict, writing_text: str,
                 budget: str = "Medium",
                 mode:   str = "Mixed",
                 level:  str = "AL") -> dict:
    """
    Run the full EduLink ML pipeline for one student.

    Args:
        mcq:          dict Q1..Q40 with values 1-5
        writing_text: string writing sample
        budget:       Low | Medium | High
        mode:         Full-time | Mixed | Online
        level:        OL | AL

    Returns:
        Complete career report as dict
    """

    print("[1/7] Career Fit Prediction...")
    career = career_predict(mcq)
    print(f"      Top1:  {career['top1_cluster']}")
    print(f"      Top2:  {career['top2_cluster']}")
    print(f"      Top3:  {career['top3_cluster']}")
    print(f"      Roles: {career['roles'][:3]}...")

    # Get primary role for each cluster
    top1_cluster = career["top1_cluster"]
    top2_cluster = career["top2_cluster"]
    top3_cluster = career["top3_cluster"]

    top1_role = _get_cluster_primary_role(top1_cluster)
    top2_role = _get_cluster_primary_role(top2_cluster)
    top3_role = _get_cluster_primary_role(top3_cluster)

    print("[2/7] Writing Analysis...")
    writing = writing_analyze(writing_text)
    print(f"      Clarity: {writing['clarity']}  Analytical: {writing['analytical']}  Overall: {writing['overall_writing_score']}")

    print("[3/7] Job Demand Forecasting...")
    # Run demand for ALL 3 clusters separately
    demand  = demand_get(career["roles"])  # overall for main report
    demand1 = demand_get([top1_role])
    demand2 = demand_get([top2_role])
    demand3 = demand_get([top3_role])
    print(f"      Overall trend:  {demand['overall_trend']}")
    print(f"      Cluster1 trend: {demand1['primary_trend']}")
    print(f"      Cluster2 trend: {demand2['primary_trend']}")
    print(f"      Cluster3 trend: {demand3['primary_trend']}")

    print("[4/7] Salary Prediction (live rate)...")
    # Run salary for ALL 3 clusters separately
    salary  = salary_predict(
        role=top1_role,
        cluster=top1_cluster,
        demand_trend=demand1["primary_trend"],
    )
    salary2 = salary_predict(
        role=top2_role,
        cluster=top2_cluster,
        demand_trend=demand2["primary_trend"],
    )
    salary3 = salary_predict(
        role=top3_role,
        cluster=top3_cluster,
        demand_trend=demand3["primary_trend"],
    )
    print(f"      Salary source: {salary['data_source']}")
    print(f"      Cluster1: LKR {salary['salary_min']:,} – {salary['salary_max']:,} (current) | LKR {salary['future_salary_mid']:,} (3-5 yrs)")
    print(f"      Cluster2: LKR {salary2['salary_min']:,} – {salary2['salary_max']:,} (current) | LKR {salary2['future_salary_mid']:,} (3-5 yrs)")
    print(f"      Cluster3: LKR {salary3['salary_min']:,} – {salary3['salary_max']:,} (current) | LKR {salary3['future_salary_mid']:,} (3-5 yrs)")

    print("[5/7] Education Path Recommendation...")
    edu = edu_recommend(
        top1_cluster=top1_cluster,
        top2_cluster=top2_cluster,
        top3_cluster=top3_cluster,
        budget=budget,
        mode=mode,
        level=level,
    )
    if edu["programs"]:
        print(f"      Top program: {edu['programs'][0]['institute']}")

    print("[6/7] Job Recommendation...")
    jobs = job_match(career["roles"])
    print(f"      Source: {jobs['source']} ({'live' if jobs['is_live'] else 'local'})")
    if jobs["matches"]:
        print(f"      Top match: {jobs['matches'][0]['title']} @ {jobs['matches'][0]['company']}")

    print("[7/7] AI Reasoning Layer...")
    final = reasoning_run(career, writing, salary, demand)
    print(f"      Final role:  {final['final_recommended_role']}")
    print(f"      Score:       {final['final_score']}")
    print(f"      Confidence:  {final['confidence_label']}")

    # ── Get profile fit scores per cluster from career model ──
    cluster_scores = career.get("cluster_scores", {})
    top1_score     = cluster_scores.get(top1_cluster, 1.0)

    def fit_percent(cluster: str) -> float:
        """Normalise cluster score against top1 score."""
        score = cluster_scores.get(cluster, 0.5)
        if top1_score == 0:
            return 50.0
        return round(min(100.0, (score / top1_score) * 100), 1)

    # ── Get education level per cluster ──────────────────────
    def edu_level(cluster: str) -> str:
        for prog in edu.get("programs", []):
            if prog.get("cluster") == cluster:
                return prog.get("level", "Degree")
        return "Degree"

    # ── Build cluster_data for Compare screen ─────────────────
    cluster_data = {
        top1_cluster: {
            "role":         top1_role,
            "salary_min":   salary["salary_min"],
            "salary_max":   salary["salary_max"],
            "salary_mid":   salary["salary_mid"],
            "demand_trend": demand1["primary_trend"],
            "demand_score": demand1["demand_score"],
            "fit_score":    fit_percent(top1_cluster),
            "edu_level":    edu_level(top1_cluster),
        },
        top2_cluster: {
            "role":         top2_role,
            "salary_min":   salary2["salary_min"],
            "salary_max":   salary2["salary_max"],
            "salary_mid":   salary2["salary_mid"],
            "demand_trend": demand2["primary_trend"],
            "demand_score": demand2["demand_score"],
            "fit_score":    fit_percent(top2_cluster),
            "edu_level":    edu_level(top2_cluster),
        },
        top3_cluster: {
            "role":         top3_role,
            "salary_min":   salary3["salary_min"],
            "salary_max":   salary3["salary_max"],
            "salary_mid":   salary3["salary_mid"],
            "demand_trend": demand3["primary_trend"],
            "demand_score": demand3["demand_score"],
            "fit_score":    fit_percent(top3_cluster),
            "edu_level":    edu_level(top3_cluster),
        },
    }

    # ── Build complete report ──────────────────────────────────
    report = {
        # Career clusters
        "top1_cluster":           top1_cluster,
        "top2_cluster":           top2_cluster,
        "top3_cluster":           top3_cluster,
        "recommended_roles":      career["roles"],
        # Personality profile data for Flutter report screen
        "interest_code":          career.get("interest_code", ""),
        "riasec":                 career.get("riasec", {}),
        "features":               career.get("features", {}),

        # Salary — top1 cluster (main report)
        "salary_min":             salary["salary_min"],
        "salary_max":             salary["salary_max"],
        "salary_mid":             salary["salary_mid"],
        "salary_currency":        "LKR",
        "exchange_rate":          salary["exchange_rate"],
        "rate_source":            salary["rate_source"],
        "salary_data_source":     salary["data_source"],

        # Per-cluster data for Compare screen
        "cluster_data":           cluster_data,

        # Writing scores
        "writing_clarity":        writing["clarity"],
        "writing_structure":      writing["structure"],
        "writing_confidence":     writing["confidence"],
        "writing_analytical":     writing["analytical"],
        "writing_creativity":     writing["creativity"],
        "overall_writing_score":  writing["overall_writing_score"],
        "writing_word_count":     writing.get("word_count", 0),

        # Demand
        "demand_trend":           demand["overall_trend"],
        "primary_demand_trend":   demand["primary_trend"],
        "demand_score":           demand["demand_score"],
        "role_demand_trends":     demand["role_trends"],

        # Education
        "education_programs":     edu["programs"],
        "education_path_steps":   edu["path_steps"],

        # Vacancies
        "vacancy_matches":        jobs["matches"],
        "vacancy_source":         jobs["source"],
        "vacancy_is_live":        jobs["is_live"],
        "vacancy_fetched_at":     jobs["fetched_at"],

        # Final XAI output
        "final_recommended_role": final["final_recommended_role"],
        "confidence_label":       final["confidence_label"],
        "final_score":            final["final_score"],
        "final_explanation":      final["final_explanation"],
        "evidence_scores":        final["evidence_scores"],
        "weights_used":           final.get("weights", {}),

        "generated_at": datetime.now().isoformat(),
    }

    return report


# ── Local test ────────────────────────────────────────────────
if __name__ == "__main__":
    TEST_MCQ = {
        "Q1":4,"Q2":5,"Q3":3,"Q4":4,"Q5":3,
        "Q6":4,"Q7":5,"Q8":3,"Q9":4,"Q10":3,
        "Q11":5,"Q12":4,"Q13":3,"Q14":4,"Q15":3,
        "Q16":4,"Q17":5,"Q18":3,"Q19":4,"Q20":3,
        "Q21":4,"Q22":5,"Q23":3,"Q24":4,"Q25":3,
        "Q26":4,"Q27":5,"Q28":3,"Q29":4,"Q30":3,
        "Q31":4,"Q32":5,"Q33":3,"Q34":4,"Q35":3,
        "Q36":4,"Q37":5,"Q38":3,"Q39":4,"Q40":3,
    }

    TEST_WRITING = """
    I recently faced a challenge when learning Python for my school project.
    At first the syntax was confusing and I made many errors. I decided to
    break the problem into smaller parts and practice each concept separately.
    I also watched tutorials and asked my teacher for help. Through this
    experience I learned that systematic thinking and patience are essential
    for solving technical problems analytically and methodically.
    """

    print("\n" + "="*55)
    print("  EduLink — Full Pipeline Test")
    print("="*55 + "\n")

    result = run_pipeline(TEST_MCQ, TEST_WRITING)

    print("\n" + "="*55)
    print("  FINAL REPORT")
    print("="*55)
    print(f"  Role:         {result['final_recommended_role']}")
    print(f"  Confidence:   {result['confidence_label']}")
    print(f"  Score:        {result['final_score']}")
    print(f"  Cluster:      {result['top1_cluster']}")
    print(f"  Salary:       LKR {result['salary_min']:,} – {result['salary_max']:,}")
    print(f"  Exchange:     1 USD = LKR {result['exchange_rate']} ({result['rate_source']})")
    print()
    print("  CLUSTER DATA:")
    for cluster, data in result["cluster_data"].items():
        print(f"    {cluster}:")
        print(f"      Role:    {data['role']}")
        print(f"      Salary:  LKR {data['salary_mid']:,}")
        print(f"      Demand:  {data['demand_trend']}")
        print(f"      Fit:     {data['fit_score']}%")
    print("="*55)
