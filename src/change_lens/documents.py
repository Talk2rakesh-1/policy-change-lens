import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Section:
    title: str
    content: str


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def split_sections(content: str) -> list[Section]:
    sections: list[Section] = []
    title = "Document"
    lines: list[str] = []
    for raw_line in content.replace("\r\n", "\n").split("\n"):
        line = raw_line.strip()
        if re.match(r"^#{1,6}\s+\S", line):
            if normalized := normalize(" ".join(lines)):
                sections.append(Section(title=title, content=normalized))
            title = re.sub(r"^#{1,6}\s+", "", line)
            lines = []
        else:
            lines.append(line)
    if normalized := normalize(" ".join(lines)):
        sections.append(Section(title=title, content=normalized))
    return sections or [Section(title="Document", content=normalize(content))]


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def similarity(left: str, right: str) -> float:
    left_tokens, right_tokens = tokens(left), tokens(right)
    union = left_tokens | right_tokens
    return len(left_tokens & right_tokens) / len(union) if union else 1.0


def excerpt(text: str, limit: int = 300) -> str:
    clean = normalize(text)
    return clean if len(clean) <= limit else clean[: limit - 1].rstrip() + "…"
