# =============================================================
# EduLink — Model 6: Job Recommendation
# Converted from: job_recommendation.ipynb
# Jaccard similarity — pure Python, no Spark needed
# =============================================================

import re

# Sri Lanka IT vacancies — matches synthetic_vacancies_sl_it.csv structure
VACANCIES = [
    {"vacancy_id":"V001","company":"WSO2","job_title":"Data Scientist","location":"Colombo","skills":"python machine learning data analysis statistics pandas","url":"https://wso2.com/careers"},
    {"vacancy_id":"V002","company":"IFS","job_title":"ML Engineer","location":"Colombo","skills":"machine learning python tensorflow deep learning mlops","url":"https://jobs.ifs.com"},
    {"vacancy_id":"V003","company":"99X Technology","job_title":"Data Engineer","location":"Remote","skills":"data engineering spark sql python etl pipeline","url":"https://99x.io/careers"},
    {"vacancy_id":"V004","company":"hSenid Mobile","job_title":"AI Developer","location":"Colombo","skills":"artificial intelligence python nlp computer vision deep learning","url":"https://hsenid.com/careers"},
    {"vacancy_id":"V005","company":"Zoho","job_title":"Analytics Engineer","location":"Colombo","skills":"analytics sql data visualization tableau python powerbi","url":"https://zoho.com/careers"},
    {"vacancy_id":"V006","company":"WSO2","job_title":"Software Engineer","location":"Colombo","skills":"java microservices rest api spring docker kubernetes","url":"https://wso2.com/careers"},
    {"vacancy_id":"V007","company":"Virtusa","job_title":"Full Stack Developer","location":"Colombo","skills":"react nodejs javascript mongodb typescript postgresql","url":"https://virtusa.com/careers"},
    {"vacancy_id":"V008","company":"Sysco LABS","job_title":"Backend Developer","location":"Colombo","skills":"python django postgresql rest api microservices aws","url":"https://syscolabs.com/careers"},
    {"vacancy_id":"V009","company":"CodeGen","job_title":"Frontend Developer","location":"Colombo","skills":"react angular typescript html css javascript vue","url":"https://codegen.net/careers"},
    {"vacancy_id":"V010","company":"IFS","job_title":"Mobile Developer","location":"Colombo","skills":"flutter dart ios android react native mobile","url":"https://jobs.ifs.com"},
    {"vacancy_id":"V011","company":"Dialog Axiata","job_title":"Network Engineer","location":"Colombo","skills":"networking cisco routing switching network security infrastructure","url":"https://dialog.lk/careers"},
    {"vacancy_id":"V012","company":"SLT Mobitel","job_title":"Cloud Engineer","location":"Colombo","skills":"aws azure kubernetes docker devops cloud infrastructure","url":"https://slt.lk/careers"},
    {"vacancy_id":"V013","company":"Virtusa","job_title":"DevOps Engineer","location":"Colombo","skills":"jenkins kubernetes docker ci cd linux devops automation","url":"https://virtusa.com/careers"},
    {"vacancy_id":"V014","company":"Pearson","job_title":"QA Engineer","location":"Remote","skills":"selenium test automation java agile jira quality assurance","url":"https://pearson.com/careers"},
    {"vacancy_id":"V015","company":"Workmate","job_title":"UI/UX Designer","location":"Colombo","skills":"figma user research prototyping user interface design thinking","url":"https://workmate.com/careers"},
    {"vacancy_id":"V016","company":"Millennium IT ESP","job_title":"Business Analyst","location":"Colombo","skills":"business analysis requirements sql stakeholder management agile","url":"https://millenniumitesp.com/careers"},
    {"vacancy_id":"V017","company":"99X Technology","job_title":"IT Project Manager","location":"Colombo","skills":"project management agile scrum stakeholder management jira planning","url":"https://99x.io/careers"},
    {"vacancy_id":"V018","company":"Calcey","job_title":"Software Engineer","location":"Colombo","skills":"python nodejs react postgresql aws software development","url":"https://calcey.com/careers"},
    {"vacancy_id":"V019","company":"Rootcode","job_title":"Data Analyst","location":"Colombo","skills":"sql python data visualization excel powerbi reporting analysis","url":"https://rootcode.io/careers"},
    {"vacancy_id":"V020","company":"WSO2","job_title":"Solutions Architect","location":"Colombo","skills":"architecture cloud microservices integration api management design","url":"https://wso2.com/careers"},
]

STOPWORDS = {
    "the","and","for","are","with","this","that","have","will",
    "can","not","you","from","they","was","been","has","its",
}


def _tokenize(text: str) -> set:
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return set(t for t in tokens if len(t) > 2 and t not in STOPWORDS)


def _jaccard(a: set, b: set) -> float:
    """Exact Jaccard formula from notebook Cell 7."""
    if not a or not b: return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union > 0 else 0.0


def match(roles: list, top_n: int = 5) -> dict:
    """
    Match job roles to vacancies using Jaccard similarity.
    Exact: title_sim*0.60 + skills_sim*0.40 from notebook Cell 7.

    Args:
        roles:  list of role names (top 10 from career fit)
        top_n:  number of vacancies to return

    Returns:
        dict with matches (list), total_searched, matches_found
    """
    target_roles = roles[:5]   # top 5 roles only
    scored = []

    for vac in VACANCIES:
        title_tokens  = _tokenize(vac["job_title"])
        skills_tokens = _tokenize(vac.get("skills", ""))
        combined      = title_tokens | skills_tokens

        best_score = 0.0
        best_role  = ""

        for role in target_roles:
            role_tokens = _tokenize(role)
            # Exact formula from notebook Cell 7
            title_sim  = _jaccard(role_tokens, title_tokens)
            skills_sim = _jaccard(role_tokens, combined)
            score      = round(title_sim * 0.60 + skills_sim * 0.40, 4)

            if score > best_score:
                best_score = score
                best_role  = role

        scored.append({
            "vacancy_id":   vac["vacancy_id"],
            "company":      vac["company"],
            "title":        vac["job_title"],
            "location":     vac["location"],
            "url":          vac["url"],
            "match_score":  best_score,
            "matched_role": best_role,
            "status":       "Active",
        })

    scored.sort(key=lambda x: x["match_score"], reverse=True)
    # Filter low scores (< 0.05) then take top N
    matches = [v for v in scored if v["match_score"] >= 0.05][:top_n]
    if len(matches) < top_n:
        matches = scored[:top_n]

    return {
        "matches":               matches,
        "total_vacancies_searched": len(VACANCIES),
        "matches_found":         len(matches),
    }
