from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
import logging
from datetime import datetime, timezone

from config import get_settings
from models import AnalysisResponse, ErrorResponse, SessionInfo
from auth import verify_api_key, session_manager
from utils import RateLimiter, sanitize_sector_name
from services import AnalysisService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# Initialize services
analysis_service = None
rate_limiter = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    global analysis_service, rate_limiter
    
    # Startup
    logger.info("Starting Trade Opportunities API...")
    
    # Initialize rate limiter
    rate_limiter = RateLimiter(
        max_requests=settings.RATE_LIMIT_REQUESTS,
        time_window=settings.RATE_LIMIT_PERIOD
    )
    logger.info(f"Rate limiter initialized: {settings.RATE_LIMIT_REQUESTS} requests per {settings.RATE_LIMIT_PERIOD}s")
    
    # Initialize analysis service
    if not settings.GEMINI_API_KEY:
        logger.warning("Gemini API key not configured! Set GEMINI_API_KEY in .env file")
        analysis_service = None
    else:
        try:
            analysis_service = AnalysisService(settings.GEMINI_API_KEY)
            logger.info("Analysis service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize analysis service: {str(e)}")
            analysis_service = None
    
    logger.info("API is ready to accept requests!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Trade Opportunities API...")


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        routes=app.routes,
    )
    
    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key"
        }
    }
    
    # Apply security to all endpoints except health
    for path in openapi_schema["paths"]:
        if path != "/health":
            for method in openapi_schema["paths"][path]:
                openapi_schema["paths"][path][method]["security"] = [{"ApiKeyAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "detail": exc.detail,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "detail": "An internal server error occurred. Please try again later.",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )


# Health check endpoint (no auth required)
@app.get("/health", tags=["System"])
async def health_check():
    """
    Health check endpoint
    
    Returns the status of the API and its services
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": settings.APP_VERSION,
        "services": {
            "api": "operational",
            "analysis_service": "operational" if analysis_service else "not_configured",
            "rate_limiter": "operational" if rate_limiter else "not_configured"
        }
    }


# Session info endpoint
@app.get(
    "/api/v1/session",
    response_model=SessionInfo,
    tags=["Session"],
    summary="Get session information"
)
async def get_session_info(
    request: Request,
    session_id: str = Depends(verify_api_key)
):
    """
    Get information about your current session
    
    Returns:
    - Session ID
    - Requests made
    - Requests remaining
    - Rate limit reset time
    """
    # Get rate limit info
    rate_info = rate_limiter.get_session_info(session_id)
    
    # Get session info
    session_data = session_manager.get_session(session_id)
    
    return SessionInfo(
        session_id=session_id,
        requests_made=rate_info["requests_made"],
        requests_remaining=rate_info["requests_remaining"],
        reset_time=rate_info["reset_time"],
        created_at=session_data["created_at"] if session_data else datetime.now(timezone.utc)
    )


# Main analysis endpoint
@app.get(
    "/api/v1/analyze/{sector}",
    response_model=AnalysisResponse,
    tags=["Analysis"],
    summary="Analyze market sector",
    responses={
        200: {"description": "Successful analysis"},
        400: {"description": "Invalid sector name"},
        401: {"description": "Invalid API key"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Internal server error"}
    }
)
async def analyze_sector(
    sector: str,
    request: Request,
    session_id: str = Depends(verify_api_key)
):
    """
    Analyze a specific market sector in India
    
    This endpoint:
    1. Searches for current market data and news
    2. Uses AI to analyze the information
    3. Generates a comprehensive markdown report
    
    Parameters:
    - **sector**: Name of the sector (e.g., pharmaceuticals, technology, agriculture)
    
    Headers:
    - **X-API-Key**: Your API key for authentication
    
    Returns a structured market analysis report that can be saved as a .md file
    
    Examples:
    - /api/v1/analyze/pharmaceuticals
    - /api/v1/analyze/technology
    - /api/v1/analyze/agriculture
    """
    
    # Check rate limit
    is_allowed, requests_remaining, reset_time = rate_limiter.is_allowed(session_id)
    
    if not is_allowed:
        # Calculate seconds until reset
        seconds_until_reset = int((reset_time - datetime.now(timezone.utc)).total_seconds())
        
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Try again in {seconds_until_reset} seconds. "
                   f"Reset time: {reset_time.isoformat()}"
        )
    
    # Validate and sanitize sector name
    try:
        sector = sanitize_sector_name(sector)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    # Check if analysis service is available
    if not analysis_service:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Analysis service is not configured. Please set GEMINI_API_KEY in .env file."
        )
    
    # Perform analysis
    try:
        logger.info(f"Processing analysis request for sector: {sector}")
        
        result = analysis_service.analyze_sector(sector)
        
        return AnalysisResponse(
            status="success",
            sector=sector,
            timestamp=datetime.now(timezone.utc),
            report=result["report"],
            session_id=session_id,
            requests_remaining=requests_remaining,
            metadata=result.get("metadata")
        )
        
    except Exception as e:
        logger.error(f"Error analyzing sector {sector}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze sector: {str(e)}"
        )


# Root endpoint
@app.get("/", tags=["System"])
async def root():
    """
    API root endpoint
    
    Provides basic information about the API
    """
    return {
        "message": "Welcome to Trade Opportunities API",
        "version": settings.APP_VERSION,
        "documentation": "/docs",
        "health": "/health",
        "endpoints": {
            "analyze": "/api/v1/analyze/{sector}",
            "session": "/api/v1/session"
        },
        "note": "All endpoints except /health and / require X-API-Key header"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )

