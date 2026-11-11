
from pathlib import Path
import pandas as pd

from src.leitura import consolidar_arquivos
from src.limpeza import converter_vendas

pasta = Path(__file__).resolve().parent.parent

# 1. Carregar Projeto A
arquivo_a = (
    pasta / "dados_entrada"
    / "comparacao"
    / "Fato_Vendas_Projeto_A.csv"
)

df_a = pd.read_csv(
    arquivo_a,
    sep=None,
    engine="python",
    dtype="string",
    encoding="utf-8-sig"
)

# Converter valores brasileiros para número
texto_a = (
    df_a["Valor_Venda"]
    .str.strip()
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
)

df_a["Venda_A"] = pd.to_numeric(
    texto_a,
    errors="raise"
)

df_a["Row ID"] = pd.to_numeric(
    df_a["ID_Linha"],
    errors="raise"
).astype("int64")

# 2. Carregar Projeto B
pasta_entrada = (
    pasta / "dados_entrada"
    / "arquivos_mensais"
)

df_b = consolidar_arquivos(pasta_entrada)
df_b = converter_vendas(df_b)

df_b["Row ID"] = pd.to_numeric(
    df_b["Row ID"],
    errors="raise"
).astype("int64")

df_b = df_b.rename(
    columns={"Sales_Tratado": "Venda_B"}
)

# 3. Conferir identificadores únicos
for nome, dados in [
    ("Projeto A", df_a),
    ("Projeto B", df_b)
]:
    if dados["Row ID"].duplicated().any():
        raise ValueError(
            f"{nome} contém Row IDs duplicados."
        )

# 4. Comparar pelo Row ID
comparacao = df_a[
    ["Row ID", "Valor_Venda", "Venda_A"]
].merge(
    df_b[
        ["Row ID", "Sales", "Venda_B"]
    ],
    on="Row ID",
    how="outer",
    validate="one_to_one",
    indicator=True
)

comparacao["Diferenca"] = (
    comparacao["Venda_B"].fillna(0)
    - comparacao["Venda_A"].fillna(0)
)

# Identificar divergências
tolerancia = 0.000001

divergencias = comparacao[
    (comparacao["_merge"] != "both")
    | (comparacao["Diferenca"].abs() > tolerancia)
    | (comparacao["Venda_A"].isna())
    | (comparacao["Venda_B"].isna())
].copy()

divergencias = divergencias.sort_values(
    "Diferenca",
    key=lambda serie: serie.abs(),
    ascending=False
)

# 5. Resumo
print("\n=== CONCILIAÇÃO DETALHADA ===")

print("Registros Projeto A:", len(df_a))
print("Registros Projeto B:", len(df_b))
print("Registros comparados:", len(comparacao))

print(
    "Registros divergentes:",
    len(divergencias)
)

print(
    "Somente no Projeto A:",
    (comparacao["_merge"] == "left_only").sum()
)

print(
    "Somente no Projeto B:",
    (comparacao["_merge"] == "right_only").sum()
)

total_a = df_a["Venda_A"].sum()
total_b = df_b["Venda_B"].sum()

print(f"\nTotal Projeto A: {total_a:,.2f}")
print(f"Total Projeto B: {total_b:,.2f}")
print(f"Diferença: {total_b - total_a:,.2f}")

print("\n=== TOP 20 DIVERGÊNCIAS ===")

print(
    divergencias[
        [
            "Row ID",
            "Valor_Venda",
            "Sales",
            "Venda_A",
            "Venda_B",
            "Diferenca"
        ]
    ].head(20).to_string(index=False)
)

# 6. Exportar divergências
destino = (
    pasta / "relatorios"
    / "Conciliacao_Projetos.xlsx"
)

destino.parent.mkdir(
    parents=True,
    exist_ok=True
)

with pd.ExcelWriter(
    destino,
    engine="openpyxl"
) as writer:

    comparacao.to_excel(
        writer,
        sheet_name="Comparacao_Completa",
        index=False
    )

    divergencias.to_excel(
        writer,
        sheet_name="Divergencias",
        index=False
    )

print("\nRelatório de conciliação:", destino)


print("\n=== ANÁLISE DAS DIVERGÊNCIAS ===")

# Considerar somente registros presentes nos dois projetos
# e com valores numéricos válidos
comparaveis = divergencias.loc[
    (divergencias["_merge"] == "both")
    & divergencias["Venda_A"].notna()
    & divergencias["Venda_B"].notna()
    & (divergencias["Venda_A"] != 0)
].copy()

comparaveis["Razao_B_A"] = (
    comparaveis["Venda_B"]
    / comparaveis["Venda_A"]
)

print("\n=== DISTRIBUIÇÃO DAS RAZÕES ===")
print(
    comparaveis["Razao_B_A"]
    .round(6)
    .value_counts()
    .sort_index()
)

print("\n=== FORMATOS ORIGINAIS ===")

comparaveis["Quantidade_Pontos"] = (
    comparaveis["Sales"]
    .astype("string")
    .str.count(r"\.")
)

print(
    comparaveis["Quantidade_Pontos"]
    .value_counts()
)

print("\n=== VALIDAÇÃO DO TOTAL ===")

print(
    "Soma das diferenças:",
    round(divergencias["Diferenca"].sum(), 4)
)

print(
    "Diferença entre os totais:",
    round(total_b - total_a, 4)
)



print("\n=== CLASSIFICAÇÃO DAS DIVERGÊNCIAS ===")

# Registros com valores ausentes
ausentes = divergencias[
    divergencias["Venda_A"].isna()
    | divergencias["Venda_B"].isna()
].copy()

print("\n=== REGISTROS COM VALORES AUSENTES ===")

print(
    ausentes[
        [
            "Row ID",
            "Valor_Venda",
            "Sales",
            "Venda_A",
            "Venda_B"
        ]
    ].to_string(index=False)
)

# Registros com valores numéricos diferentes
numericos = divergencias[
    divergencias["Venda_A"].notna()
    & divergencias["Venda_B"].notna()
].copy()

numericos["Razao"] = (
    numericos["Venda_B"]
    / numericos["Venda_A"]
)

numericos["Pontos"] = (
    numericos["Sales"]
    .astype("string")
    .str.count(r"\.")
)

print("\n=== DIVERGÊNCIAS NUMÉRICAS ===")

print(
    numericos[
        [
            "Row ID",
            "Sales",
            "Venda_A",
            "Venda_B",
            "Razao",
            "Pontos"
        ]
    ].to_string(index=False)
)

print("\n=== RESUMO ===")
print("Registros ausentes:", len(ausentes))
print("Divergências numéricas:", len(numericos))

print(
    "Diferença dos registros numéricos:",
    round(numericos["Diferenca"].sum(), 4)
)
