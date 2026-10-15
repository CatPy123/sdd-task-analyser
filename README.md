# Especificacao_SDD_TaskAnalyzer
# TaskAnalyzer — Spec-Driven Development (SDD) & AI Governance

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Code Style](https://img.shields.io/badge/code%20style-PEP%208-green.svg)](https://peps.python.org/pep-0008/)
[![Testing Framework](https://img.shields.io/badge/testing-pytest-yellow.svg)](https://docs.pytest.org/)
[![Architecture](https://img.shields.io/badge/architecture-SDD%20%2F%20AI%20Harnessing-orange.svg)](specs/task_analyzer_spec.md)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#instruções-de-execução-e-testes)
[![License](https://img.shields.io/badge/license-Academic-lightgrey.svg)](#licença-e-direitos)

> **Bootcamp III — Engenharia de Software e Governança de IA**  
> *Módulo de Análise de Métricas e Produtividade Operacional Baseado em Especificação Executável (SDD).*

---

## Sumário

- [Visão Geral do Projeto](#visão-geral-do-projeto)
- [O Paradigma SDD (Spec-Driven Development)](#o-paradigma-sdd-spec-driven-development)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Contrato Executável de Interface (SDD)](#contrato-executável-de-interface-sdd)
  - [Entradas (Inputs)](#entradas-inputs)
  - [Saídas (Outputs)](#saídas-outputs)
  - [Regras de Negócio e Restrições](#regras-de-negócio-e-restrições)
- [Governança de IA (CONTEXT_RULES)](#governança-de-ia-context_rules)
- [Pré-requisitos e Instalação](#pré-requisitos-e-instalação)
- [Instruções de Execução e Testes](#instruções-de-execução-e-testes)
  - [Executando os Testes Automatizados (`pytest`)](#executando-os-testes-automatizados-pytest)
  - [Análise Estática e Qualidade de Código (`flake8` & `mypy`)](#análise-estática-e-qualidade-de-código-flake8--mypy)
- [Test Harness e Cenários de Aceite](#test-harness-e-cenários-de-aceite)
- [Fluxo de Homologação Humana (5 Fases)](#fluxo-de-homologação-humana-5-fases)
- [Estratégia de Versionamento e Git Flow](#estratégia-de-versionamento-e-git-flow)
- [Licença e Direitos](#licença-e-direitos)

---

## Visão Geral do Projeto

O **TaskAnalyzer** é um motor analítico de produtividade projetado para processar lotes de tarefas em sistemas de gerenciamento de projetos e fluxos de trabalho corporativos. O componente opera **integralmente em memória** e fornece métricas consolidadas sobre tempos de execução, taxas de atraso e volumetria operacional.

Este repositório foi construído no contexto do **Bootcamp III (Engenharia de Software e Governança de IA)**, cujo propósito central é demonstrar a evolução do papel do engenheiro de software: de um mero escritor manual de linhas de código para um **Arquiteto de Especificações**, **Curador de Contexto** e **Homologador Crítico** de código gerado por ferramentas de Inteligência Artificial.

---

## O Paradigma SDD (Spec-Driven Development)

O **Spec-Driven Development (SDD)** estabelece a **Especificação Técnica Executável** como a única fonte da verdade (*single source of truth*) em todo o ciclo de vida do desenvolvimento. Em vez de partir diretamente para a codificação manual, a solução é construída sob uma esteira rigorosa de governança:

```text
 ┌─────────────────────────┐
 │ 1. ESPECIFICAR (SDD)    │ ➔ Definir contrato formal, regras de negócio e cenários
 └────────────┬────────────┘
              │
              ▼
 ┌─────────────────────────┐
 │ 2. GOVERNAR CONTEXTO    │ ➔ Estabelecer diretrizes e proibições rígidas (CONTEXT_RULES)
 └────────────┬────────────┘
              │
              ▼
 ┌─────────────────────────┐
 │ 3. GERAR CÓDIGO COM IA  │ ➔ Assistente de IA gera o código com base estrita no contrato
 └────────────┬────────────┘
              │
              ▼
 ┌─────────────────────────┐
 │ 4. TESTAR (TEST HARNESS)│ ➔ Validação matemática e funcional automatizada via Pytest
 └────────────┬────────────┘
              │
              ▼
 ┌─────────────────────────┐
 │ 5. HOMOLOGAR (HUMANO)   │ ➔ Revisão crítica, auditoria de segurança e chancela final
 └─────────────────────────┘
```

Principais Benefícios do SDD:
- Mitigação de Alucinações de IA: A IA opera em um espaço delimitado por contratos de interface e regras de contexto.
- Rastreabilidade Total: Cada linha de código e teste automatizado responde diretamente a um requisito de negócio especificado.
- Test-First Automatizado: O Test Harness traduz cenários Dado-Quando-Então em asserções objetivas.

---

## Estrutura do Repositório

A organização do repositório cumpre a padronização modular para a Fase 2 do Bootcamp III:

```text
sdd-task-analyzer/
├── README.md                 # Visão geral do projeto, guia de execução e status do build
├── CONTEXT_RULES.md          # Regras de arquitetura e restrições para agentes de IA
├── specs/
│   └── task_analyzer_spec.md # Especificação técnica executável SDD
├── tests/
│   └── test_harness.py       # Bateria de testes automatizados unitários e funcionais (Pytest)
└── src/
    └── task_analyzer.py      # Código-fonte do motor analítico homologado
```

---

## Contrato Executável de Interface (SDD)

A função principal do motor analítico, `analyze_tasks`, processa um lote de dicionários de tarefas e retorna indicadores estatísticos estruturados.

### Entradas (Inputs)

A função aceita uma lista de dicionários (`list[dict[str, Any]]`), onde cada item obedece à seguinte especificação de campos:

| Campo | Tipo | Obrigatório | Valores Permitidos / Formato | Descrição |
|---|---|---|---|---|
| id | int / str | Sim | Identificador único | Chave primária exclusiva da tarefa. |
| titulo | str | Sim | Texto não vazio | Descrição resumida da atividade. |
| prioridade | str | Sim | 'baixa', 'media', 'alta' | Nível de urgência da tarefa. |
| data_criacao | str / datetime | Sim | Formato ISO (YYYY-MM-DD) | Data de início de execução. |
| prazo | str / datetime | Sim | Formato ISO (YYYY-MM-DD) | Data limite acordada para conclusão. |
| data_conclusao | str / datetime | Condicional | Formato ISO (YYYY-MM-DD) | Obrigatório se status == 'concluida'. |
| status | str | Sim | 'pendente', 'em_progresso', 'concluida' | Estado atual da tarefa na esteira. |

### Saídas (Outputs)

A função retorna um dicionário estritamente estruturado (`dict[str, Any]`) com as métricas calculadas:

```json
{
  "tempo_medio_conclusao": {
    "geral": 2.75,
    "baixa": 0.0,
    "media": 3.0,
    "alta": 4.0
  },
  "taxa_atraso": {
    "geral": 0.5,
    "baixa": 0.0,
    "media": 1.0,
    "alta": 0.5
  },
  "quantidade_tarefas": {
    "total": 5,
    "por_prioridade": {
      "baixa": 1,
      "media": 2,
      "alta": 2
    },
    "por_status": {
      "pendente": 0,
      "em_progresso": 1,
      "concluida": 4
    }
  }
}
```

### Regras de Negócio e Restrições

1. Filtro do Escopo Analítico: Apenas tarefas com `status == 'concluida'` participam dos cálculos de `tempo_medio_conclusao` e `taxa_atraso`. Tarefas pendentes ou em progresso entram apenas no totalizador de volumetria.
2. Critério de Atraso: Uma tarefa concluída é contabilizada como atrasada se `data_conclusao > prazo`. Se `data_conclusao <= prazo`, considera-se concluída no prazo.
3. Validação Cronológica: Exige-se que `data_conclusao >= data_criacao`. Se a data de conclusão for anterior à criação, o sistema dispara a exceção `DataInvalidaError`.
4. Blindagem contra Divisão por Zero: Se o lote não contiver nenhuma tarefa concluída geral ou em uma prioridade específica, o sistema não lança exceção e retorna 0.0 para as médias de tempo e taxas de atraso afetadas.
5. Tratamento de Exceções Customizadas:
- Campos obrigatórios ausentes ou nulos disparam `DadosIncompletosError`.
- Prioridades ou status fora do domínio permitido disparam `ValorInvalidoError`.
- Todas as exceções herdam da classe base `TaskValidationError`.

---

## Governança de IA (CONTEXT_RULES)

O desenvolvimento assistido por IA foi guiado pelas regras de governança persistidas em `CONTEXT_RULES.md`:

- Diretrizes Arquiteturais (Obrigatórias):
  - Compatibilidade com Python 3.11+.
  - Type hints em 100% de funções, parâmetros e retornos.
  - Conformidade estrita com a PEP 8 e o princípio de responsabilidade única (SRP).
  - Documentação em Google Style Docstrings.
  - Logs estruturados usando a biblioteca nativa `logging`.
  - ...
- Proibições Explícitas (Restrições):
  - Proibido utilizar bibliotecas externas não autorizadas (ex: Pandas, NumPy, Pydantic).
  - Proibido persistir dados em arquivos ou bancos de dados (processamento estritamente em memória).
  - Proibido alterar assinaturas de funções públicas ou nomes de chaves de saída do contrato.
  - Proibido gerar código sem os testes correspondentes.
  - ...

---

## Pré-requisitos e Instalação

Pré-requisitos
- Python 3.11 ou superior.
- Git instalado.

Configuração do Ambiente Virtual

1. Clonar o repositório:
```bash
git clone [https://github.com/seu-usuario/sdd-task-analyzer.git](https://github.com/seu-usuario/sdd-task-analyzer.git)
cd sdd-task-analyzer
```

2. Criar e ativar o ambiente virtual (venv):
```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Instalar as ferramentas de qualidade e teste:
```bash
pip install --upgrade pip
pip install pytest pytest-cov flake8 mypy
```

---

## Instruções de Execução e Testes

### Executando os Testes Automatizados (pytest)

Para rodar a bateria de testes automatizados do Test Harness:

```bash
# Execução padrão dos testes em modo verboso
pytest -v

# Execução com relatório de cobertura de código (Code Coverage)
pytest --cov=src --cov-report=term-missing
```

### Análise Estática e Qualidade de Código (flake8 & mypy)

Para auditarmos a aderência do código aos padrões PEP 8 e tipagem estática:

```bash
# Verificação estática de estilo de código
flake8 src/ tests/ --max-line-length=88

# Verificação estrita de tipagem estática
mypy --strict src/
```

---

## Test Harness e Cenários de Aceite

O arquivo `tests/test_harness.py` valida o código-fonte em relação a 4 cenários essenciais:

1. Cenário de Sucesso (Métricas Corretas): Valida a exatidão matemática do tempo médio de conclusão (geral e por prioridade), taxa de atraso e volumetrias para um lote misto de tarefas.
2. Cenário de Exceção por Inconsistência de Datas: Atesta o disparo de `DataInvalidaError` caso `data_conclusao < data_criacao`.
3. Cenário de Integridade do Contrato: Valida o disparo de `DadosIncompletosError` para campos ausentes/nulos e `ValorInvalidoError` para domínios fora de especificação.
4. Cenário de Blindagem Aritmética: Garante retorno de 0.0 para médias e taxas quando não houver tarefas concluídas no lote.

---

## Fluxo de Homologação Humana (5 Fases)

O código gerado por IA passa por 5 fases obrigatórias de homologação conduzidas pelo desenvolvedor humano:

```text
 ┌──────────────────────────────────┐
 │ 1. Análise Estática (Linter)     │ ➔ Validação de PEP 8 (flake8) e Type Hints (mypy)
 └────────────────┬─────────────────┘
                  │
                  ▼
 ┌──────────────────────────────────┐
 │ 2. Execução de Testes (Harness)  │ ➔ 100% de aprovação nos testes automatizados (pytest)
 └────────────────┬─────────────────┘
                  │
                  ▼
 ┌──────────────────────────────────┐
 │ 3. Auditoria de Governança       │ ➔ Verificação de cumprimento das CONTEXT_RULES.md
 └────────────────┬─────────────────┘
                  │
                  ▼
 ┌──────────────────────────────────┐
 │ 4. Testes Manuais & Edge Cases   │ ➔ Validação de cenários limítrofes e estresse
 └────────────────┬─────────────────┘
                  │
                  ▼
 ┌──────────────────────────────────┐
 │ 5. Chancela e Assinatura Técnica │ ➔ Aprovação formal do PR e merge para a branch main
 └──────────────────────────────────┘
```

---

## Estratégia de Versionamento e Git Flow

O repositório adota o modelo Git Flow Simplificado:
- main: Branch estável de produção. Recebe apenas código homologado através de Pull Requests.
- develop: Branch de integração contínua para ciclo de desenvolvimento.
- feature/*: Branches temporárias para implementação de módulos específicos (ex: feature/sdd-spec, feature/test-harness, feature/task-analyzer).

Padronização de Commits (Semantic Commits)
- feat: Implementação de novas funcionalidades lógicas.
- test: Adição ou refatoração de suítes de teste no Harness.
- docs: Atualizações na documentação do projeto (README, SDD, CONTEXT_RULES).
- refactor: Ajustes de código mantendo o comportamento funcional.

---

## Licença e Direitos

Projeto desenvolvido para fins acadêmicos e institucionais no âmbito do Bootcamp III (Engenharia de Software e Governança de IA).
Desenvolvido e mantido sob a metodologia Spec-Driven Development (SDD). O desenvolvedor atua como arquiteto de especificações e homologador crítico do sistema.

***
