"""
Request Models for Law Firm Backend API
Modelos adequados ao projeto de escritório de advocacia
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime

class ConversationRequest(BaseModel):
    """Request model for conversation interactions"""
    message: str = Field(
        ..., 
        description="Mensagem do usuário",
        min_length=1,
        max_length=2000,
        example="Olá, preciso de ajuda jurídica"
    )
    session_id: str = Field(
        ..., 
        description="Identificador da sessão",
        example="web_session_123"
    )
    platform: Optional[str] = Field(
        default="web", 
        description="Plataforma (web/whatsapp)",
        example="web"
    )
    
    @validator('message')
    def validate_message(cls, v):
        """Validar que a mensagem não está vazia"""
        if not v or not v.strip():
            raise ValueError('Mensagem não pode estar vazia')
        return v.strip()
    
    class Config:
        schema_extra = {
            "example": {
                "message": "Olá, preciso de ajuda com um caso de direito penal",
                "session_id": "web_session_123",
                "platform": "web"
            }
        }

class PhoneSubmissionRequest(BaseModel):
    """Request model for phone number submission"""
    phone_number: str = Field(
        ..., 
        description="Número de telefone com DDD",
        example="11999999999"
    )
    session_id: str = Field(
        ..., 
        description="Identificador da sessão",
        example="web_session_123"
    )
    
    @validator('phone_number')
    def validate_phone(cls, v):
        """Validar formato do telefone brasileiro"""
        import re
        phone_clean = re.sub(r'[^\d]', '', v)
        if len(phone_clean) < 10 or len(phone_clean) > 13:
            raise ValueError('Telefone deve ter entre 10 e 13 dígitos')
        return phone_clean
    
    class Config:
        schema_extra = {
            "example": {
                "phone_number": "11999999999",
                "session_id": "web_session_123"
            }
        }

class WhatsAppAuthorizationRequest(BaseModel):
    """Request model for WhatsApp session authorization"""
    session_id: str = Field(
        ..., 
        description="ID único da sessão WhatsApp",
        example="whatsapp_session_123"
    )
    phone_number: str = Field(
        ..., 
        description="Número WhatsApp (formato: 5511999999999)",
        example="5511999999999"
    )
    source: str = Field(
        default="landing_page", 
        description="Origem da autorização",
        example="landing_chat"
    )
    user_data: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Dados do usuário da landing page"
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="Timestamp da autorização"
    )
    user_agent: Optional[str] = Field(
        default=None,
        description="User agent para tracking"
    )
    page_url: Optional[str] = Field(
        default=None,
        description="URL da página onde foi solicitada autorização"
    )
    
    @validator('phone_number')
    def validate_whatsapp_phone(cls, v):
        """Validar formato do telefone WhatsApp"""
        import re
        phone_clean = re.sub(r'[^\d]', '', v)
        if not phone_clean.startswith('55'):
            raise ValueError('Telefone deve começar com código do Brasil (55)')
        if len(phone_clean) != 13:
            raise ValueError('Telefone deve ter 13 dígitos (55 + DDD + número)')
        return phone_clean
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "whatsapp_session_123",
                "phone_number": "5511999999999",
                "source": "landing_chat",
                "user_data": {
                    "name": "João Silva",
                    "email": "joao@email.com",
                    "problem": "Questão trabalhista urgente"
                }
            }
        }

class ChatStartRequest(BaseModel):
    """Request model for starting a new chat session"""
    platform: Optional[str] = Field(
        default="web",
        description="Plataforma de origem",
        example="web"
    )
    user_agent: Optional[str] = Field(
        default=None,
        description="User agent do navegador"
    )
    referrer: Optional[str] = Field(
        default=None,
        description="URL de referência"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "platform": "web",
                "user_agent": "Mozilla/5.0...",
                "referrer": "https://mlima-advogados.com"
            }
        }

class LeadDataRequest(BaseModel):
    """Request model for lead data submission"""
    session_id: str = Field(..., description="ID da sessão")
    lead_data: Dict[str, Any] = Field(..., description="Dados coletados do lead")
    platform: str = Field(..., description="Plataforma de origem")
    qualification_score: Optional[float] = Field(
        default=None,
        description="Score de qualificação do lead (0.0 a 1.0)"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "web_session_123",
                "lead_data": {
                    "identification": "João Silva",
                    "contact_info": "11999999999 joao@email.com",
                    "area_qualification": "Direito Penal",
                    "case_details": "Preciso de defesa em processo criminal",
                    "phone": "11999999999",
                    "email": "joao@email.com"
                },
                "platform": "web",
                "qualification_score": 0.85
            }
        }

class SessionResetRequest(BaseModel):
    """Request model for session reset"""
    session_id: str = Field(..., description="ID da sessão para resetar")
    reason: Optional[str] = Field(
        default="user_request",
        description="Motivo do reset"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "web_session_123",
                "reason": "user_restart"
            }
        }