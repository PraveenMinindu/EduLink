# =============================================================
# EduLink — Model 1: Career Fit Prediction
# Converted from: career_fit_prediction.ipynb
# No Colab, No Spark, No Drive paths — pure Python callable
# =============================================================

# ── Updated scoring weights — rebalanced for better discrimination ──
SCORE_WEIGHTS = {
    "Data_AI_Engineering": {
        "Analytical_Thinking":        1.50,
        "Data_Literacy":              1.50,
        "Tech_Interest":              1.20,
        "Technical_ProblemSolving":   1.10,
        "Tech_Adaptability":          0.80,
        "Structure_Preference":       0.40,
        "Communication_Skill":        0.20,
        "Social_Intelligence":        0.10,
    },
    "Software_Web_Engineering": {
        "Technical_ProblemSolving":   1.50,
        "Tech_Adaptability":          1.40,
        "Tech_Interest":              1.20,
        "Analytical_Thinking":        1.00,
        "Process_Optimization":       0.80,
        "Innovation_Drive":           0.60,
        "Communication_Skill":        0.20,
        "Social_Intelligence":        0.10,
    },
    "Network_Infrastructure": {
        "Technical_ProblemSolving":   1.50,
        "Process_Optimization":       1.40,
        "Structure_Preference":       1.30,
        "Tech_Adaptability":          1.00,
        "Analytical_Thinking":        0.60,
        "Tech_Interest":              0.50,
        "Communication_Skill":        0.10,
        "Social_Intelligence":        0.10,
    },
    "IT_Operations_QA": {
        "Structure_Preference":       1.50,
        "Process_Optimization":       1.40,
        "Analytical_Thinking":        1.00,
        "Tech_Adaptability":          0.80,
        "Technical_ProblemSolving":   0.70,
        "Communication_Skill":        0.30,
        "Social_Intelligence":        0.20,
        "Data_Literacy":              0.10,
    },
    "UX_Creative_Tech": {
        "Creativity_Index":           2.00,
        "Tech_Interest":              1.20,
        "Innovation_Drive":           0.90,
        "Communication_Skill":        0.60,
        "Social_Intelligence":        0.40,
        "Tech_Adaptability":          0.50,
        "Analytical_Thinking":        0.20,
        "Data_Literacy":              0.10,
    },
    "Business_IT_Management": {
        "Leadership_Capability":      1.60,
        "Strategic_Vision":           1.40,
        "Business_Economics_Interest":1.30,
        "Communication_Skill":        0.80,
        "Social_Intelligence":        0.60,
        "Analytical_Thinking":        0.40,
        "Tech_Interest":              0.20,
        "Creativity_Index":           0.10,
    },
    "Digital_Marketing_Media": {
        "Entrepreneurship_Orientation":1.80,
        "Communication_Skill":         1.20,
        "Social_Intelligence":         0.90,
        "Business_Economics_Interest": 0.80,
        "Creativity_Index":            0.90,
        "Innovation_Drive":            0.50,
        "Tech_Interest":               0.20,
        "Analytical_Thinking":         0.10,
    },
    "Hardware_Systems": {
        "Technical_ProblemSolving":   1.60,
        "Analytical_Thinking":        1.20,
        "Tech_Adaptability":          1.00,
        "Process_Optimization":       0.80,
        "Structure_Preference":       0.70,
        "Data_Literacy":              0.50,
        "Tech_Interest":              0.40,
        "Communication_Skill":        0.10,
    },
}

# ── Exact CLUSTER_ROLES from notebook Cell 12 ───────────────
CLUSTER_ROLES = {
    "Software_Web_Engineering": [
        "Software Developer","Software Engineer","Computer Programmer",
        "Web Developer","Programmer Analyst","Applications Programmer",
        "Systems Programmer","Webmaster","Computer Games Developer",
    ],
    "Data_AI_Engineering": [
        "Data Scientist","ML Engineer","Data Engineer","AI Developer",
        "Database Administrator","Database Designer","Computer Database Assistant",
    ],
    "Network_Infrastructure": [
        "Network Engineer","Network Administrator","Systems Administrator",
        "IT Infrastructure Engineer","Infrastructure (IT) Architect",
        "Telecommunications Engineer","Network Architect","Network Manager",
    ],
    "IT_Operations_QA": [
        "IT Quality Assurance Specialist","IT Auditor","Software Tester",
        "QA Engineer","IT Support Engineer","IT Operations Analyst",
        "Site Reliability Associate","Helpdesk Analyst","Systems Support Officer",
    ],
    "UX_Creative_Tech": [
        "UI/UX Designer","Product Designer","Graphic Designer",
        "Creative Technologist","Interaction Designer","Motion Designer",
        "Front-End Designer","Multimedia Designer","UX Researcher",
    ],
    "Business_IT_Management": [
        "Business Analyst","IT Project Manager","Product Manager",
        "IT Manager","Scrum Master","IT Consultant",
        "Business Systems Analyst","Operations Manager","Strategy Associate",
    ],
    "Digital_Marketing_Media": [
        "Digital Marketer","SEO Specialist","Content Strategist",
        "Social Media Manager","Growth Marketer","Brand Executive",
        "Marketing Analyst","Media Planner","Campaign Manager",
    ],
    "Hardware_Systems": [
        "Embedded Systems Engineer","Hardware Engineer","IoT Engineer",
        "Systems Engineer","Field Engineer","Electronics Engineer",
        "Mechatronics Associate","Device Technician","Lab Engineer",
    ],
}


def compute_composites(mcq: dict) -> dict:
    """
    Convert raw Q1-Q40 answers (scale 1-5) to normalized composite
    features (0-1) used by the career fit model.
    """
    def n(v): return (float(v) - 1) / 4.0
    q = {k: float(v) for k, v in mcq.items()}
    return {
        "Analytical_Thinking":           round((n(q["Q1"])+n(q["Q2"])+n(q["Q3"])+n(q["Q16"]))/4, 4),
        "Creativity_Index":              round((n(q["Q5"])+n(q["Q24"])+n(q["Q30"]))/3, 4),
        "Communication_Skill":           round((n(q["Q6"])+n(q["Q13"])+n(q["Q17"]))/3, 4),
        "Emotional_Stability":           round(n(q["Q9"]), 4),
        "Strategic_Vision":              round((n(q["Q8"])+n(q["Q20"])+n(q["Q32"]))/3, 4),
        "Innovation_Drive":              round((n(q["Q5"])+n(q["Q40"]))/2, 4),
        "Social_Intelligence":           round((n(q["Q10"])+n(q["Q27"]))/2, 4),
        "Data_Literacy":                 round((n(q["Q11"])+n(q["Q18"])+n(q["Q28"]))/3, 4),
        "Tech_Adaptability":             round((n(q["Q9"])+n(q["Q12"])+n(q["Q22"]))/3, 4),
        "Technical_ProblemSolving":      round((n(q["Q14"])+n(q["Q21"]))/2, 4),
        "Leadership_Capability":         round((n(q["Q15"])+n(q["Q35"]))/2, 4),
        "Process_Optimization":          round((n(q["Q14"])+n(q["Q39"]))/2, 4),
        "Tech_Interest":                 round((n(q["Q22"])+n(q["Q31"])+n(q["Q37"]))/3, 4),
        "Business_Economics_Interest":   round((n(q["Q23"])+n(q["Q25"])+n(q["Q34"]))/3, 4),
        "Social_Impact_Motivation":      round((n(q["Q21"])+n(q["Q27"]))/2, 4),
        "Future_Orientation":            round((n(q["Q8"])+n(q["Q33"])+n(q["Q39"]))/3, 4),
        "Career_Growth_Mindset":         round((n(q["Q33"])+n(q["Q38"]))/2, 4),
        "Entrepreneurship_Orientation":  round(n(q["Q26"]), 4),
        "Global_Innovation_Alignment":   round((n(q["Q40"])+n(q["Q39"]))/2, 4),
        "Structure_Preference":          round((n(q["Q7"])+n(q["Q18"]))/2, 4),
        "R": float(q.get("Q1", 3)),
        "I": float(q.get("Q2", 3)),
        "A": float(q.get("Q5", 3)),
        "S": float(q.get("Q10", 3)),
        "E": float(q.get("Q35", 3)),
        "C": float(q.get("Q7", 3)),
    }


def build_10_roles(top1: str, top2: str, top3: str) -> list:
    """Build 10 roles using 5-3-2 split. Exact logic from notebook Cell 12."""
    def pick(c, n): return CLUSTER_ROLES.get(c, [])[:n]
    roles = pick(top1, 5) + pick(top2, 3) + pick(top3, 2)
    seen, out = set(), []
    for r in roles:
        if r and r not in seen:
            seen.add(r)
            out.append(r)
    for c in [top1, top2, top3]:
        for r in CLUSTER_ROLES.get(c, []):
            if len(out) >= 10: break
            if r not in seen:
                seen.add(r)
                out.append(r)
    return out[:10]


def predict(mcq: dict) -> dict:
    """
    Predict career clusters and roles from MCQ answers.

    Args:
        mcq: dict with keys Q1..Q40, values 1-5

    Returns:
        dict with top1_cluster, top2_cluster, top3_cluster,
              roles (list of 10), cluster_scores, features
    """
    features = compute_composites(mcq)

    scores = {}
    for cluster, weights in SCORE_WEIGHTS.items():
        scores[cluster] = round(
            sum(features.get(feat, 0.5) * w for feat, w in weights.items()), 4
        )

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top1, top2, top3 = ranked[0][0], ranked[1][0], ranked[2][0]

    return {
        "top1_cluster":   top1,
        "top2_cluster":   top2,
        "top3_cluster":   top3,
        "cluster_scores": dict(ranked),
        "roles":          build_10_roles(top1, top2, top3),
        "features":       features,
    }