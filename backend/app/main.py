from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.admin import router as admin_router
from app.api.routes.public import router as public_router
from app.db.session import create_db_and_seed
from app.core.settings import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_seed()
    yield


app = FastAPI(
    title="PyErr API",
    description="Python 报错速查 MVP 后端服务",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(public_router, prefix="/api")
app.include_router(admin_router, prefix="/api/admin")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
