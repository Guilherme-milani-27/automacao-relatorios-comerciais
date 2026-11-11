
from pathlib import Path

from src.relatorio_erros import gerar_relatorio_erros

pasta_projeto = Path(__file__).resolve().parent

detalhes = [
    {
        "Arquivo": "vendas_2015.csv",
        "Tipo_Erro": "Coluna ausente",
        "Detalhes": "Coluna Sales não encontrada"
    },
    {
        "Arquivo": "vendas_2016.csv",
        "Tipo_Erro": "Registro duplicado",
        "Detalhes": "Row ID 10 duplicado"
    }
]

destino = (
    pasta_projeto
    / "relatorios"
    / "Relatorio_Erros_Teste.xlsx"
)

arquivo = gerar_relatorio_erros(
    detalhes,
    destino
)

print("Relatório de erros criado!")
print("Arquivo:", arquivo)
