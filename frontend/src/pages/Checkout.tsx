import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useStore } from '@/store/useStore';
import { checkout as checkoutAPI, getLoyalty } from '@/lib/api';
import { formatPrice, getTierBadgeColor } from '@/lib/utils';
import { CreditCard, Truck, Store, MapPin, Tag, Award, Loader2, CheckCircle } from 'lucide-react';
import { PaymentForm } from '@/components/PaymentForm';
import type { PricingBreakdown, Coupon } from '@/types';

export const Checkout: React.FC = () => {
  const navigate = useNavigate();
  const { sessionId, customerId, cart, clearCart, loyaltyInfo, setLoyaltyInfo } = useStore();

  const [paymentMethod, setPaymentMethod] = useState<string>('UPI');
  const [fulfillmentOption, setFulfillmentOption] = useState<string>('Ship to Home');
  const [deliveryAddress, setDeliveryAddress] = useState('');
  const [storeLocation, setStoreLocation] = useState('Mumbai');
  const [selectedCoupon, setSelectedCoupon] = useState<string>('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [pricing, setPricing] = useState<PricingBreakdown | null>(null);
  const [availableCoupons, setAvailableCoupons] = useState<Coupon[]>([]);
  const [paymentDetails, setPaymentDetails] = useState<any>(null);
  const [paymentVerified, setPaymentVerified] = useState(false);

  useEffect(() => {
    if (cart.items.length === 0) {
      navigate('/');
      return;
    }

    loadLoyaltyAndPricing();
  }, [cart.subtotal]);

  const loadLoyaltyAndPricing = async () => {
    try {
      const response = await getLoyalty(customerId);
      if (response.success) {
        setLoyaltyInfo(response.loyalty);
        setAvailableCoupons(response.coupons);
        
        // Calculate pricing
        calculatePricing(response.loyalty);
      }
    } catch (error) {
      console.error('Error loading loyalty:', error);
    }
  };

  const calculatePricing = (loyalty: any) => {
    const tierDiscountPercentage = loyalty.tier === 'Platinum' ? 0.20 : loyalty.tier === 'Gold' ? 0.15 : 0.10;
    const tierDiscountAmount = cart.subtotal * tierDiscountPercentage;
    const afterTierDiscount = cart.subtotal - tierDiscountAmount;

    let couponDiscountAmount = 0;
    if (selectedCoupon) {
      const coupon = availableCoupons.find(c => c.code === selectedCoupon);
      if (coupon) {
        const discountPercent = parseFloat(coupon.discount.replace('%', '')) / 100;
        couponDiscountAmount = Math.min(afterTierDiscount * discountPercent, 5000);
      }
    }

    const finalAmount = afterTierDiscount - couponDiscountAmount;
    const pointsToEarn = Math.floor(finalAmount * 0.01 * (loyalty.tier === 'Platinum' ? 2 : loyalty.tier === 'Gold' ? 1.5 : 1));

    setPricing({
      subtotal: cart.subtotal,
      tier_discount: {
        percentage: tierDiscountPercentage * 100,
        amount: tierDiscountAmount,
        tier: loyalty.tier,
      },
      coupon_discount: {
        applied: !!selectedCoupon,
        code: selectedCoupon,
        amount: couponDiscountAmount,
        message: selectedCoupon ? 'Coupon applied' : '',
      },
      total_discount: tierDiscountAmount + couponDiscountAmount,
      final_amount: finalAmount,
      points_to_earn: pointsToEarn,
      savings: tierDiscountAmount + couponDiscountAmount,
    });
  };

  useEffect(() => {
    if (loyaltyInfo) {
      calculatePricing(loyaltyInfo);
    }
  }, [selectedCoupon]);

  const handlePaymentDetailsSubmit = (details: any) => {
    setPaymentDetails(details);
    setPaymentVerified(true);
  };

  const handleCheckout = async () => {
    if (!deliveryAddress && fulfillmentOption === 'Ship to Home') {
      alert('Please enter delivery address');
      return;
    }

    if (!paymentVerified) {
      alert('Please verify your payment details');
      return;
    }

    setIsProcessing(true);

    try {
      console.log('🛒 Starting checkout with:', {
        session_id: sessionId,
        customer_id: customerId,
        payment_method: paymentMethod,
        fulfillment_option: fulfillmentOption,
      });

      const response = await checkoutAPI({
        session_id: sessionId,
        customer_id: customerId,
        payment_method: paymentMethod,
        fulfillment_option: fulfillmentOption,
        delivery_address: fulfillmentOption === 'Ship to Home' ? deliveryAddress : undefined,
        store_location: fulfillmentOption !== 'Ship to Home' ? storeLocation : undefined,
      });

      console.log('✅ Checkout response:', response);

      if (response.success && response.order) {
        console.log('📦 Order data:', response.order);
        console.log('🚀 Navigating to confirmation page...');

        // Navigate FIRST, then clear cart
        // This ensures the order data is passed before any re-renders
        navigate('/confirmation', {
          state: { order: response.order },
          replace: true
        });

        // Clear cart after a short delay to ensure navigation happens first
        setTimeout(() => {
          clearCart();
        }, 100);
      } else {
        console.error('❌ No order data in response:', response);
        alert('Order was not created properly. Please try again.');
      }
    } catch (error: any) {
      console.error('❌ Checkout error:', error);
      console.error('Error details:', error.response?.data || error.message);
      alert(`Checkout failed: ${error.response?.data?.detail || error.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  if (!pricing || !loyaltyInfo) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Checkout</h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Forms */}
          <div className="lg:col-span-2 space-y-6">
            {/* Fulfillment Options */}
            <div className="card">
              <div className="flex items-center gap-3 mb-4">
                <Truck className="h-5 w-5 text-primary" />
                <h2 className="text-xl font-semibold">Delivery Options</h2>
              </div>

              <div className="space-y-3">
                {[
                  { value: 'Ship to Home', icon: Truck, time: '2-3 days', cost: 'Free' },
                  { value: 'Click & Collect', icon: Store, time: 'Same day', cost: 'Free' },
                  { value: 'In-Store Try-on', icon: MapPin, time: 'Visit anytime', cost: 'Free' },
                ].map((option) => (
                  <label
                    key={option.value}
                    className={`flex items-center gap-4 p-4 border-2 rounded-lg cursor-pointer transition-all ${
                      fulfillmentOption === option.value
                        ? 'border-primary bg-primary-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <input
                      type="radio"
                      name="fulfillment"
                      value={option.value}
                      checked={fulfillmentOption === option.value}
                      onChange={(e) => setFulfillmentOption(e.target.value)}
                      className="w-4 h-4 text-primary"
                    />
                    <option.icon className="h-5 w-5 text-gray-600" />
                    <div className="flex-1">
                      <p className="font-medium text-gray-900">{option.value}</p>
                      <p className="text-sm text-gray-600">{option.time} • {option.cost}</p>
                    </div>
                  </label>
                ))}
              </div>

              {fulfillmentOption === 'Ship to Home' && (
                <div className="mt-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Delivery Address
                  </label>
                  <textarea
                    value={deliveryAddress}
                    onChange={(e) => setDeliveryAddress(e.target.value)}
                    rows={3}
                    className="input"
                    placeholder="Enter your complete address"
                  />
                </div>
              )}

              {fulfillmentOption !== 'Ship to Home' && (
                <div className="mt-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Store Location
                  </label>
                  <select
                    value={storeLocation}
                    onChange={(e) => setStoreLocation(e.target.value)}
                    className="input"
                  >
                    <option value="Mumbai">Phoenix Mills, Mumbai</option>
                    <option value="Delhi">Select Citywalk, Delhi</option>
                    <option value="Bangalore">UB City, Bangalore</option>
                  </select>
                </div>
              )}
            </div>

            {/* Payment Methods */}
            <div className="card">
              <div className="flex items-center gap-3 mb-4">
                <CreditCard className="h-5 w-5 text-primary" />
                <h2 className="text-xl font-semibold">Payment Details</h2>
                {paymentVerified && (
                  <span className="ml-auto flex items-center gap-1 text-green-600 text-sm">
                    <CheckCircle className="h-4 w-4" />
                    Verified
                  </span>
                )}
              </div>

              <PaymentForm
                paymentMethod={paymentMethod}
                onPaymentMethodChange={setPaymentMethod}
                onPaymentDetailsSubmit={handlePaymentDetailsSubmit}
              />
            </div>

            {/* Coupons */}
            {availableCoupons.length > 0 && (
              <div className="card">
                <div className="flex items-center gap-3 mb-4">
                  <Tag className="h-5 w-5 text-primary" />
                  <h2 className="text-xl font-semibold">Available Coupons</h2>
                </div>

                <div className="space-y-2">
                  {availableCoupons.map((coupon) => (
                    <label
                      key={coupon.code}
                      className={`flex items-center gap-4 p-3 border-2 rounded-lg cursor-pointer transition-all ${
                        selectedCoupon === coupon.code
                          ? 'border-accent bg-accent-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <input
                        type="radio"
                        name="coupon"
                        value={coupon.code}
                        checked={selectedCoupon === coupon.code}
                        onChange={(e) => setSelectedCoupon(e.target.value)}
                        className="w-4 h-4 text-accent"
                      />
                      <div className="flex-1">
                        <p className="font-semibold text-gray-900">{coupon.code}</p>
                        <p className="text-sm text-gray-600">{coupon.description}</p>
                      </div>
                      <span className="font-bold text-accent">{coupon.discount}</span>
                    </label>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Right Column - Order Summary */}
          <div className="lg:col-span-1">
            <div className="card sticky top-24">
              <h2 className="text-xl font-semibold mb-4">Order Summary</h2>

              {/* Loyalty Badge */}
              <div className={`flex items-center gap-2 p-3 rounded-lg mb-4 ${getTierBadgeColor(loyaltyInfo.tier)}`}>
                <Award className="h-5 w-5" />
                <div>
                  <p className="font-semibold">{loyaltyInfo.tier} Member</p>
                  <p className="text-xs">{loyaltyInfo.points} points</p>
                </div>
              </div>

              {/* Items */}
              <div className="space-y-3 mb-4 pb-4 border-b">
                {cart.items.map((item) => (
                  <div key={item.product_id} className="flex justify-between text-sm">
                    <span className="text-gray-600">
                      {item.product_name} × {item.quantity}
                    </span>
                    <span className="font-medium">{formatPrice(item.price * item.quantity)}</span>
                  </div>
                ))}
              </div>

              {/* Pricing Breakdown */}
              <div className="space-y-3 mb-4 pb-4 border-b">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Subtotal</span>
                  <span className="font-medium">{formatPrice(pricing.subtotal)}</span>
                </div>
                
                <div className="flex justify-between text-sm text-green-600">
                  <span>{loyaltyInfo.tier} Discount ({pricing.tier_discount.percentage}%)</span>
                  <span>-{formatPrice(pricing.tier_discount.amount)}</span>
                </div>

                {pricing.coupon_discount.applied && (
                  <div className="flex justify-between text-sm text-green-600">
                    <span>Coupon ({pricing.coupon_discount.code})</span>
                    <span>-{formatPrice(pricing.coupon_discount.amount)}</span>
                  </div>
                )}
              </div>

              {/* Total */}
              <div className="flex justify-between text-lg font-bold mb-4">
                <span>Total</span>
                <span className="text-primary">{formatPrice(pricing.final_amount)}</span>
              </div>

              {/* Savings & Points */}
              <div className="bg-green-50 p-3 rounded-lg mb-4 space-y-1">
                <p className="text-sm text-green-800">
                  💰 You're saving {formatPrice(pricing.savings)}!
                </p>
                <p className="text-sm text-green-800">
                  ⭐ You'll earn {pricing.points_to_earn} points
                </p>
              </div>

              {/* Checkout Button */}
              <button
                onClick={handleCheckout}
                disabled={isProcessing}
                className="btn btn-primary w-full text-lg py-3 disabled:opacity-50"
              >
                {isProcessing ? (
                  <span className="flex items-center justify-center gap-2">
                    <Loader2 className="h-5 w-5 animate-spin" />
                    Processing...
                  </span>
                ) : (
                  `Pay ${formatPrice(pricing.final_amount)}`
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
