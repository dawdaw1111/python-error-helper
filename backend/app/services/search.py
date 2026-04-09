from sqlalchemy.orm import Session

from app.models import ErrorRule


def _score_rule(rule: ErrorRule, query: str) -> int:
    target = query.casefold()
    score = 0
    if target in rule.title.casefold():
        score += 5
    if target in rule.error_type.casefold():
        score += 4
    if target in rule.explanation.casefold():
        score += 2
    if any(target in tag.casefold() for tag in rule.tags):
        score += 3
    if any(target in term.casefold() for term in rule.search_terms):
        score += 4
    return score


def search_rules(db: Session, query: str) -> list[ErrorRule]:
    rules = db.query(ErrorRule).order_by(ErrorRule.id.asc()).all()
    normalized_query = query.strip()
    if not normalized_query:
        return rules[:6]

    scored = [(rule, _score_rule(rule, normalized_query)) for rule in rules]
    matched = [item for item in scored if item[1] > 0]
    matched.sort(key=lambda item: (-item[1], item[0].id))
    return [rule for rule, _ in matched]
