"""
Suíte de testes automatizados (Test Harness) para o módulo TaskAnalyzer.
Este arquivo implementa os testes unitários e funcionais em Pytest,
validando o contrato de interface, as regras de negócio, os cenários de
aceite (Dado-Quando-Então), o tratamento de exceções e a prevenção contra
divisão por zero.
"""

from typing import Any
import pytest
from datetime import datetime
from src.task_analyzer import (
    DataInvalidaError,
    DadosIncompletosError,
    TaskValidationError,
    ValorInvalidoError,
    analyze_tasks,
)

# ==============================================================================
# FIXTURES DE DADOS PARA OS TESTES
# ==============================================================================


@pytest.fixture
def lote_misto_cenario_1() -> list[dict[str, Any]]:
    """Fixture que fornece o lote de 5 tarefas do Cenário 1 (Sucesso) do SDD."""
    return [
        {
            "id": 1,
            "titulo": "Revisão de Código",
            "prioridade": "alta",
            "data_criacao": "2026-08-01",
            "prazo": "2026-08-05",
            "data_conclusao": "2026-08-03",
            "status": "concluida",
        },  # Duração: 2 dias, Atraso: Não
        {
            "id": 2,
            "titulo": "Modelar Banco",
            "prioridade": "media",
            "data_criacao": "2026-08-01",
            "prazo": "2026-08-03",
            "data_conclusao": "2026-08-04",
            "status": "concluida",
        },  # Duração: 3 dias, Atraso: Sim
        {
            "id": 3,
            "titulo": "Criar Documento",
            "prioridade": "baixa",
            "data_criacao": "2026-08-02",
            "prazo": "2026-08-10",
            "data_conclusao": "2026-08-02",
            "status": "concluida",
        },  # Duração: 0 dias, Atraso: Não
        {
            "id": 4,
            "titulo": "Deploy em Prod",
            "prioridade": "alta",
            "data_criacao": "2026-08-02",
            "prazo": "2026-08-06",
            "data_conclusao": "2026-08-08",
            "status": "concluida",
        },  # Duração: 6 dias, Atraso: Sim
        {
            "id": 5,
            "titulo": "Testes de Carga",
            "prioridade": "media",
            "data_criacao": "2026-08-05",
            "prazo": "2026-08-12",
            "data_conclusao": None,
            "status": "em_progresso",
        },  # Ignorada em tempos de conclusão e atraso
    ]


# ==============================================================================
# TESTES DO CENÁRIO 1: CAMINHO FELIZ E MÉTRICAS DE SUCESSO
# ==============================================================================

def test_analyze_tasks_sucesso_cenario_1(
    lote_misto_cenario_1: list[dict[str, Any]],
) -> None:
    """Valida as métricas calculadas para o lote do Cenário 1 da especificação SDD."""
    resultado = analyze_tasks(lote_misto_cenario_1)

    # 1. Validação do Tempo Médio de Conclusão (em dias)
    tempos = resultado["tempo_medio_conclusao"]
    assert tempos["geral"] == 2.75  # (2 + 3 + 0 + 6) / 4 = 2.75
    assert tempos["alta"] == 4.0    # (2 + 6) / 2 = 4.0
    assert tempos["media"] == 3.0   # 3 / 1 = 3.0
    assert tempos["baixa"] == 0.0   # 0 / 1 = 0.0

    # 2. Validação da Taxa de Atraso (percentual)
    atrasos = resultado["taxa_atraso"]
    assert atrasos["geral"] == 0.5  # 2 atrasadas de 4 concluídas = 0.5
    assert atrasos["alta"] == 0.5   # 1 atrasada de 2 concluídas = 0.5
    assert atrasos["media"] == 1.0  # 1 atrasada de 1 concluída = 1.0
    assert atrasos["baixa"] == 0.0  # 0 atrasadas de 1 concluída = 0.0

    # 3. Validação da Volumetria de Tarefas
    quantidades = resultado["quantidade_tarefas"]
    assert quantidades["total"] == 5
    assert quantidades["por_prioridade"] == {"baixa": 1, "media": 2, "alta": 2}
    assert quantidades["por_status"] == {
        "pendente": 0,
        "em_progresso": 1,
        "concluida": 4,
    }


def test_analyze_tasks_conclusao_exatamente_no_prazo() -> None:
    """Garante que tarefas concluídas no dia do prazo
    não sejam contadas como atrasadas."""
    tarefas = [
        {
            "id": 10,
            "titulo": "Tarefa no Prazo Exacto",
            "prioridade": "media",
            "data_criacao": "2026-08-01",
            "prazo": "2026-08-05",
            "data_conclusao": "2026-08-05",  # data_conclusao == prazo
            "status": "concluida",
        }
    ]
    resultado = analyze_tasks(tarefas)
    assert resultado["taxa_atraso"]["geral"] == 0.0
    assert resultado["taxa_atraso"]["media"] == 0.0


# ==============================================================================
# TESTES DE PREVENÇÃO DE ERROS ARITMÉTICOS (DIVISÃO POR ZERO)
# ==============================================================================

def test_analyze_tasks_lote_vazio() -> None:
    """Valida o comportamento com lote totalmente vazio ([])."""
    resultado = analyze_tasks([])
    assert resultado["quantidade_tarefas"]["total"] == 0
    assert resultado["tempo_medio_conclusao"]["geral"] == 0.0
    assert resultado["taxa_atraso"]["geral"] == 0.0


def test_analyze_tasks_sem_tarefas_concluidas() -> None:
    """Garante que lotes com zero tarefas concluídas não disparem ZeroDivisionError."""
    tarefas = [
        {
            "id": 1,
            "titulo": "Tarefa 1",
            "prioridade": "alta",
            "data_criacao": "2026-08-01",
            "prazo": "2026-08-05",
            "data_conclusao": None,
            "status": "pendente",
        },
        {
            "id": 2,
            "titulo": "Tarefa 2",
            "prioridade": "baixa",
            "data_criacao": "2026-08-01",
            "prazo": "2026-08-05",
            "data_conclusao": None,
            "status": "em_progresso",
        },
    ]
    resultado = analyze_tasks(tarefas)

    # Não deve lançar exceção e deve zerar as métricas de tempo e atraso
    assert resultado["quantidade_tarefas"]["total"] == 2
    assert resultado["tempo_medio_conclusao"]["geral"] == 0.0
    assert resultado["taxa_atraso"]["geral"] == 0.0
    assert resultado["tempo_medio_conclusao"]["alta"] == 0.0
    assert resultado["taxa_atraso"]["baixa"] == 0.0


# ==============================================================================
# TESTES DE EXCEÇÃO E VALIDAÇÕES (CENÁRIOS DE ERRO)
# ==============================================================================

def test_analyze_tasks_data_invalida_error() -> None:
    """Valida o disparo de DataInvalidaError quando data_conclusao < data_criacao."""
    tarefas_invalidas = [
        {
            "id": 99,
            "titulo": "Tarefa Data Inconsistente",
            "prioridade": "media",
            "data_criacao": "2026-08-10",
            "prazo": "2026-08-15",
            "data_conclusao": "2026-08-05",  # Conclusão ANTES da criação
            "status": "concluida",
        }
    ]
    with pytest.raises(DataInvalidaError) as exc_info:
        analyze_tasks(tarefas_invalidas)
    assert "não pode ser anterior à data de criação" in str(exc_info.value)
    assert "99" in str(exc_info.value)


def test_analyze_tasks_dados_incompletos_error_campo_ausente() -> None:
    """Valida o disparo de DadosIncompletosError quando um campo do contrato falta."""
    tarefa_sem_prioridade = [
        {
            "id": 1,
            "titulo": "Tarefa Sem Prioridade",  # "prioridade" ausente
            "data_criacao": "2026-08-01",
            "prazo": "2026-08-05",
            "status": "pendente",
        }
    ]
    with pytest.raises(DadosIncompletosError) as exc_info:
        analyze_tasks(tarefa_sem_prioridade)
    assert "prioridade" in str(exc_info.value)


def test_analyze_tasks_dados_incompletos_error_conclusao_nula() -> None:
    """Valida o disparo de DadosIncompletosError para tarefa concluída com data nula."""
    tarefa_concluida_sem_data = [
        {
            "id": 1,
            "titulo": "Tarefa Concluída Sem Data",
            "prioridade": "alta",
            "data_criacao": "2026-08-01",
            "prazo": "2026-08-05",
            "data_conclusao": None,  # Nulo para status 'concluida'
            "status": "concluida",
        }
    ]
    with pytest.raises(DadosIncompletosError) as exc_info:
        analyze_tasks(tarefa_concluida_sem_data)
    assert "data_conclusao" in str(exc_info.value)


def test_analyze_tasks_valor_invalido_error_prioridade() -> None:
    """Valida o disparo de ValorInvalidoError para prioridade fora do domínio."""
    tarefa_prioridade_invalida = [
        {
            "id": 1,
            "titulo": "Tarefa Urgente",
            "prioridade": "super_alta",  # Valor fora do domínio
            "data_criacao": "2026-08-01",
            "prazo": "2026-08-05",
            "status": "pendente",
        }
    ]
    with pytest.raises(ValorInvalidoError) as exc_info:
        analyze_tasks(tarefa_prioridade_invalida)
    assert "super_alta" in str(exc_info.value)


def test_analyze_tasks_valor_invalido_error_status() -> None:
    """Valida o disparo de ValorInvalidoError para status fora do domínio."""
    tarefa_status_invalido = [
        {
            "id": 1,
            "titulo": "Tarefa Cancelada",
            "prioridade": "media",
            "data_criacao": "2026-08-01",
            "prazo": "2026-08-05",
            "status": "cancelada",  # Valor fora do domínio
        }
    ]
    with pytest.raises(ValorInvalidoError) as exc_info:
        analyze_tasks(tarefa_status_invalido)
    assert "cancelada" in str(exc_info.value)


def test_hierarquia_excecoes_task_validation_error() -> None:
    """Garante que todas as exceções específicas
    herdem da classe base TaskValidationError."""
    assert issubclass(DataInvalidaError, TaskValidationError)
    assert issubclass(DadosIncompletosError, TaskValidationError)
    assert issubclass(ValorInvalidoError, TaskValidationError)


def test_analyze_tasks_data_como_datetime_nativo():
    """Cobre as linhas do 'if isinstance(date_value, datetime)'
    forçando parse na tarefa concluída"""
    data_obj_criacao = datetime(2026, 8, 10, 10, 0, 0)
    data_obj_conclusao = datetime(2026, 8, 15, 10, 0, 0)

    tarefas = [{
        "id": 99,
        "titulo": "Teste com datetime nativo",
        "data_criacao": data_obj_criacao,
        "prazo": "2026-08-20",
        "status": "concluida",
        "data_conclusao": data_obj_conclusao,
        "prioridade": "baixa"
    }]
    resultado = analyze_tasks(tarefas)
    assert resultado["quantidade_tarefas"]["total"] == 1


def test_analyze_tasks_formato_data_invalido_string():
    """Cobre as linhas do except ValueError
    forçando o parse da data ao estar concluída"""
    tarefas = [{
        "id": 100,
        "titulo": "Data ruim",
        "data_criacao": "10/08/2026",
        "prazo": "2026-08-20",
        "status": "concluida",
        "data_conclusao": "2026-08-15",
        "prioridade": "alta"
    }]
    with pytest.raises(ValorInvalidoError) as exc_info:
        analyze_tasks(tarefas)
    assert "Formato de data" in str(exc_info.value)


def test_analyze_tasks_tipo_data_nao_suportado():
    """Cobre o raise final caso a data não seja nem string nem datetime"""
    tarefas = [{
        "id": 101,
        "titulo": "Data bizarra",
        "data_criacao": 20260810,
        "prazo": "2026-08-20",
        "status": "concluida",
        "data_conclusao": "2026-08-15",
        "prioridade": "alta"
    }]
    with pytest.raises(ValorInvalidoError) as exc_info:
        analyze_tasks(tarefas)
    assert "Tipo de dado" in str(exc_info.value)
