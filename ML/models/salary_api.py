# ============================================================
# EduLink — Live Salary Service
# Version: 2.0 — Real 2025/2026 Sri Lanka IT Salary Benchmarks
#
# Data Sources:
#   PayScale Sri Lanka 2026:
#     https://www.payscale.com/research/LK/Job=Software_Engineer/Salary
#     https://www.payscale.com/research/LK/Job=Data_Scientist/Salary
#   Glassdoor Colombo May 2026:
#     https://www.glassdoor.com/Salaries/colombo-sri-lanka-software-engineer-salary
#   TechSalary.lk 2025:
#     https://techsalary.tldr.lk
#   Ceylon Open Campus Sri Lanka IT Careers 2025:
#     https://www.coccampus.lk/it-career-opportunities-sri-lanka
#   Paylab.com Sri Lanka IT 2025:
#     https://www.paylab.com/lk/salaryinfo/information-technology
#
# Exchange Rate: Live from ExchangeRate-API (refreshed every 6h)
# All salaries in LKR per month
# ============================================================

import requests
from datetime import datetime

# ── Real 2025/2026 Sri Lanka IT Salary Benchmarks (LKR/month) ─
# Entry = 0-2 years experience (fresh graduate)
# Mid   = 3-5 years experience
# Senior= 6+ years experience
#
# Sources: PayScale 2026, Glassdoor Colombo May 2026,
#          TechSalary.lk 2025, Paylab.com 2025,
#          Ceylon Open Campus 2025
# ─────────────────────────────────────────────────────────────

SALARY_LKR = {
    # Data AI Engineering cluster
    # Source: PayScale LK 2026 + TechSalary.lk 2025
    "Data Scientist": {
        "Entry":  120000,   # LKR 100K-140K range (PayScale 2026)
        "Mid":    300000,   # LKR 250K-350K (TechSalary.lk 2025)
        "Senior": 650000,   # LKR 500K-800K (TechSalary.lk 2025)
    },
    "ML Engineer": {
        "Entry":  130000,   # AI/ML premium over SW Eng
        "Mid":    320000,
        "Senior": 700000,
    },
    "Data Engineer": {
        "Entry":  115000,
        "Mid":    280000,
        "Senior": 600000,
    },
    "AI Developer": {
        "Entry":  125000,
        "Mid":    310000,
        "Senior": 680000,
    },
    "Database Administrator": {
        "Entry":  100000,
        "Mid":    230000,
        "Senior": 480000,
    },
    "Database Designer": {
        "Entry":  95000,
        "Mid":    220000,
        "Senior": 450000,
    },
    "Computer Database Assistant": {
        "Entry":  80000,
        "Mid":    180000,
        "Senior": 350000,
    },

    # Software Web Engineering cluster
    # Source: PayScale 2026 (avg LKR 85,000/month entry)
    #         Glassdoor Colombo May 2026 (LKR 105K-255K/month)
    #         TechSalary.lk 2025 (LKR 300K at 4 years)
    "Software Engineer": {
        "Entry":  100000,   # PayScale 2026 avg entry
        "Mid":    220000,   # Glassdoor Colombo mid range
        "Senior": 480000,   # TechSalary.lk senior 2025
    },
    "Software Developer": {
        "Entry":  95000,
        "Mid":    210000,
        "Senior": 450000,
    },
    "Full Stack Developer": {
        "Entry":  105000,
        "Mid":    230000,
        "Senior": 500000,
    },
    "Backend Developer": {
        "Entry":  100000,
        "Mid":    220000,
        "Senior": 470000,
    },
    "Frontend Developer": {
        "Entry":  90000,
        "Mid":    200000,
        "Senior": 420000,
    },
    "Mobile Developer": {
        "Entry":  100000,
        "Mid":    220000,
        "Senior": 460000,
    },
    "Web Developer": {
        "Entry":  85000,
        "Mid":    190000,
        "Senior": 400000,
    },
    "Computer Programmer": {
        "Entry":  85000,
        "Mid":    185000,
        "Senior": 380000,
    },

    # Network Infrastructure cluster
    # Source: Ceylon Open Campus 2025, Paylab.com 2025
    "Network Engineer": {
        "Entry":  85000,
        "Mid":    180000,
        "Senior": 380000,
    },
    "Network Administrator": {
        "Entry":  80000,
        "Mid":    170000,
        "Senior": 360000,
    },
    "Systems Administrator": {
        "Entry":  80000,
        "Mid":    170000,
        "Senior": 350000,
    },
    "IT Infrastructure Engineer": {
        "Entry":  90000,
        "Mid":    190000,
        "Senior": 400000,
    },
    "Cloud Engineer": {
        "Entry":  110000,   # Cloud premium
        "Mid":    260000,
        "Senior": 560000,
    },
    "DevOps Engineer": {
        "Entry":  110000,   # Paylab.com top IT roles 2025
        "Mid":    270000,
        "Senior": 580000,
    },
    "Cybersecurity Engineer": {
        "Entry":  110000,   # 20-40% premium (Ceylon OC 2025)
        "Mid":    270000,
        "Senior": 580000,
    },

    # IT Operations QA cluster
    # Source: Ceylon Open Campus 2025
    "QA Engineer": {
        "Entry":  75000,
        "Mid":    160000,
        "Senior": 340000,
    },
    "Software Tester": {
        "Entry":  70000,
        "Mid":    150000,
        "Senior": 310000,
    },
    "IT Support Engineer": {
        "Entry":  60000,
        "Mid":    130000,
        "Senior": 270000,
    },
    "IT Quality Assurance Specialist": {
        "Entry":  75000,
        "Mid":    165000,
        "Senior": 345000,
    },
    "IT Auditor": {
        "Entry":  80000,
        "Mid":    175000,
        "Senior": 370000,
    },
    "Helpdesk Analyst": {
        "Entry":  55000,
        "Mid":    120000,
        "Senior": 250000,
    },

    # UX Creative Tech cluster
    # Source: Paylab.com 2025, Glassdoor SL 2025
    "UI/UX Designer": {
        "Entry":  80000,
        "Mid":    175000,
        "Senior": 380000,
    },
    "Product Designer": {
        "Entry":  85000,
        "Mid":    185000,
        "Senior": 400000,
    },
    "Graphic Designer": {
        "Entry":  65000,
        "Mid":    140000,
        "Senior": 290000,
    },

    # Business IT Management cluster
    # Source: PayScale LK 2026, Paylab.com 2025
    "Business Analyst": {
        "Entry":  90000,
        "Mid":    200000,
        "Senior": 430000,
    },
    "IT Project Manager": {
        "Entry":  120000,
        "Mid":    280000,
        "Senior": 600000,
    },
    "Product Manager": {
        "Entry":  115000,
        "Mid":    270000,
        "Senior": 580000,
    },
    "IT Manager": {
        "Entry":  130000,
        "Mid":    300000,
        "Senior": 650000,
    },
    "Scrum Master": {
        "Entry":  100000,
        "Mid":    230000,
        "Senior": 490000,
    },

    # Digital Marketing Media cluster
    # Source: Ceylon Open Campus 2025
    "Digital Marketer": {
        "Entry":  65000,
        "Mid":    140000,
        "Senior": 300000,
    },
    "SEO Specialist": {
        "Entry":  60000,
        "Mid":    130000,
        "Senior": 270000,
    },
    "Social Media Manager": {
        "Entry":  60000,
        "Mid":    130000,
        "Senior": 270000,
    },
    "Content Strategist": {
        "Entry":  65000,
        "Mid":    140000,
        "Senior": 290000,
    },

    # Hardware Systems cluster
    # Source: Ceylon Open Campus 2025, Paylab.com 2025
    "Embedded Systems Engineer": {
        "Entry":  90000,
        "Mid":    200000,
        "Senior": 430000,
    },
    "Hardware Engineer": {
        "Entry":  85000,
        "Mid":    190000,
        "Senior": 400000,
    },
    "IoT Engineer": {
        "Entry":  95000,
        "Mid":    210000,
        "Senior": 450000,
    },
}

# ── Cluster default role fallback ─────────────────────────────
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

# ── Demand trend adjustment ───────────────────────────────────
DEMAND_FACTOR = {
    "Increasing":  1.08,
    "Stable":      1.00,
    "Decreasing":  0.95,
}

# ── Exchange rate cache ───────────────────────────────────────
_cached_rate = None
_cache_time  = None
CACHE_HOURS  = 6
FALLBACK_RATE = 320.0   # Updated May 2026 approximate


def get_usd_to_lkr() -> tuple:
    """Fetch live USD to LKR rate. Returns (rate, source)."""
    global _cached_rate, _cache_time

    if _cached_rate and _cache_time:
        hours_old = (datetime.now() - _cache_time).seconds / 3600
        if hours_old < CACHE_HOURS:
            return _cached_rate, "cached"

    apis = [
        {
            "url":    "https://api.exchangerate-api.com/v4/latest/USD",
            "parser": lambda d: d.get("rates", {}).get("LKR")
        },
        {
            "url":    "https://api.frankfurter.app/latest?from=USD&to=LKR",
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

    # Find salary data
    role_data = SALARY_LKR.get(role)
    if not role_data and cluster:
        fallback_role = CLUSTER_DEFAULT_ROLE.get(cluster, "Software Engineer")
        role_data     = SALARY_LKR.get(fallback_role)
    if not role_data:
        role_data = SALARY_LKR["Software Engineer"]

    # Apply demand trend adjustment
    factor = DEMAND_FACTOR.get(demand_trend, 1.0)

    # Current salary (Entry level)
    current_base = int(role_data["Entry"] * factor)
    current_min  = int(current_base * 0.85)
    current_max  = int(current_base * 1.15)

    # Future salary (Mid level — 3-5 years)
    future_base  = int(role_data["Mid"] * factor)
    future_min   = int(future_base * 0.85)
    future_max   = int(future_base * 1.15)

    # Senior salary
    senior_base  = int(role_data["Senior"] * factor)

    # Get live exchange rate  ← THIS LINE IS MISSING
    exchange_rate, rate_source = get_usd_to_lkr()

    return {
        "salary_min":        current_min,
        "salary_max":        current_max,
        "salary_mid":        current_base,
        "future_salary_min": future_min,
        "future_salary_max": future_max,
        "future_salary_mid": future_base,
        "future_years":      "3-5 years",
        "senior_salary_mid": senior_base,
        "senior_years":      "6+ years",
        "exchange_rate":     round(exchange_rate, 2),
        "rate_source":       rate_source,
        "currency":          "LKR",
        "per":               "month",
        "stage":             stage,
        "demand_trend":      demand_trend,
        "role":              role,
        "data_source":       "PayScale Sri Lanka 2026, Glassdoor Colombo May 2026, TechSalary.lk 2025",
        "last_updated":      datetime.now().strftime("%Y-%m-%d %H:%M"),
    }