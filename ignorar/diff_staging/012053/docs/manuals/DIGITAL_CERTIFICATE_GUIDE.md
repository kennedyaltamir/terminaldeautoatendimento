# 🔐 Guia de Obtenção de Certificado Digital (e-CNPJ A1)

Para emitir Notas Fiscais (NFC-e) pelo MesaFlow via Focus NFe, sua empresa precisa de um **Certificado Digital e-CNPJ tipo A1**.

## 1. Onde comprar?
Você deve adquirir o certificado em uma **Autoridade Certificadora (AC)**. As mais comuns no Brasil são:
- **Certisign** (www.certisign.com.br)
- **Serasa Experian** (www.serasaexperian.com.br)
- **Soluti** (www.soluti.com.br)
- **Valid** (www.validcertificadora.com.br)

## 2. Qual tipo escolher?
⚠️ **IMPORTANTE:** Escolha sempre o tipo **A1**.
- **Tipo A1:** É um arquivo digital (extensão `.pfx`) que você instala no MesaFlow/Focus NFe. Ele permite automação total.
- **Tipo A3:** É um cartão ou token físico (pendrive). **NÃO FUNCIONA** para sistemas em nuvem como o nosso.

## 3. Passo a Passo para Obter o Arquivo
1. **Compra:** Acesse o site de uma das certificadoras acima e compre o "e-CNPJ A1".
2. **Validação:** Você precisará agendar uma videoconferência ou visita presencial para provar sua identidade (levar documentos da empresa e sócios).
3. **Emissão:** Após a validação, a certificadora enviará um link para você baixar o certificado no seu computador.
4. **Exportação:** Ao baixar, o sistema gerará um arquivo (geralmente chamado `nome_da_empresa.pfx`). Você definirá uma **senha** para este arquivo.
5. **Upload:** É este arquivo `.pfx` que você deve anexar no painel da Focus NFe.

## 4. O que fazer com o arquivo?
Com o arquivo `.pfx` e a senha em mãos:
1. Vá ao painel da **Focus NFe**.
2. Acesse o cadastro da sua empresa.
3. Clique em **"ANEXAR CERTIFICADO"**.
4. Selecione o arquivo e digite a senha que você criou na emissão.
