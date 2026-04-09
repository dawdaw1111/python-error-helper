import re
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.models import ErrorRule, QueryLog, UnmatchedLog


ERROR_TYPE_REGEX = re.compile(r"([A-Za-z_]+(?:Error|Exception)):")


@dataclass
class MatchResult:
    rule: ErrorRule | None
    match_type: str
    confidence: float
    extracted_error_type: str | None


def extract_error_type(query_text: str) -> str | None:
    matches = ERROR_TYPE_REGEX.findall(query_text)
    return matches[-1] if matches else None


def _match_pattern(rule: ErrorRule, normalized_query: str) -> bool:
    if rule.pattern_type == "regex":
        return (
            re.search(rule.pattern_value, normalized_query, re.IGNORECASE | re.MULTILINE)
            is not None
        )
    if rule.pattern_type == "exact":
        return rule.pattern_value.casefold() == normalized_query.casefold().strip()
    return rule.pattern_value.casefold() in normalized_query.casefold()


def _candidate_groups(
    rules: list[ErrorRule], extracted_error_type: str | None
) -> list[tuple[str, list[ErrorRule]]]:
    if not extracted_error_type:
        return [("global", rules)]

    targeted = [rule for rule in rules if rule.error_type == extracted_error_type]
    others = [rule for rule in rules if rule.error_type != extracted_error_type]
    groups: list[tuple[str, list[ErrorRule]]] = []
    if targeted:
        groups.append(("error_type", targeted))
    if others:
        groups.append(("global", others))
    return groups


def find_best_rule(db: Session, query_text: str) -> MatchResult:
    normalized_query = query_text.strip()
    rules = db.query(ErrorRule).order_by(ErrorRule.id.asc()).all()
    extracted_error_type = extract_error_type(normalized_query)
    pattern_priority = [("regex", 0.96), ("exact", 0.88), ("contains", 0.79)]

    for group_name, candidates in _candidate_groups(rules, extracted_error_type):
        for pattern_type, confidence in pattern_priority:
            for rule in candidates:
                if rule.pattern_type != pattern_type:
                    continue
                if _match_pattern(rule, normalized_query):
                    if group_name == "global":
                        confidence -= 0.08
                    return MatchResult(
                        rule=rule,
                        match_type=f"{group_name}_{pattern_type}",
                        confidence=max(confidence, 0.55),
                        extracted_error_type=extracted_error_type,
                    )

    if extracted_error_type:
        generic_rule = (
            db.query(ErrorRule)
            .filter(ErrorRule.error_type == extracted_error_type)
            .order_by(ErrorRule.id.asc())
            .first()
        )
        if generic_rule:
            return MatchResult(
                rule=generic_rule,
                match_type="fallback_error_type",
                confidence=0.58,
                extracted_error_type=extracted_error_type,
            )

    return MatchResult(
        rule=None,
        match_type="fallback_generic",
        confidence=0.2,
        extracted_error_type=extracted_error_type,
    )


def analyze_query(db: Session, query_text: str) -> MatchResult:
    result = find_best_rule(db, query_text)
    db.add(
        QueryLog(
            query_text=query_text,
            matched_rule_id=result.rule.id if result.rule else None,
            is_matched=result.rule is not None,
        )
    )
    if result.rule is None:
        db.add(UnmatchedLog(query_text=query_text))
    db.commit()
    return result


def get_related_rules(db: Session, rule: ErrorRule | None, limit: int = 3) -> list[ErrorRule]:
    if rule is None:
        return db.query(ErrorRule).order_by(ErrorRule.id.asc()).limit(limit).all()

    related = (
        db.query(ErrorRule)
        .filter(ErrorRule.id != rule.id)
        .filter(ErrorRule.error_type == rule.error_type)
        .limit(limit)
        .all()
    )
    if len(related) >= limit:
        return related

    existing_ids = {item.id for item in related}
    existing_ids.add(rule.id)
    extras = (
        db.query(ErrorRule)
        .filter(~ErrorRule.id.in_(existing_ids))
        .order_by(ErrorRule.id.asc())
        .limit(limit - len(related))
        .all()
    )
    return [*related, *extras]
