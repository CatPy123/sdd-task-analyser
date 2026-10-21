"""
Módulo de análise de tarefas e geração de métricas de produtividade.
Este módulo implementa o contrato executável do TaskAnalyzer, processando
lotes de tarefas em memória para calcular tempo médio de conclusão,
taxa de atraso e volumetrias consolidadas por prioridade e status.
"""
from datetime import datetime
import logging
from typing import Any

# Configuração do logger estruturado segundo as diretrizes de governança
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Domínios válidos estritos conforme o contrato executável de interface
PRIORIDADES_VALIDAS = {"baixa", "media", "alta"}
STATUS_VALIDOS = {"pendente", "em_progresso", "concluida"}


class TaskValidationError(Exception):
    """Exceção base customizada para erros de validação no módulo TaskAnalyzer."""
    pass


class DataInvalidaError(TaskValidationError):
    """Exceção lançada quando há inconsistência cronológica nas datas da tarefa."""
    pass


class DadosIncompletosError(TaskValidationError):
    """Exceção lançada quando campos obrigatórios da tarefa estão ausentes ou nulos."""
    pass


class ValorInvalidoError(TaskValidationError):
    """Exceção lançada quando um campo contém valor fora do domínio permitido."""
    pass


def _parse_date(date_value: Any) -> datetime:
    """
    Converte um valor de data (string ISO/YYYY-MM-DD ou datetime) para datetime.

    Args:
        date_value (Any): Valor representando a data da tarefa.

    Returns:
        datetime: Objeto datetime correspondente.

    Raises:
        ValorInvalidoError: Se o formato ou tipo do dado de data for inválido.
    """
    if isinstance(date_value, datetime):
        return date_value

    if isinstance(date_value, str):
        try:
            return datetime.fromisoformat(date_value)
        except ValueError:
            try:
                return datetime.strptime(date_value, "%Y-%m-%d")
            except ValueError as exc:
                raise ValorInvalidoError(
                    f"Formato de data inválido: '{date_value}'. Esperado YYYY-MM-DD."
                ) from exc

    raise ValorInvalidoError(
        f"Tipo de dado de data não suportado: {type(date_value).__name__}."
    )


def analyze_tasks(tasks: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Analisa um lote de tarefas e gera métricas consolidadas de produtividade.

    Args:
        tasks (list[dict[str, Any]]): Lista de dicionários contendo as tarefas.

    Returns:
        dict[str, Any]: Dicionário estruturado com as métricas calculadas:
            - tempo_medio_conclusao: Médias em dias (geral, baixa, media, alta).
            - taxa_atraso: Percentual de atraso (geral, baixa, media, alta).
            - quantidade_tarefas: Totalizadores por prioridade e status.

    Raises:
        DadosIncompletosError: Se algum campo obrigatório estiver ausente ou nulo.
        ValorInvalidoError: Se prioridade, status ou formato de data for inválido.
        DataInvalidaError: Se data_conclusao for anterior a data_criacao.
    """
    logger.info("Iniciando análise de %d tarefas no lote.", len(tasks))

    metrics: dict[str, Any] = {
        "tempo_medio_conclusao": {
            "geral": 0.0,
            "baixa": 0.0,
            "media": 0.0,
            "alta": 0.0,
        },
        "taxa_atraso": {
            "geral": 0.0,
            "baixa": 0.0,
            "media": 0.0,
            "alta": 0.0,
        },
        "quantidade_tarefas": {
            "total": len(tasks),
            "por_prioridade": {"baixa": 0, "media": 0, "alta": 0},
            "por_status": {"pendente": 0, "em_progresso": 0, "concluida": 0},
        },
    }

    if not tasks:
        logger.warning("Lote de tarefas vazio recebido. Retornando métricas zeradas.")
        return metrics

    # Acumuladores para tempos, atrasos e contagem de tarefas concluídas
    acumuladores = {
        "geral": {"tempo_total": 0.0, "atrasos": 0, "concluidas": 0},
        "baixa": {"tempo_total": 0.0, "atrasos": 0, "concluidas": 0},
        "media": {"tempo_total": 0.0, "atrasos": 0, "concluidas": 0},
        "alta": {"tempo_total": 0.0, "atrasos": 0, "concluidas": 0},
    }

    campos_obrigatorios = [
        "id",
        "titulo",
        "prioridade",
        "data_criacao",
        "prazo",
        "status",
    ]

    for idx, task in enumerate(tasks):
        # 1. Validação de presença de campos obrigatórios do contrato
        for campo in campos_obrigatorios:
            if campo not in task or task[campo] is None:
                task_id = task.get("id", f"índice {idx}")
                logger.error(
                    "Campo obrigatório '%s' ausente na tarefa ID %s.",
                    campo,
                    task_id,
                )
                raise DadosIncompletosError(
                    f"Campo obrigatório '{campo}' ausente ou "
                    f"nulo na tarefa ID {task_id}."
                )

        prioridade = (
            str(task["prioridade"])
            .lower()
            .strip()
        )
        status = str(task["status"]).lower().strip()
        task_id = task["id"]

        # 2. Validação estrita dos domínios de prioridade e status
        if prioridade not in PRIORIDADES_VALIDAS:
            logger.error(
                "Prioridade inválida '%s' na tarefa ID %s.",
                prioridade,
                task_id
            )
            raise ValorInvalidoError(
                f"Prioridade '{prioridade}' é inválida na tarefa ID {task_id}. "
                f"Valores permitidos: {sorted(list(PRIORIDADES_VALIDAS))}."
            )

        if status not in STATUS_VALIDOS:
            logger.error("Status inválido '%s' na tarefa ID %s.", status, task_id)
            raise ValorInvalidoError(
                f"Status '{status}' é inválido na tarefa ID {task_id}. "
                f"Valores permitidos: {sorted(list(STATUS_VALIDOS))}."
            )

        # Incrementar contadores gerais de volumetria
        metrics["quantidade_tarefas"]["por_prioridade"][prioridade] += 1
        metrics["quantidade_tarefas"]["por_status"][status] += 1

        # 3. Processamento exclusivo para tarefas com status 'concluida'
        if status == "concluida":
            if "data_conclusao" not in task or task["data_conclusao"] is None:
                logger.error(
                    "Data de conclusão ausente para tarefa concluída ID %s.",
                    task_id
                )
                raise DadosIncompletosError(
                    f"Campo 'data_conclusao' é obrigatório para tarefas "
                    f"com status 'concluida' (ID {task_id})."
                )

            data_criacao = _parse_date(task["data_criacao"])
            data_conclusao = _parse_date(task["data_conclusao"])
            prazo = _parse_date(task["prazo"])

            # Validação de consistência cronológica: data_conclusao >= data_criacao
            if data_conclusao < data_criacao:
                logger.error(
                    "Inconsistência cronológica na tarefa ID %s: "
                    "conclusão (%s) < criação (%s).",
                    task_id, data_conclusao, data_criacao,
                )
                dt_concl = data_conclusao.strftime("%Y-%m-%d")
                dt_criar = data_criacao.strftime("%Y-%m-%d")
                raise DataInvalidaError(
                    f"Erro de validação cronológica: A data de conclusão "
                    f"({dt_concl}) não pode ser anterior à data de "
                    f"criação ({dt_criar}) na tarefa ID {task_id}."
                )

            # Cálculo de tempo de conclusão em dias (float)
            tempo_dias = (data_conclusao - data_criacao).total_seconds() / 86400.0

            # Verificação de atraso: data_conclusao > prazo
            atrasada = 1 if data_conclusao > prazo else 0

            # Atualizar acumuladores gerais
            acumuladores["geral"]["tempo_total"] += tempo_dias
            acumuladores["geral"]["atrasos"] += atrasada
            acumuladores["geral"]["concluidas"] += 1

            # Atualizar acumuladores específicos da prioridade
            acumuladores[prioridade]["tempo_total"] += tempo_dias
            acumuladores[prioridade]["atrasos"] += atrasada
            acumuladores[prioridade]["concluidas"] += 1

    # 4. Consolidação das métricas finais com blindagem contra divisão por zero
    for chave in ["geral", "baixa", "media", "alta"]:
        total_concluidas = acumuladores[chave]["concluidas"]
        if total_concluidas > 0:
            metrics["tempo_medio_conclusao"][chave] = round(
                acumuladores[chave]["tempo_total"] / total_concluidas, 4
            )
            metrics["taxa_atraso"][chave] = round(
                acumuladores[chave]["atrasos"] / total_concluidas, 4
            )
        else:
            # Mantém 0.0 para evitar divisão por zero se não houver concluídas
            metrics["tempo_medio_conclusao"][chave] = 0.0
            metrics["taxa_atraso"][chave] = 0.0

    logger.info("Análise de tarefas finalizada com sucesso.")
    return metrics
