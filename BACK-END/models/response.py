"""
Response Models for Law Firm Backend API
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class ConversationResponse(BaseModel):
    """Response model for conversation interactions"""
    session_id: str = Field(..., description="Session identifier")
    response: str = Field(..., description="Bot response message")
    ai_mode: bool = Field(default=False, description="Whether AI mode is active")
    flow_completed: bool = Field(default=False, description="Whether conversation flow is completed")
    phone_collected: bool = Field(default=False, description="Whether phone number was collected")
    lead_data: Dict[str, Any] = Field(default_factory=dict, description="Collected lead data")
    message_count: int = Field(default=1, description="Number of messages in conversation")
    current_step: Optional[str] = Field(default=None, description="Current conversation step")
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "web_session_123",
                "response": "Olá! Como posso ajudá-lo hoje?",
                "ai_mode": False,
                "flow_completed": False,
                "phone_collected": False,
                "lead_data": {},
                "message_count": 1,
                "current_step": "greeting"
            }
        }

class WhatsAppAuthorizationResponse(BaseModel):
    """Response model for WhatsApp authorization"""
    status: str = Field(..., description="Authorization status")
    session_id: str = Field(..., description="Session ID that was authorized")
    phone_number: str = Field(..., description="Phone number for the session")
    source: str = Field(..., description="Authorization source")
    message: str = Field(..., description="Status message")
    timestamp: str = Field(..., description="Authorization timestamp")
    expires_in: Optional[int] = Field(default=3600, description="Authorization expiry in seconds")
    whatsapp_url: str = Field(..., description="WhatsApp deep link URL")

class HealthResponse(BaseModel):
    """Response model for health checks"""
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Check timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "service": "law_firm_backend",
                "version": "1.0.0",
                "timestamp": "2024-01-15T10:30:00.000Z"
            }
        }

class ErrorResponse(BaseModel):
    """Response model for errors"""
    error: bool = Field(default=True, description="Error flag")
    message: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")
    details: Optional[str] = Field(default=None, description="Additional error details")
    
    class Config:
        schema_extra = {
            "example": {
                "error": True,
                "message": "Validation error",
                "status_code": 400,
                "details": "Message field is required"
            }
        }