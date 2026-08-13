# =============================================================
# EduLink — Model 7: AI Reasoning Layer
# Version 2.0 — Rule-Based Multi-Model Evidence Synthesis
# =============================================================
#
# ARCHITECTURE:
#   Stage 1 — Weighted evidence fusion (preserved from v1)
#              Exact weights and formulas from notebook unchanged.
#   Stage 2 — Evidence analysis (new)
#              Examines relationships between model outputs.
#              Identifies convergence, conflicts, development areas.
#   Stage 3 — Structured reasoning synthesis (new)
#              Builds 8-section personalized explanation.
#
# PRESERVED FROM V1:
#   All weights (W_CAREER, W_WRITING, W_DEMAND, W_SALARY)
#   All thresholds (CONFIDENCE_HIGH, CONFIDENCE_MEDIUM)
#   All output fields (final_recommended_role, confidence_label,
#                      final_score, evidence_scores, weights)
#   Backward-compatible: finalExplanation still returned as string
#
# ADDED IN V2:
#   reasoning_sections — structured dict of 8 named sections
#   richer finalExplanation — proper paragraphs, not pipe-separated
#
# =============================================================

# ── Exact weights from notebook Cell 14 ──────────────────────
W_CAREER  = 0.40
W_WRITING = 0.25
W_DEMAND  = 0.20
W_SALARY  = 0.15

assert abs(W_CAREER + W_WRITING + W_DEMAND + W_SALARY - 1.0) < 1e-9

# ── Career fit scores by rank — exact from notebook Cell 8 ───
CAREER_FIT_SCORES = {1: 100.0, 2: 70.0, 3: 40.0}

# ── Confidence thresholds — exact from notebook ───────────────
CONFIDENCE_HIGH   = 75.0
CONFIDENCE_MEDIUM = 55.0

# ── Role group writing weights — exact from notebook Cell 10 ──
ROLE_GROUP_WEIGHTS = {
    "analysis_communication": {
        "clarity": 0.35, "structure": 0.25,
        "confidence": 0.40, "analytical": 0.0, "creativity": 0.0},
    "analysis_reporting": {
        "clarity": 0.40, "structure": 0.30,
        "analytical": 0.30, "confidence": 0.0, "creativity": 0.0},
    "engineering": {
        "structure": 0.40, "clarity": 0.30,
        "analytical": 0.30, "confidence": 0.0, "creativity": 0.0},
    "research_analytical": {
        "analytical": 0.50, "structure": 0.25,
        "clarity": 0.25, "confidence": 0.0, "creativity": 0.0},
    "creative": {
        "creativity": 0.60, "clarity": 0.20,
        "confidence": 0.20, "analytical": 0.0, "structure": 0.0},
    "general": {
        "clarity": 0.333, "structure": 0.333,
        "confidence": 0.334, "analytical": 0.0, "creativity": 0.0},
}

# ── Key features per cluster ──────────────────────────────────
# Derived from SCORE_WEIGHTS in career_fit_prediction.py.
# These are the composite features with the highest weight
# for each cluster — used to assess evidence convergence.
# [B] Theory-informed engineering mapping.
CLUSTER_KEY_FEATURES = {
    "Data_AI_Engineering": [
        "Analytical_Thinking", "Data_Literacy", "Tech_Interest"],
    "Software_Web_Engineering": [
        "Tech_Adaptability", "Technical_ProblemSolving", "Analytical_Thinking"],
    "Network_Infrastructure": [
        "Technical_ProblemSolving", "Process_Optimization", "Structure_Preference"],
    "IT_Operations_QA": [
        "Structure_Preference", "Process_Optimization", "Analytical_Thinking"],
    "UX_Creative_Tech": [
        "Creativity_Index", "Innovation_Drive", "Social_Intelligence"],
    "Business_IT_Management": [
        "Leadership_Capability", "Business_Economics_Interest", "Communication_Skill"],
    "Digital_Marketing_Media": [
        "Communication_Skill", "Social_Intelligence", "Entrepreneurship_Orientation"],
    "Hardware_Systems": [
        "Technical_ProblemSolving", "Analytical_Thinking", "Tech_Adaptability"],
}

# ── Primary RIASEC dimension per cluster ─────────────────────
# [B] Derived from SCORE_WEIGHTS riasec entries.
CLUSTER_PRIMARY_RIASEC = {
    "Data_AI_Engineering":    "I",
    "Software_Web_Engineering": "R",
    "Network_Infrastructure": "R",
    "IT_Operations_QA":       "C",
    "UX_Creative_Tech":       "A",
    "Business_IT_Management": "E",
    "Digital_Marketing_Media": "A",
    "Hardware_Systems":       "R",
}

# ── Evidence strength thresholds ─────────────────────────────
# [B] Engineering estimates. Rationale:
#   Composite features range 0.20-1.00, normalised from 1-5 Likert.
#   0.70+ = student answered 3.5+ average → above neutral → "Strong"
#   0.55+ = student answered 2.75+ average → near neutral → "Moderate"
#   Below 0.55 = below neutral → "Developing"
FEATURE_STRONG    = 0.70   # composite score threshold
FEATURE_MODERATE  = 0.55

# RIASEC score thresholds (0-100 scale)
RIASEC_HIGH       = 65.0
RIASEC_MODERATE   = 50.0

# Writing score thresholds (0-100 scale)
WRITING_STRONG    = 65.0
WRITING_MODERATE  = 50.0

# Demand score thresholds (0-100 scale from forecasting model)
DEMAND_STRONG     = 65.0
DEMAND_WEAK       = 40.0

# Salary thresholds (LKR/month)
SALARY_HIGH_LKR   = 180000
SALARY_MED_LKR    = 120000


# =============================================================
# STAGE 1 — Preserved weighted fusion functions
# =============================================================

def _get_role_group(role: str) -> str:
    """Exact role group mapping from notebook Cell 10."""
    r = role.lower()
    if any(k in r for k in ["business analyst", "product", "project"]):
        return "analysis_communication"
    if any(k in r for k in ["data analyst", "bi", "marketing"]):
        return "analysis_reporting"
    if any(k in r for k in ["software", "developer", "frontend",
                              "backend", "full stack", "mobile"]):
        return "engineering"
    if any(k in r for k in ["ml", "ai", "data scientist"]):
        return "research_analytical"
    if any(k in r for k in ["ui", "ux", "designer"]):
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
                       s_min: float = 80000,
                       s_max: float = 230000) -> float:
    """Normalize salary_mid to 0-100. From notebook Cell 12 logic."""
    denom = max(s_max - s_min, 1.0)
    return round(max(0.0, min(100.0, ((salary_mid - s_min) / denom) * 100.0)), 2)


# =============================================================
# STAGE 2 — Evidence analysis helpers
# =============================================================

def _describe_feature(score: float) -> str:
    """Classify a composite feature score into strength label."""
    if score >= FEATURE_STRONG:    return "strong"
    if score >= FEATURE_MODERATE:  return "moderate"
    return "developing"


def _describe_riasec(score: float) -> str:
    """Classify a RIASEC dimension score into strength label."""
    if score >= RIASEC_HIGH:      return "high"
    if score >= RIASEC_MODERATE:  return "moderate"
    return "low"


def _describe_writing(score: float) -> str:
    """Classify a writing trait score into strength label."""
    if score >= WRITING_STRONG:   return "strong"
    if score >= WRITING_MODERATE: return "moderate"
    return "developing"


def _cluster_display_name(cluster: str) -> str:
    """Convert cluster ID to readable name."""
    names = {
        "Data_AI_Engineering":    "Data & AI Engineering",
        "Software_Web_Engineering": "Software & Web Engineering",
        "Network_Infrastructure": "Network & Infrastructure",
        "IT_Operations_QA":       "IT Operations & QA",
        "UX_Creative_Tech":       "UX & Creative Technology",
        "Business_IT_Management": "Business IT Management",
        "Digital_Marketing_Media": "Digital Marketing & Media",
        "Hardware_Systems":       "Hardware & Embedded Systems",
    }
    return names.get(cluster, cluster.replace("_", " "))


def analyzeCareerAlignment(
    cluster: str,
    features: dict,
    riasec: dict,
) -> dict:
    """
    Examine how well the student's psychometric profile aligns
    with the recommended career cluster.

    Checks:
    1. Whether key composite features for this cluster are strong.
    2. Whether the primary RIASEC dimension for this cluster is high.

    Returns structured alignment evidence dict.
    [B] Engineering decision: threshold values defined above.
    """
    key_features    = CLUSTER_KEY_FEATURES.get(cluster, [])
    primary_riasec  = CLUSTER_PRIMARY_RIASEC.get(cluster, "I")

    strong_features    = []
    moderate_features  = []
    developing_features = []

    for feat in key_features:
        score = features.get(feat, 0.0)
        label = _describe_feature(score)
        display = feat.replace("_", " ")
        entry = {"name": display, "score": round(score * 100, 1),
                 "raw": score, "label": label}
        if label == "strong":
            strong_features.append(entry)
        elif label == "moderate":
            moderate_features.append(entry)
        else:
            developing_features.append(entry)

    riasec_score = riasec.get(primary_riasec, 50.0)
    riasec_label = _describe_riasec(riasec_score)

    # Convergence count: how many independent signals support alignment
    convergence_count = len(strong_features)
    if riasec_label == "high":
        convergence_count += 1

    return {
        "cluster":              cluster,
        "primary_riasec":       primary_riasec,
        "riasec_score":         round(riasec_score, 1),
        "riasec_label":         riasec_label,
        "strong_features":      strong_features,
        "moderate_features":    moderate_features,
        "developing_features":  developing_features,
        "convergence_count":    convergence_count,
        "key_features_count":   len(key_features),
    }


def analyzeWritingReadiness(
    writing: dict,
    role: str,
    wf_score: float,
) -> dict:
    """
    Interpret writing analysis scores relative to career requirements.
    Does not merely report scores — interprets them in career context.

    [B] Role group mapping determines which traits matter most for
    each career type, from notebook Cell 10 (preserved).
    """
    group   = _get_role_group(role)
    weights = ROLE_GROUP_WEIGHTS.get(group, ROLE_GROUP_WEIGHTS["general"])

    # Identify which traits matter most for this role group
    primary_traits  = [t for t, w in weights.items() if w >= 0.30]
    secondary_traits = [t for t, w in weights.items() if 0.0 < w < 0.30]

    trait_labels = {
        "analytical":  "Analytical Thinking",
        "clarity":     "Clarity",
        "structure":   "Structure",
        "confidence":  "Confidence",
        "creativity":  "Creativity",
    }

    supporting = []
    developing = []

    for trait, w in weights.items():
        if w == 0.0:
            continue
        score = writing.get(trait, 50.0)
        label = _describe_writing(score)
        entry = {
            "trait":   trait_labels.get(trait, trait),
            "score":   round(score, 1),
            "weight":  w,
            "label":   label,
            "primary": w >= 0.30,
        }
        if label in ("strong", "moderate"):
            supporting.append(entry)
        else:
            developing.append(entry)

    overall = writing.get("overall_writing_score", 50.0)
    overall_label = _describe_writing(overall)

    return {
        "role":           role,
        "role_group":     group,
        "wf_score":       round(wf_score, 1),
        "overall":        round(overall, 1),
        "overall_label":  overall_label,
        "supporting":     supporting,
        "developing":     developing,
        "primary_traits": [trait_labels.get(t, t) for t in primary_traits],
    }


def analyzeMarketContext(
    demand_result: dict,
    salary_result: dict,
    role: str,
) -> dict:
    """
    Interpret market demand and salary in context of recommendation.
    Distinguishes personal suitability from market conditions.
    Does not treat market demand as proof of career suitability.
    """
    demand_score = demand_result.get("demand_score", 50.0)
    trend        = demand_result.get("primary_trend", "Stable")
    salary_mid   = salary_result.get("salary_mid", 0)
    future_mid   = salary_result.get("future_salary_mid", 0)

    if demand_score >= DEMAND_STRONG:
        demand_label = "strong"
    elif demand_score >= DEMAND_WEAK:
        demand_label = "moderate"
    else:
        demand_label = "weak"

    if salary_mid >= SALARY_HIGH_LKR:
        salary_label = "above average"
    elif salary_mid >= SALARY_MED_LKR:
        salary_label = "average"
    else:
        salary_label = "entry level"

    # Detect personal-market alignment conflict
    # [B] If career fit is strong but demand is weak,
    # this is a meaningful conflict worth surfacing.
    has_market_concern = demand_label == "weak" or trend == "Decreasing"

    return {
        "demand_score":      round(demand_score, 1),
        "demand_label":      demand_label,
        "trend":             trend,
        "salary_mid":        salary_mid,
        "future_mid":        future_mid,
        "salary_label":      salary_label,
        "has_market_concern": has_market_concern,
    }


def analyzeEvidenceConvergence(
    alignment: dict,
    writing_analysis: dict,
    market: dict,
    career_rank: int,
) -> dict:
    """
    Count how many independent evidence sources support the
    career recommendation and identify any conflicts.

    Evidence sources assessed independently:
    1. Career fit model rank (M1)
    2. RIASEC primary dimension (from M1 features)
    3. Key composite features (from M1 features)
    4. Writing analysis overall (M2)
    5. Market demand (M3)
    6. Salary positioning (M4)
    """
    supporting_sources = []
    conflicting_sources = []
    neutral_sources     = []

    # Source 1: Career fit model rank
    if career_rank == 1:
        supporting_sources.append("career fit model (ranked #1)")
    elif career_rank == 2:
        neutral_sources.append("career fit model (ranked #2)")
    else:
        conflicting_sources.append("career fit model (ranked #3)")

    # Source 2: RIASEC alignment
    if alignment["riasec_label"] == "high":
        supporting_sources.append(
            f"{alignment['primary_riasec']} RIASEC dimension")
    elif alignment["riasec_label"] == "moderate":
        neutral_sources.append(
            f"{alignment['primary_riasec']} RIASEC dimension")
    else:
        conflicting_sources.append(
            f"{alignment['primary_riasec']} RIASEC dimension")

    # Source 3: Key composite features
    strong_count = len(alignment["strong_features"])
    total_key    = alignment["key_features_count"]
    if strong_count >= max(1, total_key - 1):
        supporting_sources.append(
            f"psychological profile ({strong_count}/{total_key} key features strong)")
    elif strong_count > 0:
        neutral_sources.append(
            f"psychological profile ({strong_count}/{total_key} key features strong)")
    else:
        conflicting_sources.append("psychological profile (key features developing)")

    # Source 4: Writing readiness
    wf = writing_analysis["overall_label"]
    if wf == "strong":
        supporting_sources.append("writing analysis")
    elif wf == "moderate":
        neutral_sources.append("writing analysis")
    else:
        conflicting_sources.append("writing analysis (developing)")

    # Source 5: Market demand
    if market["demand_label"] == "strong":
        supporting_sources.append("market demand")
    elif market["demand_label"] == "moderate":
        neutral_sources.append("market demand")
    else:
        conflicting_sources.append("market demand")

    # Source 6: Salary
    if market["salary_label"] == "above average":
        supporting_sources.append("salary positioning")
    else:
        neutral_sources.append("salary positioning")

    convergence_level = len(supporting_sources)
    if convergence_level >= 4:
        convergence_label = "strong"
    elif convergence_level >= 2:
        convergence_label = "moderate"
    else:
        convergence_label = "weak"

    return {
        "supporting":        supporting_sources,
        "neutral":           neutral_sources,
        "conflicting":       conflicting_sources,
        "convergence_count": convergence_level,
        "convergence_label": convergence_label,
    }


def identifyDevelopmentAreas(
    alignment: dict,
    writing_analysis: dict,
) -> list:
    """
    Identify comparatively weaker dimensions that represent
    genuine development opportunities for this career path.
    Only flags areas that are specifically relevant to the cluster.
    """
    areas = []

    # Developing composite features for this cluster
    for feat in alignment["developing_features"]:
        areas.append({
            "area":    feat["name"],
            "context": "key requirement for this career cluster",
            "score":   feat["score"],
        })

    # Developing writing traits that matter for this role group
    for trait in writing_analysis["developing"]:
        if trait["primary"]:
            areas.append({
                "area":    f"{trait['trait']} (writing)",
                "context": f"important for {writing_analysis['role_group']} roles",
                "score":   trait["score"],
            })

    return areas


# =============================================================
# STAGE 3 — Structured reasoning synthesis
# =============================================================

def _fmt_lkr(n: int) -> str:
    """Format LKR number for readable display."""
    if n >= 100000:
        return f"LKR {n:,.0f}"
    return f"LKR {n:,}"


def buildCareerMatchSection(
    role: str,
    cluster: str,
    alignment: dict,
    convergence: dict,
    career_rank: int,
    interest_code: str,
) -> str:
    """
    Section 1: Why the recommended career fits the student's profile.
    Explains the alignment between psychometric profile and career.
    """
    cluster_name = _cluster_display_name(cluster)
    conv_label   = convergence["convergence_label"]

    strong_names = [f["name"] for f in alignment["strong_features"]]
    riasec_str   = f"{alignment['primary_riasec']} ({alignment['riasec_label']})"

    if conv_label == "strong":
        opener = (f"{role} emerges as the strongest career match "
                  f"from your psychometric profile, with multiple "
                  f"independent evidence sources converging on this "
                  f"recommendation.")
    elif conv_label == "moderate":
        opener = (f"{role} represents a meaningful career match "
                  f"based on your psychometric profile, supported "
                  f"by several evidence dimensions.")
    else:
        opener = (f"{role} is identified as a potential career "
                  f"direction, though the supporting evidence "
                  f"is mixed and warrants further exploration.")

    profile_detail = ""
    if strong_names:
        profile_detail = (
            f" Your profile shows particular strength in "
            f"{', '.join(strong_names)}, "
            f"which are key requirements for the {cluster_name} cluster.")

    riasec_detail = ""
    if alignment["riasec_label"] in ("high", "moderate"):
        riasec_detail = (
            f" Your primary RIASEC orientation is {riasec_str}, "
            f"which aligns with the vocational characteristics "
            f"of this career cluster.")

    code_detail = ""
    if interest_code:
        code_detail = (
            f" Your Holland Interest Code ({interest_code}) "
            f"further supports this direction.")

    return opener + profile_detail + riasec_detail + code_detail


def buildEvidenceConvergenceSection(
    convergence: dict,
    career_rank: int,
) -> str:
    """
    Section 2: Which independent model outputs support the recommendation.
    Distinguishes supporting from conflicting evidence explicitly.
    """
    supporting  = convergence["supporting"]
    conflicting = convergence["conflicting"]
    neutral     = convergence["neutral"]
    count       = convergence["convergence_count"]

    if count >= 4:
        opening = (f"Strong evidence convergence: {count} independent "
                   f"evidence sources support this recommendation.")
    elif count >= 2:
        opening = (f"Moderate evidence convergence: {count} independent "
                   f"evidence sources support this recommendation.")
    else:
        opening = ("Limited evidence convergence across the assessment "
                   "dimensions for this recommendation.")

    support_str = ""
    if supporting:
        support_str = (f" Supporting evidence includes: "
                       f"{', '.join(supporting)}.")

    conflict_str = ""
    if conflicting:
        conflict_str = (f" Areas of weaker or conflicting evidence: "
                        f"{', '.join(conflicting)}.")

    return opening + support_str + conflict_str


def buildPsychologicalSection(
    alignment: dict,
    riasec: dict,
    interest_code: str,
    cluster: str,
) -> str:
    """
    Section 3: Interpret RIASEC and composite feature results together.
    Connects psychometric evidence to career cluster requirements.
    """
    cluster_name = _cluster_display_name(cluster)
    primary      = alignment["primary_riasec"]
    riasec_score = alignment["riasec_score"]

    riasec_labels = {
        "R": "Realistic", "I": "Investigative", "A": "Artistic",
        "S": "Social",    "E": "Enterprising",  "C": "Conventional",
    }
    primary_name = riasec_labels.get(primary, primary)

    # Find highest RIASEC dimension overall
    top_riasec = max(riasec.items(), key=lambda x: x[1]) if riasec else (primary, riasec_score)
    top_name   = riasec_labels.get(top_riasec[0], top_riasec[0])

    riasec_str = (
        f"Your RIASEC profile shows the highest orientation in "
        f"{top_name} ({top_riasec[1]:.1f}/100)")
    if top_riasec[0] == primary:
        riasec_str += (f", which directly aligns with the {cluster_name} "
                       f"career cluster's primary vocational requirement.")
    else:
        riasec_str += (
            f". The {cluster_name} cluster primarily draws on "
            f"{primary_name} ({riasec_score:.1f}/100), which is "
            f"{'well-developed' if riasec_score >= RIASEC_HIGH else 'moderately developed'} "
            f"in your profile.")

    strong_str = ""
    if alignment["strong_features"]:
        names = [f["name"] for f in alignment["strong_features"]]
        strong_str = (f" Key psychological strengths supporting this "
                      f"career include: {', '.join(names)}.")

    developing_str = ""
    if alignment["developing_features"]:
        names = [f["name"] for f in alignment["developing_features"]]
        developing_str = (
            f" The following cluster-relevant dimensions are "
            f"comparatively lower in your current profile: "
            f"{', '.join(names)}. These represent areas for development.")

    return riasec_str + strong_str + developing_str


def buildWritingReadinessSection(
    writing_analysis: dict,
    role: str,
) -> str:
    """
    Section 4: Interpret writing analysis relative to career requirements.
    Does NOT simply report scores. Explains what they mean for the career.
    """
    overall       = writing_analysis["overall"]
    overall_label = writing_analysis["overall_label"]
    supporting    = writing_analysis["supporting"]
    developing    = writing_analysis["developing"]
    primary_traits = writing_analysis["primary_traits"]
    role_group    = writing_analysis["role_group"]

    group_descriptions = {
        "research_analytical": "strong analytical reasoning in writing",
        "engineering":
            "structured and technically precise communication",
        "analysis_communication":
            "clear, confident professional communication",
        "analysis_reporting":
            "clear, analytical data-driven writing",
        "creative":
            "creative and expressive communication",
        "general":
            "clear and structured written communication",
    }
    requirement = group_descriptions.get(role_group, "effective written communication")

    if overall_label == "strong":
        opening = (f"Your writing analysis demonstrates {requirement} "
                   f"at a strong level (overall score: {overall:.1f}/100), "
                   f"which is well-aligned with {role} requirements.")
    elif overall_label == "moderate":
        opening = (f"Your writing analysis shows a developing profile "
                   f"(overall score: {overall:.1f}/100). The role of "
                   f"{role} benefits from {requirement}.")
    else:
        opening = (f"Your writing analysis indicates that {requirement} "
                   f"is currently a development area "
                   f"(overall score: {overall:.1f}/100) for the {role} path.")

    support_str = ""
    if supporting:
        trait_names = [t["trait"] for t in supporting]
        support_str = f" Strengths include: {', '.join(trait_names)}."

    develop_str = ""
    primary_developing = [t for t in developing if t["primary"]]
    if primary_developing:
        names = [t["trait"] for t in primary_developing]
        develop_str = (f" The following traits are identified as "
                       f"development areas for this career: "
                       f"{', '.join(names)}.")

    return opening + support_str + develop_str


def buildMarketContextSection(
    market: dict,
    role: str,
    career_fit_strong: bool,
) -> str:
    """
    Section 5: Salary and demand interpreted as market context.
    Explicitly distinguishes personal suitability from market conditions.
    Does NOT treat demand as evidence of personal suitability.
    """
    trend  = market["trend"]
    dlabel = market["demand_label"]
    slabel = market["salary_label"]
    sal    = market["salary_mid"]
    future = market["future_mid"]

    demand_str = {
        "Increasing": f"market demand for {role} is currently increasing",
        "Stable":     f"market demand for {role} is currently stable",
        "Decreasing": f"market demand for {role} shows a declining trend",
    }.get(trend, f"market demand trend for {role} is {trend.lower()}")

    if market["has_market_concern"] and career_fit_strong:
        market_note = (
            f"While your personal suitability for this career is "
            f"strong based on your psychometric profile, {demand_str}. "
            f"Personal career fit and market demand are independent "
            f"factors — suitability for a role does not guarantee "
            f"immediate employment availability.")
    elif dlabel == "strong":
        market_note = (
            f"The market context is favourable: {demand_str}, "
            f"which creates additional opportunity alongside "
            f"your assessed career suitability.")
    else:
        market_note = (
            f"In terms of market context, {demand_str}. "
            f"This is a separate consideration from your "
            f"personal career suitability.")

    salary_note = ""
    if sal > 0:
        salary_note = (
            f" At entry level, the estimated salary range for "
            f"this role in the Sri Lankan IT sector is "
            f"{_fmt_lkr(market['salary_mid'] - int(market['salary_mid'] * 0.15))}"
            f"–{_fmt_lkr(market['salary_mid'] + int(market['salary_mid'] * 0.15))} "
            f"per month (ICTA benchmark).")
        if future > 0:
            salary_note += (
                f" At mid-career level, this is projected at "
                f"approximately {_fmt_lkr(future)} per month.")

    return market_note + salary_note


def buildDevelopmentAreasSection(areas: list) -> str:
    """
    Section 6: Development areas — honest, not discouraging.
    Only areas relevant to the recommended career cluster.
    """
    if not areas:
        return ("Your profile does not indicate significant development "
                "gaps relative to the requirements of this career cluster.")

    intro = (f"Based on the career cluster requirements, "
             f"the following areas represent meaningful development "
             f"opportunities:")

    area_strs = []
    for a in areas[:4]:  # cap at 4 to keep readable
        area_strs.append(f"{a['area']} ({a['context']})")

    area_list = "; ".join(area_strs) + "."

    closing = (" Addressing these areas through targeted study, "
               "practice, or mentorship would strengthen your "
               "readiness for this career path.")

    return intro + " " + area_list + closing


def buildEducationPathSection(
    education_programs: list,
    job_matches: list,
    role: str,
    cluster: str,
) -> str:
    """
    Section 7: Connect education and job evidence to career direction.
    Not just a list — explains the connection to the recommendation.
    """
    cluster_name = _cluster_display_name(cluster)
    parts = []

    if education_programs:
        top_prog = education_programs[0]
        prog_name = top_prog.get("program_name", "")
        institute = top_prog.get("institute", "")
        if prog_name and institute:
            parts.append(
                f"The top education recommendation — {prog_name} at "
                f"{institute} — provides the academic foundation "
                f"relevant to the {cluster_name} career path.")
        elif institute:
            parts.append(
                f"The education recommendations identify programmes "
                f"at institutions including {institute} as suitable "
                f"foundations for this career direction.")

    if job_matches:
        top_job     = job_matches[0]
        job_title   = top_job.get("title", "")
        job_company = top_job.get("company", "")
        if job_title and job_company:
            parts.append(
                f"Live job market data shows active vacancies including "
                f"{job_title} at {job_company}, indicating that "
                f"opportunities consistent with this career direction "
                f"are currently available.")

    if not parts:
        return (f"Education and employment pathway data for the "
                f"{cluster_name} cluster is included in your full report.")

    return " ".join(parts)


def buildOverallReasoningSection(
    role: str,
    confidence: str,
    final_score: float,
    convergence: dict,
    market: dict,
    has_development_areas: bool,
) -> str:
    """
    Section 8: Concise personalized synthesis.
    Ties all evidence together into one honest overall statement.
    """
    conv_label = convergence["convergence_label"]
    count      = convergence["convergence_count"]

    if confidence == "High" and conv_label == "strong":
        summary = (
            f"Overall, the evidence across all assessment dimensions "
            f"presents a consistent and well-supported case for "
            f"{role} as your primary career direction. "
            f"{count} independent evidence sources converge on this "
            f"recommendation, producing a high-confidence result "
            f"(score: {final_score:.1f}/100).")
    elif confidence == "Medium":
        summary = (
            f"Overall, {role} represents a well-grounded career "
            f"recommendation with moderate evidence support "
            f"(score: {final_score:.1f}/100). "
            f"The assessment identifies clear strengths alongside "
            f"specific areas where further development would "
            f"strengthen your readiness for this path.")
    else:
        summary = (
            f"Overall, {role} is identified as a potential career "
            f"direction based on your current profile "
            f"(score: {final_score:.1f}/100). The evidence base is "
            f"mixed, and exploring this recommendation alongside "
            f"professional career counselling is advised.")

    advisory = (" This report is intended to support your career "
                "decision-making and should be considered alongside "
                "professional guidance, institutional advice, and "
                "your own developing interests.")

    return summary + advisory


# =============================================================
# MAIN ENTRY POINT
# =============================================================

def run(
    career_result:   dict,
    writing_scores:  dict,
    salary_result:   dict,
    demand_result:   dict,
    salary2_result:  dict = None,
    salary3_result:  dict = None,
    education_result: dict = None,
    job_result:       dict = None,
) -> dict:
    """
    Run the AI Reasoning Layer v2.

    Stage 1: Weighted evidence fusion (preserved from v1)
    Stage 2: Multi-model evidence analysis
    Stage 3: Structured reasoning synthesis

    Args:
        career_result:    from career_fit_prediction.predict()
        writing_scores:   from writing_analysis_model.analyze()
        salary_result:    from salary_api.predict_live() top1 cluster
        demand_result:    from job_demand_forecasting.get_trend()
        salary2_result:   salary for top2 cluster
        salary3_result:   salary for top3 cluster
        education_result: from education_path.recommend()
        job_result:       from job_api.get_jobs()
    """
    salary_by_rank = {
        1: salary_result,
        2: salary2_result if salary2_result else salary_result,
        3: salary3_result if salary3_result else salary_result,
    }

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

    # ── Stage 1: Weighted fusion (exact from notebook) ────────
    for cluster, rank in clusters:
        roles  = career_result.get("roles", [])
        offset = (rank - 1) * 2
        role   = roles[offset] if len(roles) > offset else cluster

        cf         = CAREER_FIT_SCORES.get(rank, 40.0)
        wf         = _writing_fit_score(writing_scores, role)
        demand_score = demand_result.get("demand_score", 50.0)
        trend      = demand_result.get("primary_trend", "Stable")
        sal_mid    = salary_by_rank[rank].get("salary_mid", 150000)
        sal_score  = _normalize_salary(sal_mid)

        final = round(
            cf  * W_CAREER +
            wf  * W_WRITING +
            demand_score * W_DEMAND +
            sal_score * W_SALARY,
            2
        )

        all_evidence.append({
            "cluster":      cluster,
            "role":         role,
            "rank":         rank,
            "career_fit":   round(cf, 1),
            "writing_fit":  round(wf, 1),
            "demand_score": round(demand_score, 1),
            "salary_score": round(sal_score, 1),
            "salary_mid":   sal_mid,
            "final_score":  final,
            "demand_trend": trend,
        })

        if final > best_score:
            best_score = final
            best_role  = role
            best_rank  = rank
            best_trend = trend
            best_wf    = wf

    if best_score >= CONFIDENCE_HIGH:
        confidence = "High"
    elif best_score >= CONFIDENCE_MEDIUM:
        confidence = "Medium"
    else:
        confidence = "Low"

    # ── Stage 2: Evidence analysis ────────────────────────────
    best_cluster   = career_result[f"top{best_rank}_cluster"]
    features       = career_result.get("features", {})
    riasec         = career_result.get("riasec", {})
    interest_code  = career_result.get("interest_code", "")
    education_programs = (education_result or {}).get("programs", [])
    job_matches    = (job_result or {}).get("matches", [])
    best_salary    = salary_by_rank[best_rank]

    alignment        = analyzeCareerAlignment(best_cluster, features, riasec)
    writing_analysis = analyzeWritingReadiness(writing_scores, best_role, best_wf)
    market           = analyzeMarketContext(demand_result, best_salary, best_role)
    convergence      = analyzeEvidenceConvergence(
        alignment, writing_analysis, market, best_rank)
    dev_areas        = identifyDevelopmentAreas(alignment, writing_analysis)

    career_fit_strong = best_rank == 1 and best_score >= CONFIDENCE_MEDIUM

    # ── Stage 3: Build structured reasoning sections ──────────
    s1 = buildCareerMatchSection(
        best_role, best_cluster, alignment,
        convergence, best_rank, interest_code)
    s2 = buildEvidenceConvergenceSection(convergence, best_rank)
    s3 = buildPsychologicalSection(
        alignment, riasec, interest_code, best_cluster)
    s4 = buildWritingReadinessSection(writing_analysis, best_role)
    s5 = buildMarketContextSection(market, best_role, career_fit_strong)
    s6 = buildDevelopmentAreasSection(dev_areas)
    s7 = buildEducationPathSection(
        education_programs, job_matches, best_role, best_cluster)
    s8 = buildOverallReasoningSection(
        best_role, confidence, best_score,
        convergence, market, bool(dev_areas))

    reasoning_sections = {
        "career_match":       {"title": "Career Match",        "text": s1},
        "evidence":           {"title": "Evidence Convergence", "text": s2},
        "psychological":      {"title": "Psychological & Interest Alignment", "text": s3},
        "writing_readiness":  {"title": "Communication & Writing Readiness", "text": s4},
        "market_context":     {"title": "Market Context",       "text": s5},
        "development_areas":  {"title": "Development Areas",    "text": s6},
        "education_path":     {"title": "Education & Career Path", "text": s7},
        "overall":            {"title": "Overall Reasoning",    "text": s8},
    }

    # Build final_explanation as readable paragraphs
    # Backward compatible — still a single string
    final_explanation = "\n\n".join([
        f"[{v['title']}]\n{v['text']}"
        for v in reasoning_sections.values()
    ])

    return {
        # Preserved v1 fields — unchanged
        "final_recommended_role": best_role,
        "confidence_label":       confidence,
        "final_score":            best_score,
        "final_explanation":      final_explanation,
        "evidence_scores":        all_evidence,
        "weights": {
            "career_fit":  W_CAREER,
            "writing_fit": W_WRITING,
            "demand":      W_DEMAND,
            "salary":      W_SALARY,
        },
        # New v2 field — structured sections
        "reasoning_sections": reasoning_sections,
    }
