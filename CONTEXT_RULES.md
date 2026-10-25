# Governança de Contexto e Regras para Agentes de IA

## Diretrizes Arquiteturais (Obrigatórias)
- Utilizar obrigatoriamente Python 3.11+.
- Adotar o uso de type hints para todos os parâmetros e retornos.
- Respeitar o princípio da Responsabilidade Única (SRP) e PEP 8.
- Incluir documentação formal baseada no padrão Google style docstrings.
- Estruturar funções pequenas, coesas e modulares.
- Aplicar tratamento de exceções específico.
- Adicionar logs estruturados via módulo padrão logging.

## Proibições Explícitas (Regras Restritivas)
- NÃO utilizar bibliotecas externas ou frameworks não autorizados.
- NÃO alterar, omitir ou flexibilizar os cenários de teste.
- NÃO modificar a estrutura de diretórios.
- NÃO implementar lógicas para persistência de dados.
- NÃO modificar assinaturas de métodos públicos.
- NÃO gerar novas funções que não estejam cobertas por testes.
- NÃO inserir código duplicado.
- NÃO assumir comportamentos não especificados.
