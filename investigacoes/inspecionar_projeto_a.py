
from pathlib import Path
import pandas as pd

pasta = Path(__file__).resolve().parent.parent

arquivo = (
    pasta
    / "dados_entrada"
    / "comparacao"
    / "Fato_Vendas_Projeto_A.csv"
)

# Ler inicialmente como texto para preservar os valores
df = pd.read_csv(
    arquivo,
    sep=None,
    engine="python",
    dtype="string",
    encoding="utf-8-sig"
)

print("\n=== DIMENSÕES ===")
print(df.shape)

print("\n=== COLUNAS ===")
for coluna in df.columns:
    print(repr(coluna))

print("\n=== PRIMEIROS REGISTROS ===")
print(df.head(5).to_string(index=False))

print("\n=== VALORES AUSENTES ===")
print(df.isna().sum().to_string())
