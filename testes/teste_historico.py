
from pathlib import Path

from src.historico import registrar_execucao

pasta_projeto = Path(__file__).resolve().parent

arquivo = registrar_execucao(
    pasta_projeto=pasta_projeto,
    id_execucao="teste001",
    status="SUCESSO",
    tempo_segundos=8.32,
    arquivos=4,
    registros=9800,
    inconsistencias=203,
    mensagem="Execução de teste"
)

print("Histórico criado com sucesso!")
print("Arquivo:", arquivo)
