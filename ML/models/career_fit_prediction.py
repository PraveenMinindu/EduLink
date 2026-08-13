# =============================================================
# EduLink — Model 1: Career Fit Prediction
# Version: 3.0 — Full 20-composite + 6 RIASEC pipeline
# Matches: Mathematical_Layer.ipynb + career_fit_prediction_v3.ipynb
# Theoretical basis: Holland RIASEC + Trait-Factor Theory + SCCT
# =============================================================

import math

# ── Question-to-composite mapping ───────────────────────────
# Matches Mathematical_Layer.ipynb FEATURE_MAP exactly
FEATURE_MAP = {
    "Analytical_Thinking":          [1, 2, 3, 4, 16],
    "Structure_Preference":         [6, 7, 14, 19],
    "Creativity_Index":             [5, 24, 30, 40],
    "Emotional_Stability":          [9],
    "Strategic_Vision":             [8, 20, 32, 39],
    "Innovation_Drive":             [5, 21, 24, 30, 40],
    "Social_Intelligence":          [10, 13, 17, 27],
    "Data_Literacy":                [11, 18, 28],
    "Tech_Adaptability":            [12, 22, 31, 37],
    "Communication_Skill":          [6, 10, 13, 17],
    "Technical_ProblemSolving":     [14, 16, 19, 21, 38],
    "Leadership_Capability":        [15, 32, 35],
    "Process_Optimization":         [14, 19, 20, 38],
    "Tech_Interest":                [22, 30, 31, 34, 40],
    "Business_Economics_Interest":  [23, 25, 26, 34],
    "Social_Impact_Motivation":     [10, 27, 39],
    "Future_Orientation":           [8, 22, 33, 37, 39],
    "Career_Growth_Mindset":        [31, 33, 36, 37, 38],
    "Entrepreneurship_Orientation": [26, 32, 34, 35],
    "Global_Innovation_Alignment":  [31, 37, 39, 40],
}

# ── RIASEC weighted aggregation ──────────────────────────────
# Matches Mathematical_Layer.ipynb RIASEC_WEIGHTS exactly
# Based on Holland theory + O*NET importance ratings
RIASEC_WEIGHTS = {
    "R": {
        "Technical_ProblemSolving": 1.0,
        "Process_Optimization":     0.6,
        "Tech_Adaptability":        0.4,
    },
    "I": {
        "Analytical_Thinking":      1.0,
        "Data_Literacy":            0.9,
        "Strategic_Vision":         0.5,
        "Tech_Interest":            0.4,
    },
    "A": {
        "Creativity_Index":              1.0,
        "Innovation_Drive":              0.8,
        "Global_Innovation_Alignment":   0.4,
    },
    "S": {
        "Social_Intelligence":      1.0,
        "Communication_Skill":      0.9,
        "Social_Impact_Motivation": 0.6,
    },
    "E": {
        "Leadership_Capability":         1.0,
        "Entrepreneurship_Orientation":  0.9,
        "Business_Economics_Interest":   0.7,
        "Career_Growth_Mindset":         0.4,
    },
    "C": {
        "Structure_Preference":  1.0,
        "Process_Optimization":  0.8,
        "Data_Literacy":         0.5,
        "Emotional_Stability":   0.3,
    },
}

# ── Cluster scoring weights ───────────────────────────────────
# Matches Mathematical_Layer.ipynb assign_cluster() scoring
# Uses 20 composites + RIASEC scores
# Based on Holland RIASEC adapted to Sri Lanka IT sector
SCORE_WEIGHTS = {
    # High I + Data Literacy + Analytical
    "Data_AI_Engineering": {
        "Analytical_Thinking":  1.25,
        "Data_Literacy":        1.25,
        "Tech_Interest":        0.90,
        "Tech_Adaptability":    0.35,
        "I_riasec":             0.25,
    },
    # High R + Technical + Innovation
    "Software_Web_Engineering": {
        "Tech_Adaptability":        1.15,
        "Technical_ProblemSolving": 1.05,
        "Analytical_Thinking":      0.75,
        "Tech_Interest":            0.65,
        "R_riasec":                 0.25,
    },
    # High R + C + Process + Structure
    "Network_Infrastructure": {
        "Technical_ProblemSolving": 1.20,
        "Process_Optimization":     1.10,
        "Structure_Preference":     1.00,
        "Tech_Adaptability":        0.55,
        "R_riasec":                 0.25,
    },
    # High C + Structure + Emotional Stability
    "IT_Operations_QA": {
        "Structure_Preference":     1.20,
        "Process_Optimization":     1.05,
        "Analytical_Thinking":      0.85,
        "Tech_Adaptability":        0.65,
        "C_riasec":                 0.25,
    },
    # High A + Creativity + Communication
    "UX_Creative_Tech": {
        "Creativity_Index":     1.35,
        "Innovation_Drive":     0.90,
        "Social_Intelligence":  0.80,
        "Communication_Skill":  0.75,
        "A_riasec":             0.25,
    },
    # High E + Leadership + Business
    "Business_IT_Management": {
        "Leadership_Capability":         1.25,
        "Business_Economics_Interest":   1.05,
        "Communication_Skill":           0.85,
        "Social_Intelligence":           0.60,
        "E_riasec":                      0.25,
    },
    # High S + E + Communication + Social
    "Digital_Marketing_Media": {
        "Communication_Skill":           1.25,
        "Social_Intelligence":           1.05,
        "Entrepreneurship_Orientation":  0.95,
        "Creativity_Index":              0.80,
        "A_riasec":                      0.25,
    },
    # High R + Technical + Process
    "Hardware_Systems": {
        "Technical_ProblemSolving": 1.25,
        "Analytical_Thinking":      0.85,
        "Tech_Adaptability":        0.80,
        "Process_Optimization":     0.60,
        "R_riasec":                 0.25,
    },
}

# ── Cluster roles ─────────────────────────────────────────────
CLUSTER_ROLES = {
    "Software_Web_Engineering": [
        "Software Developer", "Software Engineer", "Computer Programmer",
        "Web Developer", "Programmer Analyst", "Applications Programmer",
        "Systems Programmer", "Webmaster", "Computer Games Developer",
    ],
    "Data_AI_Engineering": [
        "Data Scientist", "ML Engineer", "Data Engineer", "AI Developer",
        "Database Administrator", "Database Designer", "Computer Database Assistant",
    ],
    "Network_Infrastructure": [
        "Network Engineer", "Network Administrator", "Systems Administrator",
        "IT Infrastructure Engineer", "Infrastructure (IT) Architect",
        "Telecommunications Engineer", "Network Architect", "Network Manager",
    ],
    "IT_Operations_QA": [
        "IT Quality Assurance Specialist", "IT Auditor", "Software Tester",
        "QA Engineer", "IT Support Engineer", "IT Operations Analyst",
        "Site Reliability Associate", "Helpdesk Analyst", "Systems Support Officer",
    ],
    "UX_Creative_Tech": [
        "UI/UX Designer", "Product Designer", "Graphic Designer",
        "Creative Technologist", "Interaction Designer", "Motion Designer",
        "Front-End Designer", "Multimedia Designer", "UX Researcher",
    ],
    "Business_IT_Management": [
        "Business Analyst", "IT Project Manager", "Product Manager",
        "IT Manager", "Scrum Master", "IT Consultant",
        "Business Systems Analyst", "Operations Manager", "Strategy Associate",
    ],
    "Digital_Marketing_Media": [
        "Digital Marketer", "SEO Specialist", "Content Strategist",
        "Social Media Manager", "Growth Marketer", "Brand Executive",
        "Marketing Analyst", "Media Planner", "Campaign Manager",
    ],
    "Hardware_Systems": [
        "Embedded Systems Engineer", "Hardware Engineer", "IoT Engineer",
        "Systems Engineer", "Field Engineer", "Electronics Engineer",
        "Mechatronics Associate", "Device Technician", "Lab Engineer",
    ],
}


def compute_composites(mcq: dict) -> dict:
    """
    Convert raw Q1-Q40 answers (scale 1-5) to 20 normalized
    composite features (0.0-1.0) + 6 RIASEC scores (0-100).

    Matches Mathematical_Layer.ipynb FEATURE_MAP exactly.
    Formula: composite = mean(selected questions) / 5.0
    """
    # Normalize: (answer - 1) / 4 then divide by 5 = answer / 5
    # Equivalent to: mean(questions) / 5
    q = {}
    for k, v in mcq.items():
        try:
            val = float(v)
            q[k] = max(1.0, min(5.0, val))  # clip to 1-5
        except (ValueError, TypeError):
            q[k] = 3.0  # default neutral

    composites = {}

    # Compute 20 composite features
    for feature, questions in FEATURE_MAP.items():
        q_vals = [q.get(f"Q{qn}", 3.0) for qn in questions]
        composites[feature] = round(
            sum(q_vals) / len(q_vals) / 5.0, 4
        )

    # Compute 6 RIASEC scores from composites
    riasec = {}
    for letter, weights in RIASEC_WEIGHTS.items():
        total_w   = sum(weights.values())
        weighted  = sum(composites.get(feat, 0.5) * w
                       for feat, w in weights.items())
        riasec[letter] = round((weighted / total_w) * 100.0, 2)

    composites["R"] = riasec["R"]
    composites["I"] = riasec["I"]
    composites["A"] = riasec["A"]
    composites["S"] = riasec["S"]
    composites["E"] = riasec["E"]
    composites["C"] = riasec["C"]

    # Generate interest_code — top 3 RIASEC letters by score
    sorted_letters = sorted(riasec, key=riasec.get, reverse=True)
    composites["interest_code"] = "".join(sorted_letters[:3])

    return composites


def _cluster_score(composites: dict, weights: dict) -> float:
    """
    Score a cluster using weighted composite features + RIASEC.
    RIASEC keys in weights use _riasec suffix e.g. I_riasec.
    """
    total = 0.0
    for feat, w in weights.items():
        if feat.endswith("_riasec"):
            letter = feat[0]  # e.g. "I_riasec" -> "I"
            val    = composites.get(letter, 50.0) / 100.0
        else:
            val = composites.get(feat, 0.5)
        total += val * w
    return round(total, 4)


def build_10_roles(top1: str, top2: str, top3: str) -> list:
    """Build 10 roles using 5-3-2 split across top 3 clusters."""
    def pick(c, n): return CLUSTER_ROLES.get(c, [])[:n]
    roles = pick(top1, 5) + pick(top2, 3) + pick(top3, 2)
    seen, out = set(), []
    for r in roles:
        if r and r not in seen:
            seen.add(r)
            out.append(r)
    # Fill to 10 if needed
    for c in [top1, top2, top3]:
        for r in CLUSTER_ROLES.get(c, []):
            if len(out) >= 10:
                break
            if r not in seen:
                seen.add(r)
                out.append(r)
    return out[:10]


def predict(mcq: dict) -> dict:
    """
    Predict career clusters and roles from MCQ answers.

    Full pipeline:
      MCQ (Q1-Q40)
      → 20 composite features (0.0-1.0)
      → 6 RIASEC scores (0-100)
      → interest_code (e.g. IRC)
      → cluster scoring
      → top3 clusters + 10 roles

    Args:
        mcq: dict with keys Q1..Q40, values 1-5

    Returns:
        dict with top1_cluster, top2_cluster, top3_cluster,
              roles, cluster_scores, features, interest_code
    """
    # Step 1-3: MCQ → composites → RIASEC → interest_code
    features = compute_composites(mcq)

    # Step 4: Score all 8 clusters
    scores = {}
    for cluster, weights in SCORE_WEIGHTS.items():
        scores[cluster] = _cluster_score(features, weights)

    # Step 5: Rank clusters
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top1   = ranked[0][0]
    top2   = ranked[1][0]
    top3   = ranked[2][0]

    return {
        "top1_cluster":   top1,
        "top2_cluster":   top2,
        "top3_cluster":   top3,
        "cluster_scores": dict(ranked),
        "roles":          build_10_roles(top1, top2, top3),
        "features":       features,
        "interest_code":  features.get("interest_code", ""),
        "riasec": {
            "R": features.get("R", 50.0),
            "I": features.get("I", 50.0),
            "A": features.get("A", 50.0),
            "S": features.get("S", 50.0),
            "E": features.get("E", 50.0),
            "C": features.get("C", 50.0),
        },
    }
