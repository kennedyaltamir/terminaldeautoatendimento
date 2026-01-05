"use client";

import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { Plus, Trash2, User, Shield, ChefHat, Search, Bike, Users } from "lucide-react";
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

type RoleFilter = 'all' | 'manager' | 'cashier' | 'kitchen' | 'driver';

export default function TeamPage({ params }: { params: { slug: string } }) {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [activeTab, setActiveTab] = useState<RoleFilter>('all');
  const [searchTerm, setSearchTerm] = useState("");
  
  const { register, handleSubmit, reset } = useForm();

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
      case 'manager': return <span className="bg-purple-100 text-purple-700 px-2 py-1 rounded text-xs font-bold flex items-center gap-1 w-fit"><Shield size={12}/> Gerente</span>;
      case 'kitchen': return <span className="bg-orange-100 text-orange-700 px-2 py-1 rounded text-xs font-bold flex items-center gap-1 w-fit"><ChefHat size={12}/> Cozinha</span>;
      case 'driver': return <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs font-bold flex items-center gap-1 w-fit"><Bike size={12}/> Entregador</span>;
      default: return <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs font-bold flex items-center gap-1 w-fit"><User size={12}/> Garçom</span>;
    }
  };

  const filteredEmployees = employees.filter(emp => {
    const matchesRole = activeTab === 'all' || emp.role === activeTab;
    const matchesSearch = emp.name.toLowerCase().includes(searchTerm.toLowerCase()) || emp.email.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesRole && matchesSearch;
  });

  return (
    <div className="space-y-6 pb-20">
      <Toaster position="top-right" richColors />
      
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white flex items-center gap-2">
            <Users className="text-orange-500" /> Gestão de Equipe
          </h1>
          <p className="text-gray-400 text-sm mt-1">Controle de acesso e funções.</p>
        </div>
        <button 
          onClick={() => setIsModalOpen(true)}
          className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-xl font-bold flex items-center gap-2 transition-colors shadow-lg shadow-orange-900/20"
        >
          <Plus size={20} /> Adicionar Membro
        </button>
      </div>

      {/* Filtros e Busca */}
      <div className="flex flex-col md:flex-row gap-4 bg-gray-800 p-4 rounded-xl border border-gray-700">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
          <input 
            type="text" 
            placeholder="Buscar por nome ou email..." 
            className="w-full bg-gray-900 border border-gray-700 rounded-lg pl-10 pr-4 py-2 text-white focus:ring-2 focus:ring-orange-500 outline-none"
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
          />
        </div>
        
        <div className="flex gap-2 overflow-x-auto no-scrollbar">
          {[
            { id: 'all', label: 'Todos', icon: Users },
            { id: 'cashier', label: 'Garçons', icon: User },
            { id: 'kitchen', label: 'Cozinha', icon: ChefHat },
            { id: 'driver', label: 'Entregadores', icon: Bike },
            { id: 'manager', label: 'Gerentes', icon: Shield },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as RoleFilter)}
              className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-bold transition-all whitespace-nowrap ${
                activeTab === tab.id 
                  ? 'bg-gray-700 text-white shadow-sm ring-1 ring-gray-600' 
                  : 'text-gray-400 hover:text-white hover:bg-gray-700/50'
              }`}
            >
              <tab.icon size={14} />
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      <div className="bg-gray-800 border border-gray-700 rounded-xl overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
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
              ) : filteredEmployees.length === 0 ? (
                <tr><td colSpan={4} className="text-center py-12 text-gray-500">Nenhum membro encontrado nesta categoria.</td></tr>
              ) : (
                filteredEmployees.map((emp) => (
                  <tr key={emp.id} className="hover:bg-gray-700/50 transition-colors">
                    <td className="px-6 py-4 font-bold text-white">{emp.name}</td>
                    <td className="px-6 py-4 font-mono text-sm text-gray-400">{emp.email}</td>
                    <td className="px-6 py-4">{getRoleBadge(emp.role)}</td>
                    <td className="px-6 py-4 text-right">
                      <button 
                        onClick={() => handleDelete(emp.id)} 
                        className="text-red-400 hover:text-red-300 p-2 hover:bg-red-900/20 rounded-lg transition-colors"
                        title="Remover Acesso"
                      >
                        <Trash2 size={18} />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Novo Membro da Equipe">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="bg-blue-50 p-3 rounded-lg border border-blue-100 mb-4">
            <p className="text-xs text-blue-800">
              O novo membro receberá acesso imediato. Certifique-se de escolher a função correta para limitar as permissões.
            </p>
          </div>

          <AuthInput 
            label="Nome Completo" 
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
            label="Senha Inicial" 
            icon={Shield} 
            type="password"
            placeholder="******" 
            {...register("password", { required: true, minLength: 4 })} 
          />
          
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-1">Função & Permissões</label>
            <div className="grid grid-cols-1 gap-2">
              <label className="flex items-center gap-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
                <input type="radio" value="cashier" {...register("role")} defaultChecked className="accent-orange-600" />
                <div>
                  <span className="block font-bold text-sm text-gray-900">Garçom / Caixa</span>
                  <span className="block text-xs text-gray-500">Acesso ao App do Garçom e Mesas.</span>
                </div>
              </label>
              <label className="flex items-center gap-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
                <input type="radio" value="kitchen" {...register("role")} className="accent-orange-600" />
                <div>
                  <span className="block font-bold text-sm text-gray-900">Cozinha / Bar</span>
                  <span className="block text-xs text-gray-500">Acesso apenas ao Monitor KDS.</span>
                </div>
              </label>
              <label className="flex items-center gap-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
                <input type="radio" value="driver" {...register("role")} className="accent-orange-600" />
                <div>
                  <span className="block font-bold text-sm text-gray-900">Entregador</span>
                  <span className="block text-xs text-gray-500">Acesso ao App de Delivery.</span>
                </div>
              </label>
              <label className="flex items-center gap-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
                <input type="radio" value="manager" {...register("role")} className="accent-orange-600" />
                <div>
                  <span className="block font-bold text-sm text-gray-900">Gerente</span>
                  <span className="block text-xs text-gray-500">Acesso total (exceto dados do dono).</span>
                </div>
              </label>
            </div>
          </div>

          <button type="submit" className="w-full bg-orange-600 text-white py-3 rounded-xl font-bold hover:bg-orange-700 transition-colors shadow-lg">
            Cadastrar Membro
          </button>
        </form>
      </Modal>
    </div>
  );
}