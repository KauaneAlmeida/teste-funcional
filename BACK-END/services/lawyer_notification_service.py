"""
Lawyer Notification Service - Mock implementation for development
"""
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class LawyerNotificationService:
    def __init__(self):
        self.notifications_sent = []
    
    async def notify_lawyers_of_new_lead(
        self, 
        lead_name: str, 
        lead_phone: str, 
        category: str, 
        additional_info: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Notify lawyers of new qualified lead"""
        try:
            notification = {
                "lead_name": lead_name,
                "lead_phone": lead_phone,
                "category": category,
                "additional_info": additional_info or {},
                "timestamp": datetime.now().isoformat(),
                "notification_id": f"notif_{len(self.notifications_sent) + 1}"
            }
            
            self.notifications_sent.append(notification)
            
            logger.info(f"📧 Lawyers notified of new lead: {lead_name} ({category})")
            
            return {
                "success": True,
                "notification_id": notification["notification_id"],
                "message": "Lawyers successfully notified"
            }
            
        except Exception as e:
            logger.error(f"❌ Error notifying lawyers: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to notify lawyers"
            }

# Global instance
lawyer_notification_service = LawyerNotificationService()