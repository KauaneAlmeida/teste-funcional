"""
Request Models for Law Firm Backend API
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class ConversationRequest(BaseModel):
    """Request model for conversation interactions"""
    message: str = Field(..., description="User message")
    session_id: str = Field(..., description="Session identifier")
    platform: Optional[str] = Field(default="web", description="Platform (web/whatsapp)")
    
    class Config:
        schema_extra = {
            "example": {
                "message": "Olá, preciso de ajuda jurídica",
                "session_id": "web_session_123",
                "platform": "web"
            }
        }

class PhoneSubmissionRequest(BaseModel):
    """Request model for phone number submission"""
    phone_number: str = Field(..., description="Phone number with area code")
    session_id: str = Field(..., description="Session identifier")
    
    class Config:
        schema_extra = {
            "example": {
                "phone_number": "11999999999",
                "session_id": "web_session_123"
            }
        }

class WhatsAppAuthorizationRequest(BaseModel):
    """Request model for WhatsApp session authorization"""
    session_id: str = Field(..., description="Unique session ID for WhatsApp")
    phone_number: str = Field(..., description="WhatsApp phone number")
    source: str = Field(default="landing_page", description="Source of authorization")
    user_data: Optional[Dict[str, Any]] = Field(default=None, description="User data from landing page")
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "whatsapp_session_123",
                "phone_number": "5511999999999",
                "source": "landing_chat",
                "user_data": {
                    "name": "João Silva",
                    "email": "joao@email.com",
                    "problem": "Questão trabalhista"
                }
            }
        }