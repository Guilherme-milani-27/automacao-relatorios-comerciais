
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

df = consolidar_arquivos(pasta_entrada)
df = converter_vendas(df)

texto = df["Sales"].astype("string").str.strip()

# Identificar registros com múltiplos pontos
mascara = texto.str.count(r"\.").gt(1).fillna(False)

suspeitos = df.loc[mascara].copy()

# Separar os valores por seus componentes
suspeitos["Partes"] = (
    suspeitos["Sales"].astype(str).str.split(".")
)

suspeitos["Quantidade_Pontos"] = (
    suspeitos["Sales"].astype(str).str.count(r"\.")
)

suspeitos["Casas_Finais"] = (
    suspeitos["Partes"].apply(
        lambda partes: len(partes[-1])
    )
)

print("\n=== AUDITORIA DE MÚLTIPLOS PONTOS ===")

print("Registros encontrados:", len(suspeitos))

print("\n=== QUANTIDADE DE PONTOS ===")
print(suspeitos["Quantidade_Pontos"].value_counts())

print("\n=== DÍGITOS APÓS O ÚLTIMO PONTO ===")
print(suspeitos["Casas_Finais"].value_counts())

print("\n=== EXEMPLOS ===")
print(
    suspeitos[
        [
            "Row ID",
            "Sales",
            "Sales_Tratado",
            "Quantidade_Pontos",
            "Casas_Finais"
        ]
    ].head(20).to_string(index=False)
)

print("\n=== TOTAL DOS REGISTROS ===")
print(
    "Faturamento:",
    round(suspeitos["Sales_Tratado"].sum(), 2)
)
