from pydantic import BaseModel

from app.schemas.rule import RuleOut


class SearchResponse(BaseModel):
    query: str
    total: int
    items: list[RuleOut]


class HighlightsResponse(BaseModel):
    quick_prompts: list[str]
    popular_rules: list[RuleOut]
