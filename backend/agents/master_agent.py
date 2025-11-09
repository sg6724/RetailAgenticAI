from typing import Dict, List, Optional, Any
import asyncio
from datetime import datetime
import uuid

from utils.gemini_config import analyze_intent, generate_natural_response
from utils.redis_manager import redis_manager
from agents.recommendation_agent import recommendation_agent
from agents.inventory_agent import inventory_agent
from agents.payment_agent import payment_agent
from agents.loyalty_agent import loyalty_agent
from agents.fulfillment_agent import fulfillment_agent
from agents.support_agent import support_agent


class MasterAgent:
    """Master orchestrator agent using LangGraph-inspired workflow"""
    
    def __init__(self):
        self.name = "Master Sales Agent"
        self.agents = {
            "recommendation": recommendation_agent,
            "inventory": inventory_agent,
            "payment": payment_agent,
            "loyalty": loyalty_agent,
            "fulfillment": fulfillment_agent,
            "support": support_agent
        }
    
    async def process_query(self, user_message: str, session_id: Optional[str] = None, customer_id: Optional[str] = None) -> Dict:
        """Main orchestration method"""
        try:
            print(f"\n🤖 Master Agent Processing: '{user_message}'")
            
            # Generate or retrieve session
            if not session_id:
                session_id = str(uuid.uuid4())
            
            # Get session context
            session_data = redis_manager.get_session(session_id)
            if not session_data:
                session_data = self._initialize_session(session_id, customer_id)
            
            # Step 1: Intent Recognition using Gemini
            print(f"📊 Step 1: Analyzing intent with Gemini...")
            intent_data = analyze_intent(user_message)
            intent = intent_data.get("intent", "product_search")
            entities = intent_data.get("entities", {})
            print(f"✓ Intent: {intent}, Entities: {entities}")
            
            # Step 2: Update context with new information
            context = self._build_context(session_data, user_message, intent, entities, customer_id)
            
            # Step 3: Agent Selection and Parallel Execution
            agent_results = await self._execute_agents(intent, context)
            
            # Step 4: Response Aggregation
            aggregated_response = self._aggregate_responses(agent_results, context)
            
            # Step 5: Natural Language Generation using Gemini
            print(f"💬 Step 5: Generating natural response with Gemini...")
            natural_response = self._generate_response(aggregated_response, context, intent)
            print(f"✓ Response generated: {natural_response['message'][:100]}...")
            
            # Step 6: Update Session State
            self._update_session(session_id, user_message, natural_response, context, aggregated_response)
            
            return {
                "success": True,
                "session_id": session_id,
                "message": natural_response["message"],
                "products": natural_response.get("products"),
                "pricing": natural_response.get("pricing"),
                "fulfillment_options": natural_response.get("fulfillment_options"),
                "payment_methods": natural_response.get("payment_methods"),
                "loyalty_info": natural_response.get("loyalty_info"),
                "intent": intent,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            print(f"Master agent error: {e}")
            return {
                "success": False,
                "message": "I apologize, but I encountered an issue processing your request. Please try again.",
                "error": str(e)
            }
    
    def _initialize_session(self, session_id: str, customer_id: Optional[str]) -> Dict:
        """Initialize new session"""
        session_data = {
            "session_id": session_id,
            "customer_id": customer_id or f"GUEST_{uuid.uuid4().hex[:8]}",
            "conversation_history": [],
            "active_cart": {"items": [], "subtotal": 0},
            "context": {},
            "last_updated": datetime.now().isoformat(),
            "ttl": 86400
        }
        redis_manager.set_session(session_id, session_data)
        return session_data
    
    def _build_context(self, session_data: Dict, user_message: str, intent: str, entities: Dict, customer_id: Optional[str]) -> Dict:
        """Build context for agent execution"""
        context = session_data.get("context", {}).copy()
        
        # Update with new entities
        context.update(entities)
        context["intent"] = intent
        context["query"] = user_message
        context["customer_id"] = customer_id or session_data.get("customer_id")
        context["cart"] = session_data.get("active_cart", {"items": [], "subtotal": 0})
        
        return context
    
    async def _execute_agents(self, intent: str, context: Dict) -> Dict:
        """Execute relevant agents based on intent"""
        results = {}
        
        # Define agent execution strategy based on intent
        if intent == "product_search" or intent == "product_details":
            # Parallel execution: Recommendation + Inventory
            product_ids = context.get("product_ids", [])
            
            # Get recommendations first
            rec_result = await self.agents["recommendation"].execute(context)
            results["recommendation"] = rec_result
            
            # If we have products, check inventory
            if rec_result.get("success") and rec_result.get("recommendations"):
                product_ids = [p["id"] for p in rec_result["recommendations"]]
                context["product_ids"] = product_ids
                
                inv_result = await self.agents["inventory"].execute(context)
                results["inventory"] = inv_result
        
        elif intent == "add_to_cart":
            # Check inventory before adding
            inv_result = await self.agents["inventory"].execute(context)
            results["inventory"] = inv_result
        
        elif intent == "checkout":
            # Parallel execution: Payment + Loyalty
            tasks = [
                self.agents["payment"].execute(context),
                self.agents["loyalty"].execute(context)
            ]
            payment_result, loyalty_result = await asyncio.gather(*tasks)
            results["payment"] = payment_result
            results["loyalty"] = loyalty_result
        
        elif intent == "order_status":
            # Fulfillment agent
            fulfillment_result = await self.agents["fulfillment"].execute(context)
            results["fulfillment"] = fulfillment_result
        
        elif intent == "support":
            # Support agent
            support_result = await self.agents["support"].execute(context)
            results["support"] = support_result
        
        else:
            # Default: recommendation
            rec_result = await self.agents["recommendation"].execute(context)
            results["recommendation"] = rec_result
        
        return results
    
    def _aggregate_responses(self, agent_results: Dict, context: Dict) -> Dict:
        """Aggregate responses from multiple agents"""
        aggregated = {
            "products": [],
            "inventory": [],
            "payment_methods": [],
            "pricing": None,
            "loyalty_info": None,
            "fulfillment_options": [],
            "support_info": None
        }
        
        # Process recommendation results
        if "recommendation" in agent_results and agent_results["recommendation"].get("success"):
            aggregated["products"] = agent_results["recommendation"].get("recommendations", [])
        
        # Process inventory results
        if "inventory" in agent_results and agent_results["inventory"].get("success"):
            inventory_data = agent_results["inventory"].get("inventory", [])
            aggregated["inventory"] = inventory_data
            
            # Merge inventory with products
            for product in aggregated["products"]:
                for inv in inventory_data:
                    if product["id"] == inv["product_id"]:
                        product["stock"] = inv["availability"]
                        product["fulfillment_options"] = inv["fulfillment_options"]
        
        # Process payment results
        if "payment" in agent_results and agent_results["payment"].get("success"):
            aggregated["payment_methods"] = agent_results["payment"].get("payment_methods", [])
        
        # Process loyalty results
        if "loyalty" in agent_results and agent_results["loyalty"].get("success"):
            aggregated["pricing"] = agent_results["loyalty"].get("pricing")
            aggregated["loyalty_info"] = agent_results["loyalty"].get("loyalty_info")
        
        # Process fulfillment results
        if "fulfillment" in agent_results and agent_results["fulfillment"].get("success"):
            aggregated["fulfillment_details"] = agent_results["fulfillment"].get("fulfillment_details")
        
        # Process support results
        if "support" in agent_results and agent_results["support"].get("success"):
            aggregated["support_info"] = agent_results["support"]
        
        return aggregated
    
    def _generate_response(self, aggregated: Dict, context: Dict, intent: str) -> Dict:
        """Generate natural language response"""
        
        # Build response based on intent
        if intent == "product_search" or intent == "product_details":
            return self._generate_product_response(aggregated, context)
        elif intent == "checkout":
            return self._generate_checkout_response(aggregated, context)
        elif intent == "order_status":
            return self._generate_order_status_response(aggregated, context)
        elif intent == "support":
            return self._generate_support_response(aggregated, context)
        else:
            return self._generate_general_response(aggregated, context)
    
    def _generate_product_response(self, aggregated: Dict, context: Dict) -> Dict:
        """Generate response for product search"""
        products = aggregated.get("products", [])
        
        if not products:
            return {
                "message": "I couldn't find any products matching your criteria. Could you try different filters or let me know what you're looking for?",
                "products": []
            }
        
        # Create natural message
        count = len(products)
        category = context.get("category", "products")
        budget = context.get("budget")
        
        intro = f"I found {count} great {category}"
        if budget:
            intro += f" within your budget of ₹{budget}"
        intro += "! 🎉\n\n"
        
        product_list = []
        for i, product in enumerate(products[:3], 1):
            stock_msg = ""
            if "stock" in product:
                if product["stock"].get("available"):
                    stock_msg = " ✅ In stock"
                else:
                    stock_msg = " ⚠️ Limited stock"
            
            product_list.append(
                f"{i}. **{product['name']}** (₹{product['price']:,.0f}) - {product.get('rating', 0)}⭐{stock_msg}"
            )
        
        message = intro + "\n".join(product_list)
        message += "\n\nWhich one interests you? I can provide more details or help you add it to cart!"
        
        return {
            "message": message,
            "products": products
        }
    
    def _generate_checkout_response(self, aggregated: Dict, context: Dict) -> Dict:
        """Generate response for checkout"""
        pricing = aggregated.get("pricing")
        loyalty_info = aggregated.get("loyalty_info")
        
        if not pricing:
            return {
                "message": "Let me calculate your final price...",
                "pricing": None
            }
        
        tier = loyalty_info.get("tier", "Silver") if loyalty_info else "Silver"
        
        message = f"""Awesome! Let me calculate your final price:

**Subtotal:** ₹{pricing['subtotal']:,.2f}
**Your {tier} Tier Discount ({pricing['tier_discount']['percentage']:.0f}%):** -₹{pricing['tier_discount']['amount']:,.2f}
"""
        
        if pricing['coupon_discount']['applied']:
            message += f"**Coupon ({pricing['coupon_discount']['code']}):** -₹{pricing['coupon_discount']['amount']:,.2f}\n"
        
        message += f"""**Final Price:** ₹{pricing['final_amount']:,.2f}
**Loyalty Points to Earn:** {pricing['points_to_earn']} points

You're saving ₹{pricing['savings']:,.2f}! 💰

Ready to proceed with payment?"""
        
        return {
            "message": message,
            "pricing": pricing,
            "loyalty_info": loyalty_info,
            "payment_methods": aggregated.get("payment_methods")
        }
    
    def _generate_order_status_response(self, aggregated: Dict, context: Dict) -> Dict:
        """Generate response for order status"""
        fulfillment = aggregated.get("fulfillment_details")
        
        if not fulfillment:
            return {
                "message": "I couldn't find your order details. Could you provide your order ID?",
                "fulfillment_options": None
            }
        
        message = f"""📦 **Order Status Update**

**Type:** {fulfillment.get('type')}
**Status:** {fulfillment.get('status')}
"""
        
        if fulfillment.get('estimated_delivery'):
            message += f"**Estimated Delivery:** {fulfillment['estimated_delivery']}\n"
        
        if fulfillment.get('tracking_id'):
            message += f"**Tracking ID:** {fulfillment['tracking_id']}\n"
        
        message += "\nIs there anything else I can help you with?"
        
        return {
            "message": message,
            "fulfillment_options": [fulfillment]
        }
    
    def _generate_support_response(self, aggregated: Dict, context: Dict) -> Dict:
        """Generate response for support"""
        support_info = aggregated.get("support_info", {})
        
        message = support_info.get("message", "How can I help you today?")
        
        return {
            "message": message,
            "support_info": support_info
        }
    
    def _generate_general_response(self, aggregated: Dict, context: Dict) -> Dict:
        """Generate general response"""
        return {
            "message": "I'm here to help you find the perfect products! What are you looking for today?",
            "products": aggregated.get("products", [])
        }
    
    def _update_session(self, session_id: str, user_message: str, response: Dict, context: Dict, aggregated: Dict):
        """Update session state in Redis"""
        session_data = redis_manager.get_session(session_id)
        
        if session_data:
            # Add to conversation history
            session_data["conversation_history"].append({
                "role": "user",
                "message": user_message,
                "timestamp": datetime.now().isoformat()
            })
            
            session_data["conversation_history"].append({
                "role": "agent",
                "message": response["message"],
                "timestamp": datetime.now().isoformat(),
                "products": aggregated.get("products", [])[:3]  # Store top 3 products
            })
            
            # Update context
            session_data["context"] = context
            session_data["last_updated"] = datetime.now().isoformat()
            
            # Save to Redis
            redis_manager.set_session(session_id, session_data)


# Singleton instance
master_agent = MasterAgent()
