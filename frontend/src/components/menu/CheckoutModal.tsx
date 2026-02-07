"use client";
import { useState } from "react";
import { X, MapPin, Phone, User, CreditCard, Banknote, QrCode, Loader2 } from "lucide-react";
import Modal from "@/components/ui/Modal";
import { formatCurrency } from "@/lib/utils";

export interface CheckoutData {
  customer_name: string;
  customer_phone: string;
  delivery_address: string;
  payment_method: string;
  order_type: 'delivery' | 'takeout' | 'dine_in';
}

interface CheckoutModalProps {
  isOpen: boolean;
  onClose: () => void;
  total: number;
  onConfirm: (data: CheckoutData) => void;
  loading: boolean;
}

export default function CheckoutModal({ isOpen, onClose, total, onConfirm, loading }: CheckoutModalProps) {
  const [step, setStep] = useState(1);
  const [orderType, setOrderType] = useState<'delivery' | 'takeout' | 'dine_in'>('delivery');
  const [formData, setFormData] = useState({
    name: "",
    phone: "",
    address: "",
    payment: "pix"
  });

  const handleSubmit = () => {
    // Validação de Endereço para Delivery
    if (orderType === 'delivery' && !formData.address.trim()) {
      alert("Por favor, informe o endereço de entrega.");
      return;
    }
    if (!formData.name.trim() || !formData.phone.trim()) {
      alert("Nome e telefone são obrigatórios.");
      return;
    }

    onConfirm({
      customer_name: formData.name,
      customer_phone: formData.phone,
      delivery_address: formData.address,
      payment_method: formData.payment,
      order_type: orderType
    });
  };

  if (!isOpen) return null;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Finalizar Pedido">
      <div className="space-y-6">
        {/* Tipo de Pedido */}
        <div className="flex bg-gray-100 p-1 rounded-xl">
          <button 
            onClick={() => setOrderType('delivery')}
            className={`flex-1 py-2 rounded-lg text-sm font-bold transition-all ${orderType === 'delivery' ? 'bg-white shadow text-orange-600' : 'text-gray-500'}`}
          >
            Entrega
          </button>
          <button 
            onClick={() => setOrderType('takeout')}
            className={`flex-1 py-2 rounded-lg text-sm font-bold transition-all ${orderType === 'takeout' ? 'bg-white shadow text-orange-600' : 'text-gray-500'}`}
          >
            Retirada
          </button>
        </div>

        {/* Formulário */}
        <div className="space-y-4">
          <div className="relative">
            <User className="absolute left-3 top-3.5 text-gray-400" size={18} />
            <input 
              type="text" 
              placeholder="Seu Nome"
              className="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:border-orange-500 outline-none"
              value={formData.name}
              onChange={e => setFormData({...formData, name: e.target.value})}
            />
          </div>
          <div className="relative">
            <Phone className="absolute left-3 top-3.5 text-gray-400" size={18} />
            <input 
              type="tel" 
              placeholder="Seu WhatsApp"
              className="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:border-orange-500 outline-none"
              value={formData.phone}
              onChange={e => setFormData({...formData, phone: e.target.value})}
            />
          </div>
          
          {orderType === 'delivery' && (
            <div className="relative animate-in fade-in slide-in-from-top-2">
              <MapPin className="absolute left-3 top-3.5 text-gray-400" size={18} />
              <textarea 
                placeholder="Endereço completo (Rua, Número, Bairro, Complemento)"
                className="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:border-orange-500 outline-none h-24 resize-none"
                value={formData.address}
                onChange={e => setFormData({...formData, address: e.target.value})}
              />
            </div>
          )}
        </div>

        {/* Pagamento */}
        <div>
          <p className="text-xs font-bold text-gray-500 uppercase mb-3">Forma de Pagamento</p>
          <div className="grid grid-cols-3 gap-3">
            {[
              { id: 'pix', label: 'Pix', icon: QrCode },
              { id: 'card', label: 'Cartão', icon: CreditCard },
              { id: 'cash', label: 'Dinheiro', icon: Banknote },
            ].map(method => (
              <button
                key={method.id}
                onClick={() => setFormData({...formData, payment: method.id})}
                className={`flex flex-col items-center justify-center p-3 rounded-xl border-2 transition-all ${
                  formData.payment === method.id 
                    ? 'border-orange-500 bg-orange-50 text-orange-700' 
                    : 'border-gray-100 bg-white text-gray-500 hover:border-gray-300'
                }`}
              >
                <method.icon size={24} className="mb-1" />
                <span className="text-xs font-bold">{method.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Total e Ação */}
        <div className="pt-4 border-t border-gray-100">
          <div className="flex justify-between items-center mb-4">
            <span className="text-gray-500 font-medium">Total a Pagar</span>
            <span className="text-2xl font-black text-gray-900">{formatCurrency(total)}</span>
          </div>
          <button 
            onClick={handleSubmit}
            disabled={loading}
            className="w-full bg-orange-600 hover:bg-orange-700 text-white py-4 rounded-xl font-bold shadow-lg flex items-center justify-center gap-2 disabled:opacity-70 transition-all active:scale-[0.98]"
          >
            {loading ? <Loader2 className="animate-spin" /> : "Confirmar Pedido"}
          </button>
        </div>
      </div>
    </Modal>
  );
}
