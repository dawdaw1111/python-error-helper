from pydantic import BaseModel

from app.schemas.rule import RuleOut


class TopRule(BaseModel):
    rule_id: int
    title: str
    hits: int


class AdminStats(BaseModel):
    total_queries: int
    matched_queries: int
    unmatched_queries: int
    matched_rate: float
    total_feedback: int
    helpful_feedback: int
    helpful_rate: float
    top_rules: list[TopRule]


class RuleListResponse(BaseModel):
    items: list[RuleOut]
