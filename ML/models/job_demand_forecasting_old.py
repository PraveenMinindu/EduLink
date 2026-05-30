# =============================================================
# EduLink — Model 3: Job Demand Forecasting
# Converted from: job_Demand_Forcasting.ipynb
# Pre-computed ARIMA trends from the notebook output
# =============================================================

# Pre-computed from ARIMA analysis in the notebook
# Trends derived from synthetic_vacancies_sl_it_18mo.csv
DEMAND_TRENDS = {
    "ML/AI Engineer":       "Increasing",
    "Data Engineer":        "Increasing",
    "Data Analyst":         "Increasing",
    "Data Scientist":       "Increasing",
    "Software Engineer":    "Increasing",
    "Full Stack Developer": "Increasing",
    "Backend Developer":    "Stable",
    "Frontend Developer":   "Stable",
    "Mobile Developer":     "Increasing",
    "DevOps/SRE":           "Increasing",
    "Cloud Engineer":       "Increasing",
    "Cybersecurity":        "Increasing",
    "QA Engineer":          "Stable",
    "UI/UX Designer":       "Stable",
    "Network/Systems":      "Stable",
    "Business Analyst":     "Stable",
    "PM/PO/Scrum":          "Stable",
    "Intern/Trainee":       "Increasing",
    "Other":                "Stable",
}

TREND_SCORES = {
    "Increasing": 80.0,
    "Stable":     50.0,
    "Decreasing": 20.0,
    "Unknown":    50.0,
}


def _normalize_role(role: str) -> str:
    """Map a role name to the closest demand category key."""
    r = role.lower()
    if any(k in r for k in ["ml","machine learning","ai engineer","data scientist"]):
        return "Data Scientist"
    if "data engineer" in r:         return "Data Engineer"
    if "data analyst" in r:          return "Data Analyst"
    if "full stack" in r:            return "Full Stack Developer"
    if "backend" in r:               return "Backend Developer"
    if "frontend" in r:              return "Frontend Developer"
    if "mobile" in r or "flutter" in r or "android" in r: return "Mobile Developer"
    if "devops" in r or "sre" in r:  return "DevOps/SRE"
    if "cloud" in r:                 return "Cloud Engineer"
    if "cyber" in r or "security" in r: return "Cybersecurity"
    if "qa" in r or "quality" in r or "tester" in r: return "QA Engineer"
    if "ui" in r or "ux" in r or "designer" in r: return "UI/UX Designer"
    if "network" in r:               return "Network/Systems"
    if "business analyst" in r:      return "Business Analyst"
    if "project manager" in r or "product manager" in r or "scrum" in r: return "PM/PO/Scrum"
    if "software" in r or "developer" in r or "programmer" in r: return "Software Engineer"
    return "Other"


def get_trend(roles: list) -> dict:
    """
    Get demand trend for a list of roles.

    Args:
        roles: list of role names (top 10 from career fit)

    Returns:
        dict with overall_trend, primary_trend,
              role_trends, demand_score, primary_score
    """
    role_trends = {}
    for role in roles:
        key   = _normalize_role(role)
        trend = DEMAND_TRENDS.get(key, "Stable")
        role_trends[role] = trend

    trends_list  = list(role_trends.values())
    overall      = max(set(trends_list), key=trends_list.count) if trends_list else "Stable"
    primary_role = roles[0] if roles else "Unknown"
    primary_trend = role_trends.get(primary_role, "Stable")

    return {
        "overall_trend":  overall,
        "primary_trend":  primary_trend,
        "role_trends":    role_trends,
        "demand_score":   TREND_SCORES.get(overall, 50.0),
        "primary_score":  TREND_SCORES.get(primary_trend, 50.0),
    }
