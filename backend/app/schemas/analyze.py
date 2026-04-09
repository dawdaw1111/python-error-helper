from pydantic import BaseModel, Field

from app.schemas.rule import RuleOut


class AnalyzeRequest(BaseModel):
    query_text: str = Field(min_length=3, max_length=5000)


class AnalyzeResponse(BaseModel):
    query_text: str
    extracted_error_type: str | None
    matched: bool
    match_type: str
    confidence: float
    summary: str
    rule: RuleOut | None
    related_rules: list[RuleOut]
