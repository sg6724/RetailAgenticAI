from typing import Dict, List, Optional
import random
import string
from datetime import datetime


class PaymentAPI:
    def __init__(self):
        self.supported_methods = ["UPI", "Card", "Wallet"]
    
    def get_payment_methods(self, customer_id: str) -> List[Dict]:
        """Get available payment methods for customer"""
        # Mock saved payment methods
        methods = [
            {
                "type": "UPI",
                "id": "upi_1",
                "display": "UPI (Google Pay, PhonePe, Paytm)",
                "icon": "upi",
                "saved": False,
                "limit": None
            },
            {
                "type": "Card",
                "id": "card_1",
                "display": "Credit/Debit Card",
                "icon": "card",
                "saved": True,
                "last4": "4242",
                "brand": "Visa",
                "limit": 100000
            },
            {
                "type": "Card",
                "id": "card_2",
                "display": "Credit Card",
                "icon": "card",
                "saved": True,
                "last4": "8888",
                "brand": "Mastercard",
                "limit": 50000
            },
            {
                "type": "Wallet",
                "id": "wallet_1",
                "display": "Paytm Wallet",
                "icon": "wallet",
                "saved": True,
                "balance": 5000,
                "limit": 10000
            },
            {
                "type": "Wallet",
                "id": "wallet_2",
                "display": "Amazon Pay",
                "icon": "wallet",
                "saved": True,
                "balance": 2500,
                "limit": 10000
            }
        ]
        
        return methods
    
    def validate_payment_method(self, method_id: str, amount: float) -> Dict:
        """Validate if payment method can process the amount"""
        # Mock validation
        if amount <= 0:
            return {
                "valid": False,
                "message": "Invalid amount"
            }
        
        if amount > 100000:
            return {
                "valid": False,
                "message": "Amount exceeds maximum transaction limit"
            }
        
        return {
            "valid": True,
            "message": "Payment method validated"
        }
    
    def process_payment(
        self,
        customer_id: str,
        method_id: str,
        method_type: str,
        amount: float,
        order_id: str
    ) -> Dict:
        """Process payment (mock)"""
        
        # Validate
        validation = self.validate_payment_method(method_id, amount)
        if not validation["valid"]:
            return {
                "success": False,
                "status": "failed",
                "message": validation["message"]
            }
        
        # Simulate payment processing
        # In real scenario, this would call actual payment gateway
        transaction_id = self._generate_transaction_id()
        
        # Mock success (95% success rate)
        success = random.random() < 0.95
        
        if success:
            return {
                "success": True,
                "status": "success",
                "transaction_id": transaction_id,
                "method_type": method_type,
                "amount": amount,
                "timestamp": datetime.now().isoformat(),
                "message": "Payment processed successfully"
            }
        else:
            return {
                "success": False,
                "status": "failed",
                "message": "Payment declined. Please try another method.",
                "error_code": "PAYMENT_DECLINED"
            }
    
    def initiate_payment(
        self,
        customer_id: str,
        method_type: str,
        amount: float,
        order_id: str
    ) -> Dict:
        """Initiate payment process"""
        
        # Generate payment session
        payment_session_id = self._generate_session_id()
        
        return {
            "payment_session_id": payment_session_id,
            "amount": amount,
            "currency": "INR",
            "method_type": method_type,
            "order_id": order_id,
            "expires_at": "15 minutes",
            "redirect_url": f"/payment/confirm/{payment_session_id}"
        }
    
    def verify_payment(self, transaction_id: str) -> Dict:
        """Verify payment status"""
        # Mock verification
        return {
            "verified": True,
            "transaction_id": transaction_id,
            "status": "completed",
            "timestamp": datetime.now().isoformat()
        }
    
    def refund_payment(self, transaction_id: str, amount: float, reason: str) -> Dict:
        """Process refund (mock)"""
        refund_id = self._generate_refund_id()
        
        return {
            "success": True,
            "refund_id": refund_id,
            "transaction_id": transaction_id,
            "amount": amount,
            "status": "processing",
            "estimated_time": "5-7 business days",
            "message": "Refund initiated successfully"
        }
    
    def _generate_transaction_id(self) -> str:
        """Generate mock transaction ID"""
        return f"TXN{''.join(random.choices(string.ascii_uppercase + string.digits, k=12))}"
    
    def _generate_session_id(self) -> str:
        """Generate payment session ID"""
        return f"PAY{''.join(random.choices(string.ascii_uppercase + string.digits, k=16))}"
    
    def _generate_refund_id(self) -> str:
        """Generate refund ID"""
        return f"REF{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}"


# Singleton instance
payment_api = PaymentAPI()
