
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

# Cenário A: interpretação atual
df["Cenario_A"] = df["Sales_Tratado"]

# Identificar valores com um ponto e três dígitos
texto = df["Sales"].astype("string").str.strip()

mascara = texto.str.fullmatch(
    r"\d+\.\d{3}"
).fillna(False)

# Cenário B: começar com os valores atuais
df["Cenario_B"] = df["Cenario_A"].copy()

# Tratar pontos únicos como separador de milhar
df.loc[mascara, "Cenario_B"] = (
    pd.to_numeric(
        texto.loc[mascara].str.replace(
            ".",
            "",
            regex=False
        ),
        errors="coerce"
    )
)

total_a = df["Cenario_A"].sum()
total_b = df["Cenario_B"].sum()

print("\n=== COMPARAÇÃO DE CENÁRIOS ===")
print(f"Cenário A: {total_a:,.2f}")
print(f"Cenário B: {total_b:,.2f}")
print(f"Diferença: {total_b - total_a:,.2f}")

print("\nRegistros reinterpretados:", mascara.sum())

print("\n=== EXEMPLOS ===")
print(
    df.loc[
        mascara,
        ["Row ID", "Sales", "Cenario_A", "Cenario_B"]
    ].head(10).to_string(index=False)
)
