import React, { useEffect, useState } from 'react';
import { Sparkles, X } from 'lucide-react';
import { ProductCard } from './ProductCard';
import type { Product } from '@/types';
import axios from 'axios';

interface RecommendationPanelProps {
  productIds: string[];
  onAddToCart?: (product: Product) => void;
  onClose?: () => void;
}

export const RecommendationPanel: React.FC<RecommendationPanelProps> = ({
  productIds,
  onAddToCart,
  onClose,
}) => {
  const [recommendations, setRecommendations] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (productIds.length > 0) {
      loadRecommendations();
    }
  }, [productIds]);

  const loadRecommendations = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get(
        `/api/recommendations/related?product_ids=${productIds.join(',')}&limit=4`
      );
      if (response.data.success) {
        setRecommendations(response.data.recommendations);
      }
    } catch (error) {
      console.error('Error loading recommendations:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (recommendations.length === 0 && !isLoading) {
    return null;
  }

  return (
    <div className="bg-gradient-to-r from-primary-50 to-accent-50 border-t border-primary-200 py-8 animate-fadeIn">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary rounded-full flex items-center justify-center">
              <Sparkles className="h-5 w-5 text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-900">
                You Might Also Like
              </h2>
              <p className="text-sm text-gray-600">
                Based on items in your cart
              </p>
            </div>
          </div>
          {onClose && (
            <button
              onClick={onClose}
              className="p-2 hover:bg-white hover:bg-opacity-50 rounded-lg transition-colors"
            >
              <X className="h-5 w-5 text-gray-600" />
            </button>
          )}
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {[1, 2, 3, 4].map((i) => (
              <div
                key={i}
                className="card animate-pulse"
              >
                <div className="aspect-square bg-gray-200 rounded-lg mb-4"></div>
                <div className="h-4 bg-gray-200 rounded mb-2"></div>
                <div className="h-4 bg-gray-200 rounded w-2/3"></div>
              </div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {recommendations.map((product) => (
              <div key={product.id} className="relative">
                <ProductCard
                  product={product}
                  onAddToCart={onAddToCart}
                />
                {product.recommendation_reason && (
                  <div className="absolute top-2 right-2 bg-accent text-white text-xs px-2 py-1 rounded-full shadow-lg">
                    {product.recommendation_reason}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
