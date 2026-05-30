from sentence_transformers import SentenceTransformer, util
import torch

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

ANCHORS = {
    "clarity": {
        "good": [
            "I have a clear plan to study software engineering.",
            "My career goal is specific — I want to become a data scientist.",
            "I decided to break the problem into three clear steps.",
        ],
        "weak": [
            "I like IT and many things. Maybe I will do it.",
            "IT is good and nice. I am not sure what to do.",
        ]
    },
    "analytical": {
        "good": [
            "After comparing the data I found three key patterns.",
            "I analysed the problem systematically using evidence.",
            "I used statistics to identify the root cause.",
        ],
        "weak": [
            "I just did it and it was okay.",
            "Things worked out somehow.",
        ]
    },
    "structure": {
        "good": [
            "First I identified the problem. Then I researched solutions. Finally I implemented the best option.",
            "My response has a clear beginning, middle, and conclusion.",
        ],
        "weak": [
            "I did many things. Also other stuff happened. IT is good.",
        ]
    },
    "confidence": {
        "good": [
            "I completed the project successfully in two weeks.",
            "I will become a software engineer within three years.",
            "I achieved first place in the class competition.",
        ],
        "weak": [
            "I hope maybe I can try to learn IT if possible.",
            "I think perhaps I might be okay at computers.",
        ]
    },
    "creativity": {
        "good": [
            "I combined two unrelated ideas to create an original solution.",
            "I invented a new approach instead of following the standard method.",
            "My solution was unique because I thought differently from others.",
        ],
        "weak": [
            "I followed the standard approach exactly as taught.",
            "I copied the example from the textbook.",
        ]
    }
}

# Pre-encode all anchors once at startup
_encoded = {}
for trait, data in ANCHORS.items():
    _encoded[trait] = {
        "good": model.encode(data["good"], convert_to_tensor=True),
        "weak": model.encode(data["weak"],  convert_to_tensor=True),
    }

def analyze(text: str) -> dict:
    if not text or len(text.strip()) < 5:
        return {
            "clarity":    50.0,
            "analytical": 50.0,
            "structure":  50.0,
            "confidence": 50.0,
            "creativity": 50.0,
            "overall":    50.0,
            "word_count": 0,
        }

    student_emb = model.encode(text, convert_to_tensor=True)
    scores = {}

    for trait in ANCHORS:
        good_sims = util.cos_sim(student_emb, _encoded[trait]["good"]).mean().item()
        weak_sims = util.cos_sim(student_emb, _encoded[trait]["weak"]).mean().item()
        raw = good_sims - weak_sims
        scores[trait] = round(max(0.0, min(100.0, 50 + raw * 100)), 1)

    scores["overall"]    = round(sum(scores[t] for t in ANCHORS) / len(ANCHORS), 1)
    scores["word_count"] = len(text.split())
    return scores