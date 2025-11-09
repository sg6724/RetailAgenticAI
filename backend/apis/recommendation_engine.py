from typing import List, Dict, Optional
from apis.products_api import products_api
import random


class RecommendationEngine:
    """Advanced recommendation engine for related products"""
    
    def __init__(self):
        self.products_api = products_api
    
    def get_related_products(
        self,
        product_ids: List[str],
        limit: int = 4,
        strategy: str = "collaborative"
    ) -> List[Dict]:
        """Get related products based on cart items"""
        
        if not product_ids:
            return []
        
        # Get cart products
        cart_products = []
        for pid in product_ids:
            product = self.products_api.get_product_by_id(pid)
            if product:
                cart_products.append(product)
        
        if not cart_products:
            return []
        
        # Extract categories and brands from cart
        categories = set(p["category"] for p in cart_products)
        brands = set(p["brand"] for p in cart_products)
        avg_price = sum(p["price"] for p in cart_products) / len(cart_products)
        
        # Get all products
        all_products = self.products_api.products
        
        # Filter out products already in cart
        candidates = [p for p in all_products if p["id"] not in product_ids]
        
        # Score each candidate
        scored_products = []
        for product in candidates:
            score = self._calculate_similarity_score(
                product,
                categories,
                brands,
                avg_price
            )
            scored_products.append((score, product))
        
        # Sort by score and return top N
        scored_products.sort(reverse=True, key=lambda x: x[0])
        
        recommendations = []
        for score, product in scored_products[:limit]:
            product_copy = product.copy()
            product_copy["recommendation_score"] = round(score, 2)
            product_copy["recommendation_reason"] = self._get_recommendation_reason(
                product, categories, brands
            )
            recommendations.append(product_copy)
        
        return recommendations
    
    def _calculate_similarity_score(
        self,
        product: Dict,
        cart_categories: set,
        cart_brands: set,
        avg_price: float
    ) -> float:
        """Calculate similarity score for a product"""
        score = 0.0
        
        # Same category bonus
        if product["category"] in cart_categories:
            score += 0.4
        
        # Same brand bonus
        if product["brand"] in cart_brands:
            score += 0.2
        
        # Price similarity (within 50% range)
        price_diff = abs(product["price"] - avg_price) / avg_price
        if price_diff < 0.5:
            score += 0.2 * (1 - price_diff)
        
        # Rating bonus
        score += product["rating"] * 0.05
        
        # Trending/bestseller bonus
        if product.get("is_trending"):
            score += 0.1
        if product.get("is_bestseller"):
            score += 0.1
        
        return score
    
    def _get_recommendation_reason(
        self,
        product: Dict,
        cart_categories: set,
        cart_brands: set
    ) -> str:
        """Generate human-readable recommendation reason"""
        reasons = []
        
        if product["category"] in cart_categories:
            reasons.append("Matches your style")
        
        if product["brand"] in cart_brands:
            reasons.append(f"From {product['brand']}")
        
        if product.get("is_bestseller"):
            reasons.append("Best seller")
        
        if product.get("is_trending"):
            reasons.append("Trending now")
        
        if product["rating"] >= 4.5:
            reasons.append("Highly rated")
        
        return " • ".join(reasons) if reasons else "Recommended for you"
    
    def get_frequently_bought_together(
        self,
        product_id: str,
        limit: int = 3
    ) -> List[Dict]:
        """Get products frequently bought together"""
        
        product = self.products_api.get_product_by_id(product_id)
        if not product:
            return []
        
        # Get complementary products based on category
        complementary_map = {
            "jackets": ["sweaters", "shirts"],
            "shirts": ["jeans", "jackets"],
            "jeans": ["shirts", "sweaters"],
            "sweaters": ["jackets", "jeans"]
        }
        
        target_categories = complementary_map.get(
            product["category"],
            ["jackets", "shirts"]
        )
        
        candidates = []
        for cat in target_categories:
            products = self.products_api.get_products(category=cat, limit=5)
            candidates.extend(products)
        
        # Filter and score
        scored = []
        for p in candidates:
            if p["id"] != product_id:
                score = p["rating"] + (0.5 if p.get("is_bestseller") else 0)
                scored.append((score, p))
        
        scored.sort(reverse=True, key=lambda x: x[0])
        
        result = []
        for _, p in scored[:limit]:
            p_copy = p.copy()
            p_copy["recommendation_reason"] = "Frequently bought together"
            result.append(p_copy)
        
        return result
    
    def get_complete_the_look(
        self,
        product_ids: List[str],
        limit: int = 3
    ) -> List[Dict]:
        """Get products to complete the look"""
        
        if not product_ids:
            return []
        
        # Get cart products
        cart_products = []
        for pid in product_ids:
            product = self.products_api.get_product_by_id(pid)
            if product:
                cart_products.append(product)
        
        # Find missing categories for a complete outfit
        cart_categories = set(p["category"] for p in cart_products)
        all_outfit_categories = {"jackets", "shirts", "jeans", "sweaters"}
        missing_categories = all_outfit_categories - cart_categories
        
        if not missing_categories:
            # If outfit is complete, suggest accessories or alternatives
            return self.get_related_products(product_ids, limit)
        
        # Get products from missing categories
        suggestions = []
        for category in missing_categories:
            products = self.products_api.get_products(
                category=category,
                sort="rating",
                limit=2
            )
            for p in products:
                p_copy = p.copy()
                p_copy["recommendation_reason"] = f"Complete your look with {category}"
                suggestions.append(p_copy)
        
        return suggestions[:limit]


# Singleton instance
recommendation_engine = RecommendationEngine()
