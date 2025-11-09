import { create } from 'zustand';
import type { Product, Cart, Message, LoyaltyInfo, SessionData } from '@/types';
import { generateSessionId, getCustomerId } from '@/lib/utils';

interface StoreState {
  // Session
  sessionId: string;
  customerId: string;
  
  // Chat
  messages: Message[];
  isTyping: boolean;
  
  // Products
  products: Product[];
  selectedProduct: Product | null;
  
  // Cart
  cart: Cart;
  
  // Loyalty
  loyaltyInfo: LoyaltyInfo | null;
  
  // UI State
  isChatOpen: boolean;
  isCartOpen: boolean;
  
  // Actions
  setSessionId: (id: string) => void;
  addMessage: (message: Message) => void;
  setIsTyping: (isTyping: boolean) => void;
  setProducts: (products: Product[]) => void;
  setSelectedProduct: (product: Product | null) => void;
  setCart: (cart: Cart) => void;
  addToCart: (item: any) => void;
  removeFromCart: (productId: string) => void;
  clearCart: () => void;
  setLoyaltyInfo: (info: LoyaltyInfo) => void;
  toggleChat: () => void;
  toggleCart: () => void;
  resetSession: () => void;
}

export const useStore = create<StoreState>((set) => ({
  // Initial state
  sessionId: generateSessionId(),
  customerId: getCustomerId(),
  messages: [],
  isTyping: false,
  products: [],
  selectedProduct: null,
  cart: {
    items: [],
    subtotal: 0,
  },
  loyaltyInfo: null,
  isChatOpen: false,
  isCartOpen: false,
  
  // Actions
  setSessionId: (id) => set({ sessionId: id }),
  
  addMessage: (message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),
  
  setIsTyping: (isTyping) => set({ isTyping }),
  
  setProducts: (products) => set({ products }),
  
  setSelectedProduct: (product) => set({ selectedProduct: product }),
  
  setCart: (cart) => set({ cart }),
  
  addToCart: (item) =>
    set((state) => {
      const existingItem = state.cart.items.find(
        (i) => i.product_id === item.product_id
      );
      
      let newItems;
      if (existingItem) {
        newItems = state.cart.items.map((i) =>
          i.product_id === item.product_id
            ? { ...i, quantity: i.quantity + item.quantity }
            : i
        );
      } else {
        newItems = [...state.cart.items, item];
      }
      
      const subtotal = newItems.reduce(
        (sum, i) => sum + i.price * i.quantity,
        0
      );
      
      return {
        cart: {
          items: newItems,
          subtotal,
        },
      };
    }),
  
  removeFromCart: (productId) =>
    set((state) => {
      const newItems = state.cart.items.filter(
        (i) => i.product_id !== productId
      );
      const subtotal = newItems.reduce(
        (sum, i) => sum + i.price * i.quantity,
        0
      );
      
      return {
        cart: {
          items: newItems,
          subtotal,
        },
      };
    }),
  
  clearCart: () =>
    set({
      cart: {
        items: [],
        subtotal: 0,
      },
    }),
  
  setLoyaltyInfo: (info) => set({ loyaltyInfo: info }),
  
  toggleChat: () => set((state) => ({ isChatOpen: !state.isChatOpen })),
  
  toggleCart: () => set((state) => ({ isCartOpen: !state.isCartOpen })),
  
  resetSession: () =>
    set({
      sessionId: generateSessionId(),
      messages: [],
      products: [],
      selectedProduct: null,
      cart: {
        items: [],
        subtotal: 0,
      },
    }),
}));
