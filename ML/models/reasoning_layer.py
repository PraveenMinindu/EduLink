# =============================================================
# EduLink — Model 7: AI Reasoning Layer
# Converted from: AI_Reasoning_Layer.ipynb
# Exact weights: W_CAREER=0.40, W_DEMAND=0.20,
#                W_SALARY=0.15, W_WRITING=0.25
# =============================================================

# Exact weights from notebook Cell 14
W_CAREER  = 0.40
W_WRITING = 0.25
W_DEMAND  = 0.20
W_SALARY  = 0.15

assert abs(W_CAREER + W_WRITING + W_DEMAND + W_SALARY - 1.0) < 1e-9

# Career fit scores by rank — exact from notebook Cell 8
CAREER_FIT_SCORES = {1: 100.0, 2: 70.0, 3: 40.0}

# Confidence thresholds — exact from notebook
CONFIDENCE_HIGH   = 75.0
CONFIDENCE_MEDIUM = 55.0

# Role group writing weights — exact from notebook Cell 10
ROLE_GROUP_WEIGHTS = {
    "analysis_communication": {"clarity":0.35,"structure":0.25,"confidence":0.40,"analytical":0.0,"creativity":0.0},
    "analysis_reporting":     {"clarity":0.40,"structure":0.30,"analytical":0.30,"confidence":0.0,"creativity":0.0},
    "engineering":            {"structure":0.40,"clarity":0.30,"analytical":0.30,"confidence":0.0,"creativity":0.0},
    "research_analytical":    {"analytical":0.50,"structure":0.25,"clarity":0.25,"confidence":0.0,"creativity":0.0},
    "creative":               {"creativity":0.60,"clarity":0.20,"confidence":0.20,"analytical":0.0,"structure":0.0},
    "general":                {"clarity":0.333,"structure":0.333,"confidence":0.334,"analytical":0.0,"creativity":0.0},
}


def _get_role_group(role: str) -> str:
    """Exact role group mapping from notebook Cell 10."""
    r = role.lower()
    if any(k in r for k in ["business analyst","product","project"]):
        return "analysis_communication"
    if any(k in r for k in ["data analyst","bi","marketing"]):
        return "analysis_reporting"
    if any(k in r for k in ["software","developer","frontend","backend","full stack","mobile"]):
        return "engineering"
    if any(k in r for k in ["ml","ai","data scientist"]):
        return "research_analytical"
    if any(k in r for k in ["ui","ux","designer"]):
        return "creative"
    return "general"


def _writing_fit_score(writing: dict, role: str) -> float:
    """Exact writing fit formula from notebook Cell 10."""
    group   = _get_role_group(role)
    weights = ROLE_GROUP_WEIGHTS.get(group, ROLE_GROUP_WEIGHTS["general"])
    return round(
        sum(writing.get(trait, 50.0) * w for trait, w in weights.items()), 2
    )


def _normalize_salary(salary_mid: float,
                       s_min: float = 55000,
                       s_max: float = 650000) -> float:
    """Normalize salary_mid to 0-100. From notebook Cell 12 logic."""
    denom = max(s_max - s_min, 1.0)
    return round(max(0.0, min(100.0, ((salary_mid - s_min) / denom) * 100.0)), 2)


def _build_explanation(role: str, rank: int, demand_trend: str,
                        wf_score: float, final_score: float,
                        confidence: str, writing: dict) -> str:
    """
    Exact explanation format from notebook:
    reason_1 | reason_2 | reason_3 | reason_4 | reason_5
    """
    r1 = f"Career Fit ranked this role #{rank} (strong match)."

    r2 = (f"Market demand trend: {demand_trend}."
          if demand_trend != "Unknown"
          else "Market demand data not available; used neutral score.")

    r3 = f"Writing profile supports this role (writing fit score={round(wf_score,1)})."

    r4 = (f"Final integrated score={round(final_score,1)} "
          f"(weighted evidence integration).")

    r5 = f"Confidence label: {confidence}."

    return " | ".join([r1, r2, r3, r4, r5])


def run(
    career_result:  dict,
    writing_scores: dict,
    salary_result:  dict,
    demand_result:  dict,
) -> dict:
    """
    Run the AI Reasoning Layer.
    Exact weighted formula from notebook Cell 14.

    Args:
        career_result:  from career_fit_prediction.predict()
        writing_scores: from writing_analysis_model.analyze()
        demand_result:  from job_demand_forecasting.get_trend()

    Returns:
        dict with final_recommended_role, confidence_label,
              final_score, final_explanation, evidence_scores
    """
    clusters = [
        (career_result["top1_cluster"], 1),
        (career_result["top2_cluster"], 2),
        (career_result["top3_cluster"], 3),
    ]

    all_evidence = []
    best_score   = -1.0
    best_role    = None
    best_rank    = 1
    best_trend   = "Stable"
    best_wf      = 50.0

    for cluster, rank in clusters:
        roles  = career_result.get("roles", [])
        # Role for this cluster rank (offset by rank position)
        offset = (rank - 1) * 2
        role   = roles[offset] if len(roles) > offset else cluster

        # 1. Career fit score (exact from notebook)
        cf = CAREER_FIT_SCORES.get(rank, 40.0)

        # 2. Writing fit score (exact formula from notebook)
        wf = _writing_fit_score(writing_scores, role)

        # 3. Demand score (exact from notebook)
        demand_score = demand_result.get("demand_score", 50.0)
        trend        = demand_result.get("primary_trend", "Stable")

        # 4. Salary score (normalized)
        sal_mid   = salary_result.get("salary_mid", 150000)
        sal_score = _normalize_salary(sal_mid)

        # 5. Final weighted score — EXACT from notebook Cell 14
        final = round(
            cf  * W_CAREER +
            wf  * W_WRITING +
            demand_score * W_DEMAND +
            sal_score * W_SALARY,
            2
        )

        all_evidence.append({
            "cluster":       cluster,
            "role":          role,
            "rank":          rank,
            "career_fit":    round(cf, 1),
            "writing_fit":   round(wf, 1),
            "demand_score":  round(demand_score, 1),
            "salary_score":  round(sal_score, 1),
            "final_score":   final,
            "demand_trend":  trend,
        })

        if final > best_score:
            best_score = final
            best_role  = role
            best_rank  = rank
            best_trend = trend
            best_wf    = wf

    # Confidence label — exact from notebook
    if best_score >= CONFIDENCE_HIGH:
        confidence = "High"
    elif best_score >= CONFIDENCE_MEDIUM:
        confidence = "Medium"
    else:
        confidence = "Low"

    explanation = _build_explanation(
        best_role, best_rank, best_trend,
        best_wf, best_score, confidence, writing_scores
    )

    return {
        "final_recommended_role": best_role,
        "confidence_label":       confidence,
        "final_score":            best_score,
        "final_explanation":      explanation,
        "evidence_scores":        all_evidence,
        "weights": {
            "career_fit":  W_CAREER,
            "writing_fit": W_WRITING,
            "demand":      W_DEMAND,
            "salary":      W_SALARY,
        },
    }
