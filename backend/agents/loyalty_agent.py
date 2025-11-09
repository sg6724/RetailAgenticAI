from typing import Dict, Optional
from apis.loyalty_api import loyalty_api


class LoyaltyAgent:
    """Agent responsible for loyalty and offers"""
    
    def __init__(self):
        self.name = "Loyalty Agent"
        self.loyalty_api = loyalty_api
    
    async def execute(self, context: Dict) -> Dict:
        """Execute loyalty and pricing logic"""
        try:
            customer_id = context.get("customer_id")
            subtotal = context.get("subtotal", 0)
            coupon_code = context.get("coupon_code")
            
            if not customer_id:
                return {
                    "success": False,
                    "agent": self.name,
                    "message": "Customer ID required"
                }
            
            # Get loyalty information
            loyalty_info = self.loyalty_api.get_customer_loyalty(customer_id)
            
            # Calculate final pricing
            pricing = self.loyalty_api.calculate_final_pricing(
                customer_id=customer_id,
                subtotal=subtotal,
                coupon_code=coupon_code
            )
            
            # Get available coupons
            available_coupons = self.loyalty_api.get_available_coupons(customer_id)
            
            return {
                "success": True,
                "agent": self.name,
                "loyalty_info": loyalty_info,
                "pricing": pricing,
                "available_coupons": available_coupons,
                "message": "Loyalty benefits calculated successfully"
            }
        
        except Exception as e:
            return {
                "success": False,
                "agent": self.name,
                "error": str(e),
                "message": "Failed to calculate loyalty benefits"
            }
    
    async def apply_coupon(self, customer_id: str, coupon_code: str, amount: float) -> Dict:
        """Apply coupon code"""
        try:
            result = self.loyalty_api.apply_coupon(customer_id, coupon_code, amount)
            
            return {
                "success": result["valid"],
                "agent": self.name,
                "coupon_result": result,
                "message": result["message"]
            }
        
        except Exception as e:
            return {
                "success": False,
                "agent": self.name,
                "error": str(e),
                "message": "Failed to apply coupon"
            }
    
    async def add_points(self, customer_id: str, points: int) -> Dict:
        """Add loyalty points"""
        try:
            result = self.loyalty_api.add_points(customer_id, points)
            
            return {
                "success": result["success"],
                "agent": self.name,
                "points_result": result,
                "message": f"Added {points} points successfully"
            }
        
        except Exception as e:
            return {
                "success": False,
                "agent": self.name,
                "error": str(e),
                "message": "Failed to add points"
            }


# Singleton instance
loyalty_agent = LoyaltyAgent()
