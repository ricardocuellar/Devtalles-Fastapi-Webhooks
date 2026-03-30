"""Fastapi library"""
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./issues.db"

engine = create_engine(DATABASE_URL, echo=True)


def init_db() -> None:
    """Init DB, crea todas las tablas"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependencia para obtener una sesión de base de datos."""
    with Session(engine) as session:
        yield session
