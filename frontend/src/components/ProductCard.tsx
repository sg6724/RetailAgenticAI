import React from 'react';
import { Star, ShoppingCart, TrendingUp, Flame, Award } from 'lucide-react';
import type { Product } from '@/types';
import { formatPrice, cn } from '@/lib/utils';

interface ProductCardProps {
  product: Product;
  onAddToCart?: (product: Product) => void;
  onClick?: (product: Product) => void;
  className?: string;
}

export const ProductCard: React.FC<ProductCardProps> = ({
  product,
  onAddToCart,
  onClick,
  className,
}) => {
  const handleAddToCart = (e: React.MouseEvent) => {
    e.stopPropagation();
    onAddToCart?.(product);
  };

  const isInStock = product.stock?.available !== false;

  return (
    <div
      onClick={() => onClick?.(product)}
      className={cn(
        "card cursor-pointer transition-all duration-200 hover:shadow-lg hover:-translate-y-1",
        !isInStock && "opacity-75",
        className
      )}
    >
      {/* Image */}
      <div className="relative aspect-square overflow-hidden rounded-lg mb-4">
        <img
          src={product.image_url}
          alt={product.name}
          className="w-full h-full object-cover"
        />
        
        {/* Badges */}
        <div className="absolute top-2 left-2 flex flex-col gap-1">
          {product.is_trending && (
            <span className="badge bg-primary text-white flex items-center gap-1">
              <TrendingUp className="h-3 w-3" />
              Trending
            </span>
          )}
          {product.is_bestseller && (
            <span className="badge bg-accent text-white flex items-center gap-1">
              <Flame className="h-3 w-3" />
              Best Seller
            </span>
          )}
          {product.is_seasonal && (
            <span className="badge bg-blue-500 text-white flex items-center gap-1">
              <Award className="h-3 w-3" />
              Seasonal
            </span>
          )}
        </div>

        {/* Stock Badge */}
        {!isInStock && (
          <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
            <span className="badge badge-error text-sm">Out of Stock</span>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="space-y-2">
        {/* Brand */}
        <p className="text-xs text-gray-500 uppercase tracking-wide">
          {product.brand}
        </p>

        {/* Name */}
        <h3 className="font-semibold text-gray-900 line-clamp-2 min-h-[3rem]">
          {product.name}
        </h3>

        {/* Rating */}
        <div className="flex items-center gap-1">
          <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
          <span className="text-sm font-medium text-gray-900">
            {product.rating}
          </span>
          <span className="text-sm text-gray-500">(4.2k reviews)</span>
        </div>

        {/* Price */}
        <div className="flex items-baseline gap-2">
          <span className="text-2xl font-bold text-gray-900">
            {formatPrice(product.price)}
          </span>
        </div>

        {/* Reasoning */}
        {product.reasoning && (
          <p className="text-xs text-gray-600 italic">
            {product.reasoning}
          </p>
        )}

        {/* Stock Info */}
        {isInStock && product.stock && (
          <div className="text-xs text-green-600 flex items-center gap-1">
            <span className="w-2 h-2 bg-green-500 rounded-full"></span>
            In Stock
          </div>
        )}

        {/* Add to Cart Button */}
        <button
          onClick={handleAddToCart}
          disabled={!isInStock}
          className={cn(
            "btn btn-primary w-full flex items-center justify-center gap-2 mt-4",
            !isInStock && "opacity-50 cursor-not-allowed"
          )}
        >
          <ShoppingCart className="h-4 w-4" />
          Add to Cart
        </button>
      </div>
    </div>
  );
};
