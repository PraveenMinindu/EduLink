# ============================================================
# EduLink — Writing Routes
# POST /student/submit-writing
# ============================================================

import re
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from firebase_bridge import save_writing

router = APIRouter()

class WritingSubmission(BaseModel):
    student_id: str
    text:       str


def _count_words(text: str) -> int:
    """Count real words — ignores extra spaces and newlines."""
    return len(re.findall(r'\b\w+\b', text.strip()))


def _count_sentences(text: str) -> int:
    """Count sentences by punctuation."""
    return len(re.findall(r'[.!?]+', text))


def _count_unique_words(text: str) -> int:
    """Count vocabulary diversity."""
    words = re.findall(r'\b\w+\b', text.lower())
    return len(set(words))


def _is_repetitive(text: str) -> bool:
    """
    Detect copy-paste or repeated phrase submissions.
    Returns True if same phrase repeated more than 3 times.
    """
    words = text.lower().split()
    if len(words) < 6:
        return False
    # Check if any 3-word phrase repeats more than 3 times
    phrases = [" ".join(words[i:i+3]) for i in range(len(words)-2)]
    for phrase in phrases:
        if phrases.count(phrase) > 3:
            return True
    return False


def _is_gibberish(text: str) -> bool:
    """
    Detect keyboard mashing or random character input.
    Returns True if too many non-English characters.
    """
    total = len(text.replace(" ", ""))
    if total == 0:
        return False
    alpha = len(re.findall(r'[a-zA-Z]', text))
    ratio = alpha / total
    return ratio < 0.6


@router.post("/submit-writing")
def submit_writing(data: WritingSubmission):
    try:

        # ── Validation 1 — student_id not empty ──────────
        if not data.student_id or data.student_id.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="student_id cannot be empty"
            )

        # ── Validation 2 — text not empty ────────────────
        if not data.text or data.text.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="Writing sample cannot be empty"
            )

        word_count = _count_words(data.text)
        sentence_count = _count_sentences(data.text)
        unique_words = _count_unique_words(data.text)

        # ── Validation 3 — minimum word count ────────────
        if word_count < 30:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": f"Writing sample too short ({word_count} words).",
                    "hint":    "Please write at least 30 words. Aim for 100-150 words for the best career analysis.",
                    "minimum": 30,
                    "current": word_count
                }
            )

        # ── Validation 4 — maximum word count ────────────
        if word_count > 500:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": f"Writing sample too long ({word_count} words).",
                    "hint":    "Please keep your response under 500 words.",
                    "maximum": 500,
                    "current": word_count
                }
            )

        # ── Validation 5 — gibberish detection ───────────
        if _is_gibberish(data.text):
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Writing sample appears to contain invalid characters.",
                    "hint":    "Please write your response in English."
                }
            )

        # ── Validation 6 — repetition detection ──────────
        if _is_repetitive(data.text):
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Writing sample appears to be repetitive.",
                    "hint":    "Please write a genuine response. Repeated phrases were detected."
                }
            )

        # ── Validation 7 — vocabulary diversity ──────────
        if word_count >= 30:
            diversity_ratio = unique_words / word_count
            if diversity_ratio < 0.3:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "message": "Writing sample has very low vocabulary diversity.",
                        "hint":    "Please write using varied language. Avoid repeating the same words.",
                        "unique_words": unique_words,
                        "total_words":  word_count
                    }
                )

        # ── All valid — save ──────────────────────────────
        save_writing(data.student_id, data.text)

        # ── Quality hint for short but valid submissions ──
        quality_hint = None
        if word_count < 80:
            quality_hint = "Your response is a bit short. Writing 100-150 words gives the AI more data for a more accurate analysis."

        return {
            "status":         "success",
            "message":        "Writing sample saved successfully",
            "student_id":     data.student_id,
            "word_count":     word_count,
            "sentence_count": sentence_count,
            "unique_words":   unique_words,
            "quality_hint":   quality_hint
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))