import { ChefHat, Instagram, Linkedin, Twitter } from "lucide-react";
import Link from "next/link";

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
            <a href="https://instagram.com/mesaflow" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors"><Instagram size={20}/></a>
            <a href="https://twitter.com/mesaflow" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors"><Twitter size={20}/></a>
            <a href="https://linkedin.com/company/mesaflow" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors"><Linkedin size={20}/></a>
          </div>
        </div>
        <div>
          <h4 className="text-white font-bold mb-4">Produto</h4>
          <ul className="space-y-2 text-sm">
            <li><Link href="#recursos" className="hover:text-orange-500 transition-colors">Cardápio Digital</Link></li>
            <li><Link href="#recursos" className="hover:text-orange-500 transition-colors">KDS (Cozinha)</Link></li>
            <li><Link href="#recursos" className="hover:text-orange-500 transition-colors">Fidelidade</Link></li>
            <li><Link href="#solucoes" className="hover:text-orange-500 transition-colors">Integrações</Link></li>
          </ul>
        </div>
        <div>
          <h4 className="text-white font-bold mb-4">Empresa</h4>
          <ul className="space-y-2 text-sm">
            <li><Link href="/trust" className="hover:text-orange-500 transition-colors">Sobre Nós</Link></li>
            <li><Link href="/trust" className="hover:text-orange-500 transition-colors">Carreiras</Link></li>
            <li><Link href="/trust" className="hover:text-orange-500 transition-colors">Blog</Link></li>
            <li><Link href="/trust" className="hover:text-orange-500 transition-colors">Contato</Link></li>
          </ul>
        </div>
        <div>
          <h4 className="text-white font-bold mb-4">Legal</h4>
          <ul className="space-y-2 text-sm">
            <li><Link href="/trust/security" className="hover:text-orange-500 transition-colors">Termos de Uso</Link></li>
            <li><Link href="/trust/security" className="hover:text-orange-500 transition-colors">Privacidade</Link></li>
            <li><Link href="/trust/security" className="hover:text-orange-500 transition-colors">Cookies</Link></li>
          </ul>
        </div>
      </div>
      <div className="max-w-7xl mx-auto px-6 mt-16 pt-8 border-t border-gray-900 text-center text-xs opacity-50">
        © 2026 MesaFlow Tecnologia Ltda. Todos os direitos reservados. CNPJ: 00.000.000/0001-00.
      </div>
    </footer>
  );
}
