import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini with API key
if GEMINI_API_KEY and GEMINI_API_KEY != "your_api_key_here":
    genai.configure(api_key=GEMINI_API_KEY)
    print(f"✓ Gemini API configured successfully")
else:
    print(f"⚠️  WARNING: Gemini API key not configured! Please set GEMINI_API_KEY in backend/.env")


def get_gemini_model(model_name: str = "gemini-2.0-flash-exp"):
    """Get configured Gemini model"""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_api_key_here":
        raise Exception("Gemini API key not configured")
    
    try:
        # Try the requested model first
        model = genai.GenerativeModel(model_name)
        print(f"✓ Using Gemini model: {model_name}")
        return model
    except Exception as e:
        print(f"⚠️  Error with {model_name}: {e}")
        # Fallback to stable version
        try:
            fallback_model = "gemini-1.5-flash"
            model = genai.GenerativeModel(fallback_model)
            print(f"✓ Fallback to: {fallback_model}")
            return model
        except Exception as e2:
            print(f"❌ Error with fallback model: {e2}")
            raise


def generate_response(prompt: str, model_name: str = "gemini-2.5-flash") -> str:
    """Generate response from Gemini"""
    try:
        model = get_gemini_model(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
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
    prompt = f"""You are a friendly, helpful retail sales assistant. Generate a natural, conversational response based on this context:

Context: {context}

Guidelines:
- Be warm and enthusiastic
- Use emojis sparingly (1-2 per response)
- Keep responses concise (2-4 sentences)
- Highlight key information like prices, discounts, availability
- End with a clear call-to-action or question
- Use Indian Rupee symbol (₹) for prices

Generate only the response text, no additional formatting."""

    return generate_response(prompt)
