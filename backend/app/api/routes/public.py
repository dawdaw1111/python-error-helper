from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import create_access_token, require_admin, verify_admin_credentials
from app.core.settings import settings
from app.db.session import get_db
from app.models import FeedbackLog
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.schemas.auth import AdminProfile, AuthResponse, LoginRequest
from app.schemas.feedback import FeedbackRequest, FeedbackResponse
from app.schemas.search import HighlightsResponse, SearchResponse
from app.services.matcher import analyze_query, get_related_rules
from app.services.search import search_rules


router = APIRouter(tags=["public"])


@router.post("/auth/login", response_model=AuthResponse)
def login(payload: LoginRequest) -> AuthResponse:
    if not verify_admin_credentials(payload.username, payload.password):
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )

    return AuthResponse(
        access_token=create_access_token(payload.username),
        username=payload.username,
        expires_in=settings.token_expire_seconds,
    )


@router.get("/auth/me", response_model=AdminProfile)
def get_current_admin(_: dict = Depends(require_admin)) -> AdminProfile:
    return AdminProfile(username=settings.admin_username)


@router.get("/highlights", response_model=HighlightsResponse)
def get_highlights(db: Session = Depends(get_db)) -> HighlightsResponse:
    popular_rules = search_rules(db, "")
    return HighlightsResponse(
        quick_prompts=[
            "模块找不到",
            "缩进错误",
            "类型报错",
            "Key 不存在",
        ],
        popular_rules=popular_rules,
    )


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest, db: Session = Depends(get_db)) -> AnalyzeResponse:
    result = analyze_query(db, payload.query_text)
    related_rules = get_related_rules(db, result.rule)
    summary = (
        f"已命中 {result.rule.title}，建议按排查步骤逐项检查。"
        if result.rule
        else "暂未命中规则，建议检查完整 traceback、关键报错行和运行环境。"
    )

    return AnalyzeResponse(
        query_text=payload.query_text,
        extracted_error_type=result.extracted_error_type,
        matched=result.rule is not None,
        match_type=result.match_type,
        confidence=result.confidence,
        summary=summary,
        rule=result.rule,
        related_rules=related_rules,
    )


@router.get("/search", response_model=SearchResponse)
def search(q: str = "", db: Session = Depends(get_db)) -> SearchResponse:
    items = search_rules(db, q)
    return SearchResponse(query=q, total=len(items), items=items)


@router.post("/feedback", response_model=FeedbackResponse)
def submit_feedback(
    payload: FeedbackRequest, db: Session = Depends(get_db)
) -> FeedbackResponse:
    db.add(
        FeedbackLog(
            rule_id=payload.rule_id,
            feedback_type=payload.feedback_type,
            reason=payload.reason,
        )
    )
    db.commit()
    return FeedbackResponse(success=True, message="反馈已记录，感谢你的帮助。")
