import re

def is_safe_reply(text: str) -> bool:
    """
    Basic safety filter to avoid posting harmful or spammy replies.
    Extend this with more advanced checks if needed.
    """

    if not text or len(text.strip()) == 0:
        return False

    # Block too long replies (>200 tokens ~ 800 chars)
    if len(text) > 800:
        return False

    # Simple blacklist (expandable)
    blacklist = [
        "kill", "suicide", "hate", "terrorist", "nsfw",
        "sex", "violence", "drugs", "racist", "bomb"
    ]
    for word in blacklist:
        if re.search(rf"\b{word}\b", text.lower()):
            return False

    # Avoid repetitive spammy replies
    if text.lower().count("http") > 1:   # too many links
        return False
    if len(set(text.split())) < 5:       # very low word diversity
        return False

    return True
