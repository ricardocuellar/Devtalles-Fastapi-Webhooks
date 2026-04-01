"""Importar librerias"""
from datetime import datetime
import hmac
import hashlib
import os

from fastapi import APIRouter, Header, HTTPException, Request, Depends
from sqlmodel import Session, select
from app.db import get_session
from app.notifications import send_discord_notification
from .models import Issue

router = APIRouter()

GITHUB_SECRET = os.getenv("GITHUB_SECRET", "secretosuper123")


def verify_signature(body: bytes, signature_header: str | None) -> bool:
    """Verificar que la firma sea valida"""
    if not signature_header:
        return False

    try:
        sha_name, signature = signature_header.split(
            "=")  # sha256=firmitahexadecimal
    except ValueError:
        return False

    if sha_name != "sha256":
        return False

    mac = hmac.new(
        GITHUB_SECRET.encode("utf-8"),
        msg=body,
        digestmod=hashlib.sha256,
    )

    expected = mac.hexdigest()

    return hmac.compare_digest(expected, signature)


@router.post("/webhooks/github")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str | None = Header(default=None),
    x_github_event: str | None = Header(default=None),
    session: Session = Depends(get_session)
):
    """Endpoint que recibe los webhooks de Github"""
    body = await request.body()

    if not verify_signature(body, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Firma inválida")

    payload = await request.json()

    if x_github_event == "issues" and payload.get("action") == "opened":
        issue_data = payload["issue"]
        created_at_str = issue_data["created_at"]  # "2026-01-20T10:00:00Z"
        created_at = datetime.fromisoformat(
            created_at_str.replace("Z", "+00:00")
        )

        issue = Issue(
            github_issue_id=issue_data["id"],
            title=issue_data["title"],
            url=issue_data["html_url"],
            state=issue_data["state"],
            created_at=created_at
        )

        session.add(issue)
        session.commit()
        session.refresh(issue)

        print(f"NUEVO issue guardado: {issue.title} - {issue.url}")

        await send_discord_notification(issue)

    return {"status": "ok"}


@router.get("/issues", response_model=list[Issue])
def list_issues(session: Session = Depends(get_session)):
    """Devuelve el listado de issues guardados"""
    query = select(Issue)
    return session.exec(query).all()
