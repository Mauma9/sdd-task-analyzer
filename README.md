# TaskAnalyzer
Documentação geral do projeto. Sistema de extração de métricas de produtividade, validado com CI/CD, Docker e Governança de IA.

## Executar Localmente
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/test_harness.py -v
```

## Executar via Docker
```bash
docker compose run test_runner
```
