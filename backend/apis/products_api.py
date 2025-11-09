from typing import List, Optional
from models.schemas import ProductBase, ProductWithStock, StockInfo
import random

# Mock product catalog
MOCK_PRODUCTS = [
    {
        "id": "P001",
        "name": "Urban Winter Jacket - Premium",
        "price": 3999,
        "rating": 4.5,
        "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
        "description": "Premium winter jacket with waterproof exterior and thermal lining. Perfect for cold weather.",
        "category": "jackets",
        "brand": "UrbanWear",
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Black", "Navy", "Grey"],
        "is_trending": True,
        "is_seasonal": True,
        "is_bestseller": True
    },
    {
        "id": "P002",
        "name": "Classic Denim Jacket",
        "price": 2499,
        "rating": 4.3,
        "image_url": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=400",
        "description": "Timeless denim jacket with modern fit. Versatile for all seasons.",
        "category": "jackets",
        "brand": "DenimCo",
        "sizes": ["S", "M", "L", "XL", "XXL"],
        "colors": ["Blue", "Black", "Light Blue"],
        "is_trending": True,
        "is_seasonal": False,
        "is_bestseller": False
    },
    {
        "id": "P003",
        "name": "Bomber Jacket - Sporty",
        "price": 4499,
        "rating": 4.7,
        "image_url": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400",
        "description": "Stylish bomber jacket with ribbed cuffs and hem. Lightweight yet warm.",
        "category": "jackets",
        "brand": "SportStyle",
        "sizes": ["M", "L", "XL"],
        "colors": ["Olive", "Black", "Maroon"],
        "is_trending": False,
        "is_seasonal": True,
        "is_bestseller": True
    },
    {
        "id": "P004",
        "name": "Leather Biker Jacket",
        "price": 7999,
        "rating": 4.8,
        "image_url": "https://images.unsplash.com/photo-1520975954732-35dd22299614?w=400",
        "description": "Genuine leather biker jacket with asymmetric zipper. Premium quality.",
        "category": "jackets",
        "brand": "LeatherLux",
        "sizes": ["S", "M", "L"],
        "colors": ["Black", "Brown"],
        "is_trending": True,
        "is_seasonal": False,
        "is_bestseller": False
    },
    {
        "id": "P005",
        "name": "Puffer Jacket - Ultra Warm",
        "price": 4799,
        "rating": 4.6,
        "image_url": "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=400",
        "description": "Ultra-warm puffer jacket with down filling. Water-resistant outer shell.",
        "category": "jackets",
        "brand": "WarmTech",
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Red", "Black", "Navy"],
        "is_trending": True,
        "is_seasonal": True,
        "is_bestseller": True
    },
    {
        "id": "P006",
        "name": "Casual Cotton Shirt",
        "price": 1299,
        "rating": 4.2,
        "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400",
        "description": "Comfortable cotton shirt for everyday wear. Breathable fabric.",
        "category": "shirts",
        "brand": "CasualFit",
        "sizes": ["S", "M", "L", "XL", "XXL"],
        "colors": ["White", "Blue", "Pink", "Grey"],
        "is_trending": False,
        "is_seasonal": False,
        "is_bestseller": True
    },
    {
        "id": "P007",
        "name": "Formal Oxford Shirt",
        "price": 1899,
        "rating": 4.4,
        "image_url": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400",
        "description": "Classic Oxford shirt for formal occasions. Wrinkle-resistant fabric.",
        "category": "shirts",
        "brand": "FormalWear",
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["White", "Light Blue", "Pink"],
        "is_trending": False,
        "is_seasonal": False,
        "is_bestseller": False
    },
    {
        "id": "P008",
        "name": "Slim Fit Jeans - Dark Blue",
        "price": 2199,
        "rating": 4.5,
        "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400",
        "description": "Comfortable slim fit jeans with stretch fabric. Perfect fit guaranteed.",
        "category": "jeans",
        "brand": "DenimCo",
        "sizes": ["28", "30", "32", "34", "36"],
        "colors": ["Dark Blue", "Black", "Light Blue"],
        "is_trending": True,
        "is_seasonal": False,
        "is_bestseller": True
    },
    {
        "id": "P009",
        "name": "Relaxed Fit Jeans",
        "price": 1999,
        "rating": 4.3,
        "image_url": "https://images.unsplash.com/photo-1475178626620-a4d074967452?w=400",
        "description": "Relaxed fit jeans for maximum comfort. Classic style.",
        "category": "jeans",
        "brand": "ComfortDenim",
        "sizes": ["28", "30", "32", "34", "36", "38"],
        "colors": ["Blue", "Black", "Grey"],
        "is_trending": False,
        "is_seasonal": False,
        "is_bestseller": False
    },
    {
        "id": "P010",
        "name": "Wool Sweater - Cable Knit",
        "price": 3299,
        "rating": 4.7,
        "image_url": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400",
        "description": "Cozy wool sweater with cable knit pattern. Perfect for winter.",
        "category": "sweaters",
        "brand": "WoolCraft",
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Cream", "Navy", "Burgundy"],
        "is_trending": True,
        "is_seasonal": True,
        "is_bestseller": True
    }
]


class ProductsAPI:
    def __init__(self):
        self.products = MOCK_PRODUCTS
    
    def get_products(
        self,
        category: Optional[str] = None,
        budget: Optional[float] = None,
        sort: Optional[str] = "trending",
        limit: int = 10
    ) -> List[dict]:
        """Get products with filters"""
        filtered = self.products.copy()
        
        # Filter by category
        if category:
            filtered = [p for p in filtered if p["category"].lower() == category.lower()]
        
        # Filter by budget
        if budget:
            filtered = [p for p in filtered if p["price"] <= budget]
        
        # Sort
        if sort == "trending":
            filtered.sort(key=lambda x: (x["is_trending"], x["rating"]), reverse=True)
        elif sort == "price_low":
            filtered.sort(key=lambda x: x["price"])
        elif sort == "price_high":
            filtered.sort(key=lambda x: x["price"], reverse=True)
        elif sort == "rating":
            filtered.sort(key=lambda x: x["rating"], reverse=True)
        
        return filtered[:limit]
    
    def get_product_by_id(self, product_id: str) -> Optional[dict]:
        """Get single product by ID"""
        for product in self.products:
            if product["id"] == product_id:
                return product
        return None
    
    def search_products(self, query: str, limit: int = 10) -> List[dict]:
        """Search products by query"""
        query_lower = query.lower()
        results = []
        
        for product in self.products:
            if (query_lower in product["name"].lower() or
                query_lower in product["description"].lower() or
                query_lower in product["category"].lower() or
                query_lower in product["brand"].lower()):
                results.append(product)
        
        return results[:limit]
    
    def get_recommendations(
        self,
        customer_id: Optional[str] = None,
        category: Optional[str] = None,
        budget: Optional[float] = None,
        preferences: Optional[List[str]] = None,
        limit: int = 5
    ) -> List[dict]:
        """Get personalized recommendations"""
        # Start with filtered products
        candidates = self.get_products(category=category, budget=budget, limit=20)
        
        # Prioritize trending and bestsellers
        scored = []
        for product in candidates:
            score = product["rating"]
            if product["is_trending"]:
                score += 0.5
            if product["is_bestseller"]:
                score += 0.3
            if product["is_seasonal"]:
                score += 0.2
            scored.append((score, product))
        
        scored.sort(reverse=True, key=lambda x: x[0])
        return [p for _, p in scored[:limit]]


# Singleton instance
products_api = ProductsAPI()
