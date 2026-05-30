# =============================================================
# EduLink — Model 2: Writing Analysis
# Version: 2.0 — Expanded anchors matching Colab notebook
# Method: Sentence Transformers (paraphrase-MiniLM-L6-v2)
# Output: clarity, structure, confidence, analytical, creativity,
#         overall_writing_score (matches AI Reasoning Layer)
# =============================================================

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# ── Anchor sentences ──────────────────────────────────────────
# Expanded to 4+ per trait matching Colab notebook Cell 5
# Based on Holland RIASEC + SCCT self-efficacy theory

ANCHORS = {
    "clarity": {
        "good": [
            "I have a clear plan to study software engineering and specialize in backend development.",
            "My career goal is specific: I want to become a data scientist within three years.",
            "I decided to break the problem into three clear and specific steps.",
            "My goal is to enter IT. I will start with the basics and practice daily.",
            "I am interested in IT because I enjoy solving structured and well-defined problems.",
        ],
        "weak": [
            "I like IT and many things. Maybe I will do it. I am not sure.",
            "IT is good and nice. I do not know what to do exactly.",
            "I just want a job. Technology seems fine I think.",
            "Maybe technology is good. I am not really sure what I want to do.",
        ],
    },
    "structure": {
        "good": [
            "First I identified the problem. Then I researched solutions. Finally I implemented the best option.",
            "My plan has three phases: month 1 to 3 Python basics, month 4 to 6 web development, month 7 to 12 internship.",
            "There are three steps to my plan: foundation skills, specialization, and portfolio building.",
            "Step one is completing my degree. Step two is obtaining certifications. Step three is applying for roles.",
            "My response has a clear beginning, middle, and conclusion with logical flow throughout.",
        ],
        "weak": [
            "I want IT and many things and no clear plan. I will see later what happens.",
            "I like IT. It depends on many things I guess.",
            "I will just learn stuff and see what happens later on.",
            "I might do a course. Or maybe not. It is hard to say right now.",
        ],
    },
    "confidence": {
        "good": [
            "I am confident I can improve by practicing daily. I will set weekly goals and complete them.",
            "I believe in my ability to learn new technologies quickly given my analytical background.",
            "I completed the project successfully in two weeks ahead of the deadline.",
            "I will become a software engineer within three years. I am determined.",
            "I am determined to complete this program regardless of difficulty. I have already started.",
        ],
        "weak": [
            "Maybe I can do it but I am not sure. It might be hard for me.",
            "Perhaps I will try. I guess it depends on luck and circumstances.",
            "I hope it works out but technology is very difficult and I may fail.",
            "I do not know if I am capable. Maybe someone else would be better than me.",
        ],
    },
    "analytical": {
        "good": [
            "Because technology changes fast, I analysed job requirements and identified the top demanded skills.",
            "I compared three approaches and selected the most efficient one based on performance data.",
            "I researched that data science requires Python, statistics, and machine learning ranked by priority.",
            "After comparing the data I found three key patterns that guided my decision.",
            "I used statistics to identify the root cause and therefore chose the most evidence-based solution.",
        ],
        "weak": [
            "I just did it and it was okay. Things worked out somehow in the end.",
            "I did not really think much about it. I just went with what felt right.",
            "I chose IT because it seemed good. I did not do much research.",
            "Things worked out somehow without me needing to analyse anything deeply.",
        ],
    },
    "creativity": {
        "good": [
            "I combined two unrelated ideas to create an original and unexpected solution to the problem.",
            "I invented a new approach instead of following the standard method everyone else used.",
            "My solution was unique because I thought differently from others in my group.",
            "I designed a novel system by adapting concepts from biology to solve a software problem.",
            "I created an original project that nobody in my class had thought of before.",
        ],
        "weak": [
            "I followed the standard approach exactly as taught in class without any modifications.",
            "I copied the example from the textbook and applied it directly to my project.",
            "I did what everyone else did. I followed the instructions step by step.",
            "I used the template that was given to us. I did not change anything.",
        ],
    },
}

# ── Pre-encode all anchors once at startup ────────────────────
_encoded = {}
for trait, data in ANCHORS.items():
    _encoded[trait] = {
        "good": model.encode(data["good"], convert_to_tensor=True),
        "weak": model.encode(data["weak"], convert_to_tensor=True),
    }


def analyze(text: str) -> dict:
    """
    Analyse a writing sample and return 5 trait scores + overall.

    Method: Sentence Transformer cosine similarity vs anchor sentences.
    Formula: score = 50 + (avg_good_sim - avg_weak_sim) * 100
    Range: 0 to 100 per trait.

    Args:
        text: student writing sample string

    Returns:
        dict with keys:
          clarity, structure, confidence, analytical, creativity
          overall_writing_score  (matches AI Reasoning Layer)
          word_count
    """
    if not text or len(text.strip()) < 5:
        return {
            "clarity":               50.0,
            "analytical":            50.0,
            "structure":             50.0,
            "confidence":            50.0,
            "creativity":            50.0,
            "overall_writing_score": 50.0,
            "overall":               50.0,
            "word_count":            0,
        }

    student_emb = model.encode(text, convert_to_tensor=True)
    scores = {}

    for trait in ANCHORS:
        good_sims = util.cos_sim(
            student_emb, _encoded[trait]["good"]
        ).mean().item()
        weak_sims = util.cos_sim(
            student_emb, _encoded[trait]["weak"]
        ).mean().item()
        raw           = good_sims - weak_sims
        scores[trait] = round(
            max(0.0, min(100.0, 50.0 + raw * 100.0)), 1
        )

    overall = round(
        sum(scores[t] for t in ANCHORS) / len(ANCHORS), 1
    )
    scores["overall_writing_score"] = overall
    scores["overall"]    = overall
    scores["word_count"] = len(text.split())
    return scores
