from typing import Dict, List
from datetime import datetime, timedelta


class SupportAgent:
    """Agent responsible for post-purchase support"""
    
    def __init__(self):
        self.name = "Support Agent"
    
    async def execute(self, context: Dict) -> Dict:
        """Execute post-purchase support logic"""
        try:
            order_id = context.get("order_id")
            customer_id = context.get("customer_id")
            action = context.get("action", "feedback")
            
            if action == "feedback":
                return await self._request_feedback(order_id, customer_id)
            elif action == "recommendations":
                return await self._get_complementary_products(order_id, customer_id)
            elif action == "return":
                return await self._process_return(order_id, context.get("reason"))
            else:
                return {
                    "success": False,
                    "agent": self.name,
                    "message": "Unknown action"
                }
        
        except Exception as e:
            return {
                "success": False,
                "agent": self.name,
                "error": str(e),
                "message": "Support action failed"
            }
    
    async def _request_feedback(self, order_id: str, customer_id: str) -> Dict:
        """Request feedback from customer"""
        feedback_url = f"/feedback/{order_id}"
        
        message = f"""
        Hi! We hope you're enjoying your recent purchase! 🎉
        
        We'd love to hear your feedback. How would you rate your experience?
        
        Your feedback helps us serve you better!
        """
        
        return {
            "success": True,
            "agent": self.name,
            "action": "feedback_request",
            "message": message.strip(),
            "feedback_url": feedback_url,
            "order_id": order_id
        }
    
    async def _get_complementary_products(self, order_id: str, customer_id: str) -> Dict:
        """Get complementary product recommendations"""
        # Mock complementary products
        recommendations = [
            {
                "id": "P011",
                "name": "Leather Belt - Classic",
                "price": 899,
                "reason": "Perfect match for your jacket",
                "discount": 10
            },
            {
                "id": "P012",
                "name": "Winter Scarf - Wool",
                "price": 599,
                "reason": "Complete your winter look",
                "discount": 15
            },
            {
                "id": "P013",
                "name": "Leather Gloves",
                "price": 1299,
                "reason": "Stay warm this winter",
                "discount": 10
            }
        ]
        
        message = """
        Based on your recent purchase, you might also like these items! 
        Special discount just for you! 🎁
        """
        
        return {
            "success": True,
            "agent": self.name,
            "action": "complementary_recommendations",
            "recommendations": recommendations,
            "message": message.strip()
        }
    
    async def _process_return(self, order_id: str, reason: str = None) -> Dict:
        """Process return request"""
        return_id = f"RET{order_id[3:]}"
        
        return_details = {
            "return_id": return_id,
            "order_id": order_id,
            "status": "Initiated",
            "pickup_scheduled": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "refund_timeline": "5-7 business days after pickup",
            "reason": reason or "Not specified"
        }
        
        message = """
        Your return request has been initiated successfully.
        
        We'll arrange a pickup within 24 hours.
        Refund will be processed within 5-7 business days after we receive the item.
        
        Is there anything else we can help you with?
        """
        
        return {
            "success": True,
            "agent": self.name,
            "action": "return_initiated",
            "return_details": return_details,
            "message": message.strip()
        }
    
    async def submit_feedback(self, order_id: str, customer_id: str, rating: int, feedback_text: str = None) -> Dict:
        """Submit customer feedback"""
        try:
            feedback_id = f"FB{order_id[3:]}"
            
            return {
                "success": True,
                "agent": self.name,
                "feedback_id": feedback_id,
                "order_id": order_id,
                "rating": rating,
                "message": "Thank you for your feedback! We appreciate it. 🙏"
            }
        
        except Exception as e:
            return {
                "success": False,
                "agent": self.name,
                "error": str(e),
                "message": "Failed to submit feedback"
            }


# Singleton instance
support_agent = SupportAgent()
