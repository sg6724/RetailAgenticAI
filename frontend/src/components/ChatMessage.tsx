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

        {/* Products Grid */}
        {message.products && message.products.length > 0 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-2 w-full">
            {message.products.slice(0, 3).map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                onClick={onProductClick}
                onAddToCart={onAddToCart}
                className="max-w-sm"
              />
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
