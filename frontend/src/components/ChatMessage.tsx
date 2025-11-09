import React from 'react';
import { Bot, User } from 'lucide-react';
import type { Message } from '@/types';
import { formatRelativeTime, cn } from '@/lib/utils';
import { ProductCard } from './ProductCard';

interface ChatMessageProps {
  message: Message;
  onProductClick?: (product: any) => void;
  onAddToCart?: (product: any) => void;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({
  message,
  onProductClick,
  onAddToCart,
}) => {
  const isAgent = message.role === 'agent';

  return (
    <div
      className={cn(
        "flex gap-3 animate-fadeIn",
        isAgent ? "justify-start" : "justify-end"
      )}
    >
      {/* Avatar */}
      {isAgent && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary flex items-center justify-center">
          <Bot className="h-5 w-5 text-white" />
        </div>
      )}

      {/* Message Content */}
      <div className={cn("flex flex-col gap-2 max-w-[80%]", !isAgent && "items-end")}>
        {/* Message Bubble */}
        <div
          className={cn(
            "px-4 py-3 rounded-2xl",
            isAgent
              ? "bg-white shadow-soft text-gray-900"
              : "bg-primary text-white"
          )}
        >
          <div className="whitespace-pre-wrap text-sm md:text-base">
            {message.message.split('\n').map((line, i) => {
              // Handle bold text
              const parts = line.split(/(\*\*.*?\*\*)/g);
              return (
                <p key={i} className={i > 0 ? "mt-2" : ""}>
                  {parts.map((part, j) => {
                    if (part.startsWith('**') && part.endsWith('**')) {
                      return (
                        <strong key={j}>
                          {part.slice(2, -2)}
                        </strong>
                      );
                    }
                    return <span key={j}>{part}</span>;
                  })}
                </p>
              );
            })}
          </div>
        </div>

        {/* Products Grid - Compact for chat */}
        {message.products && message.products.length > 0 && (
          <div className="flex flex-col gap-3 mt-2 w-full max-w-full">
            {message.products.slice(0, 3).map((product) => (
              <div
                key={product.id}
                className="bg-white rounded-lg p-3 shadow-sm border border-gray-200 hover:shadow-md transition-shadow cursor-pointer"
                onClick={() => onProductClick?.(product)}
              >
                <div className="flex gap-3">
                  {/* Product Image */}
                  <div className="flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden bg-gray-100">
                    <img
                      src={product.image_url}
                      alt={product.name}
                      className="w-full h-full object-cover"
                    />
                  </div>

                  {/* Product Info */}
                  <div className="flex-1 min-w-0">
                    <p className="text-xs text-gray-500 uppercase">{product.brand}</p>
                    <h4 className="font-semibold text-sm text-gray-900 line-clamp-2 mb-1">
                      {product.name}
                    </h4>
                    <div className="flex items-center gap-1 mb-2">
                      <span className="text-xs text-gray-600">⭐ {product.rating}</span>
                      {product.is_trending && (
                        <span className="text-xs bg-primary bg-opacity-10 text-primary px-2 py-0.5 rounded">
                          🔥 Trending
                        </span>
                      )}
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-lg font-bold text-gray-900">
                        {new Intl.NumberFormat('en-IN', {
                          style: 'currency',
                          currency: 'INR',
                          maximumFractionDigits: 0,
                        }).format(product.price)}
                      </span>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onAddToCart?.(product);
                        }}
                        className="btn btn-primary text-xs px-3 py-1"
                      >
                        Add
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Timestamp */}
        <span className="text-xs text-gray-500 px-2">
          {formatRelativeTime(message.timestamp)}
        </span>
      </div>

      {/* User Avatar */}
      {!isAgent && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center">
          <User className="h-5 w-5 text-gray-600" />
        </div>
      )}
    </div>
  );
};
