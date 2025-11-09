import React from 'react';
import { X, ShoppingCart, Trash2, Plus, Minus } from 'lucide-react';
import { useStore } from '@/store/useStore';
import { formatPrice, cn } from '@/lib/utils';

interface CartProps {
  onCheckout?: () => void;
}

export const Cart: React.FC<CartProps> = ({ onCheckout }) => {
  const { isCartOpen, toggleCart, cart, removeFromCart } = useStore();

  const handleCheckout = () => {
    toggleCart();
    onCheckout?.();
  };

  return (
    <>
      {/* Sidebar */}
      <div
        className={cn(
          "fixed top-0 right-0 h-full w-full md:w-96 bg-white shadow-2xl z-50 transform transition-transform duration-300 ease-in-out flex flex-col",
          isCartOpen ? "translate-x-0" : "translate-x-full"
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b">
          <div className="flex items-center gap-3">
            <ShoppingCart className="h-5 w-5 text-gray-700" />
            <h2 className="font-semibold text-lg">
              Shopping Cart ({cart.items.length})
            </h2>
          </div>
          <button
            onClick={toggleCart}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Cart Items */}
        <div className="flex-1 overflow-y-auto p-4">
          {cart.items.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center p-6">
              <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                <ShoppingCart className="h-10 w-10 text-gray-400" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Your cart is empty
              </h3>
              <p className="text-sm text-gray-600">
                Start shopping to add items to your cart
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {cart.items.map((item) => (
                <div
                  key={item.product_id}
                  className="flex gap-4 p-4 bg-gray-50 rounded-lg"
                >
                  {/* Product Info */}
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900 mb-1">
                      {item.product_name}
                    </h4>
                    <div className="text-sm text-gray-600 space-y-1">
                      {item.size && <p>Size: {item.size}</p>}
                      {item.color && <p>Color: {item.color}</p>}
                      <p className="font-semibold text-gray-900">
                        {formatPrice(item.price)}
                      </p>
                    </div>
                    
                    {/* Quantity */}
                    <div className="flex items-center gap-2 mt-2">
                      <span className="text-sm text-gray-600">Qty:</span>
                      <span className="font-medium">{item.quantity}</span>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex flex-col items-end justify-between">
                    <button
                      onClick={() => removeFromCart(item.product_id)}
                      className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                    <p className="font-semibold text-gray-900">
                      {formatPrice(item.price * item.quantity)}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        {cart.items.length > 0 && (
          <div className="border-t p-4 space-y-4 bg-white">
            {/* Subtotal */}
            <div className="flex items-center justify-between text-lg">
              <span className="font-medium text-gray-700">Subtotal:</span>
              <span className="font-bold text-gray-900">
                {formatPrice(cart.subtotal)}
              </span>
            </div>

            {/* Checkout Button */}
            <button
              onClick={handleCheckout}
              className="btn btn-primary w-full text-lg py-3"
            >
              Proceed to Checkout
            </button>

            <p className="text-xs text-gray-500 text-center">
              Taxes and shipping calculated at checkout
            </p>
          </div>
        )}
      </div>

      {/* Overlay */}
      {isCartOpen && (
        <div
          onClick={toggleCart}
          className="fixed inset-0 bg-black bg-opacity-50 z-40"
        />
      )}
    </>
  );
};
