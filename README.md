# teste-automacao-juridica
Teste para vaga de estágio em Inteligencia artificial.

# Automação de Due Diligence e Validação Cadastral de CNPJs

Este repositório contém a solução desenvolvida para o teste técnico do processo seletivo. A automação consulta a API pública da **BrasilAPI** para realizar a validação cadastral de uma lista de CNPJs (simulando um processo de *due diligence* e cadastro de clientes), exportando os resultados organizados para um arquivo CSV resiliente a falhas.

---

## 📌 1. Estrutura da Solução

* **Linguagem**: Python 3 (utilizando apenas bibliotecas nativas: `urllib`, `json`, `csv`).
* **API Utilizada**: BrasilAPI (Endpoint de CNPJ).
* **Tratamento de Resiliência**: O script processa 10 CNPJs (incluindo entradas com erro de formato e CNPJs inexistentes). Em caso de erro de rede ou código 404/400, a exceção é tratada individualmente e registrada na coluna `status_consulta` do CSV, sem interromper o fluxo de execução.

---

## 🛠️ 2. Como Executar

1. Certifique-se de ter o Python 3.14 instalado.
2. Clone este repositório ou baixe os arquivos.
3. Execute o script via terminal:
   ```bash
   python script_cnpj.py
   ```
4. O arquivo `relatorio_due_diligence_cnpjs.csv` será gerado/atualizado na mesma pasta.

---

## 🤖 3. Histórico de Prompts e Engenharia de Prompt (Uso da IA)

Conforme solicitado no teste, segue a documentação das instruções e iteratividade aplicadas com a Inteligência Artificial para a construção do script:

### Prompt 1: Definição da Arquitetura e Regras de Negócio
> "Atue como um Engenheiro de Software Sênior. Preciso criar um script Python que consulte uma API pública (BrasilAPI - CNPJ) para 10 entradas e gere um CSV. O foco é resiliência no contexto de um escritório de advocacia. Requisitos: sem libs externas complexas (usar stdlib), try/except individual por item com timeout de requisição, tratamento de CNPJs inválidos e criação de uma coluna `status_consulta` para auditoria no CSV sem quebrar a execução."

### Prompt 2: Refinamento e Contextualização Jurídica
> "Adapte a lógica para focar em Due Diligence e verificação cadastral de CNPJs de clientes na Receita Federal. O CSV precisa ter codificação UTF-8 com BOM e delimitador ponto e vírgula para abrir corretamente no Excel sem desconfigurar caracteres."

### Prompt 3: Validação da Resiliência
> "Garantir que se um CNPJ tiver menos de 14 dígitos ou a API retornar 404, o script preencha as colunas com 'N/A' e siga para a próxima consulta sem travar."
