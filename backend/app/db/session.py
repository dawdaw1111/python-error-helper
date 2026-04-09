from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.constants import DATABASE_URL
from app.core.seed_data import SEED_RULES
from app.db.base import Base
from app.models import ErrorRule


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db_and_seed() -> None:
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        has_rules = session.query(ErrorRule).first()
        if has_rules:
            return

        session.add_all([ErrorRule(**rule) for rule in SEED_RULES])
        session.commit()
