import re

SUSPICIOUS_PATTERNS = (
    r"ignore (all |any )?(previous|prior) instructions",
    r"system prompt",
    r"developer message",
    r"reveal (your |the )?(secret|token|credentials)",
)


def document_warnings(*documents: str) -> list[str]:
    warnings: list[str] = []
    for index, content in enumerate(documents, start=1):
        if any(re.search(pattern, content, re.IGNORECASE) for pattern in SUSPICIOUS_PATTERNS):
            warnings.append(
                f"Document {index} contains instruction-like text; it was treated as data only."
            )
    return warnings
