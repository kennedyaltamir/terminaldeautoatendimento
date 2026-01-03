"use client";

import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { Plus, Trash2, User, Shield, ChefHat, Search, Bike } from "lucide-react";
import { toast, Toaster } from "sonner";
import Modal from "@/components/ui/Modal";
import AuthInput from "@/components/ui/AuthInput";
import { getToken } from "@/lib/auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

interface Employee {
  id: number;
  name: string;
  email: string;
  role: "kitchen" | "cashier" | "manager" | "driver";
  is_active: boolean;
}

export default function TeamPage({ params }: { params: { slug: string } }) {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  const { register, handleSubmit, reset, formState: { errors } } = useForm();

  const fetchEmployees = async () => {
    try {
      const token = getToken();
      const res = await fetch(`${API_URL}/admin/employees`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setEmployees(data);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchEmployees(); }, []);

  const onSubmit = async (data: any) => {
    try {
      const token = getToken();
      const res = await fetch(`${API_URL}/admin/employees`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}` 
        },
        body: JSON.stringify(data)
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Erro ao criar");
      }

      toast.success("Funcionário adicionado!");
      setIsModalOpen(false);
      reset();
      fetchEmployees();
    } catch (e: any) {
      toast.error(e.message);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Remover este funcionário?")) return;
    try {
      const token = getToken();
      await fetch(`${API_URL}/admin/employees/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` }
      });
      toast.success("Removido com sucesso");
      fetchEmployees();
    } catch (e) {
      toast.error("Erro ao remover");
    }
  };

  const getRoleBadge = (role: string) => {
    switch(role) {
      case 'manager': return <span className="bg-purple-100 text-purple-700 px-2 py-1 rounded text-xs font-bold flex items-center gap-1"><Shield size={12}/> Gerente</span>;
      case 'kitchen': return <span className="bg-orange-100 text-orange-700 px-2 py-1 rounded text-xs font-bold flex items-center gap-1"><ChefHat size={12}/> Cozinha</span>;
      case 'driver': return <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs font-bold flex items-center gap-1"><Bike size={12}/> Entregador</span>;
      default: return <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs font-bold flex items-center gap-1"><User size={12}/> Garçom</span>;
    }
  };

  return (
    <div className="space-y-6 pb-20">
      <Toaster position="top-right" richColors />
      
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">Equipe</h1>
          <p className="text-gray-400 text-sm">Gerencie quem tem acesso ao sistema.</p>
        </div>
        <button 
          onClick={() => setIsModalOpen(true)}
          className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-xl font-bold flex items-center gap-2 transition-colors"
        >
          <Plus size={20} /> Adicionar Membro
        </button>
      </div>

      <div className="bg-gray-800 border border-gray-700 rounded-xl overflow-hidden">
        <table className="w-full text-left text-gray-300">
          <thead className="bg-gray-900 text-xs uppercase font-bold text-gray-500">
            <tr>
              <th className="px-6 py-4">Nome</th>
              <th className="px-6 py-4">Email (Login)</th>
              <th className="px-6 py-4">Função</th>
              <th className="px-6 py-4 text-right">Ações</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-700">
            {loading ? (
              <tr><td colSpan={4} className="text-center py-8">Carregando...</td></tr>
            ) : employees.length === 0 ? (
              <tr><td colSpan={4} className="text-center py-8 text-gray-500">Nenhum funcionário cadastrado.</td></tr>
            ) : (
              employees.map((emp) => (
                <tr key={emp.id} className="hover:bg-gray-700/50 transition-colors">
                  <td className="px-6 py-4 font-bold text-white">{emp.name}</td>
                  <td className="px-6 py-4 font-mono text-sm">{emp.email}</td>
                  <td className="px-6 py-4">{getRoleBadge(emp.role)}</td>
                  <td className="px-6 py-4 text-right">
                    <button onClick={() => handleDelete(emp.id)} className="text-red-400 hover:text-red-300 p-2 hover:bg-red-900/20 rounded transition-colors">
                      <Trash2 size={18} />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Novo Membro">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <AuthInput 
            label="Nome" 
            icon={User} 
            placeholder="Ex: João Silva" 
            {...register("name", { required: true })} 
          />
          <AuthInput 
            label="Email de Acesso" 
            icon={User} 
            type="email"
            placeholder="joao@restaurante.com" 
            {...register("email", { required: true })} 
          />
          <AuthInput 
            label="Senha" 
            icon={Shield} 
            type="password"
            placeholder="******" 
            {...register("password", { required: true, minLength: 4 })} 
          />
          
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-1">Função</label>
            <select {...register("role")} className="w-full border rounded-lg p-3 bg-white">
              <option value="cashier">Garçom / Caixa</option>
              <option value="kitchen">Cozinha (KDS)</option>
              <option value="driver">Entregador (Motoboy)</option>
              <option value="manager">Gerente</option>
            </select>
          </div>

          <button type="submit" className="w-full bg-orange-600 text-white py-3 rounded-xl font-bold hover:bg-orange-700 transition-colors">
            Cadastrar
          </button>
        </form>
      </Modal>
    </div>
  );
}