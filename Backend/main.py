"""
FastAPI Main Application

PolyDeal Growth Curve Prediction System
"""

from pathlib import Path
import os

from dotenv import load_dotenv

# Load .env from Backend, project root, and Frontend (GNEWS_API_KEY)
load_dotenv(Path(__file__).parent / ".env")
load_dotenv(Path(__file__).parent.parent / ".env")
load_dotenv(Path(__file__).parent.parent / "Frontend" / ".env")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager

from routes import analytics, companies, dashboard, news

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting PolyDeal API...")
    # Initialize services here if needed
    yield
    logger.info("Shutting down PolyDeal API...")


# Create FastAPI app
app = FastAPI(
    title="PolyDeal API",
    description="Growth Curve Prediction and Analytics API",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
# Configure CORS
allowed_origins_env = os.environ.get("ALLOWED_ORIGINS")
if allowed_origins_env:
    # allow comma-separated values in ALLOWED_ORIGINS
    allowed_origins = [o.strip() for o in allowed_origins_env.split(",") if o.strip()]
else:
    allowed_origins = ["*"]  # fallback permissive for development

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(companies.router, prefix="/api/companies", tags=["Companies"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(news.router, prefix="/api/news", tags=["News"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "PolyDeal Growth Curve Prediction API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "polydeal-api"
    }


if __name__ == "__main__":
    import uvicorn
    # Support environment-provided PORT (Render, Heroku, etc.)
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
