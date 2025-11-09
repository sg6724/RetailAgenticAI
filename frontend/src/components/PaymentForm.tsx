import React, { useState } from 'react';
import { CreditCard, Smartphone, Wallet, Lock, CheckCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

interface PaymentFormProps {
  paymentMethod: string;
  onPaymentMethodChange: (method: string) => void;
  onPaymentDetailsSubmit: (details: any) => void;
}

export const PaymentForm: React.FC<PaymentFormProps> = ({
  paymentMethod,
  onPaymentMethodChange,
  onPaymentDetailsSubmit,
}) => {
  const [cardNumber, setCardNumber] = useState('');
  const [cardName, setCardName] = useState('');
  const [expiryDate, setExpiryDate] = useState('');
  const [cvv, setCvv] = useState('');
  const [upiId, setUpiId] = useState('');
  const [walletProvider, setWalletProvider] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});

  const formatCardNumber = (value: string) => {
    const cleaned = value.replace(/\s/g, '');
    const formatted = cleaned.match(/.{1,4}/g)?.join(' ') || cleaned;
    return formatted.slice(0, 19); // 16 digits + 3 spaces
  };

  const formatExpiryDate = (value: string) => {
    const cleaned = value.replace(/\D/g, '');
    if (cleaned.length >= 2) {
      return cleaned.slice(0, 2) + '/' + cleaned.slice(2, 4);
    }
    return cleaned;
  };

  const validateCard = () => {
    const newErrors: Record<string, string> = {};

    if (!cardNumber || cardNumber.replace(/\s/g, '').length !== 16) {
      newErrors.cardNumber = 'Please enter a valid 16-digit card number';
    }

    if (!cardName || cardName.length < 3) {
      newErrors.cardName = 'Please enter the cardholder name';
    }

    if (!expiryDate || expiryDate.length !== 5) {
      newErrors.expiryDate = 'Please enter expiry date (MM/YY)';
    } else {
      const [month, year] = expiryDate.split('/');
      const currentYear = new Date().getFullYear() % 100;
      const currentMonth = new Date().getMonth() + 1;
      
      if (parseInt(month) < 1 || parseInt(month) > 12) {
        newErrors.expiryDate = 'Invalid month';
      } else if (parseInt(year) < currentYear || 
                (parseInt(year) === currentYear && parseInt(month) < currentMonth)) {
        newErrors.expiryDate = 'Card has expired';
      }
    }

    if (!cvv || cvv.length < 3) {
      newErrors.cvv = 'Please enter CVV';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const validateUPI = () => {
    const newErrors: Record<string, string> = {};
    
    if (!upiId || !upiId.includes('@')) {
      newErrors.upiId = 'Please enter a valid UPI ID (e.g., user@paytm)';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const validateWallet = () => {
    const newErrors: Record<string, string> = {};
    
    if (!walletProvider) {
      newErrors.walletProvider = 'Please select a wallet provider';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = () => {
    let isValid = false;
    let details = {};

    if (paymentMethod === 'Card') {
      isValid = validateCard();
      if (isValid) {
        details = {
          type: 'Card',
          cardNumber: cardNumber.replace(/\s/g, ''),
          cardName,
          expiryDate,
          cvv,
        };
      }
    } else if (paymentMethod === 'UPI') {
      isValid = validateUPI();
      if (isValid) {
        details = {
          type: 'UPI',
          upiId,
        };
      }
    } else if (paymentMethod === 'Wallet') {
      isValid = validateWallet();
      if (isValid) {
        details = {
          type: 'Wallet',
          provider: walletProvider,
        };
      }
    }

    if (isValid) {
      onPaymentDetailsSubmit(details);
    }
  };

  return (
    <div className="space-y-6">
      {/* Payment Method Selection */}
      <div className="grid grid-cols-3 gap-3">
        <button
          onClick={() => onPaymentMethodChange('Card')}
          className={cn(
            "p-4 border-2 rounded-lg transition-all flex flex-col items-center gap-2",
            paymentMethod === 'Card'
              ? "border-primary bg-primary-50"
              : "border-gray-200 hover:border-gray-300"
          )}
        >
          <CreditCard className="h-6 w-6" />
          <span className="text-sm font-medium">Card</span>
        </button>

        <button
          onClick={() => onPaymentMethodChange('UPI')}
          className={cn(
            "p-4 border-2 rounded-lg transition-all flex flex-col items-center gap-2",
            paymentMethod === 'UPI'
              ? "border-primary bg-primary-50"
              : "border-gray-200 hover:border-gray-300"
          )}
        >
          <Smartphone className="h-6 w-6" />
          <span className="text-sm font-medium">UPI</span>
        </button>

        <button
          onClick={() => onPaymentMethodChange('Wallet')}
          className={cn(
            "p-4 border-2 rounded-lg transition-all flex flex-col items-center gap-2",
            paymentMethod === 'Wallet'
              ? "border-primary bg-primary-50"
              : "border-gray-200 hover:border-gray-300"
          )}
        >
          <Wallet className="h-6 w-6" />
          <span className="text-sm font-medium">Wallet</span>
        </button>
      </div>

      {/* Card Payment Form */}
      {paymentMethod === 'Card' && (
        <div className="space-y-4 animate-fadeIn">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Card Number
            </label>
            <div className="relative">
              <input
                type="text"
                value={cardNumber}
                onChange={(e) => setCardNumber(formatCardNumber(e.target.value))}
                placeholder="1234 5678 9012 3456"
                className={cn(
                  "input pl-10",
                  errors.cardNumber && "border-red-500"
                )}
                maxLength={19}
              />
              <CreditCard className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
            </div>
            {errors.cardNumber && (
              <p className="text-red-500 text-xs mt-1">{errors.cardNumber}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Cardholder Name
            </label>
            <input
              type="text"
              value={cardName}
              onChange={(e) => setCardName(e.target.value.toUpperCase())}
              placeholder="JOHN DOE"
              className={cn(
                "input",
                errors.cardName && "border-red-500"
              )}
            />
            {errors.cardName && (
              <p className="text-red-500 text-xs mt-1">{errors.cardName}</p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Expiry Date
              </label>
              <input
                type="text"
                value={expiryDate}
                onChange={(e) => setExpiryDate(formatExpiryDate(e.target.value))}
                placeholder="MM/YY"
                className={cn(
                  "input",
                  errors.expiryDate && "border-red-500"
                )}
                maxLength={5}
              />
              {errors.expiryDate && (
                <p className="text-red-500 text-xs mt-1">{errors.expiryDate}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                CVV
              </label>
              <input
                type="password"
                value={cvv}
                onChange={(e) => setCvv(e.target.value.replace(/\D/g, ''))}
                placeholder="123"
                className={cn(
                  "input",
                  errors.cvv && "border-red-500"
                )}
                maxLength={4}
              />
              {errors.cvv && (
                <p className="text-red-500 text-xs mt-1">{errors.cvv}</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* UPI Payment Form */}
      {paymentMethod === 'UPI' && (
        <div className="space-y-4 animate-fadeIn">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              UPI ID
            </label>
            <div className="relative">
              <input
                type="text"
                value={upiId}
                onChange={(e) => setUpiId(e.target.value.toLowerCase())}
                placeholder="yourname@paytm"
                className={cn(
                  "input pl-10",
                  errors.upiId && "border-red-500"
                )}
              />
              <Smartphone className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
            </div>
            {errors.upiId && (
              <p className="text-red-500 text-xs mt-1">{errors.upiId}</p>
            )}
          </div>

          <div className="bg-blue-50 p-4 rounded-lg">
            <p className="text-sm text-blue-800">
              <CheckCircle className="h-4 w-4 inline mr-2" />
              Supports Google Pay, PhonePe, Paytm, and all UPI apps
            </p>
          </div>
        </div>
      )}

      {/* Wallet Payment Form */}
      {paymentMethod === 'Wallet' && (
        <div className="space-y-4 animate-fadeIn">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Wallet
            </label>
            <select
              value={walletProvider}
              onChange={(e) => setWalletProvider(e.target.value)}
              className={cn(
                "input",
                errors.walletProvider && "border-red-500"
              )}
            >
              <option value="">Choose a wallet</option>
              <option value="paytm">Paytm Wallet</option>
              <option value="amazonpay">Amazon Pay</option>
              <option value="mobikwik">MobiKwik</option>
              <option value="freecharge">FreeCharge</option>
            </select>
            {errors.walletProvider && (
              <p className="text-red-500 text-xs mt-1">{errors.walletProvider}</p>
            )}
          </div>
        </div>
      )}

      {/* Security Badge */}
      <div className="flex items-center justify-center gap-2 text-sm text-gray-600 bg-gray-50 p-3 rounded-lg">
        <Lock className="h-4 w-4" />
        <span>Secured by 256-bit SSL encryption</span>
      </div>

      {/* Submit Button */}
      <button
        onClick={handleSubmit}
        className="btn btn-primary w-full text-lg py-3"
      >
        Verify & Continue
      </button>
    </div>
  );
};
