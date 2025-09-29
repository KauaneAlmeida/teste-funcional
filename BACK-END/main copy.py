from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
import os
import asyncio
from dotenv import load_dotenv

# Import routes
from app.routes.test import router as test_router
from app.routes.chat import router as chat_router
from app.routes.conversation import router as conversation_router
from app.routes.whatsapp import router as whatsapp_router
from app.routes.leads import router as leads_router

# Import services for startup
from app.services.firebase_service import initialize_firebase
from app.services.baileys_service import baileys_service

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI instance
app = FastAPI(
    title="Law Firm AI Chat Backend",
    description="Production-ready FastAPI backend for law firm client intake with WhatsApp integration",
    version="2.0.0"
)

# -------------------------
# CORS Configuration
# -------------------------
allowed_origins = [
    "https://projectlawyer.netlify.app",
    "https://68cdc61---projectlawyer.netlify.app",
    "https://*.netlify.app",
    "https://law-firm-backend-936902782519.us-central1.run.app",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8080",
    "http://localhost:8000",
]

def is_origin_allowed(origin: str) -> bool:
    if not origin:
        return False
    if origin in allowed_origins:
        return True
    if origin.startswith("http://localhost:") or origin.startswith("http://127.0.0.1:"):
        return True
    if ".netlify.app" in origin and origin.startswith("https://"):
        return True
    return False

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    if request.method == "OPTIONS":
        origin = request.headers.get("origin")
        headers = {
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Expose-Headers": "*",
            "Access-Control-Max-Age": "3600",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Origin": origin if is_origin_allowed(origin) else "*",
        }
        from fastapi.responses import Response
        return Response(status_code=200, headers=headers)
    
    response = await call_next(request)
    origin = request.headers.get("origin")
    response.headers["Access-Control-Allow-Origin"] = origin if is_origin_allowed(origin) else "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

# -------------------------
# Include routers
# -------------------------
app.include_router(test_router, prefix="/api/v1", tags=["Test"])
app.include_router(chat_router, prefix="/api/v1", tags=["Chat"])
app.include_router(conversation_router, prefix="/api/v1", tags=["Conversation"])
app.include_router(whatsapp_router, prefix="/api/v1", tags=["WhatsApp"])
app.include_router(leads_router, prefix="/api/v1", tags=["Leads"])

# -------------------------
# Startup & Shutdown Events
# -------------------------
@app.on_event("startup")
async def startup_event():
    port = os.environ.get("PORT", "8080")
    logger.info(f"🚀 Starting FastAPI application on port {port}...")
    
    try:
        # Inicializar apenas Firebase no startup (rápido)
        initialize_firebase()
        logger.info("✅ Firebase initialized successfully")
        
        # ✅ CRITICAL: Confirmar que servidor está pronto IMEDIATAMENTE
        logger.info(f"✅ FastAPI READY - listening on 0.0.0.0:{port}")
        
        # Inicializar Baileys em background (não bloqueia startup)
        asyncio.create_task(initialize_baileys_background())
        
    except Exception as e:
        logger.error(f"❌ Critical startup error: {str(e)}")
        # Não fazer raise - permitir que FastAPI continue rodando

async def initialize_baileys_background():
    """Inicializa Baileys em background sem bloquear startup"""
    try:
        await asyncio.sleep(10)  # Free tier precisa de mais tempo
        logger.info("🔌 Initializing Baileys WhatsApp service in background...")
        await baileys_service.initialize()
        logger.info("✅ Baileys WhatsApp service initialized")
    except Exception as e:
        logger.error(f"❌ Baileys initialization failed (non-critical): {str(e)}")
        # No free tier, não tente reconectar automaticamente

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("📴 Shutting down FastAPI application...")
    try:
        await baileys_service.cleanup()
        logger.info("✅ Services cleaned up")
    except Exception as e:
        logger.warning(f"⚠️ Cleanup warning: {str(e)}")

# -------------------------
# ✅ HEALTH CHECK SIMPLIFICADO - RESPOSTA IMEDIATA
# -------------------------
@app.get("/health")
@app.head("/health")
async def health_check():
    """Health check que responde IMEDIATAMENTE - crítico para Cloud Run"""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "message": "FastAPI is running",
            "port": os.environ.get("PORT", "8080"),
            "service": "law-firm-backend"
        }
    )

# -------------------------
# Status Detalhado (sem timeout)
# -------------------------
@app.get("/api/v1/status")
async def detailed_status():
    """Status detalhado dos serviços - pode demorar mais"""
    try:
        from app.services.orchestration_service import intelligent_orchestrator
        
        # Usar timeout para evitar travamento
        try:
            service_status = await asyncio.wait_for(
                intelligent_orchestrator.get_overall_service_status(),
                timeout=3.0
            )
        except asyncio.TimeoutError:
            service_status = {"overall_status": "timeout"}
        
        try:
            whatsapp_status = await asyncio.wait_for(
                baileys_service.get_connection_status(),
                timeout=2.0
            )
        except asyncio.TimeoutError:
            whatsapp_status = {"status": "timeout"}

        return {
            "overall_status": service_status.get("overall_status", "unknown"),
            "services": {
                "fastapi": "active",
                "whatsapp_bot": whatsapp_status,
                "firebase": service_status.get("firebase_status", {}).get("status", "unknown"),
                "gemini_ai": service_status.get("ai_status", {}).get("status", "unknown")
            },
            "features": [
                "guided_conversation_flow",
                "whatsapp_integration",
                "lead_management",
                "session_persistence"
            ],
            "port": os.environ.get("PORT", "8080")
        }
    except Exception as e:
        logger.error(f"Status check error: {str(e)}")
        return JSONResponse(
            status_code=200,  # Não retornar 500 - apenas status degradado
            content={
                "overall_status": "degraded",
                "services": {"fastapi": "active"},
                "error": str(e)
            }
        )

# -------------------------
# Exception Handlers
# -------------------------
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        },
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "message": "Validation error",
            "details": exc.errors(),
        },
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error"
        },
    )

# -------------------------
# Root Endpoint
# -------------------------
@app.get("/")
async def root():
    return {
        "message": "Law Firm AI Chat Backend API",
        "version": "2.0.0",
        "status": "running",
        "port": os.environ.get("PORT", "8080"),
        "docs_url": "/docs",
        "health_check": "/health",
        "endpoints": {
            "conversation_start": "/api/v1/conversation/start",
            "conversation_respond": "/api/v1/conversation/respond",
            "chat": "/api/v1/chat",
            "whatsapp_status": "/api/v1/whatsapp/status"
        }
    }

# -------------------------
# ✅ CRITICAL: Inicialização para Cloud Run
# -------------------------
if __name__ == "__main__":
    import uvicorn
    
    # Cloud Run injeta a variável PORT
    port = int(os.environ.get("PORT", 8080))
    
    logger.info(f"🚀 Starting server on 0.0.0.0:{port}")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        access_log=True,
        timeout_keep_alive=300,
        limit_concurrency=100
    )