
from pathlib import Path
import pandas as pd

from src.leitura import consolidar_arquivos
from src.limpeza import converter_vendas

pasta_projeto = Path(__file__).resolve().parent.parent

pasta_entrada = (
    pasta_projeto
    / "dados_entrada"
    / "arquivos_mensais"
)

# Carregar e tratar os dados
df = consolidar_arquivos(pasta_entrada)
df = converter_vendas(df)

# Preservar a representação textual original
vendas = df["Sales"].astype("string").str.strip()

# Identificar padrões numéricos
mascara_multiplos_pontos = (
    vendas.str.count(r"\.").gt(1).fillna(False)
)

mascara_tres_decimais = (
    vendas.str.fullmatch(r"\d+\.\d{3}").fillna(False)
)

mascara_ausentes = df["Sales"].isna()

print("\n=== AUDITORIA FINANCEIRA ===")

print("Registros totais:", len(df))
print("Vendas ausentes:", mascara_ausentes.sum())

print(
    "Valores com múltiplos pontos:",
    mascara_multiplos_pontos.sum()
)

print(
    "Valores com um ponto e três dígitos:",
    mascara_tres_decimais.sum()
)

print("\n=== EXEMPLOS AMBÍGUOS ===")

colunas = [
    "Row ID",
    "Sales",
    "Sales_Tratado",
    "Arquivo_Origem"
]

print(
    df.loc[
        mascara_tres_decimais,
        colunas
    ].head(20).to_string(index=False)
)

print("\n=== TOTAIS ===")

print(
    "Faturamento calculado:",
    round(df["Sales_Tratado"].sum(), 2)
)

print(
    "Registros com venda válida:",
    df["Sales_Tratado"].notna().sum()
)
