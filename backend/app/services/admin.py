from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import ErrorRule, FeedbackLog, QueryLog, UnmatchedLog


def build_admin_stats(db: Session) -> dict:
    total_queries = db.query(func.count(QueryLog.id)).scalar() or 0
    matched_queries = (
        db.query(func.count(QueryLog.id)).filter(QueryLog.is_matched.is_(True)).scalar() or 0
    )
    unmatched_queries = db.query(func.count(UnmatchedLog.id)).scalar() or 0
    total_feedback = db.query(func.count(FeedbackLog.id)).scalar() or 0
    helpful_feedback = (
        db.query(func.count(FeedbackLog.id))
        .filter(FeedbackLog.feedback_type == "helpful")
        .scalar()
        or 0
    )

    top_rows = (
        db.query(
            QueryLog.matched_rule_id,
            ErrorRule.title,
            func.count(QueryLog.id).label("hits"),
        )
        .join(ErrorRule, ErrorRule.id == QueryLog.matched_rule_id)
        .group_by(QueryLog.matched_rule_id, ErrorRule.title)
        .order_by(func.count(QueryLog.id).desc(), QueryLog.matched_rule_id.asc())
        .limit(5)
        .all()
    )

    return {
        "total_queries": total_queries,
        "matched_queries": matched_queries,
        "unmatched_queries": unmatched_queries,
        "matched_rate": round((matched_queries / total_queries) if total_queries else 0, 3),
        "total_feedback": total_feedback,
        "helpful_feedback": helpful_feedback,
        "helpful_rate": round((helpful_feedback / total_feedback) if total_feedback else 0, 3),
        "top_rules": [
            {"rule_id": row.matched_rule_id, "title": row.title, "hits": row.hits}
            for row in top_rows
        ],
    }
