# =============================================================
# EduLink — Model 5: Education Path Recommendation
# Primary source: Firestore degree_programs (Admin Panel data)
# Fallback source: Hardcoded Sri Lanka IT catalogue
# =============================================================
#
# DESIGN DECISION:
#   Programmes are NOT filtered by career cluster.
#   Reason: Any IT degree can lead to any IT career cluster.
#   The career cluster comes from the student's psychological
#   profile — not from the degree programme.
#   Example: BSc CS at UOM can lead to Data Science,
#            Software Engineering, or Network Infrastructure.
#
#   Programmes are filtered only by practical constraints:
#     - Budget (cost_level)
#     - Study mode (Full-time / Online / Mixed)
#     - Entry qualification (OL / AL)
#     - Duration preference
#
#   Top 5 programmes are returned ranked by score.
# =============================================================

import os
import sys

BACKEND_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..', '..', 'Backend')
if BACKEND_PATH not in sys.path:
    sys.path.insert(0, BACKEND_PATH)

try:
    from firebase_bridge import get_db
    FIREBASE_AVAILABLE = True
except Exception:
    FIREBASE_AVAILABLE = False

from datetime import datetime

COST_RANK = {"Low": 1, "Medium": 2, "High": 3}

# Hardcoded fallback catalogue — used when Firestore unavailable
CATALOG = [
    {"program_id": "P001",
     "program_name": "BSc (Hons) in Computer Science and Engineering",
     "institute": "University of Moratuwa",
     "institute_location": "Moratuwa, Colombo",
     "program_level": "Degree",
     "duration_months": 48,
     "cost_level": "Low",
     "delivery_mode": "Full-time"},

    {"program_id": "P002",
     "program_name": "BSc (Hons) in Computer Science",
     "institute": "UCSC - University of Colombo",
     "institute_location": "Colombo",
     "program_level": "Degree",
     "duration_months": 48,
     "cost_level": "Low",
     "delivery_mode": "Full-time"},

    {"program_id": "P003",
     "program_name": "BSc (Hons) in Information Technology",
     "institute": "SLIIT",
     "institute_location": "Colombo",
     "program_level": "Degree",
     "duration_months": 48,
     "cost_level": "Medium",
     "delivery_mode": "Full-time"},

    {"program_id": "P004",
     "program_name": "BSc (Hons) in Software Engineering",
     "institute": "NSBM Green University",
     "institute_location": "Homagama, Colombo",
     "program_level": "Degree",
     "duration_months": 48,
     "cost_level": "Medium",
     "delivery_mode": "Full-time"},

    {"program_id": "P005",
     "program_name": "BSc (Hons) in Computing",
     "institute": "APIIT Sri Lanka",
     "institute_location": "Colombo",
     "program_level": "Degree",
     "duration_months": 36,
     "cost_level": "High",
     "delivery_mode": "Full-time"},

    {"program_id": "P006",
     "program_name": "Higher National Diploma in IT",
     "institute": "NIBM",
     "institute_location": "Colombo",
     "program_level": "Diploma",
     "duration_months": 18,
     "cost_level": "Low",
     "delivery_mode": "Mixed"},

    {"program_id": "P007",
     "program_name": "BSc (Hons) in Information Systems",
     "institute": "UCSC - University of Colombo",
     "institute_location": "Colombo",
     "program_level": "Degree",
     "duration_months": 48,
     "cost_level": "Low",
     "delivery_mode": "Full-time"},

    {"program_id": "P008",
     "program_name": "Diploma in Web Development",
     "institute": "ESOFT Metro Campus",
     "institute_location": "Colombo",
     "program_level": "Diploma",
     "duration_months": 12,
     "cost_level": "Low",
     "delivery_mode": "Mixed"},
]


def _fetch_firestore_programs() -> list:
    """
    Fetch ALL active degree programmes from Firestore.
    No cluster filter — all IT programmes are eligible.
    """
    if not FIREBASE_AVAILABLE:
        return []
    try:
        db   = get_db()
        docs = db.collection("degree_programs") \
                 .where("status", "==", "Active") \
                 .stream()

        programs = []
        for doc in docs:
            d = doc.to_dict()

            # Map tuition fee to cost level if cost_level missing
            fee       = float(d.get("tuitionFee", 0) or 0)
            cost_level = _map_fee_to_cost(fee, d.get("feeType", ""))

            programs.append({
                "program_id":       doc.id,
                "program_name":     d.get("degreeName", ""),
                "institute":        d.get("universityName", ""),
                "institute_location": d.get("address", "Sri Lanka").split(",")[-2].strip()
                                    if "," in d.get("address", "")
                                    else "Sri Lanka",
                "program_level":    d.get("qualification", "Degree"),
                "duration_months":  int(d.get("durationMonths", 48)),
                "cost_level":       cost_level,
                "delivery_mode":    d.get("studyMode", "Full-time"),
                "faculty":          d.get("faculty", ""),
                "entry_requirements": d.get("entryRequirements", ""),
                "next_intake":      d.get("nextIntake", ""),
                "apply_url":        d.get("applyNowUrl", d.get("officialWebsite", "")),
            })
        return programs

    except Exception as e:
        print(f"Failed to fetch active programs from Firestore. "
              f"Firestore may be unavailable.\n{e}")
        return []


def _map_fee_to_cost(fee: float, fee_type: str = "") -> str:
    """Map tuition fee to Low / Medium / High cost level."""
    if fee_type.lower() in ["free", "government"]:
        return "Low"
    if fee == 0:
        return "Low"
    elif fee < 200000:
        return "Low"
    elif fee < 600000:
        return "Medium"
    else:
        return "High"


def recommend(
    top1_cluster: str,
    top2_cluster: str = None,
    top3_cluster: str = None,
    budget:       str = "Medium",
    mode:         str = "Mixed",
    level:        str = "AL",
    time_horizon: str = "Normal",
) -> dict:
    """
    Recommend top 5 education programmes for the student.

    Programmes are NOT filtered by career cluster.
    All active IT programmes from Admin Panel are considered.
    Programmes are filtered by student practical constraints
    and ranked by score.

    Args:
        top1_cluster:  primary career cluster (used for display only)
        budget:        Low | Medium | High
        mode:          Full-time | Online | Mixed
        level:         OL | AL
        time_horizon:  Fast | Normal
    """
    budget_rank  = COST_RANK.get(budget, 2)
    max_duration = 12 if time_horizon == "Fast" else 60

    # Try Firestore first
    all_programs = _fetch_firestore_programs()
    source_name  = "firestore"

    # Fallback to hardcoded catalogue
    if not all_programs:
        all_programs = CATALOG
        source_name  = "catalog"

    # Filter by practical constraints only
    candidates = []
    for prog in all_programs:
        # Budget constraint
        if COST_RANK.get(prog["cost_level"], 2) > budget_rank:
            continue
        # Duration constraint
        if prog["duration_months"] > max_duration:
            continue
        # Mode constraint
        if mode != "Mixed" and prog["delivery_mode"] not in [mode, "Mixed", "Online"]:
            continue
        candidates.append(prog)

    # If no candidates after filtering relax budget constraint
    if not candidates:
        candidates = [p for p in all_programs
                      if p["duration_months"] <= max_duration]

    # If still nothing use all programmes
    if not candidates:
        candidates = all_programs

    # Weighted scoring
    def score(p):
        s = 0
        # Cost preference
        if p["cost_level"] == budget:
            s += 30
        elif COST_RANK.get(p["cost_level"], 2) < budget_rank:
            s += 15

        # Level preference
        if level == "AL" and p["program_level"] == "Degree":
            s += 40
        elif level == "AL" and p["program_level"] == "Diploma":
            s += 20
        elif level == "OL" and p["program_level"] in ["Short", "Diploma"]:
            s += 40
        elif level == "OL" and p["program_level"] == "Degree":
            s += 10

        # Duration preference (shorter = higher score within constraints)
        s += max(0, (60 - p["duration_months"])) * 0.3

        # Mode preference
        if mode != "Mixed" and p["delivery_mode"] == mode:
            s += 20
        elif p["delivery_mode"] == "Mixed":
            s += 10

        return s

    candidates.sort(key=score, reverse=True)
    top5 = candidates[:5]

    programs = []
    for i, p in enumerate(top5):
        programs.append({
            "rank":             i + 1,
            "program_id":       p.get("program_id", ""),
            "program_name":     p.get("program_name", ""),
            "institute":        p.get("institute", ""),
            # Both field name versions for compatibility
            "location":             p.get("institute_location", ""),
            "institute_location":   p.get("institute_location", ""),
            "level":                p.get("program_level", ""),
            "program_level":        p.get("program_level", ""),
            "duration_months":      p.get("duration_months", 0),
            "cost_level":           p.get("cost_level", ""),
            "mode":                 p.get("delivery_mode", ""),
            "delivery_mode":        p.get("delivery_mode", ""),
            "faculty":              p.get("faculty", ""),
            "entry_requirements":   p.get("entry_requirements", ""),
            "next_intake":          p.get("next_intake", ""),
            "apply_url":            p.get("apply_url", ""),
            "source":               source_name,
        })

    return {
        "programs":   programs,
        "path_steps": [
            "Step 1: Select one recommended programme and submit your application.",
            "Step 2: Complete the coursework and required assessments.",
            "Step 3: Obtain the qualification and begin your IT career.",
        ],
    }
