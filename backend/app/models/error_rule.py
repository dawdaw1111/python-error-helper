from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ErrorRule(Base):
    __tablename__ = "error_rules"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    error_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    pattern_type: Mapped[str] = mapped_column(String(20), nullable=False)
    pattern_value: Mapped[str] = mapped_column(String(255), nullable=False)
    example_query: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    common_causes: Mapped[list[str]] = mapped_column(JSON, default=list)
    troubleshooting_steps: Mapped[list[str]] = mapped_column(JSON, default=list)
    solutions: Mapped[list[str]] = mapped_column(JSON, default=list)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    search_terms: Mapped[list[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
