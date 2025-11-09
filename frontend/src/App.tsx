import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Navbar } from '@/components/Navbar';
import { ConversationSidebar } from '@/components/ConversationSidebar';
import { Cart } from '@/components/Cart';
import { Home } from '@/pages/Home';
import { Checkout } from '@/pages/Checkout';
import { Confirmation } from '@/pages/Confirmation';
import { useNavigate } from 'react-router-dom';

const AppContent: React.FC = () => {
  const navigate = useNavigate();

  const handleCheckout = () => {
    navigate('/checkout');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/checkout" element={<Checkout />} />
        <Route path="/confirmation" element={<Confirmation />} />
      </Routes>

      <ConversationSidebar />
      <Cart onCheckout={handleCheckout} />
    </div>
  );
};

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
