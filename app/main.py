from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.routes import document
from app.db.mongodb import close_mongo_connection, connect_to_mongo, ping_mongo
from app.core.logging import setup_logging

# Initialize centralized logging
setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    try:
        yield
    finally:
        await close_mongo_connection()


app = FastAPI(
    title="Document Intelligence Platform API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(document.router, prefix="/api/v1/documents", tags=["documents"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "mongodb": "ok" if await ping_mongo() else "unavailable"}
