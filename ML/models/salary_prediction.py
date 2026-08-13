# =============================================================
# EduLink — Model 4: Salary Prediction
# Converted from: Salary_prediction.ipynb
# Exact BASE_SALARY_MAP from notebook Cell 5
# =============================================================

# Exact salary map from notebook Cell 5 (LKR/month, Sri Lanka IT)
BASE_SALARY_MAP = {
    "Software Engineer":    170000,
    "Full Stack Developer": 185000,
    "Backend Developer":    175000,
    "Frontend Developer":   165000,
    "QA Engineer":          140000,
    "Data Analyst":         155000,
    "Data Engineer":        190000,
    "ML/AI Engineer":       220000,
    "DevOps/SRE":           210000,
    "Cloud Engineer":       205000,
    "Cybersecurity":        200000,
    "Network/Systems":      160000,
    "UI/UX Designer":       150000,
    "Mobile Developer":     175000,
    "Business Analyst":     155000,
    "PM/PO/Scrum":          230000,
    "Intern/Trainee":        80000,
    "Other":                130000,
    # Additional roles from CLUSTER_ROLES
    "Software Developer":         165000,
    "Computer Programmer":        155000,
    "Web Developer":              150000,
    "Programmer Analyst":         160000,
    "Data Scientist":             220000,
    "AI Developer":               215000,
    "Database Administrator":     155000,
    "Network Engineer":           160000,
    "Systems Administrator":      155000,
    "IT Infrastructure Engineer": 160000,
    "IT Quality Assurance Specialist": 140000,
    "Software Tester":            135000,
    "IT Support Engineer":        110000,
    "Helpdesk Analyst":           100000,
    "UI/UX Designer":             150000,
    "Product Designer":           155000,
    "Graphic Designer":           130000,
    "IT Project Manager":         195000,
    "Product Manager":            200000,
    "IT Manager":                 210000,
    "Scrum Master":               185000,
    "IT Consultant":              180000,
    "Digital Marketer":           130000,
    "SEO Specialist":             120000,
    "Content Strategist":         125000,
    "Social Media Manager":       120000,
    "Embedded Systems Engineer":  175000,
    "Hardware Engineer":          160000,
    "IoT Engineer":               180000,
}

# Stage multipliers from notebook Cell 5 logic
STAGE_MULTIPLIERS = {
    "Entry":  1.00,
    "Junior": 1.15,
    "Mid":    1.40,
    "Senior": 1.75,
}

# Demand bonus from notebook trend mapping
TREND_BONUS = {
    "Increasing":  0.08,
    "Stable":      0.00,
    "Decreasing": -0.05,
    "Unknown":     0.00,
}

# Cluster → default role fallback
CLUSTER_DEFAULT = {
    "Data_AI_Engineering":      "Data Scientist",
    "Software_Web_Engineering": "Software Engineer",
    "Network_Infrastructure":   "Network Engineer",
    "IT_Operations_QA":         "QA Engineer",
    "UX_Creative_Tech":         "UI/UX Designer",
    "Business_IT_Management":   "Business Analyst",
    "Digital_Marketing_Media":  "Digital Marketer",
    "Hardware_Systems":         "Embedded Systems Engineer",
}


def predict(
    role:         str,
    cluster:      str   = None,
    stage:        str   = "Entry",
    demand_trend: str   = "Stable",
    skills_score: float = 60.0,
) -> dict:
    """
    Predict salary range for a given role.

    Args:
        role:         job role name
        cluster:      career cluster (fallback if role not in map)
        stage:        Entry | Junior | Mid | Senior
        demand_trend: Increasing | Stable | Decreasing
        skills_score: overall writing/skills score 0-100

    Returns:
        dict with salary_min, salary_max, salary_mid, currency, role
    """
    base = BASE_SALARY_MAP.get(role)
    if base is None and cluster:
        fallback = CLUSTER_DEFAULT.get(cluster, "Software Engineer")
        base = BASE_SALARY_MAP.get(fallback, 150000)
    if base is None:
        base = 150000

    stage_mult   = STAGE_MULTIPLIERS.get(stage, 1.0)
    trend_bonus  = TREND_BONUS.get(demand_trend, 0.0)
    skills_bonus = (skills_score - 50) / 1000.0   # small adjustment

    mid = base * stage_mult * (1 + trend_bonus + skills_bonus)

    return {
        "salary_min":    int(mid * 0.85),
        "salary_max":    int(mid * 1.15),
        "salary_mid":    int(mid),
        "currency":      "LKR",
        "per":           "month",
        "stage":         stage,
        "demand_trend":  demand_trend,
        "role":          role,
    }
