from typing import Dict, List, Optional
from datetime import datetime, timedelta


class LoyaltyAPI:
    def __init__(self):
        self.tier_benefits = {
            "Silver": {"discount": 0.10, "points_multiplier": 1.0, "free_shipping": False},
            "Gold": {"discount": 0.15, "points_multiplier": 1.5, "free_shipping": True},
            "Platinum": {"discount": 0.20, "points_multiplier": 2.0, "free_shipping": True}
        }
        
        self.tier_thresholds = {
            "Silver": 0,
            "Gold": 10000,
            "Platinum": 50000
        }
    
    def get_customer_loyalty(self, customer_id: str) -> Dict:
        """Get customer loyalty information"""
        # Mock customer data
        mock_customers = {
            "C123": {
                "tier": "Silver",
                "points": 98,
                "lifetime_spend": 8500,
                "available_coupons": ["FESTIVAL5", "WELCOME10"],
                "next_tier": "Gold",
                "points_to_next_tier": 1500
            },
            "C456": {
                "tier": "Gold",
                "points": 2500,
                "lifetime_spend": 25000,
                "available_coupons": ["VIP15", "BIRTHDAY20"],
                "next_tier": "Platinum",
                "points_to_next_tier": 25000
            },
            "C789": {
                "tier": "Platinum",
                "points": 8000,
                "lifetime_spend": 75000,
                "available_coupons": ["PLATINUM25", "EXCLUSIVE30"],
                "next_tier": None,
                "points_to_next_tier": 0
            }
        }
        
        # Default for new customers
        if customer_id not in mock_customers:
            return {
                "tier": "Silver",
                "points": 0,
                "lifetime_spend": 0,
                "available_coupons": ["WELCOME10"],
                "next_tier": "Gold",
                "points_to_next_tier": 10000
            }
        
        return mock_customers[customer_id]
    
    def calculate_discount(self, customer_id: str, amount: float) -> Dict:
        """Calculate discount based on loyalty tier"""
        loyalty = self.get_customer_loyalty(customer_id)
        tier = loyalty["tier"]
        
        discount_percentage = self.tier_benefits[tier]["discount"]
        discount_amount = amount * discount_percentage
        final_amount = amount - discount_amount
        
        return {
            "original_amount": amount,
            "discount_percentage": discount_percentage * 100,
            "discount_amount": round(discount_amount, 2),
            "final_amount": round(final_amount, 2),
            "tier": tier
        }
    
    def apply_coupon(self, customer_id: str, coupon_code: str, amount: float) -> Dict:
        """Apply coupon code"""
        # Mock coupon data
        coupons = {
            "FESTIVAL5": {"discount": 0.05, "min_purchase": 1000, "max_discount": 500},
            "WELCOME10": {"discount": 0.10, "min_purchase": 500, "max_discount": 200},
            "VIP15": {"discount": 0.15, "min_purchase": 2000, "max_discount": 1000},
            "BIRTHDAY20": {"discount": 0.20, "min_purchase": 1500, "max_discount": 1500},
            "PLATINUM25": {"discount": 0.25, "min_purchase": 5000, "max_discount": 3000},
            "EXCLUSIVE30": {"discount": 0.30, "min_purchase": 10000, "max_discount": 5000}
        }
        
        if coupon_code not in coupons:
            return {
                "valid": False,
                "message": "Invalid coupon code"
            }
        
        coupon = coupons[coupon_code]
        
        if amount < coupon["min_purchase"]:
            return {
                "valid": False,
                "message": f"Minimum purchase of ₹{coupon['min_purchase']} required"
            }
        
        discount_amount = min(amount * coupon["discount"], coupon["max_discount"])
        
        return {
            "valid": True,
            "coupon_code": coupon_code,
            "discount_amount": round(discount_amount, 2),
            "discount_percentage": coupon["discount"] * 100,
            "message": "Coupon applied successfully"
        }
    
    def calculate_final_pricing(
        self,
        customer_id: str,
        subtotal: float,
        coupon_code: Optional[str] = None
    ) -> Dict:
        """Calculate final pricing with tier discount and coupon"""
        
        # Apply tier discount
        tier_discount = self.calculate_discount(customer_id, subtotal)
        amount_after_tier = tier_discount["final_amount"]
        
        # Apply coupon if provided
        coupon_discount = 0
        coupon_valid = False
        coupon_message = ""
        
        if coupon_code:
            coupon_result = self.apply_coupon(customer_id, coupon_code, amount_after_tier)
            if coupon_result["valid"]:
                coupon_discount = coupon_result["discount_amount"]
                coupon_valid = True
                coupon_message = coupon_result["message"]
            else:
                coupon_message = coupon_result["message"]
        
        final_amount = amount_after_tier - coupon_discount
        total_discount = tier_discount["discount_amount"] + coupon_discount
        
        # Calculate points to earn
        loyalty = self.get_customer_loyalty(customer_id)
        tier = loyalty["tier"]
        points_multiplier = self.tier_benefits[tier]["points_multiplier"]
        points_to_earn = int(final_amount * 0.01 * points_multiplier)  # 1% of amount as points
        
        return {
            "subtotal": subtotal,
            "tier_discount": {
                "percentage": tier_discount["discount_percentage"],
                "amount": tier_discount["discount_amount"],
                "tier": tier
            },
            "coupon_discount": {
                "applied": coupon_valid,
                "code": coupon_code if coupon_valid else None,
                "amount": coupon_discount,
                "message": coupon_message
            },
            "total_discount": round(total_discount, 2),
            "final_amount": round(final_amount, 2),
            "points_to_earn": points_to_earn,
            "savings": round(total_discount, 2)
        }
    
    def add_points(self, customer_id: str, points: int) -> Dict:
        """Add loyalty points to customer account"""
        loyalty = self.get_customer_loyalty(customer_id)
        new_points = loyalty["points"] + points
        
        return {
            "success": True,
            "previous_points": loyalty["points"],
            "points_added": points,
            "new_points": new_points,
            "tier": loyalty["tier"]
        }
    
    def get_available_coupons(self, customer_id: str) -> List[Dict]:
        """Get all available coupons for customer"""
        loyalty = self.get_customer_loyalty(customer_id)
        
        coupon_details = {
            "FESTIVAL5": {
                "code": "FESTIVAL5",
                "description": "5% off on orders above ₹1000",
                "discount": "5%",
                "min_purchase": 1000,
                "expires": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            },
            "WELCOME10": {
                "code": "WELCOME10",
                "description": "10% off for new customers",
                "discount": "10%",
                "min_purchase": 500,
                "expires": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            },
            "VIP15": {
                "code": "VIP15",
                "description": "15% off for Gold members",
                "discount": "15%",
                "min_purchase": 2000,
                "expires": (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
            },
            "BIRTHDAY20": {
                "code": "BIRTHDAY20",
                "description": "20% birthday special discount",
                "discount": "20%",
                "min_purchase": 1500,
                "expires": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
            },
            "PLATINUM25": {
                "code": "PLATINUM25",
                "description": "25% off for Platinum members",
                "discount": "25%",
                "min_purchase": 5000,
                "expires": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            },
            "EXCLUSIVE30": {
                "code": "EXCLUSIVE30",
                "description": "30% exclusive member discount",
                "discount": "30%",
                "min_purchase": 10000,
                "expires": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            }
        }
        
        available = []
        for coupon_code in loyalty["available_coupons"]:
            if coupon_code in coupon_details:
                available.append(coupon_details[coupon_code])
        
        return available


# Singleton instance
loyalty_api = LoyaltyAPI()
