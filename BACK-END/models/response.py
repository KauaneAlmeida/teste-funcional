"""
Response Models for Law Firm Backend API
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

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