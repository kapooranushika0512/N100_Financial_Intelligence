import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import (
    companies,
    documents,
    health,
    market_cap,
    peers,
    portfolio,
    screener,
    sectors,
    valuation,
)

APP_START_TIME = time.time()

app = FastAPI(
    title="Financial Intelligence API",
    description="REST API for the N100 Financial Intelligence Dashboard",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request, call_next):
    """Log incoming HTTP request method, path, and execution time."""

    start = time.time()

    response = await call_next(request)

    elapsed = round(time.time() - start, 4)

    print(f"[{request.method}] {request.url.path} {elapsed}s")

    return response


app.include_router(
    health.router,
    prefix="/api/v1",
)

app.include_router(
    companies.router,
    prefix="/api/v1",
)

app.include_router(
    screener.router,
    prefix="/api/v1",
)

app.include_router(
    sectors.router,
    prefix="/api/v1",
)

app.include_router(
    peers.router,
    prefix="/api/v1",
)

app.include_router(
    valuation.router,
    prefix="/api/v1",
)

app.include_router(
    market_cap.router,
    prefix="/api/v1",
)

app.include_router(
    portfolio.router,
    prefix="/api/v1",
)

app.include_router(
    documents.router,
    prefix="/api/v1",
)


@app.get("/", tags=["Root"])
def root():
    """Return welcome message, API version, and documentation links."""

    return {
        "message": "Financial Intelligence API Running",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health",
    }
