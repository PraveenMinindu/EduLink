# =============================================================
# EduLink — Shared Firestore Utilities
# Improvement 2: single serialize helper used by all admin routes
# =============================================================


def serialize(doc_id: str, data: dict) -> dict:
    """
    Convert a Firestore document dict to a JSON-safe dict.

    - Adds 'id' field from the document ID
    - Converts Firestore DatetimeWithNanoseconds to ISO 8601 string
    - Handles SERVER_TIMESTAMP sentinel values safely
    """
    result = {"id": doc_id}
    for k, v in data.items():
        if hasattr(v, "isoformat"):
            result[k] = v.isoformat()
        else:
            result[k] = v
    return result
