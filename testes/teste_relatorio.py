
from config import ARQUIVO_RELATORIO
from src.validacao_relatorio import validar_relatorio

print("Iniciando teste de divergência financeira...")

validar_relatorio(
    caminho=ARQUIVO_RELATORIO,
    registros_esperados=9800,
    faturamento_esperado=2261536.78
)

print("Teste finalizado!")

