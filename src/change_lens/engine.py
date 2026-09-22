from uuid import uuid4

from change_lens.documents import Section, excerpt, similarity, split_sections
from change_lens.guardrails import document_warnings
from change_lens.models import (
    ChangeFinding,
    ChangeKind,
    CompareRequest,
    CompareResponse,
    Evaluation,
    Evidence,
    SearchHit,
)


def compare_documents(request: CompareRequest) -> CompareResponse:
    before = split_sections(request.before.content)
    after = split_sections(request.after.content)
    findings: list[ChangeFinding] = []
    unmatched_after = set(range(len(after)))

    for old in before:
        match_index, score = _best_match(old, after, unmatched_after)
        if match_index is None or score < request.similarity_threshold:
            findings.append(_finding(ChangeKind.REMOVED, old.title, 0.0, request.before.name, old))
            continue
        new = after[match_index]
        unmatched_after.remove(match_index)
        if old.content != new.content or old.title != new.title:
            findings.append(
                ChangeFinding(
                    kind=ChangeKind.MODIFIED,
                    section=new.title,
                    summary=f"Content changed from '{old.title}' to '{new.title}'.",
                    similarity=round(score, 3),
                    evidence=[
                        Evidence(
                            document=request.before.name,
                            section=old.title,
                            quote=excerpt(old.content),
                        ),
                        Evidence(
                            document=request.after.name,
                            section=new.title,
                            quote=excerpt(new.content),
                        ),
                    ],
                )
            )

    for index in sorted(unmatched_after):
        new = after[index]
        findings.append(_finding(ChangeKind.ADDED, new.title, 0.0, request.after.name, new))

    cited = sum(bool(finding.evidence) for finding in findings)
    coverage = cited / len(findings) if findings else 1.0
    return CompareResponse(
        request_id=str(uuid4()),
        findings=findings,
        evaluation=Evaluation(
            findings=len(findings),
            findings_with_evidence=cited,
            citation_coverage=coverage,
        ),
        warnings=document_warnings(request.before.content, request.after.content),
    )


def search_document(content: str, query: str, limit: int) -> list[SearchHit]:
    ranked = sorted(
        (
            SearchHit(
                section=section.title,
                score=round(similarity(query, section.content), 3),
                quote=excerpt(section.content),
            )
            for section in split_sections(content)
        ),
        key=lambda hit: hit.score,
        reverse=True,
    )
    return [hit for hit in ranked if hit.score > 0][:limit]


def _best_match(
    source: Section, candidates: list[Section], available: set[int]
) -> tuple[int | None, float]:
    scored = [
        (index, max(similarity(source.title, item.title), similarity(source.content, item.content)))
        for index, item in enumerate(candidates)
        if index in available
    ]
    return max(scored, key=lambda pair: pair[1], default=(None, 0.0))


def _finding(
    kind: ChangeKind, section: str, score: float, document: str, source: Section
) -> ChangeFinding:
    return ChangeFinding(
        kind=kind,
        section=section,
        summary=f"Section '{section}' was {kind.value}.",
        similarity=score,
        evidence=[Evidence(document=document, section=section, quote=excerpt(source.content))],
    )
