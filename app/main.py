"""Importar librerias"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .github_webhook import router as github_router

from app.db import init_db
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ciclo de vida de la aplicación"""
    # Startup
    init_db()
    yield
    # Shutdown

app = FastAPI(lifespan=lifespan, title="Webhooks")

app.include_router(github_router)
