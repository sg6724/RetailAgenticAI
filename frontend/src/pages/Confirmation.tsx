import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { CheckCircle, Package, Truck, Store, Home, Printer, AlertCircle } from 'lucide-react';
import { formatPrice, formatDate } from '@/lib/utils';
import { useStore } from '@/store/useStore';
import type { OrderConfirmation } from '@/types';

export const Confirmation: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [isChecking, setIsChecking] = useState(true);
  const order = location.state?.order as OrderConfirmation;
  const { loyaltyInfo } = useStore();

  useEffect(() => {
    console.log('🔍 Confirmation page - checking order data...');
    console.log('Location state:', location.state);
    console.log('Order data:', order);
    console.log('Order exists?', !!order);
    console.log('Order order_id:', order?.order_id);

    // Give it a moment to ensure state is loaded
    const timer = setTimeout(() => {
      if (!order || !order.order_id) {
        console.error('❌ No order data found after timeout');
        console.error('Full location:', location);
        console.error('Order object:', order);
        alert('Order confirmation data not found. Redirecting to home...');
        navigate('/', { replace: true });
      } else {
        console.log('✅ Order confirmation loaded successfully!');
        console.log('Order ID:', order.order_id);
        console.log('Total Amount:', order.total_amount);
        setIsChecking(false);
      }
    }, 500);

    return () => clearTimeout(timer);
  }, [order, navigate, location]);

  if (isChecking) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-primary bg-opacity-10 rounded-full mb-4 animate-pulse">
            <Package className="h-8 w-8 text-primary" />
          </div>
          <p className="text-lg text-gray-600">Loading order confirmation...</p>
        </div>
      </div>
    );
  }

  if (!order) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto p-6">
          <AlertCircle className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Order Not Found</h2>
          <p className="text-gray-600 mb-6">
            We couldn't find your order confirmation. This might be a technical issue.
          </p>
          <button
            onClick={() => navigate('/')}
            className="btn btn-primary"
          >
            Return to Home
          </button>
        </div>
      </div>
    );
  }

  const getFulfillmentIcon = () => {
    const type = order.fulfillment_details?.type;
    if (type === 'Ship to Home') return Truck;
    if (type === 'Click & Collect') return Store;
    return Package;
  };

  const FulfillmentIcon = getFulfillmentIcon();

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Success Message */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-green-100 rounded-full mb-4">
            <CheckCircle className="h-12 w-12 text-green-600" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Order Confirmed! 🎉
          </h1>
          <p className="text-lg text-gray-600">
            Thank you for your purchase
          </p>
        </div>

        {/* Order Details Card */}
        <div className="card mb-6">
          <div className="border-b pb-4 mb-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Order ID</p>
                <p className="text-xl font-bold text-gray-900">{order.order_id}</p>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-600">Order Date</p>
                <p className="font-medium text-gray-900">
                  {formatDate(order.timestamp)}
                </p>
              </div>
            </div>
          </div>

          {/* Payment Info */}
          <div className="space-y-3 mb-6">
            <div className="flex justify-between">
              <span className="text-gray-600">Total Amount</span>
              <span className="text-2xl font-bold text-primary">
                {formatPrice(order.total_amount)}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Payment Status</span>
              <span className="badge badge-success">
                {order.payment_status}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Transaction ID</span>
              <span className="font-mono text-sm text-gray-900">
                {order.transaction_id}
              </span>
            </div>
          </div>

          {/* Fulfillment Details */}
          <div className="bg-blue-50 p-4 rounded-lg">
            <div className="flex items-start gap-3">
              <FulfillmentIcon className="h-6 w-6 text-blue-600 mt-1" />
              <div className="flex-1">
                <p className="font-semibold text-gray-900 mb-2">
                  {order.fulfillment_details?.type}
                </p>
                
                {order.fulfillment_details?.type === 'Ship to Home' && (
                  <>
                    <p className="text-sm text-gray-600 mb-1">
                      <strong>Delivery Address:</strong>
                    </p>
                    <p className="text-sm text-gray-700 mb-3">
                      {order.fulfillment_details?.delivery_address}
                    </p>
                    <div className="bg-white p-3 rounded-md border-l-4 border-blue-500 mb-2">
                      <p className="text-sm font-semibold text-blue-900 mb-1">
                        📦 Estimated Delivery
                      </p>
                      <p className="text-lg font-bold text-blue-700">
                        {order.estimated_delivery}
                      </p>
                      <p className="text-xs text-gray-600 mt-1">
                        Your order will arrive in 2 business days
                      </p>
                    </div>
                    <p className="text-sm text-gray-600">
                      <strong>Carrier:</strong> {order.fulfillment_details?.carrier || 'BlueDart Express'}
                    </p>
                  </>
                )}

                {order.fulfillment_details?.type === 'Click & Collect' && (
                  <>
                    <p className="text-sm text-gray-600 mb-1">
                      <strong>Pickup Location:</strong>
                    </p>
                    <p className="text-sm text-gray-700 mb-3">
                      {order.fulfillment_details?.pickup_location || order.fulfillment_details?.store_location}
                    </p>
                    <div className="bg-white p-3 rounded-md border-l-4 border-green-500 mb-2">
                      <p className="text-sm font-semibold text-green-900 mb-1">
                        🏪 Ready for Pickup
                      </p>
                      <p className="text-lg font-bold text-green-700">
                        {order.estimated_delivery}
                      </p>
                    </div>
                    <p className="text-sm text-gray-500 mt-2 bg-white p-2 rounded">
                      💡 {order.fulfillment_details?.pickup_instructions || 'Show order ID at the collection counter'}
                    </p>
                  </>
                )}

                {order.fulfillment_details?.type === 'In-Store Try-on' && (
                  <>
                    <p className="text-sm text-gray-600 mb-1">
                      <strong>Store Location:</strong>
                    </p>
                    <p className="text-sm text-gray-700 mb-2">
                      {order.fulfillment_details?.store_location}
                    </p>
                    <p className="text-sm text-gray-600">
                      <strong>Store Hours:</strong> {order.fulfillment_details?.store_hours || '10 AM - 10 PM'}
                    </p>
                    <p className="text-sm text-gray-500 mt-2">
                      Visit the store anytime during business hours to try on your reserved items
                    </p>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Next Steps */}
        <div className="card mb-6 no-print">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">What's Next?</h2>
          <div className="space-y-3">
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 bg-primary text-white rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0">
                1
              </div>
              <div>
                <p className="font-medium text-gray-900">Order Confirmation</p>
                <p className="text-sm text-gray-600">
                  You'll receive an email confirmation shortly
                </p>
              </div>
            </div>
            
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 bg-primary text-white rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0">
                2
              </div>
              <div>
                <p className="font-medium text-gray-900">
                  {order.fulfillment_details?.type === 'Ship to Home' ? 'Shipping Updates' : 'Preparation'}
                </p>
                <p className="text-sm text-gray-600">
                  {order.fulfillment_details?.type === 'Ship to Home' 
                    ? 'Track your order status and delivery updates'
                    : 'We\'ll notify you when your order is ready'}
                </p>
              </div>
            </div>
            
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 bg-primary text-white rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0">
                3
              </div>
              <div>
                <p className="font-medium text-gray-900">Feedback</p>
                <p className="text-sm text-gray-600">
                  We'll ask for your feedback in 48 hours
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 no-print">
          <button
            onClick={() => window.print()}
            className="btn btn-primary flex-1 flex items-center justify-center gap-2"
          >
            <Printer className="h-5 w-5" />
            Print Receipt
          </button>
          <button
            onClick={() => navigate('/')}
            className="btn btn-secondary flex-1 flex items-center justify-center gap-2"
          >
            <Home className="h-5 w-5" />
            Continue Shopping
          </button>
        </div>

        {/* Print-friendly receipt information */}
        <div className="print:block hidden mt-8 border-t-2 border-dashed pt-8">
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold">ORDER RECEIPT</h2>
            <p className="text-sm text-gray-600">Thank you for shopping with us!</p>
          </div>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p className="font-semibold">Order ID:</p>
              <p>{order.order_id}</p>
            </div>
            <div>
              <p className="font-semibold">Date:</p>
              <p>{formatDate(order.timestamp)}</p>
            </div>
            <div>
              <p className="font-semibold">Total Amount:</p>
              <p className="text-xl font-bold">{formatPrice(order.total_amount)}</p>
            </div>
            <div>
              <p className="font-semibold">Payment Status:</p>
              <p>{order.payment_status}</p>
            </div>
          </div>
          {loyaltyInfo && (
            <div className="mt-4 text-sm">
              <p className="font-semibold">Loyalty Member:</p>
              <p>{loyaltyInfo.tier} - {loyaltyInfo.points} points</p>
            </div>
          )}
        </div>

        {/* Support Message */}
        <div className="mt-8 text-center no-print">
          <p className="text-sm text-gray-600">
            Need help? Contact our support team or chat with our AI assistant
          </p>
        </div>
      </div>
    </div>
  );
};
