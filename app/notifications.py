"""Importar librerias"""
import httpx
from .models import Issue
import os

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")


async def send_discord_notification(issue: Issue) -> None:
    """Envía una notificacio2n a un canal de Discord"""
    if not DISCORD_WEBHOOK_URL:
        print("Discord webhook no configurado. Saltando notificación.")
        return

    content = (
        f"NUEVO issue creado en Github:\n"
        f"**{issue.title}**\n"
        f"📎 {issue.url}\n"
        f"📁 Estado: {issue.state}"
    )

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                DISCORD_WEBHOOK_URL,
                json={"content": content},
                timeout=10
            )
            response.raise_for_status()
            print("Notificación enviada a Discord")
        except Exception as e:
            print(f"Error al enviar notificación a Discord: {e}")
