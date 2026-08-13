# ============================================================
# EduLink — Live Job Board Service
# Primary:   Adzuna API (free tier, India region)
# Fallback:  Sri Lanka IT company vacancies (curated list)
# ============================================================
#
# PHASE 3 FIX:
#   Expanded Jaccard query from role-name-only tokens to
#   role-name + cluster-specific skill tokens.
#   Previously: query = {"network", "engineer"}  (2 tokens)
#   Now:        query = {"network", "engineer", "cisco",
#                        "routing", "switching", ...}
#   This produces more meaningful similarity scores against
#   job descriptions that use technical skill terminology
#   rather than exact role title matches.
#
#   TopJobs.lk scraping removed — was unreliable and added
#   no value when Adzuna is available and fallback exists.
#   Three-tier architecture maintained:
#     Priority 1: Adzuna live API
#     Priority 2: Curated Sri Lanka IT fallback
# ============================================================

import requests
import re
from datetime import datetime

ADZUNA_APP_ID  = "8ed884a5"
ADZUNA_APP_KEY = "2a8d6f97d7e05630624dde8a54250af9"

# Cluster-to-skill token mapping used to expand Jaccard query.
# These are the representative technical skills for each career cluster.
# They supplement the role name tokens to improve matching accuracy
# against job descriptions that use skill keywords rather than role titles.
CLUSTER_SKILL_TOKENS = {
    "Data_AI_Engineering":      [
        "python", "machine", "learning", "tensorflow", "pytorch",
        "data", "sql", "pandas", "numpy", "statistics",
        "deep", "neural", "nlp", "analytics", "spark",
    ],
    "Software_Web_Engineering": [
        "java", "python", "react", "nodejs", "javascript",
        "typescript", "api", "microservices", "docker",
        "postgresql", "mongodb", "aws", "agile",
    ],
    "Network_Infrastructure":   [
        "cisco", "networking", "routing", "switching",
        "infrastructure", "linux", "cloud", "azure",
        "aws", "kubernetes", "security", "firewall",
    ],
    "IT_Operations_QA":         [
        "testing", "selenium", "automation", "jira",
        "agile", "devops", "jenkins", "linux",
        "ci", "cd", "support", "helpdesk",
    ],
    "UX_Creative_Tech":         [
        "figma", "ui", "ux", "design", "user",
        "research", "prototyping", "wireframe",
        "adobe", "interaction", "usability",
    ],
    "Business_IT_Management":   [
        "agile", "scrum", "project", "management",
        "stakeholder", "requirements", "analysis",
        "jira", "strategy", "product", "roadmap",
    ],
    "Digital_Marketing_Media":  [
        "seo", "marketing", "google", "analytics",
        "social", "media", "content", "campaign",
        "digital", "powerbi", "tableau", "reporting",
    ],
    "Hardware_Systems":         [
        "embedded", "firmware", "rtos", "microcontroller",
        "iot", "hardware", "electronics", "cpp",
        "arduino", "raspberry", "circuit", "pcb",
    ],
}

# Role to Adzuna keyword mapping (unchanged from original)
ROLE_KEYWORDS = {
    "Data Scientist":            "data scientist",
    "ML Engineer":               "machine learning engineer",
    "Data Engineer":             "data engineer",
    "AI Developer":              "AI developer",
    "Software Engineer":         "software engineer",
    "Full Stack Developer":      "full stack developer",
    "Backend Developer":         "backend developer",
    "Frontend Developer":        "frontend developer",
    "Mobile Developer":          "mobile developer flutter",
    "DevOps Engineer":           "devops engineer",
    "Cloud Engineer":            "cloud engineer AWS",
    "QA Engineer":               "QA engineer test automation",
    "UI/UX Designer":            "UI UX designer",
    "Business Analyst":          "business analyst IT",
    "IT Project Manager":        "IT project manager",
    "Network Engineer":          "network engineer",
    "Cybersecurity Engineer":    "cybersecurity engineer",
    "Digital Marketer":          "digital marketing",
    "Embedded Systems Engineer": "embedded systems engineer",
    "Database Administrator":    "database administrator",
}

# Curated Sri Lanka IT fallback vacancies
FALLBACK_VACANCIES = [
    {"id":"V001","company":"WSO2","title":"Data Scientist",
     "location":"Colombo, Sri Lanka","url":"https://wso2.com/careers",
     "description":"python machine learning data analysis statistics pandas tensorflow",
     "type":"Full-time","source":"company_careers"},
    {"id":"V002","company":"IFS R&D","title":"ML Engineer",
     "location":"Colombo, Sri Lanka","url":"https://jobs.ifs.com",
     "description":"machine learning tensorflow deep learning mlops python pytorch",
     "type":"Full-time","source":"company_careers"},
    {"id":"V003","company":"99X Technology","title":"Data Engineer",
     "location":"Colombo / Remote","url":"https://99x.io/careers",
     "description":"data engineering spark sql python etl pipeline kafka",
     "type":"Full-time","source":"company_careers"},
    {"id":"V004","company":"hSenid Mobile","title":"AI Developer",
     "location":"Colombo, Sri Lanka","url":"https://hsenidmobile.com/careers",
     "description":"artificial intelligence python nlp computer vision deep learning",
     "type":"Full-time","source":"company_careers"},
    {"id":"V005","company":"Virtusa","title":"Software Engineer",
     "location":"Colombo, Sri Lanka","url":"https://virtusa.com/careers",
     "description":"java microservices rest api spring boot docker kubernetes",
     "type":"Full-time","source":"company_careers"},
    {"id":"V006","company":"Sysco LABS","title":"Full Stack Developer",
     "location":"Colombo, Sri Lanka","url":"https://syscolabs.com/careers",
     "description":"react nodejs javascript mongodb typescript postgresql aws",
     "type":"Full-time","source":"company_careers"},
    {"id":"V007","company":"CodeGen International","title":"Backend Developer",
     "location":"Colombo, Sri Lanka","url":"https://codegen.net/careers",
     "description":"python django postgresql rest api microservices aws lambda",
     "type":"Full-time","source":"company_careers"},
    {"id":"V008","company":"IFS R&D","title":"Mobile Developer",
     "location":"Colombo, Sri Lanka","url":"https://jobs.ifs.com",
     "description":"flutter dart ios android react native mobile development",
     "type":"Full-time","source":"company_careers"},
    {"id":"V009","company":"Dialog Axiata","title":"Network Engineer",
     "location":"Colombo, Sri Lanka","url":"https://dialog.lk/careers",
     "description":"networking cisco routing switching network security infrastructure",
     "type":"Full-time","source":"company_careers"},
    {"id":"V010","company":"SLT Mobitel","title":"Cloud Engineer",
     "location":"Colombo, Sri Lanka","url":"https://slt.lk/careers",
     "description":"aws azure kubernetes docker devops terraform cloud infrastructure",
     "type":"Full-time","source":"company_careers"},
    {"id":"V011","company":"Pearson","title":"QA Engineer",
     "location":"Colombo / Remote","url":"https://pearson.com/careers",
     "description":"selenium test automation java agile jira quality assurance testing",
     "type":"Full-time","source":"company_careers"},
    {"id":"V012","company":"Workmate","title":"UI/UX Designer",
     "location":"Colombo, Sri Lanka","url":"https://workmate.com/careers",
     "description":"figma user research prototyping user interface design thinking ux",
     "type":"Full-time","source":"company_careers"},
    {"id":"V013","company":"Millennium IT ESP","title":"Business Analyst",
     "location":"Colombo, Sri Lanka","url":"https://millenniumitesp.com/careers",
     "description":"business analysis requirements sql stakeholder management agile scrum",
     "type":"Full-time","source":"company_careers"},
    {"id":"V014","company":"99X Technology","title":"IT Project Manager",
     "location":"Colombo, Sri Lanka","url":"https://99x.io/careers",
     "description":"project management agile scrum stakeholder jira planning delivery",
     "type":"Full-time","source":"company_careers"},
    {"id":"V015","company":"Rootcode Labs","title":"Data Analyst",
     "location":"Colombo, Sri Lanka","url":"https://rootcode.io/careers",
     "description":"sql python data visualisation excel powerbi reporting tableau",
     "type":"Full-time","source":"company_careers"},
    {"id":"V016","company":"Virtusa","title":"DevOps Engineer",
     "location":"Colombo, Sri Lanka","url":"https://virtusa.com/careers",
     "description":"jenkins kubernetes docker ci cd linux gitlab devops automation",
     "type":"Full-time","source":"company_careers"},
    {"id":"V017","company":"Calcey Technologies","title":"Software Developer",
     "location":"Colombo, Sri Lanka","url":"https://calcey.com/careers",
     "description":"python nodejs react postgresql aws software development agile",
     "type":"Full-time","source":"company_careers"},
    {"id":"V018","company":"Surge Global","title":"Cybersecurity Engineer",
     "location":"Colombo, Sri Lanka","url":"https://surgeglobal.com/careers",
     "description":"cybersecurity penetration testing siem network security compliance",
     "type":"Full-time","source":"company_careers"},
    {"id":"V019","company":"hSenid Mobile","title":"Embedded Systems Engineer",
     "location":"Colombo, Sri Lanka","url":"https://hsenidmobile.com/careers",
     "description":"embedded systems c cpp iot firmware rtos microcontroller hardware",
     "type":"Full-time","source":"company_careers"},
    {"id":"V020","company":"WSO2","title":"Solutions Architect",
     "location":"Colombo, Sri Lanka","url":"https://wso2.com/careers",
     "description":"architecture cloud microservices integration api management design",
     "type":"Full-time","source":"company_careers"},
]

STOPWORDS = {
    "the","and","for","are","with","this","that",
    "have","will","can","not","from","they",
}


def _tokenize(text: str) -> set:
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return set(t for t in tokens if len(t) > 2 and t not in STOPWORDS)


def _jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _build_query_tokens(roles: list, cluster: str = None) -> set:
    """
    Build expanded query token set from role names + cluster skills.

    Previously only role name tokens were used, producing a very small
    token set (e.g. {"network", "engineer"}) that matched poorly against
    job descriptions using technical skill terminology.

    Now cluster-specific skill tokens are added to the query, producing
    a richer token set that matches job descriptions more accurately.
    The cluster skills are sourced from CLUSTER_SKILL_TOKENS which maps
    each career cluster to its representative technical skills.

    Args:
        roles:   list of role names from career fit prediction
        cluster: primary career cluster name (optional)

    Returns:
        Combined token set from role names and cluster skills
    """
    # Role name tokens
    role_tokens = set()
    for role in roles[:3]:
        role_tokens |= _tokenize(role)

    # Cluster skill tokens (expand query beyond role name)
    skill_tokens = set()
    if cluster and cluster in CLUSTER_SKILL_TOKENS:
        skill_tokens = set(CLUSTER_SKILL_TOKENS[cluster])

    return role_tokens | skill_tokens


def _fetch_adzuna(keyword: str, top_n: int = 5) -> list:
    """Fetch live jobs from Adzuna API (India region endpoint)."""
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        return []
    try:
        r = requests.get(
            "https://api.adzuna.com/v1/api/jobs/in/search/1",
            params={
                "app_id":           ADZUNA_APP_ID,
                "app_key":          ADZUNA_APP_KEY,
                "what":             keyword,
                "content-type":     "application/json",
                "results_per_page": top_n,
                "sort_by":          "date",
            },
            timeout=8,
        )
        if r.status_code != 200:
            return []

        jobs   = r.json().get("results", [])
        result = []
        for job in jobs:
            result.append({
                "id":          str(job.get("id", "")),
                "company":     job.get("company", {}).get("display_name", "Company"),
                "title":       job.get("title", ""),
                "location":    job.get("location", {}).get("display_name", "Remote"),
                "url":         job.get("redirect_url", ""),
                "description": job.get("description", "")[:300],
                "type":        "Full-time",
                "posted":      job.get("created", "")[:10],
                "match_score": 0.85,
                "source":      "adzuna_live",
            })
        return result
    except Exception:
        return []


def _match_fallback(roles: list, cluster: str, top_n: int = 5) -> list:
    """
    Match roles and cluster skills to curated Sri Lanka fallback
    vacancies using expanded Jaccard similarity.

    Query tokens now include both role name tokens and cluster
    skill tokens, producing more accurate matching.
    """
    query_tokens = _build_query_tokens(roles, cluster)
    scored = []

    for vac in FALLBACK_VACANCIES:
        title_tok = _tokenize(vac["title"])
        desc_tok  = _tokenize(vac["description"])
        combined  = title_tok | desc_tok

        title_sim  = _jaccard(query_tokens, title_tok)
        skills_sim = _jaccard(query_tokens, combined)
        score      = round(title_sim * 0.6 + skills_sim * 0.4, 4)

        scored.append({**vac, "match_score": score})

    scored.sort(key=lambda x: x["match_score"], reverse=True)
    return scored[:top_n]


def get_jobs(roles: list, cluster: str = None, top_n: int = 5) -> dict:
    """
    Get job matches for given roles using two-tier source strategy.

    Priority 1: Adzuna live API (India region — closest proxy for Sri Lanka)
    Priority 2: Curated Sri Lanka IT company fallback vacancies

    TopJobs.lk scraping removed in Phase 3 — was unreliable and
    produced empty results in most cases due to HTML structure changes.

    Args:
        roles:   list of role names from career fit prediction
        cluster: primary career cluster (used for expanded Jaccard query)
        top_n:   number of matches to return

    Returns:
        dict with matches, source, is_live, fetched_at
    """
    primary_role = roles[0] if roles else "Software Engineer"
    keyword      = ROLE_KEYWORDS.get(primary_role, primary_role)

    # Priority 1 — Adzuna live API
    live_jobs = _fetch_adzuna(keyword, top_n)
    if live_jobs:
        return {
            "matches":      live_jobs,
            "source":       "adzuna_live",
            "is_live":      True,
            "fetched_at":   datetime.now().strftime("%Y-%m-%d %H:%M"),
            "total_found":  len(live_jobs),
            "primary_role": primary_role,
        }

    # Priority 2 — Curated Sri Lanka fallback with expanded Jaccard
    matches = _match_fallback(roles, cluster, top_n)
    return {
        "matches":      matches,
        "source":       "local_sri_lanka_it",
        "is_live":      False,
        "fetched_at":   datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_found":  len(matches),
        "primary_role": primary_role,
    }
