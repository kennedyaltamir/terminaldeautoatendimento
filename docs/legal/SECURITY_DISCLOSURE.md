# 🔓 Política de Divulgação Responsável de Vulnerabilidades

**Data de Vigência:** Janeiro de 2026
**Contato de Segurança:** security@mesaflow.com.br

O MesaFlow valoriza a comunidade de segurança e encoraja a divulgação responsável de vulnerabilidades. Esta política define as regras para pesquisadores de segurança (White Hat Hackers) que desejam testar e reportar falhas em nossos sistemas.

## 1. Compromisso (Safe Harbor)
Se você seguir estas diretrizes ao reportar uma vulnerabilidade:
- Não iniciaremos ações legais contra você.
- Trabalharemos com você para entender e resolver o problema rapidamente.
- Reconheceremos sua contribuição publicamente (se desejar).

## 2. Escopo
### ✅ Permitido (In-Scope)
- `*.mesaflow.com.br` (Aplicações Web e API)
- Aplicativos Móveis oficiais (Android/iOS)
- Vulnerabilidades de OWASP Top 10 (XSS, SQLi, IDOR, RCE)

### ❌ Proibido (Out-of-Scope)
- Ataques de Negação de Serviço (DoS/DDoS).
- Engenharia Social (Phishing) contra funcionários ou clientes.
- Acesso físico a escritórios ou datacenters.
- Testes em contas de clientes reais (use apenas suas próprias contas de teste).

## 3. Como Reportar
Envie um e-mail para **security@mesaflow.com.br** contendo:
1.  **Título:** [VULN] Tipo de Vulnerabilidade - Componente Afetado.
2.  **Descrição:** Detalhes técnicos e impacto estimado.
3.  **PoC (Proof of Concept):** Passos para reprodução, scripts ou screenshots.

*Recomendamos o uso de PGP para criptografar relatórios sensíveis (Chave pública disponível mediante solicitação).*

## 4. Processo de Resolução
1.  **Recebimento:** Confirmaremos o recebimento em até 48 horas.
2.  **Triagem:** Validaremos a vulnerabilidade e definiremos a severidade (CVSS).
3.  **Correção:** Trabalharemos na correção conforme nossos SLAs internos.
4.  **Divulgação:** Após a correção e validação, poderemos publicar um boletim de segurança.

## 5. Recompensas
Atualmente, não oferecemos recompensas financeiras (Bug Bounty), mas oferecemos reconhecimento em nosso Hall of Fame para reportes válidos de alta severidade.
