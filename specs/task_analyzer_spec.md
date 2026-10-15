# Especificação SDD — TaskAnalyzer

### *Módulo Avançado de Métricas e Produtividade Operacional*

---

## 1. VISÃO GERAL E CONTRATO DE NEGÓCIO (SDD)

### 1.1 Identificação
* **Nome completo do estudante:** [Insira seu Nome Completo]
* **Curso:** [Insira seu Curso — ex: Engenharia de Software / ADS]
* **Polo/Turma:** [Insira sua Turma/Polo]
* **E-mail institucional:** [Insira seu E-mail Institucional]
* **Data de elaboração:** 31 de Agosto de 2026
* **Versão da especificação:** v1.0 (Fase 1)

---

### 1.2 Propósito do Módulo TaskAnalyzer
Apresentação do escopo do sistema de análise de tarefas e produtividade:
* **Analisar tarefas executadas e gerar métricas de produtividade.**
* **Calcular tempo médio de conclusão por tipo/prioridade.**
* **Identificar taxa de atraso (tarefas concluídas após o prazo).**
* **Gerar indicadores por prioridade (baixa, média, alta).**
* **Fornecer métricas para tomada de decisão e melhoria contínua.**

---

### 1.3 Contrato Executável de Interface

#### 1.3.1 Entradas (Inputs)
Detalhamento formal das entradas, tipos de dados e restrições estritas:

| Campo | Tipo | Obrigatório | Descrição / Restrições |
| :--- | :--- | :--- | :--- |
| `id` | `int` / `str` | **Sim** | Identificador único de cada tarefa. |
| `titulo` | `str` | **Sim** | Descrição da tarefa (UTC). |
| `prioridade` | `str` | **Sim** | Domínio estrito: `baixa`, `media`, `alta`. |
| `data_criacao` | `data/str` | **Sim** | Data de início da execução (formato ISO `YYYY-MM-DD`). |
| `data_conclusao` | `data/str` | *Condicional* | Data final de conclusão da execução. Obrigatório se `status == 'concluida'`. |
| `prazo` | `data/str` | **Sim** | Data de vencimento acordada (formato ISO `YYYY-MM-DD`). |
| `status` | `str` | **Sim** | Domínio estrito: `pendente`, `em_progresso`, `concluida`. |

#### 1.3.2 Saídas (Outputs)
Detalhamento formal das saídas retornadas pela função principal `analyze_tasks`:
* **`tempo_medio_conclusao`** (`float`): Tempo médio geral e por prioridade (expresso em dias).
* **`taxa_atraso`** (`float`): Percentual de tarefas concluídas com atraso (geral e por prioridade).
* **`quantidade_tarefas`** (`dict/obj`): Totalizadores agrupados por prioridade (`baixa`, `media`, `alta`) e por status (`pendente`, `em_progresso`, `concluida`).

#### 1.3.3 Regras de Negócio e Restrições
1. **Filtro de Status:** Considerar apenas tarefas com status `"concluida"` para calcular o tempo médio de conclusão e a taxa de atraso. Tarefas pendentes ou em progresso entram apenas nas contagens de volumetria.
2. **Condição de Atraso:** Uma tarefa concluída é considerada em atraso se `data_conclusao > prazo`. Se `data_conclusao <= prazo`, considera-se concluída no prazo de forma regular.
3. **Consistência de Datas:** Validar que `data_conclusao >= data_criacao`. Caso a data de conclusão seja anterior à data de criação, o sistema deve disparar a exceção de validação `DataInvalidaError`.
4. **Prevenção de Divisão por Zero:** Evitar erro aritmético de divisão por zero caso não haja tarefas concluídas no lote geral ou em uma prioridade específica. O sistema deve retornar `0.0` para as médias de tempo e taxas de atraso afetadas.
5. **Tratamento de Exceções Customizadas:**
   * Campos obrigatórios ausentes ou nulos disparam `DadosIncompletosError`.
   * Valores informados fora do domínio permitido de prioridades ou status disparam `ValorInvalidoError`.
   * Todas as exceções de validação herdam da classe base `TaskValidationError`.

---

## 2. ESPECIFICAÇÃO DE CENÁRIOS DE ACEITE E TEST HARNESS

### 2.1 Cenários de Aceite (Modelo Dado-Quando-Então)

#### Cenário 1: Sucesso (Métricas Corretas)
* **Dado** um conjunto de tarefas válidas com diferentes prioridades, prazos e status (concluídas e pendentes),
* **Quando** o analisador de tarefas (`TaskAnalyzer`) for executado,
* **Então** deve retornar as métricas corretas, incluindo:
  * Tempo médio de conclusão por prioridade e geral;
  * Taxa de atraso por prioridade e geral;
  * Quantidade de tarefas correta por prioridade e por status.

#### Cenário 2: Exceção / Erro (Entradas Inválidas)
* **Dado** uma entrada com datas inválidas (ex: conclusão anterior à criação) ou divisão por zero,
* **Quando** o analisador de tarefas (`TaskAnalyzer`) for executado,
* **Então** deve disparar uma exceção específica tratada (`DataInvalidaError`, `DadosIncompletosError` ou `ValorInvalidoError`), com mensagem clara e objetiva ao usuário.

---

### 2.2 Planejamento do Test Harness
Explicação de como estes cenários de aceite textuais se transformarão em testes automatizados utilizando o framework **`pytest`** na Fase 2 para garantir que o código gerado por IA esteja correto:

```text
┌──────────────────────────┐
│ 1. Cenários Escritos     │ ➔ Especificação contratual SDD em task_analyzer_spec.md
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ 2. Casos de Testes       │ ➔ Mapeamento de tabelas com dados de entrada e saídas esperadas
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ 3. Testes Automatizados  │ ➔ Implementação das asserções no arquivo tests/test_harness.py
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ 4. Validação por IA      │ ➔ Homologação funcional automatizada e prevenção de falhas
└──────────────────────────┘
```

