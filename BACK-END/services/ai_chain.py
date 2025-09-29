"""
AI Chain Service - Mock implementation for development
"""
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class AIOrchestrator:
    def __init__(self):
        self.session_memory = {}
    
    async def generate_response(self, message: str, session_id: str) -> str:
        """Generate AI response (mock implementation)"""
        try:
            # Simple mock responses for development
            message_lower = message.lower()
            
            if any(word in message_lower for word in ['oi', 'olá', 'hello', 'bom dia', 'boa tarde', 'boa noite']):
                return "Olá! Bem-vindo ao escritório m.lima. Como posso ajudá-lo hoje?"
            
            if any(word in message_lower for word in ['nome', 'chamo', 'sou']):
                return "Prazer em conhecê-lo! Agora preciso de suas informações de contato."
            
            if any(word in message_lower for word in ['telefone', 'email', 'contato']):
                return "Perfeito! Em qual área do direito você precisa de nossa ajuda?"
            
            if any(word in message_lower for word in ['penal', 'criminal', 'saúde', 'plano']):
                return "Entendi. Pode me contar mais detalhes sobre sua situação?"
            
            return "Obrigado pelas informações. Nossa equipe entrará em contato em breve!"
            
        except Exception as e:
            logger.error(f"❌ Error generating AI response: {str(e)}")
            return "Desculpe, ocorreu um erro. Como posso ajudá-lo?"
    
    def clear_session_memory(self, session_id: str):
        """Clear session memory"""
        if session_id in self.session_memory:
            del self.session_memory[session_id]

# Global instance
ai_orchestrator = AIOrchestrator()