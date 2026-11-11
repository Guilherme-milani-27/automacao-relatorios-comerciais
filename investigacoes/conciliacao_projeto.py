
from pathlib import Path
import pandas as pd

from src.leitura import consolidar_arquivos
from src.limpeza import converter_vendas

pasta = Path(__file__).resolve().parent.parent

df = consolidar_arquivos(
    pasta / "dados_entrada" / "arquivos_mensais"
)

df = converter_vendas(df)

texto = df["Sales"].astype("string").str.strip()

mascara_multiplos = (
    texto.str.count(r"\.").gt(1).fillna(False)
)

# Separar grupos para conciliação
df["Grupo_Formato"] = "Outros formatos"

df.loc[
    mascara_multiplos,
    "Grupo_Formato"
] = "Multiplos pontos"

resumo = (
    df.groupby("Grupo_Formato", as_index=False)
    .agg(
        Registros=("Row ID", "count"),
        Faturamento=("Sales_Tratado", "sum")
    )
)

print("\n=== FATURAMENTO POR FORMATO ===")
print(resumo.to_string(index=False))

total_b = df["Sales_Tratado"].sum()
total_a = 2261536.78

print("\n=== CONCILIAÇÃO ===")
print(f"Projeto A: {total_a:,.2f}")
print(f"Projeto B: {total_b:,.2f}")
print(f"Diferença: {total_b - total_a:,.2f}")

print("\n=== SIMULAÇÃO ===")

total_sem_multiplos = df.loc[
    ~mascara_multiplos,
    "Sales_Tratado"
].sum()

print(
    "Total sem múltiplos pontos:",
    round(total_sem_multiplos, 2)
)

print(
    "Diferença para Projeto A:",
    round(total_sem_multiplos - total_a, 2)
)
