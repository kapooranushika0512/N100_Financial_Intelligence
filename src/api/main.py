from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

from src.api.routers import (
    health,
    companies,
    screener,
    sectors,
    peers,
    valuation,
    market_cap,
    portfolio,
    documents,
)

APP_START_TIME = time.time()

app = FastAPI(
    title="Financial Intelligence API",
    description="REST API for the N100 Financial Intelligence Dashboard",
    version="1.0.0",
)

# ---------------------------------------------------
# CORS
# ---------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# REQUEST LOGGING
# ---------------------------------------------------

@app.middleware("http")
async def log_requests(request, call_next):

    start = time.time()

    response = await call_next(request)

    elapsed = round(time.time() - start, 4)

    print(f"[{request.method}] {request.url.path} {elapsed}s")

    return response


# ---------------------------------------------------
# API ROUTERS
# ---------------------------------------------------

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

# ---------------------------------------------------
# ROOT
# ---------------------------------------------------

@app.get("/", tags=["Root"])
def root():

    return {
        "message": "Financial Intelligence API Running",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health",
    }