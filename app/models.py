"""Librerias de SQLModel"""
from datetime import datetime

from sqlmodel import SQLModel, Field


class Issue(SQLModel, table=True):
    """Modelo para issue de Github"""
    id: int | None = Field(default=None, primary_key=True)
    github_issue_id: int
    title: str
    url: str
    state: str
    created_at: datetime
