import React from 'react';
import { ShoppingCart, MessageCircle, Award } from 'lucide-react';
import { useStore } from '@/store/useStore';
import { getTierBadgeColor } from '@/lib/utils';

export const Navbar: React.FC = () => {
  const { cart, toggleCart, toggleChat, loyaltyInfo } = useStore();

  const cartItemCount = cart.items.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <nav className="sticky top-0 z-30 bg-white border-b shadow-soft">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
              <ShoppingCart className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">RetailAI</h1>
              <p className="text-xs text-gray-500">Smart Shopping</p>
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-4">
            {/* Loyalty Badge */}
            {loyaltyInfo && (
              <div className="hidden md:flex items-center gap-2 px-3 py-1.5 bg-gray-100 rounded-full">
                <Award className="h-4 w-4 text-gray-600" />
                <span className={`text-sm font-medium ${getTierBadgeColor(loyaltyInfo.tier)}`}>
                  {loyaltyInfo.tier}
                </span>
                <span className="text-xs text-gray-600">
                  {loyaltyInfo.points} pts
                </span>
              </div>
            )}

            {/* Chat Button */}
            <button
              onClick={toggleChat}
              className="relative p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <MessageCircle className="h-6 w-6 text-gray-700" />
            </button>

            {/* Cart Button */}
            <button
              onClick={toggleCart}
              className="relative p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <ShoppingCart className="h-6 w-6 text-gray-700" />
              {cartItemCount > 0 && (
                <span className="absolute -top-1 -right-1 w-5 h-5 bg-accent text-white text-xs font-bold rounded-full flex items-center justify-center">
                  {cartItemCount}
                </span>
              )}
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};
