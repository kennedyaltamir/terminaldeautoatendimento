import { ChefHat, Instagram, Linkedin, Twitter } from "lucide-react";

export default function Footer() {
  return (
    <footer className="bg-gray-950 text-gray-400 py-16 border-t border-gray-900">
      <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-4 gap-12">
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-white">
            <ChefHat className="text-orange-600" />
            <span className="text-xl font-bold">MesaFlow</span>
          </div>
          <p className="text-sm leading-relaxed">
            Transformando o fluxo de atendimento em ambientes de alto tráfego através da tecnologia.
          </p>
          <div className="flex gap-4 pt-2">
            <a href="#" className="hover:text-white transition-colors"><Instagram size={20}/></a>
            <a href="#" className="hover:text-white transition-colors"><Twitter size={20}/></a>
            <a href="#" className="hover:text-white transition-colors"><Linkedin size={20}/></a>
          </div>
        </div>

        <div>
          <h4 className="text-white font-bold mb-4">Produto</h4>
          <ul className="space-y-2 text-sm">
            <li><a href="#" className="hover:text-orange-500 transition-colors">Cardápio Digital</a></li>
            <li><a href="#" className="hover:text-orange-500 transition-colors">KDS (Cozinha)</a></li>
            <li><a href="#" className="hover:text-orange-500 transition-colors">Fidelidade</a></li>
            <li><a href="#" className="hover:text-orange-500 transition-colors">Integrações</a></li>
          </ul>
        </div>

        <div>
          <h4 className="text-white font-bold mb-4">Empresa</h4>
          <ul className="space-y-2 text-sm">
            <li><a href="#" className="hover:text-orange-500 transition-colors">Sobre Nós</a></li>
            <li><a href="#" className="hover:text-orange-500 transition-colors">Carreiras</a></li>
            <li><a href="#" className="hover:text-orange-500 transition-colors">Blog</a></li>
            <li><a href="#" className="hover:text-orange-500 transition-colors">Contato</a></li>
          </ul>
        </div>

        <div>
          <h4 className="text-white font-bold mb-4">Legal</h4>
          <ul className="space-y-2 text-sm">
            <li><a href="#" className="hover:text-orange-500 transition-colors">Termos de Uso</a></li>
            <li><a href="#" className="hover:text-orange-500 transition-colors">Privacidade</a></li>
            <li><a href="#" className="hover:text-orange-500 transition-colors">Cookies</a></li>
          </ul>
        </div>
      </div>
      
      <div className="max-w-7xl mx-auto px-6 mt-16 pt-8 border-t border-gray-900 text-center text-xs opacity-50">
        © 2026 MesaFlow Tecnologia Ltda. Todos os direitos reservados. CNPJ: 00.000.000/0001-00.
      </div>
    </footer>
  );
}