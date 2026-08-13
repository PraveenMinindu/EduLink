# =============================================================
# EduLink — Model 3: Job Demand Forecasting
# Version: 2.0 — Live Adzuna data collection + ARIMA
#
# How it works:
#   1. collect_monthly_demand() — called once per month
#      Fetches real job counts from Adzuna API
#      Saves to Firebase Firestore as time series
#
#   2. calculate_trend() — called when pipeline runs
#      Reads history from Firestore
#      Runs ARIMA when 6+ months available
#      Falls back to linear trend for < 6 months
#
#   3. get_trend() — called by main_pipeline.py
#      Tries Firestore real data first
#      Falls back to pre-computed baseline if no data yet
# =============================================================

import requests
import warnings
from datetime import datetime
from collections import defaultdict

warnings.filterwarnings("ignore")

# ── Adzuna API credentials ────────────────────────────────────
ADZUNA_APP_ID  = "8ed884a5"
ADZUNA_APP_KEY = "2a8d6f97d7e05630624dde8a54250af9"

# ── Role to Adzuna search keyword mapping ─────────────────────
ROLE_SEARCH_KEYWORDS = {
    "ML/AI Engineer":       "machine learning engineer AI",
    "Data Engineer":        "data engineer",
    "Data Analyst":         "data analyst",
    "Data Scientist":       "data scientist",
    "Software Engineer":    "software engineer developer",
    "Full Stack Developer": "full stack developer",
    "Backend Developer":    "backend developer",
    "Frontend Developer":   "frontend developer",
    "Mobile Developer":     "mobile developer flutter android",
    "DevOps/SRE":           "devops engineer",
    "Cloud Engineer":       "cloud engineer AWS azure",
    "Cybersecurity":        "cybersecurity engineer",
    "QA Engineer":          "QA engineer testing",
    "UI/UX Designer":       "UI UX designer figma",
    "Network/Systems":      "network engineer",
    "Business Analyst":     "business analyst IT",
    "PM/PO/Scrum":          "IT project manager scrum",
}

# ── Baseline trends (pre-computed from ARIMA on synthetic data) ──
# Used as fallback when Firestore has insufficient real data
# Source: job_Demand_Forcasting_.ipynb
BASELINE_TRENDS = {
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
    "Other":                "Stable",
}

TREND_SCORES = {
    "Increasing": 80.0,
    "Stable":     50.0,
    "Decreasing": 20.0,
    "Unknown":    50.0,
}

MIN_MONTHS_FOR_ARIMA  = 6
MIN_MONTHS_FOR_LINEAR = 3


# ── Step 1: Monthly data collection ──────────────────────────

def _fetch_adzuna_count(keyword: str) -> int:
    """
    Fetch total job count for a keyword from Adzuna API.
    Uses India region (closest to Sri Lanka).
    Returns count or 0 on failure.
    """
    try:
        r = requests.get(
            "https://api.adzuna.com/v1/api/jobs/in/search/1",
            params={
                "app_id":           ADZUNA_APP_ID,
                "app_key":          ADZUNA_APP_KEY,
                "what":             keyword,
                "results_per_page": 1,
                "content-type":     "application/json",
            },
            timeout=8,
        )
        if r.status_code == 200:
            return int(r.json().get("count", 0))
        return 0
    except Exception:
        return 0


def collect_monthly_demand(firebase_bridge=None) -> dict:
    """
    Collect real job counts from Adzuna for all roles.
    Call this function once per month (manually or scheduled).

    Saves each role's count to Firestore:
      Collection: job_demand_history
      Document:   {role}_{YYYY-MM}
      Fields:     role, month, count, source, collected_at

    Args:
        firebase_bridge: firebase_bridge module (optional)
                         if None, returns data without saving

    Returns:
        dict of {role: count} for this month
    """
    month   = datetime.now().strftime("%Y-%m")
    results = {}

    print(f"Collecting job demand data for {month}...")

    for role, keyword in ROLE_SEARCH_KEYWORDS.items():
        count = _fetch_adzuna_count(keyword)
        results[role] = count
        print(f"  {role}: {count} jobs found")

        if firebase_bridge:
            try:
                firebase_bridge.save_demand_datapoint(
                    role=role,
                    month=month,
                    count=count,
                    source="adzuna_live",
                )
            except Exception as e:
                print(f"  Warning: could not save {role} to Firestore: {e}")

    print(f"Collection complete. {len(results)} roles processed.")
    return results


# ── Step 2: ARIMA trend calculation ───────────────────────────

def _linear_trend(counts: list) -> str:
    """
    Simple linear regression trend for < 6 months of data.
    Returns Increasing / Stable / Decreasing.
    """
    n = len(counts)
    if n < 2:
        return "Stable"

    x_mean = (n - 1) / 2.0
    y_mean = sum(counts) / n

    numerator   = sum((i - x_mean) * (counts[i] - y_mean) for i in range(n))
    denominator = sum((i - x_mean) ** 2 for i in range(n))

    if denominator == 0:
        return "Stable"

    slope = numerator / denominator

    # Slope threshold: 10% change over the period
    threshold = y_mean * 0.10 / n if y_mean > 0 else 0.5

    if slope > threshold:
        return "Increasing"
    elif slope < -threshold:
        return "Decreasing"
    else:
        return "Stable"


def _arima_trend(counts: list, forecast_steps: int = 3) -> str:
    """
    Run ARIMA on historical counts and return trend.
    Requires statsmodels installed.
    Falls back to linear trend if ARIMA fails.
    """
    try:
        from statsmodels.tsa.arima.model import ARIMA

        ORDERS = [(1, 1, 1), (2, 1, 2), (1, 1, 0), (0, 1, 1)]
        best_model = None
        best_aic   = float("inf")

        for order in ORDERS:
            try:
                fit = ARIMA(counts, order=order).fit()
                if fit.aic < best_aic:
                    best_aic   = fit.aic
                    best_model = fit
            except Exception:
                continue

        if best_model is None:
            return _linear_trend(counts)

        forecast = best_model.forecast(steps=forecast_steps)
        avg_fc   = sum(forecast) / len(forecast)
        last_val = counts[-1]

        if avg_fc > last_val * 1.10:
            return "Increasing"
        elif avg_fc < last_val * 0.90:
            return "Decreasing"
        else:
            return "Stable"

    except ImportError:
        # statsmodels not installed — use linear
        return _linear_trend(counts)
    except Exception:
        return _linear_trend(counts)


def calculate_trend(role: str, history: list) -> str:
    """
    Calculate demand trend for a role given its history.

    Args:
        role:    role name
        history: list of monthly job counts ordered oldest to newest

    Returns:
        "Increasing" | "Stable" | "Decreasing"
    """
    if not history or len(history) == 0:
        return BASELINE_TRENDS.get(role, "Stable")

    if len(history) < MIN_MONTHS_FOR_LINEAR:
        return BASELINE_TRENDS.get(role, "Stable")

    if len(history) < MIN_MONTHS_FOR_ARIMA:
        return _linear_trend(history)

    return _arima_trend(history)


# ── Step 3: Role normalization ────────────────────────────────

def _normalize_role(role: str) -> str:
    """Map a role name to the demand category key."""
    r = role.lower()
    if any(k in r for k in ["ml", "machine learning", "ai engineer", "data scientist"]):
        return "Data Scientist"
    if "data engineer" in r:
        return "Data Engineer"
    if "data analyst" in r:
        return "Data Analyst"
    if "full stack" in r:
        return "Full Stack Developer"
    if "backend" in r:
        return "Backend Developer"
    if "frontend" in r:
        return "Frontend Developer"
    if "mobile" in r or "flutter" in r or "android" in r:
        return "Mobile Developer"
    if "devops" in r or "sre" in r:
        return "DevOps/SRE"
    if "cloud" in r:
        return "Cloud Engineer"
    if "cyber" in r or "security" in r:
        return "Cybersecurity"
    if "qa" in r or "quality" in r or "tester" in r:
        return "QA Engineer"
    if "ui" in r or "ux" in r or "designer" in r:
        return "UI/UX Designer"
    if "network" in r:
        return "Network/Systems"
    if "business analyst" in r:
        return "Business Analyst"
    if "project manager" in r or "product manager" in r or "scrum" in r:
        return "PM/PO/Scrum"
    if "software" in r or "developer" in r or "programmer" in r:
        return "Software Engineer"
    return "Other"


# ── Main function called by pipeline ─────────────────────────

def get_trend(roles: list, firebase_bridge=None) -> dict:
    """
    Get demand trend for a list of roles.
    Tries Firestore real data first.
    Falls back to baseline if insufficient data.

    Args:
        roles:           list of role names from career fit
        firebase_bridge: firebase_bridge module (optional)
                         pass it to use Firestore real data

    Returns:
        dict with overall_trend, primary_trend,
              role_trends, demand_score, primary_score,
              data_source
    """
    role_trends  = {}
    data_sources = {}

    for role in roles:
        normalized_role = _normalize_role(role)
        trend           = None
        source          = "baseline"

        # Try Firestore real data
        if firebase_bridge:
            try:
                history = firebase_bridge.get_demand_history(normalized_role)
                if history and len(history) >= MIN_MONTHS_FOR_LINEAR:
                    counts = [h["count"] for h in sorted(
                        history, key=lambda x: x["month"]
                    )]
                    trend  = calculate_trend(normalized_role, counts)
                    source = f"firestore_live ({len(counts)} months)"
            except Exception:
                pass

        # Fall back to baseline
        if trend is None:
            trend  = BASELINE_TRENDS.get(normalized_role, "Stable")
            source = "baseline_arima"

        role_trends[role]  = trend
        data_sources[role] = source

    trends_list   = list(role_trends.values())
    overall       = max(set(trends_list), key=trends_list.count) \
                    if trends_list else "Stable"
    primary_role  = roles[0] if roles else "Unknown"
    primary_trend = role_trends.get(primary_role, "Stable")

    return {
        "overall_trend":  overall,
        "primary_trend":  primary_trend,
        "role_trends":    role_trends,
        "demand_score":   TREND_SCORES.get(overall, 50.0),
        "primary_score":  TREND_SCORES.get(primary_trend, 50.0),
        "data_sources":   data_sources,
        "data_source":    "firestore_live" if any(
            "firestore" in s for s in data_sources.values()
        ) else "baseline_arima",
    }
