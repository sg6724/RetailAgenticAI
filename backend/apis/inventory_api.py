from typing import Dict, Optional
import random

# Mock inventory data
MOCK_INVENTORY = {
    "P001": {"warehouse": 50, "stores": {"Mumbai": 15, "Delhi": 12, "Bangalore": 8}},
    "P002": {"warehouse": 30, "stores": {"Mumbai": 8, "Delhi": 10, "Bangalore": 5}},
    "P003": {"warehouse": 45, "stores": {"Mumbai": 10, "Delhi": 15, "Bangalore": 12}},
    "P004": {"warehouse": 20, "stores": {"Mumbai": 5, "Delhi": 3, "Bangalore": 4}},
    "P005": {"warehouse": 60, "stores": {"Mumbai": 20, "Delhi": 18, "Bangalore": 15}},
    "P006": {"warehouse": 100, "stores": {"Mumbai": 25, "Delhi": 30, "Bangalore": 20}},
    "P007": {"warehouse": 80, "stores": {"Mumbai": 18, "Delhi": 22, "Bangalore": 16}},
    "P008": {"warehouse": 70, "stores": {"Mumbai": 20, "Delhi": 25, "Bangalore": 18}},
    "P009": {"warehouse": 55, "stores": {"Mumbai": 15, "Delhi": 18, "Bangalore": 12}},
    "P010": {"warehouse": 40, "stores": {"Mumbai": 12, "Delhi": 10, "Bangalore": 8}},
}


class InventoryAPI:
    def __init__(self):
        self.inventory = MOCK_INVENTORY
    
    def get_stock(self, product_id: str) -> Optional[Dict]:
        """Get stock information for a product"""
        return self.inventory.get(product_id)
    
    def check_availability(self, product_id: str, location: Optional[str] = None) -> Dict:
        """Check if product is available"""
        stock = self.get_stock(product_id)
        
        if not stock:
            return {
                "available": False,
                "warehouse": 0,
                "stores": {},
                "message": "Product not found"
            }
        
        warehouse_available = stock["warehouse"] > 0
        store_available = False
        available_stores = {}
        
        if location:
            # Check specific location
            store_stock = stock["stores"].get(location, 0)
            if store_stock > 0:
                store_available = True
                available_stores[location] = store_stock
        else:
            # Check all locations
            for store, qty in stock["stores"].items():
                if qty > 0:
                    store_available = True
                    available_stores[store] = qty
        
        return {
            "available": warehouse_available or store_available,
            "warehouse": stock["warehouse"],
            "stores": available_stores,
            "message": "In stock" if (warehouse_available or store_available) else "Out of stock"
        }
    
    def get_fulfillment_options(self, product_id: str, location: Optional[str] = None) -> list:
        """Get available fulfillment options"""
        availability = self.check_availability(product_id, location)
        options = []
        
        if availability["warehouse"] > 0:
            options.append({
                "type": "Ship to Home",
                "available": True,
                "estimated_time": "2-3 days",
                "cost": 0 if availability["warehouse"] > 5 else 50,
                "description": "Free shipping on orders above ₹500"
            })
        
        if availability["stores"]:
            for store, qty in availability["stores"].items():
                if qty > 0:
                    options.append({
                        "type": "Click & Collect",
                        "available": True,
                        "location": store,
                        "estimated_time": "Same day",
                        "cost": 0,
                        "description": f"Pick up from {store} store today"
                    })
                    
                    options.append({
                        "type": "In-Store Try-on",
                        "available": True,
                        "location": store,
                        "estimated_time": "Visit anytime",
                        "cost": 0,
                        "description": f"Try before you buy at {store}"
                    })
        
        return options
    
    def reserve_stock(self, product_id: str, quantity: int, location: Optional[str] = None) -> Dict:
        """Reserve stock for a product (mock operation)"""
        stock = self.get_stock(product_id)
        
        if not stock:
            return {
                "success": False,
                "message": "Product not found"
            }
        
        # Check if enough stock available
        if location and location in stock["stores"]:
            available = stock["stores"][location]
        else:
            available = stock["warehouse"]
        
        if available >= quantity:
            return {
                "success": True,
                "message": f"Reserved {quantity} units",
                "reservation_id": f"RES_{product_id}_{random.randint(1000, 9999)}"
            }
        else:
            return {
                "success": False,
                "message": f"Only {available} units available"
            }
    
    def get_nearby_stores(self, location: str) -> list:
        """Get nearby stores based on location"""
        # Mock store data
        all_stores = {
            "Mumbai": {
                "name": "Phoenix Mills Store",
                "address": "High Street Phoenix, Lower Parel, Mumbai",
                "distance": "2.5 km",
                "hours": "10 AM - 10 PM"
            },
            "Delhi": {
                "name": "Select Citywalk Store",
                "address": "Saket, New Delhi",
                "distance": "3.2 km",
                "hours": "11 AM - 9 PM"
            },
            "Bangalore": {
                "name": "UB City Store",
                "address": "Vittal Mallya Road, Bangalore",
                "distance": "1.8 km",
                "hours": "10 AM - 9 PM"
            }
        }
        
        if location in all_stores:
            return [all_stores[location]]
        
        return list(all_stores.values())


# Singleton instance
inventory_api = InventoryAPI()
