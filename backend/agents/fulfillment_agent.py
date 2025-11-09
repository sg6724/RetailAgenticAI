from typing import Dict
from datetime import datetime, timedelta
import random
import string


class FulfillmentAgent:
    """Agent responsible for order fulfillment"""
    
    def __init__(self):
        self.name = "Fulfillment Agent"
    
    async def execute(self, context: Dict) -> Dict:
        """Execute fulfillment scheduling"""
        try:
            order_id = context.get("order_id")
            fulfillment_option = context.get("fulfillment_option")
            location = context.get("location")
            delivery_address = context.get("delivery_address")
            
            if not order_id:
                return {
                    "success": False,
                    "agent": self.name,
                    "message": "Order ID required"
                }
            
            # Generate fulfillment details based on option
            fulfillment_details = self._generate_fulfillment_details(
                fulfillment_option,
                location,
                delivery_address
            )
            
            # Generate tracking information
            tracking_id = self._generate_tracking_id()
            
            return {
                "success": True,
                "agent": self.name,
                "fulfillment_details": fulfillment_details,
                "tracking_id": tracking_id,
                "message": "Fulfillment scheduled successfully"
            }
        
        except Exception as e:
            return {
                "success": False,
                "agent": self.name,
                "error": str(e),
                "message": "Failed to schedule fulfillment"
            }
    
    def _generate_fulfillment_details(
        self,
        option: str,
        location: str = None,
        delivery_address: str = None
    ) -> Dict:
        """Generate fulfillment details based on option"""
        
        if option == "Ship to Home":
            estimated_delivery = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
            return {
                "type": "Ship to Home",
                "delivery_address": delivery_address or "Default address",
                "estimated_delivery": estimated_delivery,
                "estimated_time": "2-3 days",
                "status": "Processing",
                "carrier": "BlueDart Express",
                "shipping_cost": 0
            }
        
        elif option == "Click & Collect":
            estimated_pickup = (datetime.now() + timedelta(hours=4)).strftime("%Y-%m-%d %H:%M")
            return {
                "type": "Click & Collect",
                "pickup_location": location or "Phoenix Mills Store",
                "estimated_ready": estimated_pickup,
                "estimated_time": "Same day",
                "status": "Preparing",
                "pickup_instructions": "Show order ID at the collection counter"
            }
        
        elif option == "In-Store Try-on":
            return {
                "type": "In-Store Try-on",
                "store_location": location or "Phoenix Mills Store",
                "status": "Reserved",
                "reservation_valid": "48 hours",
                "store_hours": "10 AM - 10 PM",
                "instructions": "Visit the store anytime during business hours"
            }
        
        else:
            return {
                "type": "Standard",
                "status": "Pending",
                "message": "Fulfillment option not specified"
            }
    
    def _generate_tracking_id(self) -> str:
        """Generate tracking ID"""
        return f"TRK{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}"
    
    async def get_tracking_status(self, tracking_id: str) -> Dict:
        """Get tracking status (mock)"""
        # Mock tracking statuses
        statuses = [
            {"status": "Order Placed", "timestamp": "2 hours ago", "location": "Mumbai"},
            {"status": "Processing", "timestamp": "1 hour ago", "location": "Warehouse"},
            {"status": "Shipped", "timestamp": "30 mins ago", "location": "In Transit"},
        ]
        
        return {
            "success": True,
            "agent": self.name,
            "tracking_id": tracking_id,
            "current_status": "In Transit",
            "history": statuses,
            "estimated_delivery": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        }


# Singleton instance
fulfillment_agent = FulfillmentAgent()
