
from pathlib import Path
import pandas as pd

pasta_projeto = Path(__file__).resolve().parent

pasta_entrada = (
    pasta_projeto
    / "dados_entrada"
    / "arquivos_mensais"
)

# Ler um arquivo existente
arquivo_original = pasta_entrada / "vendas_2015.csv"

dados = pd.read_csv(arquivo_original)

# Selecionar cinco registros
dados_teste = dados.head(5).copy()

# Remover uma coluna obrigatória
dados_teste = dados_teste.drop(
    columns=["Sales"]
)

# Criar arquivo propositalmente incorreto
arquivo_teste = (
    pasta_entrada / "vendas_teste_erro.csv"
)

dados_teste.to_csv(
    arquivo_teste,
    index=False,
    encoding="utf-8-sig"
)

print("Arquivo de teste criado:")
print(arquivo_teste)
