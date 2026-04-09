from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import require_admin
from app.db.session import get_db
from app.models import ErrorRule
from app.schemas.admin import AdminStats, RuleListResponse
from app.schemas.rule import RuleCreate, RuleOut, RuleUpdate
from app.services.admin import build_admin_stats


router = APIRouter(tags=["admin"], dependencies=[Depends(require_admin)])


def _apply_rule_payload(rule: ErrorRule, payload: RuleCreate | RuleUpdate) -> ErrorRule:
    rule.title = payload.title
    rule.error_type = payload.error_type
    rule.pattern_type = payload.pattern_type
    rule.pattern_value = payload.pattern_value
    rule.example_query = payload.example_query
    rule.explanation = payload.explanation
    rule.common_causes = payload.common_causes
    rule.troubleshooting_steps = payload.troubleshooting_steps
    rule.solutions = payload.solutions
    rule.tags = payload.tags
    rule.search_terms = payload.search_terms
    return rule


@router.get("/rules", response_model=RuleListResponse)
def list_rules(db: Session = Depends(get_db)) -> RuleListResponse:
    items = db.query(ErrorRule).order_by(ErrorRule.id.asc()).all()
    return RuleListResponse(items=items)


@router.post("/rules", response_model=RuleOut, status_code=status.HTTP_201_CREATED)
def create_rule(payload: RuleCreate, db: Session = Depends(get_db)) -> RuleOut:
    rule = _apply_rule_payload(ErrorRule(), payload)
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


@router.put("/rules/{rule_id}", response_model=RuleOut)
def update_rule(
    rule_id: int, payload: RuleUpdate, db: Session = Depends(get_db)
) -> RuleOut:
    rule = db.get(ErrorRule, rule_id)
    if rule is None:
        raise HTTPException(status_code=404, detail="规则不存在")

    rule = _apply_rule_payload(rule, payload)
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


@router.delete("/rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rule(rule_id: int, db: Session = Depends(get_db)) -> None:
    rule = db.get(ErrorRule, rule_id)
    if rule is None:
        raise HTTPException(status_code=404, detail="规则不存在")

    db.delete(rule)
    db.commit()


@router.get("/stats", response_model=AdminStats)
def get_admin_stats(db: Session = Depends(get_db)) -> AdminStats:
    return AdminStats(**build_admin_stats(db))
