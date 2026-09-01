# Diretrizes Arquiteturais (Obrigatórias)

* **Linguagem:** Python 3.11 ou superior como versão mínima obrigatória.
* **Anotações de Tipo:** Utilizar type hints em todas as funções e métodos.
* **Princípio Single Responsibility (SRP):** Seguir o SRP e manter o código limpo (PEP 8).
* **Documentação:** Docstring no padrão 'Google style docstrings' para módulos, classes, funções e parâmetros.
* **Rastreabilidade de Logs:** Logs estruturados utilizando o módulo padrão logging.
* **Exceções Claras:** Tratamento de exceções específico e mensagens de erro claras.
* **Legibilidade:** Código deve ser legível, manutenível e com nomes de variáveis e funções descritivos.
* **Modularização:** Separar responsabilidades (SRP) e evitar lógica em cascata.

## 3.2 Proibições Explícitas (Regras Restritivas)

* Não utilizar bibliotecas externas não autorizadas (ex: pandas, numpy, etc.).
* Não alterar, remover ou adaptar os cenários de teste fornecidos.
* Não modificar a estrutura de pastas definida nesta especificação.
* Não persistir dados em arquivos ou bancos de dados (tudo deve ser mantido transiente na memória RAM).
* Não alterar a assinatura (nome e parâmetros) das funções públicas sem autorização.
* Não gerar código sem testes correspondentes para as novas funcionalidades.
* Não inserir código duplicado ou sem necessidade.
* Não assumir comportamentos não especificados no contrato de negócio.
* Não comentar código em excesso (apenas o necessário para explicar regras de negócio complexas).
* Não retornar valores diferentes do contrato definido.
