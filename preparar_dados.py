
# preparar_dados.py

import pandas as pd
from pathlib import Path

pasta_projeto = Path(__file__).resolve().parent

entrada = pasta_projeto / "dados_entrada" / "train_referencia.csv"
saida = pasta_projeto / "dados_entrada" / "arquivos_mensais"

saida.mkdir(parents=True, exist_ok=True)

# Carregar base original
df = pd.read_csv(
    entrada,
    sep=",",
    encoding="utf-8-sig",
    dtype={"Sales": "string"}
)


print("\n=== VERIFICAÇÃO DA LEITURA ORIGINAL ===")

ids_teste = [4, 182, 400, 8106]

print("\nTipos de dados:")
print(df[["Row ID", "Sales"]].dtypes)

print("\nRegistros selecionados:")
print(
    df.loc[
        df["Row ID"].isin(ids_teste),
        ["Row ID", "Sales"]
    ].to_string(index=False)
)

print("\nValores ausentes em Sales:")
print(df["Sales"].isna().sum())


# Converter datas para extrair o ano
datas = pd.to_datetime(
    df["Order Date"],
    format="%d/%m/%Y"
)

df["Ano"] = datas.dt.year

# Criar um arquivo por ano
for ano, grupo in df.groupby("Ano"):

    caminho = saida / f"vendas_{ano}.csv"

    grupo.drop(columns=["Ano"]).to_csv(
        caminho,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"Arquivo criado: vendas_{ano}.csv "
        f"({len(grupo)} registros)"
    )

print("\nArquivos de teste criados!")


# Validar os arquivos gerados

arquivos = sorted(saida.glob("vendas_*.csv"))

total_registros = 0

for arquivo in arquivos:
    dados = pd.read_csv(arquivo)

    total_registros += len(dados)

    print(f"{arquivo.name}: {len(dados)} registros")

print("\n=== VALIDAÇÃO ===")
print("Registros originais:", len(df))
print("Registros divididos:", total_registros)
print("Diferença:", len(df) - total_registros)
