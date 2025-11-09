# AI-Driven Retail Sales Agent

A fully functional multi-channel AI-driven conversational sales platform using Google Gemini for agent orchestration.

A fully functional multi-channel AI-driven conversational sales platform using Google Gemini for agent orchestration. Experience intelligent product recommendations, real-time cart management, and seamless checkout with an AI assistant that understands natural language.

## ✨ Features

- 🤖 **AI-Powered Chat Assistant** - Natural language product search and recommendations with compact, optimized display
- 🛒 **Smart Shopping Cart** - Real-time cart management with automatic session handling and loyalty discounts
- 💳 **Seamless Checkout** - Multiple payment and fulfillment options with detailed order confirmation
- 🎯 **Agent Orchestration** - Multi-agent workflow with parallel processing for optimal performance
- 🏆 **Loyalty Program** - Tier-based discounts (Silver 10%/Gold 15%/Platinum 20%)
- 📦 **Flexible Fulfillment** - Ship to Home (2-day delivery), Click & Collect (same day), In-Store Try-on
- 📱 **Responsive Design** - Mobile-first, works flawlessly on all devices
- 🖨️ **Print-Ready Receipts** - Professional order confirmations with printable receipts
- 🔄 **Auto-Session Management** - Automatic session creation and cart synchronization

## Tech Stack

### Backend
- **FastAPI** - Async Python web framework
- **Google Gemini** - AI/LLM for natural language processing
- **PostgreSQL** - Primary database
- **Redis** - Session management and caching
- **SQLAlchemy** - ORM

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Zustand** - State management
- **Vite** - Build tool

## Quick Start

### Prerequisites
- Python 3.13+ (or 3.11+)
- Node.js 18+
- PostgreSQL 15+ (optional - for production)
- Redis 7+ (optional - falls back to in-memory storage)
- Google Gemini API Key ([Get yours here](https://ai.google.dev/))

### 1. Clone and Setup

```bash
git clone https://github.com/sg6724/RetailAgenticAI.git
cd RetailAgenticAI
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your Google Gemini API key
# GOOGLE_API_KEY=your_api_key_here
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
```

### 4. Start Services

#### Option A: Using Docker (Recommended)

```bash
# Start PostgreSQL and Redis
docker-compose up -d
```

#### Option B: Manual Setup

Start PostgreSQL and Redis manually on your system.

### 5. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python main.py
```

Backend will run on: http://localhost:8000

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Frontend will run on: http://localhost:5173

### 6. Access the Application

Open your browser and navigate to: **http://localhost:5173**

## Environment Variables

### Backend (.env)
```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional (defaults provided)
DATABASE_URL=postgresql://postgres:password@localhost:5432/retail_db
REDIS_URL=redis://localhost:6379/0
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

> **Note:** Redis is optional - the application will automatically fall back to in-memory storage if Redis is not available.

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

## Usage Guide

### 1. Search for Products
- Use the search bar: "Show me winter jackets under ₹5000"
- Browse by category
- Use quick filters

### 2. Chat with AI Assistant
- Click the chat icon in the top right
- Ask natural language questions
- Get personalized recommendations

### 3. Add to Cart
- Click "Add to Cart" on any product
- View cart by clicking the cart icon
- Adjust quantities or remove items

### 4. Checkout
- Click "Proceed to Checkout"
- Choose delivery option (Ship/Collect/Try-on)
- Select payment method (UPI/Card/Wallet)
- Apply available coupons
- Verify payment details
- Complete purchase

### 5. Order Confirmation
- View order details with estimated delivery date
- Print professional receipt
- Track order status
- See loyalty points earned

### 6. Loyalty Benefits
- Automatic tier-based discounts (10-20% off)
- Earn points on every purchase
- Access exclusive coupons
- Points-based tier progression

## Demo Scenarios

### Scenario 1: Product Search
```
User: "Show me winter jackets under ₹5000 in Mumbai"
AI: Returns 3-5 jackets with availability and pricing
```

### Scenario 2: Checkout with Loyalty
```
User adds items to cart → Proceeds to checkout
System applies Silver tier 10% discount
Shows: ₹9800 → -₹980 → ₹8820
User completes payment
```

### Scenario 3: Multi-turn Conversation
```
User: "Show me jackets"
AI: Shows 5 jackets
User: "Show me similar but in red"
AI: Updates results with red jackets
```

## 🔌 API Endpoints

### Chat
- `POST /api/chat` - Send message to AI assistant
- `WS /ws/chat` - WebSocket for real-time chat (available but not used)

### Products
- `GET /api/products` - Get products with filters
- `GET /api/products/{id}` - Get single product
- `GET /api/products/search/{query}` - Search products

### Cart
- `POST /api/cart/add` - Add item to cart (auto-creates session)
- `GET /api/cart/{session_id}` - Get cart contents
- `DELETE /api/cart/{session_id}/item/{product_id}` - Remove item

### Checkout
- `POST /api/checkout` - Process checkout and create order

### Loyalty
- `GET /api/loyalty/{customer_id}` - Get loyalty info and coupons

### Recommendations
- `GET /api/recommendations/related` - Get related products
- `GET /api/recommendations/frequently-bought/{product_id}` - Frequently bought together
- `GET /api/recommendations/complete-look` - Complete the look suggestions

## Architecture

### Agent Orchestration Flow
```
User Query → Master Agent → Intent Recognition (Gemini)
    ↓
Agent Selection & Parallel Execution
    ├─ Recommendation Agent (Product suggestions)
    ├─ Inventory Agent (Stock check)
    ├─ Payment Agent (Payment methods)
    └─ Loyalty Agent (Discounts & points)
    ↓
Response Aggregation → Natural Language Generation (Gemini)
    ↓
User Response with Products/Pricing
```

## Project Structure

```
retailP/
├── backend/
│   ├── agents/              # AI agents
│   │   ├── master_agent.py
│   │   ├── recommendation_agent.py
│   │   ├── inventory_agent.py
│   │   ├── payment_agent.py
│   │   ├── loyalty_agent.py
│   │   ├── fulfillment_agent.py
│   │   └── support_agent.py
│   ├── apis/                # Mock APIs
│   │   ├── products_api.py
│   │   ├── inventory_api.py
│   │   ├── payment_api.py
│   │   └── loyalty_api.py
│   ├── models/              # Data models
│   │   ├── schemas.py
│   │   └── database.py
│   ├── utils/               # Utilities
│   │   ├── redis_manager.py
│   │   └── gemini_config.py
│   ├── main.py              # FastAPI app
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── lib/             # API & utilities
│   │   ├── store/           # State management
│   │   ├── types/           # TypeScript types
│   │   └── styles/          # CSS styles
│   ├── package.json
│   └── vite.config.ts
└── docker-compose.yml
```

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Database connection error:**
```bash
# Check PostgreSQL is running
docker-compose ps
# Or check local PostgreSQL
sudo systemctl status postgresql
```

**Redis connection error:**
```bash
# Check Redis is running
docker-compose ps
# Or check local Redis
redis-cli ping
```

### Frontend Issues

**Module not found:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Port already in use:**
```bash
# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

**API connection error:**
- Check backend is running on port 8000
- Verify VITE_API_URL in .env
- Check browser console for detailed error logs

**Python 3.13 compatibility issues:**
```bash
# Update dependencies to latest versions
cd backend
pip install --upgrade pydantic fastapi uvicorn
```

**Checkout redirects to home page:**
- Check browser console for error logs
- Verify session is being created (check backend logs)
- Ensure cart has items before checkout

## Testing

### Test Queries
- "Show me winter jackets under ₹5000"
- "What's trending in jackets?"
- "Show me bestsellers"
- "I need a formal shirt"
- "Show products in Mumbai"

### Test Customer IDs
- `C123` - Silver tier, 98 points
- `C456` - Gold tier, 2500 points
- `C789` - Platinum tier, 8000 points

## Performance

- Backend response time: < 500ms
- AI response time: 1-3s (depending on Gemini API)
- Frontend load time: < 2s
- Supports 100+ concurrent users

## Security

- API key stored in environment variables
- Session-based authentication
- CORS protection
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy ORM

## 🎯 Future Enhancements

### High Priority
- [ ] Real payment gateway integration (Razorpay/Stripe)
- [ ] Email/SMS notifications for orders
- [ ] Real-time order tracking
- [ ] Product reviews and ratings system
- [ ] Advanced search filters (size, color, brand)

### Medium Priority
- [ ] Wishlist functionality
- [ ] Voice search integration
- [ ] Save cart for later
- [ ] Product comparison feature
- [ ] Recently viewed products

### Long Term
- [ ] Multi-language support (Hindi, regional languages)
- [ ] Advanced analytics dashboard
- [ ] Inventory management system
- [ ] Vendor/seller portal
- [ ] Mobile app (React Native)

## 📜 License

MIT License - feel free to use this project for learning and development!

## 👥 Contributors

- **Samriddhi Gupta** ([@sg6724](https://github.com/sg6724))
- **Jainam Oswal** ([@JainamOswal18](https://github.com/JainamOswal18))

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 💬 Support

- 🐛 **Bug Reports:** [Open an issue](https://github.com/sg6724/RetailAgenticAI/issues)
- 💡 **Feature Requests:** [Open an issue](https://github.com/sg6724/RetailAgenticAI/issues)
- 📧 **Contact:** Open an issue or reach out to contributors

## ⭐ Show Your Support

Give a ⭐️ if this project helped you learn about AI agents and e-commerce platforms!

## 📝 Changelog

### Version 1.1.0 (Current)
- Enhanced order confirmation with smart delivery dates
- Improved chat product display
- Auto-session management
- Python 3.13 support
- Multiple bug fixes and improvements

### Version 1.0.0
- Initial release
- Multi-agent orchestration
- AI-powered chat
- Cart and checkout functionality
- Loyalty program

---

**Built with ❤️ using Google Gemini AI**

*Last Updated: November 2025*
