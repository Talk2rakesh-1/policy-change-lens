from enum import StrEnum

from pydantic import BaseModel, Field, field_validator


class ChangeKind(StrEnum):
    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"


class DocumentInput(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    content: str = Field(min_length=1, max_length=500_000)

    @field_validator("content")
    @classmethod
    def reject_null_bytes(cls, value: str) -> str:
        if "\x00" in value:
            raise ValueError("content cannot contain null bytes")
        return value


class CompareRequest(BaseModel):
    before: DocumentInput
    after: DocumentInput
    similarity_threshold: float = Field(default=0.35, ge=0.0, le=1.0)


class Evidence(BaseModel):
    document: str
    section: str
    quote: str = Field(max_length=500)


class ChangeFinding(BaseModel):
    kind: ChangeKind
    section: str
    summary: str
    similarity: float = Field(ge=0.0, le=1.0)
    evidence: list[Evidence]


class Evaluation(BaseModel):
    findings: int
    findings_with_evidence: int
    citation_coverage: float = Field(ge=0.0, le=1.0)


class CompareResponse(BaseModel):
    request_id: str
    findings: list[ChangeFinding]
    evaluation: Evaluation
    warnings: list[str]


class QueryRequest(BaseModel):
    document: DocumentInput
    query: str = Field(min_length=1, max_length=1_000)
    limit: int = Field(default=3, ge=1, le=10)


class SearchHit(BaseModel):
    section: str
    score: float
    quote: str
