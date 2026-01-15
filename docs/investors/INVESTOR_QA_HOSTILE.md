
# 🥊 Investor Q&A: The "Hostile" Tech Interview
**Cenário:** Due Diligence com um CTO cético de um fundo de Venture Capital Series A.

---

### Q1: "Por que Python/FastAPI e não Node.js ou Go? Python não é lento para alta escala?"

**A:** Para I/O Bound (que é 99% de um SaaS), Python moderno (Asyncio) é extremamente performático. O gargalo real é sempre o Banco de Dados, não a linguagem.
Além disso, Python nos dá acesso nativo às melhores bibliotecas de IA/ML (Scikit, Pandas) para o nosso roadmap de previsão de demanda. Reescrever em Go agora seria otimização prematura. O Instagram e o Shopify escalaram com Python/Ruby.

### Q2: "Vocês usam Monolito. Isso não é dívida técnica? Por que não Microserviços?"

**A:** Microserviços no estágio atual seriam "Resume Driven Development". Eles introduzem latência de rede, complexidade de deploy e dificuldade de transações distribuídas.
Nosso **Monolito Modular** permite desenvolvimento rápido e refatoração segura. Os módulos (`orders`, `billing`, `auth`) são desacoplados logicamente. Quando (e se) um módulo precisar escalar independentemente, podemos extraí-lo para um serviço em < 1 semana.

### Q3: "O que acontece se o Neon (Banco) dobrar o preço? Vocês estão presos (Vendor Lock-in)?"

**A:** Não. Usamos PostgreSQL padrão. Não utilizamos *stored procedures* proprietárias ou recursos exclusivos do Neon que impeçam a migração.
Podemos mover o banco para AWS RDS, Google Cloud SQL ou DigitalOcean Managed Database em questão de horas usando `pg_dump` e `pg_restore`. Nossa aplicação é agnóstica à infraestrutura (Docker).

### Q4: "Como vocês garantem que um estagiário não vai derrubar o banco de produção?"

**A:**
1.  **CI/CD Rígido:** Ninguém tem acesso de escrita direto em produção. Tudo passa por Pull Request e Pipeline de Testes.
2.  **RLS (Row-Level Security):** O banco impede que queries sem contexto de tenant retornem dados.
3.  **Read-Only Replicas:** Relatórios pesados rodam em réplicas de leitura, não impactando a operação transacional.

### Q5: "Se a AWS cair (Region Outage), qual o plano?"

**A:**
1.  **Frontend:** Está na Vercel (Edge Network Global), continua servindo estáticos.
2.  **Backend:** O Render permite redeploy em outra região rapidamente.
3.  **Dados:** O Neon possui redundância.
4.  **Operação:** O modo Offline-First dos apps permite que a operação local continue (lançar pedidos, imprimir) até a sincronização ser restaurada.

---

**Conclusão:** Nossas escolhas são pragmáticas, focadas em **Time-to-Market** e **Robustez**, não em hype.

