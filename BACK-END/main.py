"""
🚀 MAIN APPLICATION - LAW FIRM BACKEND
FastAPI application with CORS and route integration
"""

import logging
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

# Import routes
from services.routes.conversation import router as conversation_router
from services.routes.whatsapp import router as whatsapp_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("🚀 Starting Law Firm Backend Application")
    
    # Startup
    try:
        # Initialize services
        from services.orchestration import intelligent_orchestrator
        from services.baileys_service import baileys_service
        
        # Initialize orchestrator
        logger.info("🔧 Initializing intelligent orchestrator...")
        
        # Initialize WhatsApp service
        logger.info("📱 Initializing WhatsApp service...")
        await baileys_service.initialize()
        
        logger.info("✅ All services initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Error during startup: {str(e)}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Law Firm Backend Application")
    try:
        await baileys_service.cleanup()
        logger.info("✅ Cleanup completed")
    except Exception as e:
        logger.error(f"❌ Error during shutdown: {str(e)}")

# Create FastAPI app
app = FastAPI(
    title="Law Firm Backend API",
    description="Backend API for m.lima Law Firm with WhatsApp integration",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://*.replit.dev",
        "https://*.repl.co",
        "*"  # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(conversation_router, prefix="/api/v1", tags=["conversation"])
app.include_router(whatsapp_router, prefix="/api/v1", tags=["whatsapp"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Law Firm Backend API",
        "status": "active",
        "version": "1.0.0",
        "endpoints": {
            "conversation": "/api/v1/conversation/*",
            "whatsapp": "/api/v1/whatsapp/*",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        from services.orchestration import intelligent_orchestrator
        
        # Get service status
        service_status = await intelligent_orchestrator.get_overall_service_status()
        
        return {
            "status": "healthy",
            "service": "law_firm_backend",
            "version": "1.0.0",
            "services": service_status,
            "endpoints_active": True
        }
    except Exception as e:
        logger.error(f"❌ Health check error: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "service": "law_firm_backend",
                "error": str(e)
            }
        )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"❌ Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "path": str(request.url)
        }
    )

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"🚀 Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )