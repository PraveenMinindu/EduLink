# ============================================================
# EduLink — Live Salary Service
# ICTA Sri Lanka IT Salary Benchmarks + Live Exchange Rate
# ============================================================

import requests
from datetime import datetime

# ICTA Sri Lanka IT Salary Survey benchmarks (USD/month)
ICTA_SALARY_USD = {
    "Data Scientist":              {"Entry": 800,  "Mid": 1800, "Senior": 3500},
    "ML Engineer":                 {"Entry": 900,  "Mid": 2000, "Senior": 4000},
    "Data Engineer":               {"Entry": 750,  "Mid": 1700, "Senior": 3200},
    "AI Developer":                {"Entry": 850,  "Mid": 1900, "Senior": 3800},
    "Software Engineer":           {"Entry": 600,  "Mid": 1400, "Senior": 2800},
    "Full Stack Developer":        {"Entry": 650,  "Mid": 1500, "Senior": 3000},
    "Backend Developer":           {"Entry": 600,  "Mid": 1400, "Senior": 2700},
    "Frontend Developer":          {"Entry": 550,  "Mid": 1300, "Senior": 2500},
    "Mobile Developer":            {"Entry": 600,  "Mid": 1450, "Senior": 2800},
    "DevOps Engineer":             {"Entry": 700,  "Mid": 1600, "Senior": 3200},
    "Cloud Engineer":              {"Entry": 750,  "Mid": 1700, "Senior": 3400},
    "QA Engineer":                 {"Entry": 450,  "Mid": 1000, "Senior": 2000},
    "Software Tester":             {"Entry": 400,  "Mid": 900,  "Senior": 1800},
    "UI/UX Designer":              {"Entry": 500,  "Mid": 1100, "Senior": 2200},
    "Product Designer":            {"Entry": 520,  "Mid": 1150, "Senior": 2300},
    "Business Analyst":            {"Entry": 550,  "Mid": 1200, "Senior": 2400},
    "IT Project Manager":          {"Entry": 700,  "Mid": 1600, "Senior": 3000},
    "Product Manager":             {"Entry": 700,  "Mid": 1600, "Senior": 3200},
    "Network Engineer":            {"Entry": 500,  "Mid": 1100, "Senior": 2200},
    "Systems Administrator":       {"Entry": 480,  "Mid": 1050, "Senior": 2100},
    "Cybersecurity Engineer":      {"Entry": 700,  "Mid": 1600, "Senior": 3200},
    "Digital Marketer":            {"Entry": 400,  "Mid": 900,  "Senior": 1800},
    "SEO Specialist":              {"Entry": 350,  "Mid": 800,  "Senior": 1600},
    "Embedded Systems Engineer":   {"Entry": 600,  "Mid": 1300, "Senior": 2600},
    "Hardware Engineer":           {"Entry": 550,  "Mid": 1200, "Senior": 2400},
    "Database Administrator":      {"Entry": 500,  "Mid": 1100, "Senior": 2200},
    "IT Support Engineer":         {"Entry": 350,  "Mid": 750,  "Senior": 1500},
}

CLUSTER_DEFAULT_ROLE = {
    "Data_AI_Engineering":      "Data Scientist",
    "Software_Web_Engineering": "Software Engineer",
    "Network_Infrastructure":   "Network Engineer",
    "IT_Operations_QA":         "QA Engineer",
    "UX_Creative_Tech":         "UI/UX Designer",
    "Business_IT_Management":   "Business Analyst",
    "Digital_Marketing_Media":  "Digital Marketer",
    "Hardware_Systems":         "Embedded Systems Engineer",
}

# Cache exchange rate for 6 hours
_cached_rate  = None
_cache_time   = None
CACHE_HOURS   = 6
FALLBACK_RATE = 310.0  # approximate current USD/LKR


def get_usd_to_lkr() -> tuple:
    """
    Fetch live USD to LKR exchange rate.
    Returns (rate, source) tuple.
    """
    global _cached_rate, _cache_time

    # Return cached rate if still fresh
    if _cached_rate and _cache_time:
        hours_old = (datetime.now() - _cache_time).seconds / 3600
        if hours_old < CACHE_HOURS:
            return _cached_rate, "cached"

    # Try free exchange rate APIs in order
    apis = [
        {
            "url": "https://api.exchangerate-api.com/v4/latest/USD",
            "parser": lambda d: d.get("rates", {}).get("LKR")
        },
        {
            "url": "https://api.frankfurter.app/latest?from=USD&to=LKR",
            "parser": lambda d: d.get("rates", {}).get("LKR")
        },
    ]

    for api in apis:
        try:
            r = requests.get(api["url"], timeout=5)
            if r.status_code == 200:
                rate = api["parser"](r.json())
                if rate and float(rate) > 200:
                    _cached_rate = float(rate)
                    _cache_time  = datetime.now()
                    return _cached_rate, "live"
        except Exception:
            continue

    return FALLBACK_RATE, "fallback"


def predict_live(
    role:         str,
    cluster:      str = None,
    stage:        str = "Entry",
    demand_trend: str = "Stable",
) -> dict:
    """
    Predict salary using ICTA benchmarks + live exchange rate.

    Args:
        role:         job role name
        cluster:      career cluster (fallback if role not found)
        stage:        Entry | Mid | Senior
        demand_trend: Increasing | Stable | Decreasing

    Returns:
        dict with salary in USD and LKR with live exchange rate
    """
    # Find salary data
    role_data = ICTA_SALARY_USD.get(role)
    if not role_data and cluster:
        fallback_role = CLUSTER_DEFAULT_ROLE.get(cluster, "Software Engineer")
        role_data     = ICTA_SALARY_USD.get(fallback_role)
    if not role_data:
        role_data = ICTA_SALARY_USD["Software Engineer"]

    # Get base USD salary
    salary_usd = role_data.get(stage, role_data["Entry"])

    # Apply demand trend adjustment
    if demand_trend == "Increasing":
        salary_usd = int(salary_usd * 1.08)
    elif demand_trend == "Decreasing":
        salary_usd = int(salary_usd * 0.95)

    # Get live exchange rate
    exchange_rate, rate_source = get_usd_to_lkr()

    # Convert to LKR with ±15% range
    salary_lkr_mid = int(salary_usd * exchange_rate)
    salary_lkr_min = int(salary_lkr_mid * 0.85)
    salary_lkr_max = int(salary_lkr_mid * 1.15)

    return {
        "salary_usd":      salary_usd,
        "salary_min":      salary_lkr_min,
        "salary_max":      salary_lkr_max,
        "salary_mid":      salary_lkr_mid,
        "currency":        "LKR",
        "per":             "month",
        "exchange_rate":   round(exchange_rate, 2),
        "rate_source":     rate_source,
        "stage":           stage,
        "demand_trend":    demand_trend,
        "role":            role,
        "data_source":     "ICTA Sri Lanka IT Salary Survey",
        "last_updated":    datetime.now().strftime("%Y-%m-%d %H:%M"),
    }