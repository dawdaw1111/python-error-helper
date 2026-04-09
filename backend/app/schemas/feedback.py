from pydantic import BaseModel, Field


class FeedbackRequest(BaseModel):
    rule_id: int
    feedback_type: str = Field(pattern="^(helpful|not_helpful)$")
    reason: str | None = Field(default=None, max_length=500)


class FeedbackResponse(BaseModel):
    success: bool
    message: str
