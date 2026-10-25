import pytest
from datetime import datetime, timedelta
from src.task_analyzer import analyze_tasks, TaskValidationError

def test_cenario_sucesso_calculo_metricas():
    agora = datetime.now()
    tasks = [
        {"id": 1, "titulo": "A1", "prioridade": "ALTA", "data_criacao": agora, "data_vencimento": agora + timedelta(hours=5), "data_conclusao": agora + timedelta(hours=2)},
        {"id": 2, "titulo": "A2", "prioridade": "ALTA", "data_criacao": agora, "data_vencimento": agora + timedelta(hours=5), "data_conclusao": agora + timedelta(hours=4)},
        {"id": 3, "titulo": "M1", "prioridade": "MEDIA", "data_criacao": agora, "data_vencimento": agora + timedelta(hours=2), "data_conclusao": agora + timedelta(hours=3)},
        {"id": 4, "titulo": "B1", "prioridade": "BAIXA", "data_criacao": agora, "data_vencimento": agora + timedelta(hours=10), "data_conclusao": None},
    ]
    
    resultado = analyze_tasks(tasks)
    
    assert resultado['taxa_atraso_percentual'] == 25.00
    assert resultado['total_tarefas_concluidas'] == 3
    assert resultado['tempo_medio_conclusao_horas'] == 3.00
    
    assert resultado['indicadores_prioridade']['ALTA']['total_tarefas_concluidas'] == 2
    assert resultado['indicadores_prioridade']['ALTA']['tempo_medio_conclusao_horas'] == 3.00
    
    assert resultado['indicadores_prioridade']['MEDIA']['total_tarefas_concluidas'] == 1
    assert resultado['indicadores_prioridade']['MEDIA']['tempo_medio_conclusao_horas'] == 3.00
    
    assert resultado['indicadores_prioridade']['BAIXA']['total_tarefas_concluidas'] == 0
    assert resultado['indicadores_prioridade']['BAIXA']['tempo_medio_conclusao_horas'] == 0.00

def test_cenario_erro_inconsistencia_temporal():
    agora = datetime.now()
    tasks = [
        {"id": 1, "titulo": "A1", "prioridade": "ALTA", "data_criacao": agora, "data_vencimento": agora + timedelta(hours=5), "data_conclusao": agora - timedelta(hours=2)}
    ]
    
    with pytest.raises(TaskValidationError, match="Inconsistência cronológica: data_conclusao não pode ser anterior a data_criacao"):
        analyze_tasks(tasks)

def test_cenario_casos_borda():
    resultado_vazio = analyze_tasks([])
    assert resultado_vazio['tempo_medio_conclusao_horas'] == 0.0
    assert resultado_vazio['taxa_atraso_percentual'] == 0.0
    assert resultado_vazio['total_tarefas_concluidas'] == 0
