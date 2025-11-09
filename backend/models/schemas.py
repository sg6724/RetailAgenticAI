from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class LoyaltyTier(str, Enum):
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = "Platinum"


class FulfillmentOption(str, Enum):
    SHIP_TO_HOME = "Ship to Home"
    CLICK_AND_COLLECT = "Click & Collect"
    IN_STORE_TRYON = "In-Store Try-on"


class PaymentMethod(str, Enum):
    UPI = "UPI"
    CARD = "Card"
    WALLET = "Wallet"


class ProductBase(BaseModel):
    id: str
    name: str
    price: float
    rating: float
    image_url: str
    description: str
    category: str
    brand: str
    sizes: List[str]
    colors: List[str]
    is_trending: bool = False
    is_seasonal: bool = False
    is_bestseller: bool = False


class StockInfo(BaseModel):
    warehouse: int
    stores: Dict[str, int]


class ProductWithStock(ProductBase):
    stock: StockInfo


class CartItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    price: float
    size: Optional[str] = None
    color: Optional[str] = None


class Cart(BaseModel):
    items: List[CartItem]
    subtotal: float


class LoyaltyInfo(BaseModel):
    tier: LoyaltyTier
    points: int
    discount_percentage: float
    available_coupons: List[str]


class PricingBreakdown(BaseModel):
    original_price: float
    discount_amount: float
    discount_percentage: float
    final_price: float
    points_to_earn: int


class QueryRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    customer_id: Optional[str] = None


class AgentResponse(BaseModel):
    message: str
    products: Optional[List[ProductWithStock]] = None
    pricing: Optional[PricingBreakdown] = None
    fulfillment_options: Optional[List[Dict[str, Any]]] = None
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ConversationMessage(BaseModel):
    role: str  # "user" or "agent"
    message: str
    timestamp: datetime
    products: Optional[List[ProductWithStock]] = None


class SessionContext(BaseModel):
    session_id: str
    customer_id: Optional[str] = None
    conversation_history: List[ConversationMessage]
    active_cart: Cart
    context: Dict[str, Any]
    last_updated: datetime
    ttl: int = 86400


class OrderRequest(BaseModel):
    session_id: str
    customer_id: str
    payment_method: PaymentMethod
    fulfillment_option: FulfillmentOption
    delivery_address: Optional[str] = None
    store_location: Optional[str] = None


class OrderConfirmation(BaseModel):
    order_id: str
    total_amount: float
    payment_status: str
    transaction_id: str
    fulfillment_details: Dict[str, Any]
    estimated_delivery: Optional[str] = None
    timestamp: datetime


class FeedbackRequest(BaseModel):
    order_id: str
    customer_id: str
    rating: int = Field(ge=1, le=5)
    feedback_text: Optional[str] = None


class RecommendationRequest(BaseModel):
    customer_id: Optional[str] = None
    category: Optional[str] = None
    budget: Optional[float] = None
    location: Optional[str] = None
    preferences: Optional[List[str]] = None
