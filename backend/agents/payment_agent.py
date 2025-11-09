from typing import Dict, Optional
from apis.payment_api import payment_api


class PaymentAgent:
    """Agent responsible for payment processing"""
    
    def __init__(self):
        self.name = "Payment Agent"
        self.payment_api = payment_api
    
    async def execute(self, context: Dict) -> Dict:
        """Execute payment preparation logic"""
        try:
            customer_id = context.get("customer_id")
            
            if not customer_id:
                return {
                    "success": False,
                    "agent": self.name,
                    "message": "Customer ID required"
                }
            
            # Get available payment methods
            payment_methods = self.payment_api.get_payment_methods(customer_id)
            
            return {
                "success": True,
                "agent": self.name,
                "payment_methods": payment_methods,
                "message": "Payment methods retrieved successfully"
            }
        
        except Exception as e:
            return {
                "success": False,
                "agent": self.name,
                "error": str(e),
                "message": "Failed to get payment methods"
            }
    
    async def process_payment(
        self,
        customer_id: str,
        method_id: str,
        method_type: str,
        amount: float,
        order_id: str
    ) -> Dict:
        """Process payment"""
        try:
            result = self.payment_api.process_payment(
                customer_id=customer_id,
                method_id=method_id,
                method_type=method_type,
                amount=amount,
                order_id=order_id
            )
            
            return {
                "success": result["success"],
                "agent": self.name,
                "payment_result": result,
                "message": result["message"]
            }
        
        except Exception as e:
            return {
                "success": False,
                "agent": self.name,
                "error": str(e),
                "message": "Payment processing failed"
            }
    
    async def validate_payment(self, method_id: str, amount: float) -> Dict:
        """Validate payment method"""
        try:
            result = self.payment_api.validate_payment_method(method_id, amount)
            
            return {
                "success": result["valid"],
                "agent": self.name,
                "validation": result,
                "message": result["message"]
            }
        
        except Exception as e:
            return {
                "success": False,
                "agent": self.name,
                "error": str(e),
                "message": "Payment validation failed"
            }


# Singleton instance
payment_agent = PaymentAgent()
