from typing import Dict, List, Optional
from apis.inventory_api import inventory_api


class InventoryAgent:
    """Agent responsible for inventory and fulfillment options"""
    
    def __init__(self):
        self.name = "Inventory Agent"
        self.inventory_api = inventory_api
    
    async def execute(self, context: Dict) -> Dict:
        """Execute inventory check logic"""
        try:
            product_ids = context.get("product_ids", [])
            location = context.get("location")
            
            if not product_ids:
                return {
                    "success": False,
                    "agent": self.name,
                    "message": "No products specified"
                }
            
            # Check inventory for each product
            inventory_results = []
            for product_id in product_ids:
                availability = self.inventory_api.check_availability(product_id, location)
                fulfillment_options = self.inventory_api.get_fulfillment_options(product_id, location)
                
                inventory_results.append({
                    "product_id": product_id,
                    "availability": availability,
                    "fulfillment_options": fulfillment_options,
                    "in_stock": availability["available"]
                })
            
            # Get nearby stores if location provided
            nearby_stores = []
            if location:
                nearby_stores = self.inventory_api.get_nearby_stores(location)
            
            return {
                "success": True,
                "agent": self.name,
                "inventory": inventory_results,
                "nearby_stores": nearby_stores,
                "message": "Inventory checked successfully"
            }
        
        except Exception as e:
            return {
                "success": False,
                "agent": self.name,
                "error": str(e),
                "message": "Failed to check inventory"
            }
    
    async def reserve_stock(self, product_id: str, quantity: int, location: Optional[str] = None) -> Dict:
        """Reserve stock for a product"""
        try:
            result = self.inventory_api.reserve_stock(product_id, quantity, location)
            return {
                "success": result["success"],
                "agent": self.name,
                "reservation": result,
                "message": result["message"]
            }
        except Exception as e:
            return {
                "success": False,
                "agent": self.name,
                "error": str(e),
                "message": "Failed to reserve stock"
            }


# Singleton instance
inventory_agent = InventoryAgent()
