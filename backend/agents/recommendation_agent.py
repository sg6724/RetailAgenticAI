from typing import Dict, List, Optional
from apis.products_api import products_api


class RecommendationAgent:
    """Agent responsible for product recommendations"""
    
    def __init__(self):
        self.name = "Recommendation Agent"
        self.products_api = products_api
    
    async def execute(self, context: Dict) -> Dict:
        """Execute recommendation logic"""
        try:
            # Extract parameters from context
            category = context.get("category")
            budget = context.get("budget")
            location = context.get("location")
            preferences = context.get("preferences", [])
            customer_id = context.get("customer_id")
            query = context.get("query", "")
            
            # Get recommendations
            if query and not category:
                # Search-based recommendations
                products = self.products_api.search_products(query, limit=5)
            else:
                # Filter-based recommendations
                products = self.products_api.get_recommendations(
                    customer_id=customer_id,
                    category=category,
                    budget=budget,
                    preferences=preferences,
                    limit=5
                )
            
            # Add reasoning for each recommendation
            recommendations = []
            for product in products:
                reasoning = self._generate_reasoning(product, context)
                recommendations.append({
                    **product,
                    "reasoning": reasoning,
                    "confidence_score": self._calculate_confidence(product, context)
                })
            
            return {
                "success": True,
                "agent": self.name,
                "recommendations": recommendations,
                "count": len(recommendations),
                "message": f"Found {len(recommendations)} products matching your preferences"
            }
        
        except Exception as e:
            return {
                "success": False,
                "agent": self.name,
                "error": str(e),
                "message": "Failed to get recommendations"
            }
    
    def _generate_reasoning(self, product: Dict, context: Dict) -> str:
        """Generate reasoning for recommendation"""
        reasons = []
        
        if product.get("is_bestseller"):
            reasons.append("Best seller")
        
        if product.get("is_trending"):
            reasons.append("Trending now")
        
        if product.get("rating", 0) >= 4.5:
            reasons.append(f"Highly rated ({product['rating']}⭐)")
        
        budget = context.get("budget")
        if budget and product["price"] <= budget * 0.8:
            reasons.append("Great value")
        
        if product.get("is_seasonal"):
            reasons.append("Perfect for the season")
        
        return " • ".join(reasons) if reasons else "Recommended for you"
    
    def _calculate_confidence(self, product: Dict, context: Dict) -> float:
        """Calculate confidence score for recommendation"""
        score = 0.5  # Base score
        
        if product.get("is_bestseller"):
            score += 0.15
        
        if product.get("is_trending"):
            score += 0.1
        
        if product.get("rating", 0) >= 4.5:
            score += 0.15
        
        budget = context.get("budget")
        if budget and product["price"] <= budget:
            score += 0.1
        
        return min(score, 1.0)


# Singleton instance
recommendation_agent = RecommendationAgent()
