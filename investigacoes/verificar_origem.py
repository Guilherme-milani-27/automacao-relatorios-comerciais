
from pathlib import Path
import pandas as pd

pasta_projeto = Path(__file__).resolve().parent.parent

arquivo = (
    pasta_projeto
    / "dados_entrada"
    / "train.csv"
)

df = pd.read_csv(
    arquivo,
    dtype={"Sales": "string"},
    sep=";"
)

ids = [8, 9, 12, 69, 114, 116, 117, 125, 147, 158]

print("\n=== VALORES NO ARQUIVO ORIGINAL ===")

print(
    df.loc[
        df["Row ID"].isin(ids),
        ["Row ID", "Sales"]
    ].to_string(index=False)
)

print("\n=== PADRÕES DA COLUNA SALES ===")

texto = df["Sales"].str.strip()

print(
    "Múltiplos pontos:",
    texto.str.count(r"\.").gt(1).sum()
)

print(
    "Um ponto e três dígitos:",
    texto.str.fullmatch(r"\d+\.\d{3}").sum()
)

print(
    "Vendas ausentes:",
    df["Sales"].isna().sum()
)
