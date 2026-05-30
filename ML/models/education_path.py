# =============================================================
# EduLink — Model 5: Education Path Recommendation
# Converted from: Education_path_recommendation.ipynb
# Exact: hard constraint filtering + weighted scoring
# =============================================================

# Sri Lanka institute catalog — matches institutes_catalog_v2.csv structure
CATALOG = [
    # Data & AI
    {"program_id":"P001","institute":"University of Moratuwa","institute_location":"Colombo","program_cluster":"Data_AI_Engineering","program_level":"Degree","duration_months":48,"cost_level":"Medium","delivery_mode":"Full-time"},
    {"program_id":"P002","institute":"UCSC - University of Colombo","institute_location":"Colombo","program_cluster":"Data_AI_Engineering","program_level":"Degree","duration_months":48,"cost_level":"Low","delivery_mode":"Full-time"},
    {"program_id":"P003","institute":"NIBM","institute_location":"Colombo","program_cluster":"Data_AI_Engineering","program_level":"Diploma","duration_months":18,"cost_level":"Low","delivery_mode":"Mixed"},
    {"program_id":"P004","institute":"SLIIT","institute_location":"Colombo","program_cluster":"Data_AI_Engineering","program_level":"Degree","duration_months":48,"cost_level":"Medium","delivery_mode":"Full-time"},
    {"program_id":"P005","institute":"IIT - Informatics Institute","institute_location":"Colombo","program_cluster":"Data_AI_Engineering","program_level":"Degree","duration_months":36,"cost_level":"High","delivery_mode":"Full-time"},
    # Software & Web
    {"program_id":"P006","institute":"University of Moratuwa","institute_location":"Colombo","program_cluster":"Software_Web_Engineering","program_level":"Degree","duration_months":48,"cost_level":"Medium","delivery_mode":"Full-time"},
    {"program_id":"P007","institute":"SLIIT","institute_location":"Colombo","program_cluster":"Software_Web_Engineering","program_level":"Degree","duration_months":48,"cost_level":"Medium","delivery_mode":"Full-time"},
    {"program_id":"P008","institute":"NIBM","institute_location":"Colombo","program_cluster":"Software_Web_Engineering","program_level":"Diploma","duration_months":18,"cost_level":"Low","delivery_mode":"Mixed"},
    {"program_id":"P009","institute":"ICBT Campus","institute_location":"Colombo","program_cluster":"Software_Web_Engineering","program_level":"Degree","duration_months":36,"cost_level":"Medium","delivery_mode":"Mixed"},
    {"program_id":"P010","institute":"ESOFT Metro Campus","institute_location":"Colombo","program_cluster":"Software_Web_Engineering","program_level":"Diploma","duration_months":12,"cost_level":"Low","delivery_mode":"Mixed"},
    # Network & Infrastructure
    {"program_id":"P011","institute":"NIBM","institute_location":"Colombo","program_cluster":"Network_Infrastructure","program_level":"Diploma","duration_months":12,"cost_level":"Low","delivery_mode":"Mixed"},
    {"program_id":"P012","institute":"SLIIT","institute_location":"Colombo","program_cluster":"Network_Infrastructure","program_level":"Degree","duration_months":48,"cost_level":"Medium","delivery_mode":"Full-time"},
    {"program_id":"P013","institute":"Cisco Networking Academy","institute_location":"Online","program_cluster":"Network_Infrastructure","program_level":"Short","duration_months":6,"cost_level":"Low","delivery_mode":"Online"},
    # Business IT
    {"program_id":"P014","institute":"University of Colombo","institute_location":"Colombo","program_cluster":"Business_IT_Management","program_level":"Degree","duration_months":48,"cost_level":"Low","delivery_mode":"Full-time"},
    {"program_id":"P015","institute":"ICBT Campus","institute_location":"Colombo","program_cluster":"Business_IT_Management","program_level":"Degree","duration_months":36,"cost_level":"Medium","delivery_mode":"Mixed"},
    {"program_id":"P016","institute":"NIBM","institute_location":"Colombo","program_cluster":"Business_IT_Management","program_level":"Diploma","duration_months":18,"cost_level":"Low","delivery_mode":"Mixed"},
    # UX Creative
    {"program_id":"P017","institute":"University of Visual Arts","institute_location":"Colombo","program_cluster":"UX_Creative_Tech","program_level":"Degree","duration_months":48,"cost_level":"Medium","delivery_mode":"Full-time"},
    {"program_id":"P018","institute":"SLIIT","institute_location":"Colombo","program_cluster":"UX_Creative_Tech","program_level":"Diploma","duration_months":24,"cost_level":"Medium","delivery_mode":"Mixed"},
    {"program_id":"P019","institute":"ESOFT Metro Campus","institute_location":"Colombo","program_cluster":"UX_Creative_Tech","program_level":"Short","duration_months":6,"cost_level":"Low","delivery_mode":"Mixed"},
    # IT Operations & QA
    {"program_id":"P020","institute":"NIBM","institute_location":"Colombo","program_cluster":"IT_Operations_QA","program_level":"Diploma","duration_months":12,"cost_level":"Low","delivery_mode":"Mixed"},
    {"program_id":"P021","institute":"SLIIT","institute_location":"Colombo","program_cluster":"IT_Operations_QA","program_level":"Degree","duration_months":48,"cost_level":"Medium","delivery_mode":"Full-time"},
    # Digital Marketing
    {"program_id":"P022","institute":"SLIM","institute_location":"Colombo","program_cluster":"Digital_Marketing_Media","program_level":"Diploma","duration_months":12,"cost_level":"Low","delivery_mode":"Mixed"},
    {"program_id":"P023","institute":"ICBT Campus","institute_location":"Colombo","program_cluster":"Digital_Marketing_Media","program_level":"Degree","duration_months":36,"cost_level":"Medium","delivery_mode":"Mixed"},
    # Hardware Systems
    {"program_id":"P024","institute":"University of Peradeniya","institute_location":"Kandy","program_cluster":"Hardware_Systems","program_level":"Degree","duration_months":48,"cost_level":"Low","delivery_mode":"Full-time"},
    {"program_id":"P025","institute":"SLIIT","institute_location":"Colombo","program_cluster":"Hardware_Systems","program_level":"Diploma","duration_months":24,"cost_level":"Medium","delivery_mode":"Full-time"},
]

COST_RANK = {"Low": 1, "Medium": 2, "High": 3}


def recommend(
    top1_cluster: str,
    top2_cluster: str  = None,
    top3_cluster: str  = None,
    budget:       str  = "Medium",
    mode:         str  = "Mixed",
    level:        str  = "AL",
    time_horizon: str  = "Normal",
) -> dict:
    """
    Recommend top 3 education programs.
    Exact logic: hard constraint filtering then weighted scoring.

    Args:
        top1_cluster:  primary career cluster
        top2_cluster:  secondary cluster
        top3_cluster:  tertiary cluster
        budget:        Low | Medium | High
        mode:          Full-time | Online | Mixed
        level:         OL | AL
        time_horizon:  Fast | Normal

    Returns:
        dict with programs (list of 3), path_steps (list of 3)
    """
    clusters     = [c for c in [top1_cluster, top2_cluster, top3_cluster] if c]
    budget_rank  = COST_RANK.get(budget, 2)
    max_duration = 12 if time_horizon == "Fast" else 48

    # ── Hard constraint filtering (exact from notebook Cell 8) ──
    candidates = []
    for prog in CATALOG:
        if prog["program_cluster"] not in clusters:
            continue
        if COST_RANK.get(prog["cost_level"], 2) > budget_rank:
            continue
        if prog["duration_months"] > max_duration:
            continue
        if mode != "Mixed" and prog["delivery_mode"] not in [mode, "Mixed", "Online"]:
            continue
        candidates.append(prog)

    # ── Weighted scoring (exact from notebook Cell 9) ──
    def score(p):
        s = 0
        # cluster_weight * 100
        if p["program_cluster"] == top1_cluster:   s += 300
        elif p["program_cluster"] == top2_cluster: s += 200
        else:                                       s += 100
        # budget_bonus * 5
        if p["cost_level"] == budget: s += 15
        elif COST_RANK.get(p["cost_level"], 2) < budget_rank: s += 5
        # level_bonus * 5
        if level == "AL" and p["program_level"] == "Degree":   s += 15
        elif level == "AL" and p["program_level"] == "Diploma": s += 10
        elif level == "OL" and p["program_level"] in ["Short","Diploma"]: s += 15
        # score_duration
        s += max(0, (60 - p["duration_months"])) * 0.2
        return s

    candidates.sort(key=score, reverse=True)
    top3 = candidates[:3]

    # Fallback if no matches
    if not top3:
        top3 = [p for p in CATALOG if p["program_cluster"] == top1_cluster][:3]

    programs = []
    for i, p in enumerate(top3):
        programs.append({
            "rank":            i + 1,
            "program_id":      p["program_id"],
            "institute":       p["institute"],
            "location":        p["institute_location"],
            "cluster":         p["program_cluster"],
            "level":           p["program_level"],
            "duration_months": p["duration_months"],
            "cost_level":      p["cost_level"],
            "mode":            p["delivery_mode"],
            "display":         f"[{p['program_id']}] {p['program_level']} in {p['program_cluster']} @ {p['institute']} - {p['delivery_mode']}, {p['duration_months']} months, cost={p['cost_level']}",
        })

    return {
        "programs": programs,
        "path_steps": [
            "Step 1: Select one recommended program and enroll.",
            "Step 2: Follow the syllabus and complete all assessments.",
            "Step 3: Complete the qualification and progress to the next level.",
        ],
    }
