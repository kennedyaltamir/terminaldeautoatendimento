"use client";

import { useEffect, useState, use, useMemo, useCallback } from "react";
import { getEmployees, createEmployee, updateEmployee, deleteEmployee } from "@/lib/employeeApi";
import { getCompanySettings } from "@/lib/api";
import { Employee, Company, RoleConfig } from "@/types";
import { 
  Check, FileText, History, Loader2, Crown, Shield, 
  DollarSign, ChefHat, Smartphone, Bike 
} from "lucide-react";
import { toast } from "sonner";
import Modal from "@/components/ui/Modal";
import RoleSelector from "@/components/admin/team/RoleSelector";
import UpgradeModal from "@/components/admin/team/UpgradeModal";
import AuditTimeline from "@/components/admin/team/AuditTimeline";
import EmployeeCard from "@/components/admin/team/EmployeeCard";
import TeamFilters, { SortOption, SortDirection, FilterStatus } from "@/components/admin/team/TeamFilters";
import PLGBanner from "@/components/admin/team/PLGBanner";
import { analytics } from "@/lib/analytics";
import { auditLogger } from "@/lib/audit-logger";
import { useOptimisticLocking } from "@/hooks/useOptimisticLocking";
import { useDebounce } from "@/hooks/useDebounce";

// 🛡️ Sincronização de Contrato v1.9: Adicionado contrastColor para conformidade WCAG AAA
const ROLE_CONFIG: Record<string, RoleConfig> = {
  owner: { 
    label: "Dono", 
    icon: Crown, 
    color: "text-yellow-500", 
    bg: "bg-yellow-500/10 border-yellow-500/20",
    contrastColor: "#EAB308" 
  },
  manager: { 
    label: "Gerente", 
    icon: Shield, 
    color: "text-purple-500", 
    bg: "bg-purple-500/10 border-purple-500/20",
    contrastColor: "#A855F7"
  },
  cashier: { 
    label: "Caixa", 
    icon: DollarSign, 
    color: "text-emerald-500", 
    bg: "bg-emerald-500/10 border-emerald-500/20",
    contrastColor: "#10B981"
  },
  kitchen: { 
    label: "Cozinha", 
    icon: ChefHat, 
    color: "text-orange-500", 
    bg: "bg-orange-500/10 border-orange-500/20",
    contrastColor: "#F97316"
  },
  waiter: { 
    label: "Garçom", 
    icon: Smartphone, 
    color: "text-blue-500", 
    bg: "bg-blue-500/10 border-blue-500/20",
    contrastColor: "#3B82F6"
  },
  driver: { 
    label: "Entregador", 
    icon: Bike, 
    color: "text-cyan-500", 
    bg: "bg-cyan-500/10 border-cyan-500/20",
    contrastColor: "#06B6D4"
  },
};

const FREE_LIMIT = 2; 

export default function TeamPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = use(params);

  const [employees, setEmployees] = useState<Employee[]>([]);
  const [company, setCompany] = useState<Company | null>(null);
  const [loading, setLoading] = useState(true);
  
  const [searchTerm, setSearchTerm] = useState("");
  const debouncedSearch = useDebounce(searchTerm, 300);
  const [filterStatus, setFilterStatus] = useState<FilterStatus>('all');
  const [sortBy, setSortBy] = useState<SortOption>('name');
  const [sortDirection, setSortDirection] = useState<SortDirection>('asc');

  const [isFormModalOpen, setIsFormModalOpen] = useState(false);
  const [isUpgradeModalOpen, setIsUpgradeModalOpen] = useState(false);
  const [activeTab, setActiveTab] = useState<'details' | 'history'>('details');
  
  const [editingEmployee, setEditingEmployee] = useState<Employee | null>(null);
  const [formData, setFormData] = useState({ name: "", email: "", role: "waiter", password: "" });
  const [saving, setSaving] = useState(false);
  
  const { trackVersion, isConflictError, handleConflict } = useOptimisticLocking<Employee>();

  const fetchData = useCallback(async () => {
    try {
      const [emps, comp] = await Promise.all([
        getEmployees(slug),
        getCompanySettings()
      ]);
      setEmployees(emps);
      setCompany(comp);
    } catch (e) {
      toast.error("Erro ao carregar dados da equipe.");
    } finally {
      setLoading(false);
    }
  }, [slug]);

  useEffect(() => {
    fetchData();
    analytics.track("view_team_management", { slug });
  }, [fetchData, slug]);

  useEffect(() => {
    if (debouncedSearch) {
      analytics.track("employee_search", { query: debouncedSearch, status: filterStatus });
    }
  }, [debouncedSearch, filterStatus]);

  const handleSortChange = (option: SortOption) => {
    if (sortBy === option) {
      setSortDirection(prev => prev === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(option);
      setSortDirection('asc');
    }
  };

  const handleNewMemberClick = () => {
    const isFree = company?.plan_tier === 'free';
    if (isFree && employees.length >= FREE_LIMIT) {
      analytics.track("limit_reached_trigger", { feature: "team_members", current_count: employees.length });
      setIsUpgradeModalOpen(true);
      return;
    }
    openFormModal();
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      if (editingEmployee) {
        await updateEmployee(slug, editingEmployee.id, { ...formData, updated_at: editingEmployee.updated_at });
        toast.success("Colaborador atualizado!");
        analytics.track("employee_role_updated", { role: formData.role });
      } else {
        await createEmployee(slug, formData);
        toast.success("Novo membro adicionado!");
        analytics.track("employee_created", { role: formData.role });
      }
      setIsFormModalOpen(false);
      fetchData();
    } catch (err: any) {
      if (isConflictError(err)) {
        handleConflict(() => { fetchData(); setIsFormModalOpen(false); });
        return;
      }
      if (err.message?.includes("email")) {
        toast.error("E-mail já cadastrado.");
        analytics.track("employee_creation_failed", { reason: "duplicate_email" });
      } else {
        toast.error("Erro ao salvar.", { description: err.message });
      }
    } finally {
      setSaving(false);
    }
  };

  const handleRevokeAccess = async (id: number, email: string) => {
    if (!confirm("⚠️ ATENÇÃO: Isso revogará o acesso IMEDIATAMENTE.\n\nO usuário será desconectado de todos os dispositivos.")) return;
    try {
      await deleteEmployee(slug, id);
      auditLogger.logAttempt(email, true, "ACCESS_REVOKED_BY_ADMIN");
      analytics.track("auth_revocation_success", { employee_id: id });
      toast.success("Acesso revogado com sucesso.");
      fetchData();
    } catch (e: any) {
      toast.error("Erro ao revogar acesso.");
      analytics.track("auth_revocation_failed", { error: e.message });
    }
  };

  const openFormModal = (employee?: Employee) => {
    setActiveTab('details');
    if (employee) {
      setEditingEmployee(employee);
      trackVersion(employee);
      setFormData({ name: employee.name, email: employee.email, role: employee.role, password: "" });
    } else {
      setEditingEmployee(null);
      setFormData({ name: "", email: "", role: "waiter", password: "" });
    }
    setIsFormModalOpen(true);
  };

  const openHistoryModal = (employee: Employee) => {
    setEditingEmployee(employee);
    setActiveTab('history');
    setIsFormModalOpen(true);
  };

  const filteredEmployees = useMemo(() => {
    let result = employees.filter(emp => {
      const matchesSearch = 
        emp.name.toLowerCase().includes(debouncedSearch.toLowerCase()) ||
        emp.email.toLowerCase().includes(debouncedSearch.toLowerCase()) ||
        emp.role.toLowerCase().includes(debouncedSearch.toLowerCase());
      
      const matchesStatus = 
        filterStatus === 'all' ? true :
        filterStatus === 'active' ? emp.is_active :
        !emp.is_active;

      return matchesSearch && matchesStatus;
    });

    result.sort((a, b) => {
      let comparison = 0;
      if (sortBy === 'name') comparison = a.name.localeCompare(b.name);
      if (sortBy === 'role') comparison = a.role.localeCompare(b.role);
      if (sortBy === 'status') comparison = Number(b.is_active) - Number(a.is_active);
      return sortDirection === 'asc' ? comparison : -comparison;
    });

    return result;
  }, [employees, debouncedSearch, filterStatus, sortBy, sortDirection]);

  const isPro = company?.plan_tier === 'pro' || company?.plan_tier === 'enterprise';

  return (
    <div className="space-y-8 p-6 md:p-10 animate-in fade-in duration-500 min-h-screen pb-32">
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6">
        <div>
          <h1 className="text-3xl font-black text-white tracking-tight">Gestão de Equipe</h1>
          <p className="text-slate-400 text-sm mt-1">
            Controle de acesso, permissões e auditoria de segurança.
          </p>
        </div>
        
        <div className="flex gap-4">
          <div className="bg-slate-900/50 border border-slate-800 px-4 py-2 rounded-xl">
            <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Total</p>
            <p className="text-2xl font-black text-white">{employees.length}</p>
          </div>
          <div className="bg-slate-900/50 border border-slate-800 px-4 py-2 rounded-xl">
            <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Ativos</p>
            <p className="text-2xl font-black text-emerald-500">{employees.filter(e => e.is_active).length}</p>
          </div>
        </div>
      </div>

      <TeamFilters 
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
        filterStatus={filterStatus}
        onFilterChange={setFilterStatus}
        sortBy={sortBy}
        sortDirection={sortDirection}
        onSortChange={handleSortChange}
        onNewMember={handleNewMemberClick}
      />

      {loading ? (
        <div className="flex justify-center py-20">
          <Loader2 className="animate-spin text-orange-500" size={40} />
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {filteredEmployees.map((emp) => (
            <EmployeeCard 
              key={emp.id}
              employee={emp}
              roleConfig={ROLE_CONFIG[emp.role] || ROLE_CONFIG.waiter}
              searchTerm={debouncedSearch}
              onEdit={openFormModal}
              onHistory={openHistoryModal}
              onRevoke={handleRevokeAccess}
            />
          ))}
        </div>
      )}

      {!isPro && <PLGBanner onUpgrade={() => setIsUpgradeModalOpen(true)} />}

      <Modal 
        isOpen={isFormModalOpen} 
        onClose={() => setIsFormModalOpen(false)} 
        title={editingEmployee ? "Editar Colaborador" : "Novo Colaborador"}
      >
        {editingEmployee && (
          <div className="flex gap-2 mb-6 border-b border-slate-800 pb-1">
            <button
              onClick={() => setActiveTab('details')}
              className={`px-4 py-2 text-xs font-bold uppercase tracking-wider transition-colors ${activeTab === 'details' ? "text-orange-500 border-b-2 border-orange-500" : "text-slate-500 hover:text-slate-300"}`}
            >
              <div className="flex items-center gap-2"><FileText size={14} /> Detalhes</div>
            </button>
            <button
              onClick={() => setActiveTab('history')}
              className={`px-4 py-2 text-xs font-bold uppercase tracking-wider transition-colors ${activeTab === 'history' ? "text-orange-500 border-b-2 border-orange-500" : "text-slate-500 hover:text-slate-300"}`}
            >
              <div className="flex items-center gap-2"><History size={14} /> Histórico</div>
            </button>
          </div>
        )}

        {activeTab === 'details' ? (
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase mb-1.5">Nome Completo</label>
                <input 
                  required
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-white focus:ring-2 focus:ring-orange-500 outline-none transition-all"
                  value={formData.name}
                  onChange={e => setFormData({...formData, name: e.target.value})}
                  placeholder="Ex: João Silva"
                  autoFocus
                  autoComplete="off"
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase mb-1.5">E-mail de Acesso</label>
                <input 
                  type="email"
                  required
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-white focus:ring-2 focus:ring-orange-500 outline-none transition-all"
                  value={formData.email}
                  onChange={e => setFormData({...formData, email: e.target.value})}
                  placeholder="joao@exemplo.com"
                  disabled={!!editingEmployee}
                  autoComplete="off"
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase mb-3">Função & Permissões</label>
                <RoleSelector 
                  value={formData.role} 
                  onChange={(role) => setFormData({...formData, role})} 
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase mb-1.5">
                  {editingEmployee ? "Redefinir Senha (Opcional)" : "Senha Inicial"}
                </label>
                <input 
                  type="password"
                  required={!editingEmployee}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-white focus:ring-2 focus:ring-orange-500 outline-none transition-all"
                  value={formData.password}
                  onChange={e => setFormData({...formData, password: e.target.value})}
                  placeholder="••••••••"
                  minLength={4}
                  autoComplete="new-password"
                />
              </div>
            </div>
            <button 
              type="submit"
              disabled={saving}
              className="w-full bg-orange-600 hover:bg-orange-700 text-white font-bold py-4 rounded-xl mt-4 flex items-center justify-center gap-2 disabled:opacity-50 shadow-lg active:scale-95 transition-all"
            >
              {saving ? <Loader2 className="animate-spin" size={20} /> : <Check size={20} />}
              {editingEmployee ? "Salvar Alterações" : "Cadastrar Membro"}
            </button>
          </form>
        ) : (
          <AuditTimeline employeeId={editingEmployee!.id} />
        )}
      </Modal>

      <UpgradeModal 
        isOpen={isUpgradeModalOpen} 
        onClose={() => setIsUpgradeModalOpen(false)} 
        slug={slug} 
      />
    </div>
  );
}