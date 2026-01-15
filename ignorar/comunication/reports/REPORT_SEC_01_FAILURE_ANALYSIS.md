
# 📝 Análise de Falha: SEC-01 (Ciclo 1)

## 1. Descrição do Incidente
O script de validação de RLS falhou durante a fase de injeção de dados de teste.

## 2. Causa Raiz
O comando SQL `INSERT INTO companies` omitiu a coluna `payment_provider`. No schema atual do MesaFlow, esta coluna é definida como `nullable=False`. Embora o modelo SQLAlchemy possua um `default`, inserções via SQL puro ignoram defaults de nível de aplicação, exigindo o valor explicitamente ou um default de nível de banco de dados (que não está presente nesta coluna).

## 3. Ação Corretiva
- Atualizado o script `sec_01_rls_integrity.py` para incluir `payment_provider` e `is_active`.
- Implementada limpeza automática de dados de teste para evitar erros de duplicidade em retentativas.
- Adicionado log de qual Role está sendo usada no teste para diferenciar testes como Superuser vs AppUser.

## 4. Próximo Passo
Re-executar a validação SEC-01.

