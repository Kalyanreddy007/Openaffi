"""
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from app.config import settings
from app.database import init_db
from app.routers import auth, companies, contacts, leads

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="AI-powered B2B Intelligence and Decision-Maker Discovery Platform",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "environment": settings.environment
    }


# Root endpoint
@app.get("/", tags=["Root"])
def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "AI-powered B2B Intelligence and Decision-Maker Discovery Platform",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json"
    }


# Include routers
app.include_router(auth.router)
app.include_router(companies.router)
app.include_router(contacts.router)
app.include_router(leads.router)


# Startup event
@app.on_event("startup")
def startup_event():
    """Initialize database on startup."""
    logger.info("Starting up OpenAffi application")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


# Shutdown event
@app.on_event("shutdown")
def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down OpenAffi application")


# Exception handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )
