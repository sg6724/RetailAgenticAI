import React, { useState, useEffect } from 'react';
import { SearchBar } from '@/components/SearchBar';
import { ProductCard } from '@/components/ProductCard';
import { RecommendationPanel } from '@/components/RecommendationPanel';
import { useStore } from '@/store/useStore';
import { sendMessage, addToCart as addToCartAPI, getLoyalty } from '@/lib/api';
import type { Product } from '@/types';
import { Sparkles, TrendingUp, Tag } from 'lucide-react';

export const Home: React.FC = () => {
  const {
    sessionId,
    customerId,
    products,
    setProducts,
    addMessage,
    setIsTyping,
    addToCart,
    setLoyaltyInfo,
  } = useStore();

  const [isLoading, setIsLoading] = useState(false);
  const [showRecommendations, setShowRecommendations] = useState(false);

  useEffect(() => {
    // Load loyalty info on mount
    loadLoyaltyInfo();
    
    // Load initial trending products
    loadTrendingProducts();
  }, []);

  const loadLoyaltyInfo = async () => {
    try {
      const response = await getLoyalty(customerId);
      if (response.success) {
        setLoyaltyInfo(response.loyalty);
      }
    } catch (error) {
      console.error('Error loading loyalty info:', error);
    }
  };

  const loadTrendingProducts = async () => {
    setIsLoading(true);
    try {
      const response = await sendMessage(
        "Show me trending products",
        sessionId,
        customerId
      );

      if (response.products) {
        setProducts(response.products);
      }
    } catch (error) {
      console.error('Error loading products:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = async (query: string) => {
    setIsLoading(true);
    setIsTyping(true);

    // Add user message
    addMessage({
      role: 'user',
      message: query,
      timestamp: new Date().toISOString(),
    });

    try {
      const response = await sendMessage(query, sessionId, customerId);

      // Add agent response
      addMessage({
        role: 'agent',
        message: response.message,
        timestamp: response.timestamp,
        products: response.products,
      });

      // Update products
      if (response.products) {
        setProducts(response.products);
      }
    } catch (error) {
      console.error('Error searching:', error);
      addMessage({
        role: 'agent',
        message: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
      });
    } finally {
      setIsLoading(false);
      setIsTyping(false);
    }
  };

  const handleAddToCart = async (product: Product) => {
    try {
      const cartItem = {
        product_id: product.id,
        product_name: product.name,
        quantity: 1,
        price: product.price,
      };

      // Add to local state
      addToCart(cartItem);

      // Sync with backend
      await addToCartAPI(sessionId, cartItem);

      // Show recommendations
      setShowRecommendations(true);

      // Show success message
      addMessage({
        role: 'agent',
        message: `Great choice! I've added ${product.name} to your cart. 🎉 Check out the recommendations below!`,
        timestamp: new Date().toISOString(),
      });

      // Scroll to recommendations
      setTimeout(() => {
        const recPanel = document.getElementById('recommendations');
        if (recPanel) {
          recPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }, 300);
    } catch (error) {
      console.error('Error adding to cart:', error);
    }
  };

  const categories = [
    { name: 'Jackets', icon: '🧥', query: 'Show me jackets' },
    { name: 'Shirts', icon: '👔', query: 'Show me shirts' },
    { name: 'Jeans', icon: '👖', query: 'Show me jeans' },
    { name: 'Sweaters', icon: '🧶', query: 'Show me sweaters' },
  ];

  const quickFilters = [
    { label: 'Under ₹3000', query: 'Show products under ₹3000' },
    { label: 'Under ₹5000', query: 'Show products under ₹5000' },
    { label: 'Best Rated', query: 'Show best rated products' },
    { label: 'New Arrivals', query: 'Show new arrivals' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-50 to-white py-12 md:py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-8">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Find Your Perfect Style
            </h1>
            <p className="text-lg md:text-xl text-gray-600 mb-8">
              AI-powered shopping assistant at your service
            </p>
          </div>

          {/* Search Bar */}
          <div className="max-w-3xl mx-auto">
            <SearchBar
              onSearch={handleSearch}
              isLoading={isLoading}
              placeholder="Try: 'Show me winter jackets under ₹5000 in Mumbai'"
            />
          </div>

          {/* Quick Filters */}
          <div className="flex flex-wrap justify-center gap-2 mt-6">
            {quickFilters.map((filter) => (
              <button
                key={filter.label}
                onClick={() => handleSearch(filter.query)}
                disabled={isLoading}
                className="px-4 py-2 bg-white text-gray-700 rounded-full text-sm font-medium hover:bg-gray-100 transition-colors shadow-soft disabled:opacity-50"
              >
                {filter.label}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="py-8 border-b bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3 mb-4">
            <Tag className="h-5 w-5 text-primary" />
            <h2 className="text-xl font-bold text-gray-900">Shop by Category</h2>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {categories.map((category) => (
              <button
                key={category.name}
                onClick={() => handleSearch(category.query)}
                disabled={isLoading}
                className="p-6 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors text-center disabled:opacity-50"
              >
                <div className="text-4xl mb-2">{category.icon}</div>
                <p className="font-medium text-gray-900">{category.name}</p>
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Products Grid */}
      <section className="py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {products.length > 0 ? (
            <>
              <div className="flex items-center gap-3 mb-6">
                <Sparkles className="h-5 w-5 text-primary" />
                <h2 className="text-2xl font-bold text-gray-900">
                  Recommended for You
                </h2>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {products.map((product) => (
                  <ProductCard
                    key={product.id}
                    product={product}
                    onAddToCart={handleAddToCart}
                  />
                ))}
              </div>
            </>
          ) : (
            <div className="text-center py-20">
              <div className="w-20 h-20 bg-primary bg-opacity-10 rounded-full flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="h-10 w-10 text-primary" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Start Your Shopping Journey
              </h3>
              <p className="text-gray-600 mb-6">
                Search for products or browse categories to get started
              </p>
            </div>
          )}
        </div>
      </section>

      {/* Recommendations Panel */}
      {showRecommendations && (
        <div id="recommendations">
          <RecommendationPanel
            productIds={useStore.getState().cart.items.map(item => item.product_id)}
            onAddToCart={handleAddToCart}
            onClose={() => setShowRecommendations(false)}
          />
        </div>
      )}
    </div>
  );
};
