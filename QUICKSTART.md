# Quick Start Guide (No Docker)

## Prerequisites
- Python 3.11+
- Node.js 18+
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

## Setup (One-time)

### 1. Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

### 2. Add Your API Key
Edit `backend/.env` and replace `your_api_key_here` with your actual Google Gemini API key:
```bash
nano backend/.env
# or
code backend/.env
```

## Run the Application

```bash
chmod +x start.sh
./start.sh
```

The application will start:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Manual Setup (Alternative)

If the scripts don't work, run these commands manually:

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=sqlite:///./retail.db
REDIS_URL=redis://localhost:6379/0
GOOGLE_API_KEY=your_api_key_here
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
EOF

# Start backend
python main.py
```

### Frontend (New Terminal)
```bash
cd frontend
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env

# Start frontend
npm run dev
```

## Test the Application

1. Open http://localhost:5173 in your browser
2. Try searching: "Show me winter jackets under ₹5000"
3. Click the chat icon to talk with the AI assistant
4. Add products to cart and test checkout

## Demo Credentials

Test with these customer IDs for different loyalty tiers:
- `C123` - Silver tier (10% discount)
- `C456` - Gold tier (15% discount)
- `C789` - Platinum tier (20% discount)

## Troubleshooting

### Backend won't start
```bash
# Check Python version
python3 --version  # Should be 3.11+

# Check if port 8000 is in use
lsof -ti:8000 | xargs kill -9

# Try running directly
cd backend
source venv/bin/activate
python main.py
```

### Frontend won't start
```bash
# Check Node version
node --version  # Should be 18+

# Clear and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

# Check if port 5173 is in use
lsof -ti:5173 | xargs kill -9

# Try running directly
npm run dev
```

### API Key Issues
- Make sure you have a valid Google Gemini API key
- Check that it's properly set in `backend/.env`
- The key should start with `AIza...`

### Module Not Found Errors
```bash
# Backend
cd backend
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules
npm install
```

## Features to Test

1. **Search**: "Show me jackets under ₹5000"
2. **Chat**: Click chat icon, ask "What's trending?"
3. **Categories**: Click category buttons
4. **Cart**: Add items, view cart, adjust quantities
5. **Checkout**: Complete a purchase with different options
6. **Loyalty**: See tier-based discounts applied

## Notes

- The app uses SQLite for database (no PostgreSQL needed)
- Redis is optional (falls back to in-memory storage)
- All data is mock/demo data
- Sessions persist in memory/SQLite

## Stop the Application

Press `Ctrl+C` in the terminal where you ran `./start.sh`

Or manually:
```bash
# Kill backend
lsof -ti:8000 | xargs kill -9

# Kill frontend
lsof -ti:5173 | xargs kill -9
```
