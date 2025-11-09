from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import uvicorn
import os
from dotenv import load_dotenv

from models.schemas import (
    QueryRequest, AgentResponse, OrderRequest, OrderConfirmation,
    FeedbackRequest, CartItem
)
from agents.master_agent import master_agent
from utils.redis_manager import redis_manager
from apis.products_api import products_api
from apis.inventory_api import inventory_api
from apis.payment_api import payment_api
from apis.loyalty_api import loyalty_api
from apis.recommendation_engine import recommendation_engine
import random
import string
from datetime import datetime

load_dotenv()

app = FastAPI(
    title="AI Retail Sales Agent",
    description="Multi-channel AI-driven conversational sales platform",
    version="1.0.0"
)

# CORS Configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)


manager = ConnectionManager()


@app.get("/")
async def root():
    return {
        "message": "AI Retail Sales Agent API",
        "version": "1.0.0",
        "status": "active"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


# Chat endpoint
@app.post("/api/chat")
async def chat(request: QueryRequest):
    """Process user query through master agent"""
    try:
        response = await master_agent.process_query(
            user_message=request.message,
            session_id=request.session_id,
            customer_id=request.customer_id
        )
        
        return JSONResponse(content=response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# WebSocket endpoint for real-time chat
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await manager.connect(websocket)
    session_id = None
    
    try:
        while True:
            data = await websocket.receive_json()
            
            message = data.get("message")
            session_id = data.get("session_id")
            customer_id = data.get("customer_id")
            
            if not message:
                await manager.send_message(
                    {"error": "Message is required"},
                    websocket
                )
                continue
            
            # Process through master agent
            response = await master_agent.process_query(
                user_message=message,
                session_id=session_id,
                customer_id=customer_id
            )
            
            await manager.send_message(response, websocket)
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        await manager.send_message(
            {"error": str(e)},
            websocket
        )
        manager.disconnect(websocket)


# Products endpoints
@app.get("/api/products")
async def get_products(
    category: Optional[str] = None,
    budget: Optional[float] = None,
    sort: Optional[str] = "trending",
    limit: int = 10
):
    """Get products with filters"""
    try:
        products = products_api.get_products(category, budget, sort, limit)
        return {"success": True, "products": products, "count": len(products)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/products/{product_id}")
async def get_product(product_id: str):
    """Get single product by ID"""
    try:
        product = products_api.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"success": True, "product": product}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/products/search/{query}")
async def search_products(query: str, limit: int = 10):
    """Search products"""
    try:
        products = products_api.search_products(query, limit)
        return {"success": True, "products": products, "count": len(products)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Inventory endpoints
@app.get("/api/inventory/{product_id}")
async def get_inventory(product_id: str, location: Optional[str] = None):
    """Get inventory for product"""
    try:
        availability = inventory_api.check_availability(product_id, location)
        fulfillment_options = inventory_api.get_fulfillment_options(product_id, location)
        
        return {
            "success": True,
            "product_id": product_id,
            "availability": availability,
            "fulfillment_options": fulfillment_options
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Cart endpoints
@app.post("/api/cart/add")
async def add_to_cart(session_id: str, item: CartItem):
    """Add item to cart"""
    try:
        session_data = redis_manager.get_session(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        cart = session_data.get("active_cart", {"items": [], "subtotal": 0})
        
        # Check if item already exists
        existing_item = None
        for cart_item in cart["items"]:
            if cart_item["product_id"] == item.product_id:
                existing_item = cart_item
                break
        
        if existing_item:
            existing_item["quantity"] += item.quantity
        else:
            cart["items"].append(item.dict())
        
        # Recalculate subtotal
        cart["subtotal"] = sum(i["price"] * i["quantity"] for i in cart["items"])
        
        session_data["active_cart"] = cart
        redis_manager.set_session(session_id, session_data)
        
        return {"success": True, "cart": cart}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/cart/{session_id}")
async def get_cart(session_id: str):
    """Get cart contents"""
    try:
        session_data = redis_manager.get_session(session_id)
        if not session_data:
            return {"success": True, "cart": {"items": [], "subtotal": 0}}
        
        cart = session_data.get("active_cart", {"items": [], "subtotal": 0})
        return {"success": True, "cart": cart}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/cart/{session_id}/item/{product_id}")
async def remove_from_cart(session_id: str, product_id: str):
    """Remove item from cart"""
    try:
        session_data = redis_manager.get_session(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        cart = session_data.get("active_cart", {"items": [], "subtotal": 0})
        cart["items"] = [i for i in cart["items"] if i["product_id"] != product_id]
        cart["subtotal"] = sum(i["price"] * i["quantity"] for i in cart["items"])
        
        session_data["active_cart"] = cart
        redis_manager.set_session(session_id, session_data)
        
        return {"success": True, "cart": cart}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Checkout and Order endpoints
@app.post("/api/checkout")
async def checkout(order_request: OrderRequest):
    """Process checkout"""
    try:
        session_data = redis_manager.get_session(order_request.session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        cart = session_data.get("active_cart", {"items": [], "subtotal": 0})
        if not cart["items"]:
            raise HTTPException(status_code=400, detail="Cart is empty")
        
        # Calculate final pricing with loyalty
        pricing = loyalty_api.calculate_final_pricing(
            customer_id=order_request.customer_id,
            subtotal=cart["subtotal"]
        )
        
        # Process payment
        payment_result = payment_api.process_payment(
            customer_id=order_request.customer_id,
            method_id="default",
            method_type=order_request.payment_method.value,
            amount=pricing["final_amount"],
            order_id=f"ORD{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}"
        )
        
        if not payment_result["success"]:
            raise HTTPException(status_code=400, detail="Payment failed")
        
        # Generate order ID
        order_id = payment_result["transaction_id"].replace("TXN", "ORD")
        
        # Prepare fulfillment details
        fulfillment_details = {
            "type": order_request.fulfillment_option.value,
            "delivery_address": order_request.delivery_address,
            "store_location": order_request.store_location,
            "estimated_delivery": "2-3 days" if order_request.fulfillment_option.value == "Ship to Home" else "Same day"
        }
        
        # Add loyalty points
        loyalty_api.add_points(order_request.customer_id, pricing["points_to_earn"])
        
        # Clear cart
        session_data["active_cart"] = {"items": [], "subtotal": 0}
        redis_manager.set_session(order_request.session_id, session_data)
        
        order_confirmation = {
            "order_id": order_id,
            "total_amount": pricing["final_amount"],
            "payment_status": "success",
            "transaction_id": payment_result["transaction_id"],
            "fulfillment_details": fulfillment_details,
            "estimated_delivery": fulfillment_details["estimated_delivery"],
            "timestamp": datetime.now().isoformat()
        }
        
        return {"success": True, "order": order_confirmation}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Loyalty endpoints
@app.get("/api/loyalty/{customer_id}")
async def get_loyalty(customer_id: str):
    """Get customer loyalty information"""
    try:
        loyalty_info = loyalty_api.get_customer_loyalty(customer_id)
        coupons = loyalty_api.get_available_coupons(customer_id)
        
        return {
            "success": True,
            "loyalty": loyalty_info,
            "coupons": coupons
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Feedback endpoint
@app.post("/api/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """Submit customer feedback"""
    try:
        from agents.support_agent import support_agent
        
        result = await support_agent.submit_feedback(
            order_id=feedback.order_id,
            customer_id=feedback.customer_id,
            rating=feedback.rating,
            feedback_text=feedback.feedback_text
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Session endpoint
@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """Get session data"""
    try:
        session_data = redis_manager.get_session(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return {"success": True, "session": session_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Recommendation endpoints
@app.get("/api/recommendations/related")
async def get_related_products(product_ids: str, limit: int = 4):
    """Get related products based on cart items"""
    try:
        ids = product_ids.split(',')
        recommendations = recommendation_engine.get_related_products(ids, limit)
        return {"success": True, "recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/recommendations/frequently-bought/{product_id}")
async def get_frequently_bought(product_id: str, limit: int = 3):
    """Get products frequently bought together"""
    try:
        recommendations = recommendation_engine.get_frequently_bought_together(product_id, limit)
        return {"success": True, "recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/recommendations/complete-look")
async def get_complete_look(product_ids: str, limit: int = 3):
    """Get products to complete the look"""
    try:
        ids = product_ids.split(',')
        recommendations = recommendation_engine.get_complete_the_look(ids, limit)
        return {"success": True, "recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
