# Task: Criação de Assets Técnicos Placeholder (Mobile)

## Contexto
O arquivo `mobile/app.json` referencia diversos arquivos de imagem (`icon.png`, `splash.png`, etc.) que são obrigatórios para a inicialização do Expo, mas que não existiam no sistema de arquivos, causando erros no comando `npx expo start`.

## Decisões Técnicas
- **Imagens 1x1:** Para evitar o envio de binários pesados e garantir a integridade dos arquivos via transferência de texto, foi criado um script gerador que escreve a sequência de bytes de um PNG válido de 1x1 pixel.
- **Centralização de Validação:** O script `verify_mobile_setup.py` foi expandido para garantir que nenhum asset obrigatório seja removido acidentalmente.
- **Isolamento:** Os assets foram colocados estritamente dentro de `mobile/assets/`, respeitando a estrutura do monorepo.

## Arquivos Afetados
- `mobile/assets/icon.png`
- `mobile/assets/splash.png`
- `mobile/assets/adaptive-icon.png`
- `mobile/assets/favicon.png`
- `scripts/setup/verify_mobile_setup.py`
- `scripts/setup/generate_mobile_placeholders.py`

## Política de Testes
[TEST_EXEMPT: Validado pela execução do script `verify_mobile_setup.py`, que confirma a existência física dos arquivos gerados.]
