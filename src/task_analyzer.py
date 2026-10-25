from typing import List, Dict, Any
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskValidationError(ValueError):
    """Exceção levantada para inconsistências nos dados das tarefas."""
    pass

def analyze_tasks(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analisa um conjunto de tarefas e retorna métricas de produtividade.
    """
    total_tarefas = len(tasks)
    if total_tarefas == 0:
        return {
            'tempo_medio_conclusao_horas': 0.0,
            'taxa_atraso_percentual': 0.0,
            'total_tarefas_concluidas': 0,
            'indicadores_prioridade': {
                'ALTA': {'tempo_medio_conclusao_horas': 0.0, 'total_tarefas_concluidas': 0},
                'MEDIA': {'tempo_medio_conclusao_horas': 0.0, 'total_tarefas_concluidas': 0},
                'BAIXA': {'tempo_medio_conclusao_horas': 0.0, 'total_tarefas_concluidas': 0}
            }
        }

    total_atrasadas = 0
    concluidas_geral = []
    concluidas_por_prioridade = {'ALTA': [], 'MEDIA': [], 'BAIXA': []}

    for task in tasks:
        data_criacao = task['data_criacao']
        data_conclusao = task.get('data_conclusao')
        data_vencimento = task['data_vencimento']
        prioridade = task['prioridade']

        if data_conclusao:
            if data_conclusao < data_criacao:
                raise TaskValidationError("Inconsistência cronológica: data_conclusao não pode ser anterior a data_criacao")
            
            horas_decorridas = (data_conclusao - data_criacao).total_seconds() / 3600.0
            concluidas_geral.append(horas_decorridas)
            if prioridade in concluidas_por_prioridade:
                concluidas_por_prioridade[prioridade].append(horas_decorridas)
            
            if data_conclusao > data_vencimento:
                total_atrasadas += 1

    def calcular_media(tempos: List[float]) -> float:
        if not tempos:
            return 0.0
        media = sum(tempos) / len(tempos)
        return float(Decimal(str(media)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

    taxa_atraso = (total_atrasadas / total_tarefas) * 100
    taxa_atraso_arredondada = float(Decimal(str(taxa_atraso)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

    return {
        'tempo_medio_conclusao_horas': calcular_media(concluidas_geral),
        'taxa_atraso_percentual': taxa_atraso_arredondada,
        'total_tarefas_concluidas': len(concluidas_geral),
        'indicadores_prioridade': {
            p: {
                'tempo_medio_conclusao_horas': calcular_media(tempos),
                'total_tarefas_concluidas': len(tempos)
            } for p, tempos in concluidas_por_prioridade.items()
        }
    }
