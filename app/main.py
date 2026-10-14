import logging
import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.engine = create_async_engine(
        os.environ["DATABASE_URL"],
        pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
        max_overflow=0,
        pool_timeout=2,
        connect_args={"server_settings": {"statement_timeout": "3000"}},
    )
    try:
        yield
    finally:
        await app.state.engine.dispose()

app = FastAPI(title="Distributed Booking Lab — Stage 1", lifespan=lifespan)

@app.middleware("http")
async def timing(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Response-Time-Ms"] = f"{(time.perf_counter() - started) * 1000:.2f}"
    return response

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/ready")
async def ready(request: Request):
    try:
        async with request.app.state.engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:
        logger.exception("Database readiness failed")
        raise HTTPException(503, "Database unavailable")
    return {"status": "ready"}

@app.get("/events/{event_id}")
async def event(event_id: int, request: Request):
    async with request.app.state.engine.connect() as conn:
        result = await conn.execute(
            text("SELECT id, name, total_tickets, available_tickets FROM events WHERE id = :id"),
            {"id": event_id},
        )
        row = result.mappings().first()
    if row is None:
        raise HTTPException(404, "Event not found")
    return dict(row)
