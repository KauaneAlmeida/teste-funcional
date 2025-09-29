"""
🚀 MAIN APPLICATION - LAW FIRM BACKEND
FastAPI application with CORS and route integration
Baseado na estrutura original do projeto m.lima
"""

import logging
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

# Import routes - usando a estrutura original do projeto
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
    logger.info("🚀 Starting m.lima Law Firm Backend Application")
    
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
    logger.info("🛑 Shutting down m.lima Law Firm Backend Application")
    try:
        await baileys_service.cleanup()
        logger.info("✅ Cleanup completed")
    except Exception as e:
        logger.error(f"❌ Error during shutdown: {str(e)}")

# Create FastAPI app - mantendo estrutura original
app = FastAPI(
    title="m.lima Advogados Backend API",
    description="Backend API para escritório m.lima com integração WhatsApp",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration - adequado para o projeto
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://*.replit.dev",
        "https://*.repl.co",
        "https://projectlawyer.netlify.app",
        "https://*.netlify.app",
        "*"  # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers - mantendo estrutura original
app.include_router(conversation_router, prefix="/api/v1", tags=["conversation"])
app.include_router(whatsapp_router, prefix="/api/v1", tags=["whatsapp"])

@app.get("/")
async def root():
    """Root endpoint - informações do projeto m.lima"""
    return {
        "service": "m.lima Advogados Backend API",
        "status": "active",
        "version": "1.0.0",
        "description": "Sistema de atendimento inteligente para escritório de advocacia",
        "areas_atendimento": [
            "Direito Penal",
            "Direito da Saúde"
        ],
        "endpoints": {
            "conversation": "/api/v1/conversation/*",
            "whatsapp": "/api/v1/whatsapp/*",
            "health": "/health",
            "docs": "/docs"
        },
        "features": [
            "Chat inteligente para captação de leads",
            "Integração WhatsApp via Baileys",
            "Fluxo conversacional estruturado",
            "Notificação automática de advogados",
            "Qualificação inteligente de leads"
        ]
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
            "service": "m.lima_law_firm_backend",
            "version": "1.0.0",
            "services": service_status,
            "endpoints_active": True,
            "escritorio": "m.lima Advogados Associados",
            "areas": ["Direito Penal", "Direito da Saúde"]
        }
    except Exception as e:
        logger.error(f"❌ Health check error: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "service": "m.lima_law_firm_backend",
                "error": str(e),
                "escritorio": "m.lima Advogados Associados"
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
            "message": "Ocorreu um erro inesperado no sistema",
            "path": str(request.url),
            "service": "m.lima_law_firm_backend"
        }
    )

# Endpoint adicional para informações do escritório
@app.get("/api/v1/escritorio")
async def escritorio_info():
    """Informações do escritório m.lima"""
    return {
        "nome": "m.lima Advogados Associados",
        "areas_especializacao": [
            {
                "area": "Direito Penal",
                "descricao": "Defesa criminal, investigações, processos penais",
                "especialidades": [
                    "Crimes contra a pessoa",
                    "Crimes patrimoniais", 
                    "Crimes de trânsito",
                    "Defesa em inquéritos policiais"
                ]
            },
            {
                "area": "Direito da Saúde",
                "descricao": "Ações contra planos de saúde, direitos do paciente",
                "especialidades": [
                    "Negativa de cobertura",
                    "Reembolsos médicos",
                    "Liminares para tratamentos",
                    "Erro médico"
                ]
            }
        ],
        "contato": {
            "whatsapp": "+5511918368812",
            "sistema_atendimento": "Chat inteligente 24h"
        },
        "tecnologia": {
            "chat_bot": "Sistema de qualificação automática de leads",
            "whatsapp_integration": "Baileys WhatsApp Bot",
            "ai_powered": "Fluxo conversacional inteligente"
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"🚀 Starting m.lima server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )