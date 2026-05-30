# ============================================================
# EduLink — Skill Extractor
# Extracts required skills from Adzuna job descriptions
# Option B — Live job data analysis
# ============================================================

import requests
import re
from datetime import datetime
from collections import Counter

ADZUNA_APP_ID  = "8ed884a5"
ADZUNA_APP_KEY = "2a8d6f97d7e05630624dde8a54250af9"

# IT skill keywords to detect in job descriptions
SKILL_KEYWORDS = [
    # Programming languages
    "python", "java", "javascript", "typescript", "c++", "c#",
    "kotlin", "swift", "dart", "ruby", "php", "scala", "r",

    # Web and mobile
    "react", "angular", "vue", "nodejs", "flutter", "html", "css",
    "django", "fastapi", "spring boot", "laravel",

    # Data and AI
    "machine learning", "deep learning", "tensorflow", "pytorch",
    "pandas", "numpy", "sql", "data analysis", "statistics",
    "natural language processing", "computer vision", "tableau",
    "power bi", "excel", "spark", "hadoop",

    # Cloud and DevOps
    "aws", "azure", "google cloud", "docker", "kubernetes",
    "jenkins", "git", "linux", "ci/cd", "terraform",

    # Design
    "figma", "adobe xd", "photoshop", "illustrator",
    "user research", "wireframing", "prototyping",

    # Business and management
    "agile", "scrum", "jira", "project management",
    "stakeholder management", "business analysis",
    "requirements gathering",

    # Networking and security
    "networking", "cisco", "cybersecurity", "penetration testing",
    "firewalls", "routing", "switching",

    # Databases
    "mysql", "postgresql", "mongodb", "firebase", "redis",
    "database design",
]

ROLE_KEYWORDS = {
    "Data Scientist":           "data scientist machine learning",
    "ML Engineer":              "machine learning engineer",
    "Data Engineer":            "data engineer pipeline",
    "Software Engineer":        "software engineer developer",
    "Full Stack Developer":     "full stack developer web",
    "Backend Developer":        "backend developer API",
    "Frontend Developer":       "frontend developer React",
    "Mobile Developer":         "mobile developer flutter android",
    "DevOps Engineer":          "devops engineer cloud",
    "Cloud Engineer":           "cloud engineer AWS",
    "QA Engineer":              "QA engineer testing automation",
    "UI/UX Designer":           "UI UX designer figma",
    "Business Analyst":         "business analyst IT",
    "IT Project Manager":       "IT project manager agile",
    "Network Engineer":         "network engineer cisco",
    "Cybersecurity Engineer":   "cybersecurity engineer",
    "Digital Marketer":         "digital marketing SEO",
    "Embedded Systems Engineer":"embedded systems engineer IoT",
}


def _fetch_job_descriptions(role: str, count: int = 10) -> list:
    """Fetch job descriptions from Adzuna."""
    keyword = ROLE_KEYWORDS.get(role, role)
    try:
        r = requests.get(
            "https://api.adzuna.com/v1/api/jobs/in/search/1",
            params={
                "app_id":           ADZUNA_APP_ID,
                "app_key":          ADZUNA_APP_KEY,
                "what":             keyword,
                "results_per_page": count,
                "content-type":     "application/json",
            },
            timeout=10,
        )
        if r.status_code != 200:
            return []

        jobs = r.json().get("results", [])
        return [j.get("description", "") for j in jobs if j.get("description")]

    except Exception:
        return []


def _extract_skills_from_text(text: str) -> list:
    """Find skill keywords in text."""
    text_lower = text.lower()
    found = []
    for skill in SKILL_KEYWORDS:
        if skill in text_lower:
            found.append(skill)
    return found


def extract_skills(role: str, cluster: str,
                   top_n: int = 8) -> dict:
    """
    Extract top required skills for a role
    by analysing real Adzuna job descriptions.
    """
    descriptions = _fetch_job_descriptions(role, count=10)

    if not descriptions:
        return _fallback_skills(cluster)

    # Count skill mentions across all job postings
    skill_counter = Counter()
    for desc in descriptions:
        skills_found = _extract_skills_from_text(desc)
        skill_counter.update(skills_found)

    # Get top skills
    top_skills = skill_counter.most_common(top_n)

    if not top_skills:
        return _fallback_skills(cluster)

    # Format result
    total_jobs = len(descriptions)
    skills_list = []
    for skill, count in top_skills:
        frequency = round((count / total_jobs) * 100)
        skills_list.append({
            "name":      skill.title(),
            "frequency": frequency,
            "count":     count,
            "type":      _classify_skill(skill),
        })

    return {
        "cluster":     cluster,
        "role":        role,
        "skills":      skills_list,
        "total_jobs":  total_jobs,
        "source":      "adzuna_live",
        "region":      "India / Sri Lanka",
        "updated_at":  datetime.now().isoformat(),
    }


def _classify_skill(skill: str) -> str:
    """Classify skill as technical or soft."""
    soft_skills = [
        "agile", "scrum", "project management",
        "stakeholder", "communication", "requirements",
        "business analysis", "user research"
    ]
    return "soft" if any(s in skill for s in soft_skills) else "technical"


def _fallback_skills(cluster: str) -> dict:
    """Fallback skills when Adzuna unavailable."""
    fallbacks = {
        "Data_AI_Engineering": [
            {"name": "Python",           "frequency": 90, "type": "technical"},
            {"name": "Machine Learning", "frequency": 85, "type": "technical"},
            {"name": "SQL",              "frequency": 80, "type": "technical"},
            {"name": "Statistics",       "frequency": 75, "type": "technical"},
            {"name": "TensorFlow",       "frequency": 60, "type": "technical"},
            {"name": "Data Analysis",    "frequency": 70, "type": "technical"},
            {"name": "Pandas",           "frequency": 65, "type": "technical"},
            {"name": "Agile",            "frequency": 50, "type": "soft"},
        ],
        "Software_Web_Engineering": [
            {"name": "Java",             "frequency": 85, "type": "technical"},
            {"name": "Python",           "frequency": 80, "type": "technical"},
            {"name": "React",            "frequency": 75, "type": "technical"},
            {"name": "SQL",              "frequency": 70, "type": "technical"},
            {"name": "Git",              "frequency": 90, "type": "technical"},
            {"name": "Docker",           "frequency": 60, "type": "technical"},
            {"name": "Agile",            "frequency": 80, "type": "soft"},
            {"name": "Scrum",            "frequency": 65, "type": "soft"},
        ],
        "UX_Creative_Tech": [
            {"name": "Figma",            "frequency": 90, "type": "technical"},
            {"name": "User Research",    "frequency": 80, "type": "soft"},
            {"name": "Prototyping",      "frequency": 75, "type": "technical"},
            {"name": "Html",             "frequency": 60, "type": "technical"},
            {"name": "Css",              "frequency": 60, "type": "technical"},
            {"name": "Adobe Xd",         "frequency": 55, "type": "technical"},
            {"name": "Wireframing",      "frequency": 70, "type": "technical"},
            {"name": "Agile",            "frequency": 50, "type": "soft"},
        ],
        "Business_IT_Management": [
            {"name": "Project Management","frequency": 85, "type": "soft"},
            {"name": "Agile",            "frequency": 80, "type": "soft"},
            {"name": "Scrum",            "frequency": 75, "type": "soft"},
            {"name": "Jira",             "frequency": 70, "type": "technical"},
            {"name": "Excel",            "frequency": 80, "type": "technical"},
            {"name": "Sql",              "frequency": 60, "type": "technical"},
            {"name": "Stakeholder Management","frequency": 75, "type": "soft"},
            {"name": "Business Analysis","frequency": 70, "type": "soft"},
        ],
        "Digital_Marketing_Media": [
            {"name": "Seo",              "frequency": 85, "type": "technical"},
            {"name": "Google Analytics", "frequency": 80, "type": "technical"},
            {"name": "Excel",            "frequency": 70, "type": "technical"},
            {"name": "Agile",            "frequency": 50, "type": "soft"},
            {"name": "Tableau",          "frequency": 55, "type": "technical"},
            {"name": "Project Management","frequency": 60, "type": "soft"},
        ],
        "Network_Infrastructure": [
            {"name": "Cisco",            "frequency": 85, "type": "technical"},
            {"name": "Linux",            "frequency": 80, "type": "technical"},
            {"name": "Networking",       "frequency": 90, "type": "technical"},
            {"name": "Aws",              "frequency": 70, "type": "technical"},
            {"name": "Docker",           "frequency": 60, "type": "technical"},
            {"name": "Kubernetes",       "frequency": 55, "type": "technical"},
        ],
        "IT_Operations_QA": [
            {"name": "Agile",            "frequency": 85, "type": "soft"},
            {"name": "Jira",             "frequency": 80, "type": "technical"},
            {"name": "Scrum",            "frequency": 75, "type": "soft"},
            {"name": "Python",           "frequency": 60, "type": "technical"},
            {"name": "Sql",              "frequency": 65, "type": "technical"},
            {"name": "Git",              "frequency": 70, "type": "technical"},
        ],
        "Hardware_Systems": [
            {"name": "C++",              "frequency": 85, "type": "technical"},
            {"name": "Linux",            "frequency": 80, "type": "technical"},
            {"name": "Python",           "frequency": 70, "type": "technical"},
            {"name": "Git",              "frequency": 75, "type": "technical"},
            {"name": "Docker",           "frequency": 55, "type": "technical"},
        ],
    }

    skills = fallbacks.get(cluster,
             fallbacks["Software_Web_Engineering"])

    return {
        "cluster":    cluster,
        "role":       "",
        "skills":     skills,
        "total_jobs": 0,
        "source":     "fallback",
        "region":     "Sri Lanka",
        "updated_at": datetime.now().isoformat(),
    }