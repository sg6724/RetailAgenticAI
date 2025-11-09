import axios from 'axios';
import type { Product, Cart, CartItem, LoyaltyInfo, Coupon, ChatResponse, OrderConfirmation } from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Chat API
export const sendMessage = async (
  message: string,
  sessionId?: string,
  customerId?: string
): Promise<ChatResponse> => {
  const response = await api.post('/api/chat', {
    message,
    session_id: sessionId,
    customer_id: customerId,
  });
  return response.data;
};

// Products API
export const getProducts = async (
  category?: string,
  budget?: number,
  sort: string = 'trending',
  limit: number = 10
): Promise<{ success: boolean; products: Product[]; count: number }> => {
  const params = new URLSearchParams();
  if (category) params.append('category', category);
  if (budget) params.append('budget', budget.toString());
  params.append('sort', sort);
  params.append('limit', limit.toString());
  
  const response = await api.get(`/api/products?${params.toString()}`);
  return response.data;
};

export const getProduct = async (productId: string): Promise<{ success: boolean; product: Product }> => {
  const response = await api.get(`/api/products/${productId}`);
  return response.data;
};

export const searchProducts = async (
  query: string,
  limit: number = 10
): Promise<{ success: boolean; products: Product[]; count: number }> => {
  const response = await api.get(`/api/products/search/${encodeURIComponent(query)}?limit=${limit}`);
  return response.data;
};

// Inventory API
export const getInventory = async (
  productId: string,
  location?: string
): Promise<any> => {
  const params = location ? `?location=${location}` : '';
  const response = await api.get(`/api/inventory/${productId}${params}`);
  return response.data;
};

// Cart API
export const addToCart = async (
  sessionId: string,
  item: CartItem
): Promise<{ success: boolean; cart: Cart }> => {
  const response = await api.post(`/api/cart/add?session_id=${sessionId}`, item);
  return response.data;
};

export const getCart = async (sessionId: string): Promise<{ success: boolean; cart: Cart }> => {
  const response = await api.get(`/api/cart/${sessionId}`);
  return response.data;
};

export const removeFromCart = async (
  sessionId: string,
  productId: string
): Promise<{ success: boolean; cart: Cart }> => {
  const response = await api.delete(`/api/cart/${sessionId}/item/${productId}`);
  return response.data;
};

// Checkout API
export const checkout = async (orderData: {
  session_id: string;
  customer_id: string;
  payment_method: string;
  fulfillment_option: string;
  delivery_address?: string;
  store_location?: string;
}): Promise<{ success: boolean; order: OrderConfirmation }> => {
  const response = await api.post('/api/checkout', orderData);
  return response.data;
};

// Loyalty API
export const getLoyalty = async (
  customerId: string
): Promise<{ success: boolean; loyalty: LoyaltyInfo; coupons: Coupon[] }> => {
  const response = await api.get(`/api/loyalty/${customerId}`);
  return response.data;
};

// Feedback API
export const submitFeedback = async (feedbackData: {
  order_id: string;
  customer_id: string;
  rating: number;
  feedback_text?: string;
}): Promise<any> => {
  const response = await api.post('/api/feedback', feedbackData);
  return response.data;
};

// Session API
export const getSession = async (sessionId: string): Promise<any> => {
  const response = await api.get(`/api/session/${sessionId}`);
  return response.data;
};

export default api;
