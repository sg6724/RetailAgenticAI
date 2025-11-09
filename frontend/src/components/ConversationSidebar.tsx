import React, { useState, useRef, useEffect } from 'react';
import { X, Send, Loader2, MessageCircle } from 'lucide-react';
import { useStore } from '@/store/useStore';
import { ChatMessage } from './ChatMessage';
import { sendMessage } from '@/lib/api';
import { cn } from '@/lib/utils';

interface ConversationSidebarProps {
  onProductClick?: (product: any) => void;
  onAddToCart?: (product: any) => void;
}

export const ConversationSidebar: React.FC<ConversationSidebarProps> = ({
  onProductClick,
  onAddToCart,
}) => {
  const {
    isChatOpen,
    toggleChat,
    messages,
    addMessage,
    isTyping,
    setIsTyping,
    sessionId,
    customerId,
    setProducts,
  } = useStore();

  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');

    // Add user message immediately for better UX
    addMessage({
      role: 'user',
      message: userMessage,
      timestamp: new Date().toISOString(),
    });

    setIsLoading(true);
    setIsTyping(true);

    try {
      // Use HTTP API for reliable delivery
      const response = await sendMessage(userMessage, sessionId, customerId);

      // Simulate typing delay for more natural feel
      await new Promise(resolve => setTimeout(resolve, 500));

      // Add agent response
      addMessage({
        role: 'agent',
        message: response.message,
        timestamp: response.timestamp,
        products: response.products,
      });

      // Update products in store
      if (response.products) {
        setProducts(response.products);
      }
    } catch (error) {
      console.error('Error sending message:', error);
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

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const quickQueries = [
    "Show me winter jackets under ₹5000",
    "What's trending in jackets?",
    "I need a formal shirt",
    "Show me bestsellers",
  ];

  return (
    <>
      {/* Floating Chat Button */}
      {!isChatOpen && (
        <button
          onClick={toggleChat}
          className="fixed bottom-6 right-6 z-50 w-14 h-14 bg-primary text-white rounded-full shadow-lg hover:bg-primary-600 transition-all duration-200 flex items-center justify-center"
        >
          <MessageCircle className="h-6 w-6" />
        </button>
      )}

      {/* Sidebar */}
      <div
        className={cn(
          "fixed top-0 right-0 h-full w-full md:w-96 bg-white shadow-2xl z-50 transform transition-transform duration-300 ease-in-out flex flex-col",
          isChatOpen ? "translate-x-0" : "translate-x-full"
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b bg-primary text-white">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
              <MessageCircle className="h-5 w-5" />
            </div>
            <div>
              <h2 className="font-semibold">AI Sales Assistant</h2>
              <p className="text-xs text-primary-100">Always here to help</p>
            </div>
          </div>
          <button
            onClick={toggleChat}
            className="p-2 hover:bg-white hover:bg-opacity-10 rounded-lg transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center p-6">
              <div className="w-16 h-16 bg-primary bg-opacity-10 rounded-full flex items-center justify-center mb-4">
                <MessageCircle className="h-8 w-8 text-primary" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Welcome! 👋
              </h3>
              <p className="text-sm text-gray-600 mb-6">
                I'm your AI shopping assistant. Ask me anything!
              </p>
              
              {/* Quick Queries */}
              <div className="w-full space-y-2">
                <p className="text-xs text-gray-500 font-medium mb-3">
                  Try asking:
                </p>
                {quickQueries.map((query, index) => (
                  <button
                    key={index}
                    onClick={() => {
                      setInput(query);
                      setTimeout(handleSend, 100);
                    }}
                    className="w-full text-left px-4 py-2 bg-white rounded-lg text-sm text-gray-700 hover:bg-gray-100 transition-colors shadow-soft"
                  >
                    {query}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <>
              {messages.map((message, index) => (
                <ChatMessage
                  key={index}
                  message={message}
                  onProductClick={onProductClick}
                  onAddToCart={onAddToCart}
                />
              ))}
              
              {/* Typing Indicator */}
              {isTyping && (
                <div className="flex gap-3">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary flex items-center justify-center">
                    <MessageCircle className="h-5 w-5 text-white" />
                  </div>
                  <div className="bg-white shadow-soft px-4 py-3 rounded-2xl">
                    <div className="flex gap-1">
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></span>
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></span>
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></span>
                    </div>
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        {/* Input */}
        <div className="p-4 border-t bg-white">
          <div className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              disabled={isLoading}
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:opacity-50"
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
              className="btn btn-primary px-4 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <Send className="h-5 w-5" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Overlay */}
      {isChatOpen && (
        <div
          onClick={toggleChat}
          className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
        />
      )}
    </>
  );
};
