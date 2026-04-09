from datetime import datetime

from pydantic import BaseModel, Field


class RuleBase(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    error_type: str = Field(min_length=3, max_length=80)
    pattern_type: str = Field(pattern="^(regex|exact|contains)$")
    pattern_value: str = Field(min_length=2, max_length=255)
    example_query: str = Field(min_length=3, max_length=500)
    explanation: str = Field(min_length=10, max_length=2000)
    common_causes: list[str]
    troubleshooting_steps: list[str]
    solutions: list[str]
    tags: list[str]
    search_terms: list[str] = Field(default_factory=list)


class RuleCreate(RuleBase):
    pass


class RuleUpdate(RuleBase):
    pass


class RuleOut(RuleBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
