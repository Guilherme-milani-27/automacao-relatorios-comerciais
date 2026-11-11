
from pathlib import Path
import pandas as pd

pasta_projeto = Path(__file__).resolve().parent

pasta_entrada = (
    pasta_projeto
    / "dados_entrada"
    / "arquivos_mensais"
)

# Arquivo original
arquivo_original = pasta_entrada / "vendas_2015.csv"

# Ler os dados
df = pd.read_csv(arquivo_original)

# Copiar cinco registros existentes
df_duplicados = df.head(5).copy()

# Criar arquivo de teste
arquivo_teste = (
    pasta_entrada / "vendas_teste_duplicado.csv"
)

df_duplicados.to_csv(
    arquivo_teste,
    index=False,
    encoding="utf-8-sig"
)

print("Arquivo de duplicidades criado!")
print("Registros duplicados:", len(df_duplicados))
print("Row IDs:", df_duplicados["Row ID"].tolist())
