"""
Response Models for Law Firm Backend API
Modelos de resposta adequados ao projeto de escritório de advocacia
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class ConversationResponse(BaseModel):
    """Response model for conversation interactions"""
    session_id: str = Field(..., description="Identificador da sessão")
    response: str = Field(..., description="Resposta do bot/assistente")
    ai_mode: bool = Field(default=False, description="Se está em modo AI")
    flow_completed: bool = Field(default=False, description="Se o fluxo foi completado")
    phone_collected: bool = Field(default=False, description="Se o telefone foi coletado")
    lawyers_notified: bool = Field(default=False, description="Se os advogados foram notificados")
    lead_data: Dict[str, Any] = Field(default_factory=dict, description="Dados coletados do lead")
    message_count: int = Field(default=1, description="Número de mensagens na conversa")
    current_step: Optional[str] = Field(default=None, description="Passo atual da conversa")
    qualification_score: Optional[float] = Field(default=None, description="Score de qualificação")
    next_action: Optional[str] = Field(default=None, description="Próxima ação sugerida")
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "web_session_123",
                "response": "Olá! Bem-vindo ao escritório m.lima. Como posso ajudá-lo hoje?",
                "ai_mode": False,
                "flow_completed": False,
                "phone_collected": False,
                "lawyers_notified": False,
                "lead_data": {},
                "message_count": 1,
                "current_step": "greeting",
                "qualification_score": 0.0,
                "next_action": "collect_name"
            }
        }

class WhatsAppAuthorizationResponse(BaseModel):
    """Response model for WhatsApp authorization"""
    status: str = Field(..., description="Status da autorização")
    session_id: str = Field(..., description="ID da sessão autorizada")
    phone_number: str = Field(..., description="Número de telefone da sessão")
    source: str = Field(..., description="Origem da autorização")
    message: str = Field(..., description="Mensagem de status")
    timestamp: str = Field(..., description="Timestamp da autorização")
    expires_in: Optional[int] = Field(default=3600, description="Expiração em segundos")
    whatsapp_url: str = Field(..., description="URL deep link do WhatsApp")
    lead_type: Optional[str] = Field(default=None, description="Tipo de lead")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "authorized",
                "session_id": "whatsapp_session_123",
                "phone_number": "5511999999999",
                "source": "landing_chat",
                "message": "Sessão WhatsApp autorizada com sucesso",
                "timestamp": "2024-01-15T10:30:00.000Z",
                "expires_in": 3600,
                "whatsapp_url": "https://wa.me/5511999999999",
                "lead_type": "landing_chat_lead"
            }
        }

class HealthResponse(BaseModel):
    """Response model for health checks"""
    status: str = Field(..., description="Status do serviço")
    service: str = Field(..., description="Nome do serviço")
    version: str = Field(..., description="Versão do serviço")
    timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat(), 
        description="Timestamp da verificação"
    )
    services: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Status dos serviços integrados"
    )
    features: Optional[List[str]] = Field(
        default=None,
        description="Funcionalidades disponíveis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "service": "law_firm_backend",
                "version": "1.0.0",
                "timestamp": "2024-01-15T10:30:00.000Z",
                "services": {
                    "firebase": "active",
                    "whatsapp_bot": "connected",
                    "ai_service": "active"
                },
                "features": [
                    "conversation_flow",
                    "whatsapp_integration",
                    "lead_management"
                ]
            }
        }

class ErrorResponse(BaseModel):
    """Response model for errors"""
    error: bool = Field(default=True, description="Flag de erro")
    message: str = Field(..., description="Mensagem de erro")
    status_code: int = Field(..., description="Código de status HTTP")
    details: Optional[str] = Field(default=None, description="Detalhes adicionais do erro")
    timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Timestamp do erro"
    )
    session_id: Optional[str] = Field(default=None, description="ID da sessão (se aplicável)")
    
    class Config:
        schema_extra = {
            "example": {
                "error": True,
                "message": "Erro de validação",
                "status_code": 400,
                "details": "Campo 'message' é obrigatório",
                "timestamp": "2024-01-15T10:30:00.000Z",
                "session_id": "web_session_123"
            }
        }

class LeadResponse(BaseModel):
    """Response model for lead operations"""
    lead_id: str = Field(..., description="ID do lead criado")
    status: str = Field(..., description="Status da operação")
    message: str = Field(..., description="Mensagem de confirmação")
    lead_data: Dict[str, Any] = Field(..., description="Dados do lead")
    qualification_score: Optional[float] = Field(default=None, description="Score de qualificação")
    lawyers_notified: bool = Field(default=False, description="Se advogados foram notificados")
    whatsapp_sent: bool = Field(default=False, description="Se WhatsApp foi enviado")
    
    class Config:
        schema_extra = {
            "example": {
                "lead_id": "lead_123456",
                "status": "created",
                "message": "Lead criado e advogados notificados",
                "lead_data": {
                    "name": "João Silva",
                    "phone": "11999999999",
                    "area": "Direito Penal"
                },
                "qualification_score": 0.85,
                "lawyers_notified": True,
                "whatsapp_sent": True
            }
        }

class SessionStatusResponse(BaseModel):
    """Response model for session status"""
    session_id: str = Field(..., description="ID da sessão")
    exists: bool = Field(..., description="Se a sessão existe")
    platform: Optional[str] = Field(default=None, description="Plataforma da sessão")
    current_step: Optional[str] = Field(default=None, description="Passo atual")
    flow_completed: bool = Field(default=False, description="Se o fluxo foi completado")
    phone_collected: bool = Field(default=False, description="Se o telefone foi coletado")
    lawyers_notified: bool = Field(default=False, description="Se advogados foram notificados")
    message_count: int = Field(default=0, description="Número de mensagens")
    qualification_score: Optional[float] = Field(default=None, description="Score de qualificação")
    created_at: Optional[str] = Field(default=None, description="Data de criação")
    last_updated: Optional[str] = Field(default=None, description="Última atualização")
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "web_session_123",
                "exists": True,
                "platform": "web",
                "current_step": "step3_area",
                "flow_completed": False,
                "phone_collected": False,
                "lawyers_notified": False,
                "message_count": 3,
                "qualification_score": 0.6,
                "created_at": "2024-01-15T10:00:00.000Z",
                "last_updated": "2024-01-15T10:30:00.000Z"
            }
        }

class WhatsAppStatusResponse(BaseModel):
    """Response model for WhatsApp service status"""
    service: str = Field(..., description="Nome do serviço")
    status: str = Field(..., description="Status da conexão")
    connected: bool = Field(..., description="Se está conectado")
    phone_number: Optional[str] = Field(default=None, description="Número conectado")
    has_qr: bool = Field(default=False, description="Se tem QR code disponível")
    qr_url: Optional[str] = Field(default=None, description="URL do QR code")
    service_healthy: bool = Field(default=True, description="Se o serviço está saudável")
    timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Timestamp da verificação"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "service": "baileys_whatsapp",
                "status": "connected",
                "connected": True,
                "phone_number": "5511918368812",
                "has_qr": False,
                "qr_url": None,
                "service_healthy": True,
                "timestamp": "2024-01-15T10:30:00.000Z"
            }
        }

class ServiceStatusResponse(BaseModel):
    """Response model for overall service status"""
    overall_status: str = Field(..., description="Status geral do sistema")
    services: Dict[str, Any] = Field(..., description="Status dos serviços individuais")
    features: Dict[str, bool] = Field(..., description="Funcionalidades disponíveis")
    timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Timestamp da verificação"
    )
    version: str = Field(default="1.0.0", description="Versão do sistema")
    
    class Config:
        schema_extra = {
            "example": {
                "overall_status": "active",
                "services": {
                    "firebase": {"status": "active"},
                    "ai_service": {"status": "active"},
                    "whatsapp_bot": {"status": "connected"}
                },
                "features": {
                    "conversation_flow": True,
                    "ai_responses": True,
                    "whatsapp_integration": True,
                    "lead_collection": True
                },
                "timestamp": "2024-01-15T10:30:00.000Z",
                "version": "1.0.0"
            }
        }

class PhoneSubmissionResponse(BaseModel):
    """Response model for phone submission"""
    status: str = Field(..., description="Status da submissão")
    message: str = Field(..., description="Mensagem de confirmação")
    phone_submitted: bool = Field(..., description="Se o telefone foi aceito")
    phone_number: Optional[str] = Field(default=None, description="Telefone formatado")
    whatsapp_sent: bool = Field(default=False, description="Se WhatsApp foi enviado")
    lead_finalized: bool = Field(default=False, description="Se o lead foi finalizado")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "message": "Telefone coletado com sucesso! Nossa equipe entrará em contato.",
                "phone_submitted": True,
                "phone_number": "5511999999999",
                "whatsapp_sent": True,
                "lead_finalized": True
            }
        }