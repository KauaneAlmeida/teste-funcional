"""
Firebase Service - Mock implementation for development
"""
import logging
import json
from typing import Dict, Any, Optional
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

# In-memory storage for development (replace with real Firebase in production)
_sessions = {}
_leads = {}
_conversation_flow = {}

async def get_user_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Get user session data"""
    try:
        session_data = _sessions.get(session_id)
        if session_data:
            logger.info(f"📊 Session retrieved: {session_id}")
            return session_data
        return None
    except Exception as e:
        logger.error(f"❌ Error getting session {session_id}: {str(e)}")
        return None

async def save_user_session(session_id: str, session_data: Dict[str, Any]) -> bool:
    """Save user session data"""
    try:
        _sessions[session_id] = session_data
        logger.info(f"💾 Session saved: {session_id}")
        return True
    except Exception as e:
        logger.error(f"❌ Error saving session {session_id}: {str(e)}")
        return False

async def save_lead_data(lead_data: Dict[str, Any]) -> str:
    """Save lead data and return lead ID"""
    try:
        lead_id = f"lead_{len(_leads) + 1}_{int(datetime.now().timestamp())}"
        _leads[lead_id] = {
            **lead_data,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "lead_id": lead_id
        }
        logger.info(f"💾 Lead saved: {lead_id}")
        return lead_id
    except Exception as e:
        logger.error(f"❌ Error saving lead: {str(e)}")
        return f"error_{int(datetime.now().timestamp())}"

async def get_conversation_flow() -> Dict[str, Any]:
    """Get conversation flow configuration"""
    return {
        "flow_type": "structured_questions",
        "steps": [
            {"id": 1, "field": "identification", "question": "Qual é o seu nome completo?"},
            {"id": 2, "field": "contact_info", "question": "Qual seu telefone e email?"},
            {"id": 3, "field": "area_qualification", "question": "Em qual área do direito você precisa de ajuda?"},
            {"id": 4, "field": "case_details", "question": "Conte-me mais detalhes sobre sua situação"},
            {"id": 5, "field": "confirmation", "question": "Podemos prosseguir com seu atendimento?"}
        ]
    }

async def get_firebase_service_status() -> Dict[str, Any]:
    """Get Firebase service status"""
    return {
        "service": "firebase_mock",
        "status": "active",
        "sessions_count": len(_sessions),
        "leads_count": len(_leads),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

async def reset_user_session(session_id: str) -> bool:
    """Reset user session"""
    try:
        if session_id in _sessions:
            del _sessions[session_id]
            logger.info(f"🔄 Session reset: {session_id}")
        return True
    except Exception as e:
        logger.error(f"❌ Error resetting session {session_id}: {str(e)}")
        return False