export interface Product {
  id: string;
  name: string;
  price: number;
  rating: number;
  image_url: string;
  description: string;
  category: string;
  brand: string;
  sizes: string[];
  colors: string[];
  is_trending?: boolean;
  is_seasonal?: boolean;
  is_bestseller?: boolean;
  stock?: StockInfo;
  fulfillment_options?: FulfillmentOption[];
  reasoning?: string;
  confidence_score?: number;
  recommendation_reason?: string;
  recommendation_score?: number;
}

export interface StockInfo {
  available: boolean;
  warehouse: number;
  stores: Record<string, number>;
  message?: string;
}

export interface FulfillmentOption {
  type: string;
  available: boolean;
  location?: string;
  estimated_time: string;
  cost: number;
  description: string;
}

export interface CartItem {
  product_id: string;
  product_name: string;
  quantity: number;
  price: number;
  size?: string;
  color?: string;
}

export interface Cart {
  items: CartItem[];
  subtotal: number;
}

export interface LoyaltyInfo {
  tier: 'Silver' | 'Gold' | 'Platinum';
  points: number;
  lifetime_spend: number;
  available_coupons: string[];
  next_tier?: string;
  points_to_next_tier?: number;
}

export interface Coupon {
  code: string;
  description: string;
  discount: string;
  min_purchase: number;
  expires: string;
}

export interface PricingBreakdown {
  subtotal: number;
  tier_discount: {
    percentage: number;
    amount: number;
    tier: string;
  };
  coupon_discount: {
    applied: boolean;
    code?: string;
    amount: number;
    message: string;
  };
  total_discount: number;
  final_amount: number;
  points_to_earn: number;
  savings: number;
}

export interface Message {
  role: 'user' | 'agent';
  message: string;
  timestamp: string;
  products?: Product[];
}

export interface ChatResponse {
  success: boolean;
  session_id: string;
  message: string;
  products?: Product[];
  pricing?: PricingBreakdown;
  fulfillment_options?: FulfillmentOption[];
  payment_methods?: PaymentMethod[];
  loyalty_info?: LoyaltyInfo;
  intent?: string;
  timestamp: string;
}

export interface PaymentMethod {
  type: string;
  id: string;
  display: string;
  icon: string;
  saved: boolean;
  last4?: string;
  brand?: string;
  balance?: number;
  limit?: number;
}

export interface OrderConfirmation {
  order_id: string;
  total_amount: number;
  payment_status: string;
  transaction_id: string;
  fulfillment_details: any;
  estimated_delivery?: string;
  timestamp: string;
}

export interface SessionData {
  session_id: string;
  customer_id: string;
  conversation_history: Message[];
  active_cart: Cart;
  context: Record<string, any>;
  last_updated: string;
}
