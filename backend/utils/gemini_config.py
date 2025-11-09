import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def get_gemini_model(model_name: str = "gemini-2.5-flash"):
    """Get configured Gemini model"""
    if not GEMINI_API_KEY:
        print("⚠️  Warning: GEMINI_API_KEY not set. AI responses will be limited.")
        return None
    
    try:
        # Try Gemini 2.0 Flash first
        model = genai.GenerativeModel(model_name)
        print(f"✓ Using Gemini model: {model_name}")
        return model
    except Exception as e:
        print(f"Error with {model_name}: {e}")
        try:
            # Fallback to Gemini 1.5 Flash
            fallback_model = "gemini-2.5-flash"
            model = genai.GenerativeModel(fallback_model)
            print(f"✓ Using fallback model: {fallback_model}")
            return model
        except Exception as e2:
            print(f"Error with fallback model: {e2}")
            return None


def generate_response(prompt: str, model_name: str = "gemini-2.0-flash-exp") -> str:
    """Generate response from Gemini"""
    try:
        model = get_gemini_model(model_name)
        if not model:
            return "I apologize, but I'm having trouble connecting to the AI service. Please check your API key configuration."
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        print(f"Prompt was: {prompt[:200]}...")
        return "I apologize, but I'm having trouble processing your request right now. Please try again."


def analyze_intent(user_message: str) -> dict:
    """Analyze user intent using Gemini"""
    prompt = f"""Analyze the following customer message and classify the intent.
Return a JSON object with:
- intent: one of ["product_search", "product_details", "add_to_cart", "checkout", "order_status", "support", "general"]
- entities: extracted entities like category, budget, location, product_name, etc.
- confidence: confidence score 0-1

Customer message: "{user_message}"

Return only valid JSON, no additional text."""

    try:
        response = generate_response(prompt)
        # Parse JSON from response
        import json
        # Try to extract JSON from response
        if "{" in response and "}" in response:
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            json_str = response[json_start:json_end]
            return json.loads(json_str)
        else:
            # Default fallback
            return {
                "intent": "product_search",
                "entities": {},
                "confidence": 0.5
            }
    except Exception as e:
        print(f"Intent analysis error: {e}")
        return {
            "intent": "product_search",
            "entities": {},
            "confidence": 0.5
        }


def generate_natural_response(context: dict) -> str:
    """Generate natural language response based on context"""
    
    intent = context.get("intent", "general")
    user_message = context.get("user_message", "")
    aggregated_data = context.get("aggregated_data", {})
    products = aggregated_data.get("products", [])
    pricing = aggregated_data.get("pricing")
    loyalty_info = aggregated_data.get("loyalty_info")
    
    # Build detailed context for Gemini
    context_details = f"""You are an enthusiastic AI retail sales assistant helping a customer shop online.

USER'S MESSAGE: "{user_message}"
INTENT: {intent}

"""
    
    if products:
        context_details += f"\nPRODUCTS FOUND ({len(products)} items):\n"
        for i, p in enumerate(products[:5], 1):
            context_details += f"{i}. {p['name']} - ₹{p['price']:,.0f} ({p['rating']}⭐) - {p['brand']}\n"
    
    if pricing:
        context_details += f"\nPRICING DETAILS:\n"
        context_details += f"- Subtotal: ₹{pricing['subtotal']:,.2f}\n"
        context_details += f"- Discount: ₹{pricing.get('savings', 0):,.2f}\n"
        context_details += f"- Final Amount: ₹{pricing['final_amount']:,.2f}\n"
    
    if loyalty_info:
        context_details += f"\nLOYALTY INFO:\n"
        context_details += f"- Tier: {loyalty_info.get('tier', 'Silver')}\n"
        context_details += f"- Points: {loyalty_info.get('points', 0)}\n"
    
    prompt = f"""{context_details}

TASK: Generate a natural, conversational response as a friendly sales assistant.

GUIDELINES:
- Be warm, enthusiastic, and helpful
- Use 1-2 emojis maximum
- Keep it concise (2-4 sentences)
- Mention specific product names, prices, and key features
- Highlight discounts and savings if applicable
- End with a clear call-to-action or helpful question
- Use Indian Rupee symbol (₹) for all prices
- Sound natural and human-like, not robotic

Generate ONLY the response message, no additional text or formatting:"""

    return generate_response(prompt)
