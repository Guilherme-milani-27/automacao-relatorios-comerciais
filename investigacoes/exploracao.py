
# %% 0 - CONFIGURAÇÃO E CARREGAMENTO

import pandas as pd
from pathlib import Path

pasta_projeto = Path(__file__).resolve().parent.parent
caminho_arquivo = pasta_projeto / "dados_entrada" / "train.csv"

df = pd.read_csv(caminho_arquivo, sep=";")

print("Base carregada com sucesso!")
print("Dimensões:", df.shape)


# %%ETAPA 1.3 - INVESTIGAÇÃO DOS DADOS

print("\n=== AMOSTRA DOS VALORES DE VENDAS ===")
print(df["Sales"].head(20).to_list())

print("\n=== VENDAS COM MAIS DE UM PONTO ===")
vendas_multiplos_pontos = df[
    df["Sales"].astype("string").str.count(r"\.") > 1
]

print(vendas_multiplos_pontos[["Row ID", "Sales"]].head(15))
print("Quantidade:", len(vendas_multiplos_pontos))

print("\n=== REGISTROS COM VENDAS NULAS ===")
print(df[df["Sales"].isna()][["Row ID", "Order ID", "Sales"]])

print("\n=== REGISTROS COM CEP NULO ===")
print(df[df["Postal Code"].isna()][
    ["Row ID", "City", "State", "Postal Code"]
].head(15))

print("\n=== DUPLICIDADES ===")
print("Linhas totalmente duplicadas:", df.duplicated().sum())
print("Row IDs duplicados:", df["Row ID"].duplicated().sum())

print("\n=== EXEMPLOS DE DATAS ===")
print(df[["Order Date", "Ship Date"]].head(10))


# %% ETAPA 1.4 - INVESTIGAÇÃO DOS FORMATOS

# Trabalhar com valores não nulos
vendas = df["Sales"].dropna().astype(str)

# Separar os valores pelos pontos
partes = vendas.str.split(".")

# Identificar os padrões de quantidade de dígitos
padroes = partes.apply(
    lambda lista: "-".join(str(len(parte)) for parte in lista)
)

print("=== PADRÕES ENCONTRADOS ===")
print(padroes.value_counts())

print("\n=== EXEMPLOS POR PADRÃO ===")

for padrao in padroes.unique():
    exemplos = vendas[padroes == padrao].head(5).tolist()

    print(f"\nPadrão {padrao}:")
    print(exemplos)


# %% ETAPA 1.5 - TESTE DE CONVERSÃO

def converter_venda(valor):
    if pd.isna(valor):
        return float("nan")

    texto = str(valor).strip()

    if texto.count(".") > 1:
        partes = texto.split(".")
        texto = "".join(partes[:-1]) + "." + partes[-1]

    return float(texto)


# Criar uma coluna temporária para teste
df["Sales_Teste"] = df["Sales"].apply(converter_venda)

print("=== COMPARAÇÃO DOS VALORES ===")

print(
    df[["Sales", "Sales_Teste"]]
    .head(20)
    .to_string(index=False)
)

print("\n=== FATURAMENTO CALCULADO ===")
print(f"R$ {df['Sales_Teste'].sum():,.2f}")

print("\n=== VALORES NULOS ===")
print(df["Sales_Teste"].isna().sum())

print("\n=== ESTATÍSTICAS ===")
print(df["Sales_Teste"].describe())

# %% ETAPA 1.6 - AUDITORIA DA CONVERSÃO

# Identificar registros com múltiplos pontos
mascara = (
    df["Sales"]
    .astype("string")
    .str.count(r"\.")
    .gt(1)
    .fillna(False)
)

vendas_especiais = df.loc[mascara]

vendas_normais = df.loc[~mascara]

print("=== VENDAS COM MÚLTIPLOS PONTOS ===")
print("Quantidade:", len(vendas_especiais))
print("Total:", round(vendas_especiais["Sales_Teste"].sum(), 2))

print("\n=== DEMAIS VENDAS ===")
print("Quantidade:", len(vendas_normais))
print("Total:", round(vendas_normais["Sales_Teste"].sum(), 2))

print("\n=== MAIORES VENDAS ===")
print(
    df[["Row ID", "Sales", "Sales_Teste"]]
    .sort_values("Sales_Teste", ascending=False)
    .head(15)
    .to_string(index=False)
)

print("\n=== TOTAL POR ANO ===")

datas = pd.to_datetime(
    df["Order Date"],
    format="%d/%m/%Y",
    errors="coerce"
)

print(
    df.groupby(datas.dt.year)["Sales_Teste"]
    .sum()
    .round(2)
)

# %% ETAPA 1.7 - VALIDAÇÃO FINANCEIRA

import numpy as np

print("=== VALIDAÇÃO FINANCEIRA ===")

print("Registros totais:", len(df))

print(
    "Valores nulos:",
    df["Sales_Teste"].isna().sum()
)

print(
    "Valores negativos:",
    (df["Sales_Teste"] < 0).sum()
)

print(
    "Valores iguais a zero:",
    (df["Sales_Teste"] == 0).sum()
)

# Verificar valores com mais de duas casas decimais
valores = df["Sales_Teste"].dropna()

tres_casas = ~np.isclose(
    valores * 100,
    np.round(valores * 100),
    atol=1e-7,
    rtol=0
)

print(
    "Valores com mais de 2 casas decimais:",
    tres_casas.sum()
)

# Conferir total anual contra total geral
total_geral = df["Sales_Teste"].sum()

total_anual = df.groupby(
    pd.to_datetime(
        df["Order Date"],
        format="%d/%m/%Y",
        errors="coerce"
    ).dt.year
)["Sales_Teste"].sum().sum()

print("\n=== CONCILIAÇÃO ===")
print("Total geral:", round(total_geral, 2))
print("Soma dos anos:", round(total_anual, 2))
print("Diferença:", round(total_geral - total_anual, 2))


# %% ETAPA 1.8 - TESTANDO O MÓDULO

from src.limpeza import converter_vendas

df_limpo = converter_vendas(df)

print("=== RESULTADO DO MÓDULO ===")

print(
    df_limpo[
        ["Sales", "Sales_Tratado"]
    ].head(10)
)

print("\nTotal de vendas:")
print(round(df_limpo["Sales_Tratado"].sum(), 2))

print("\nValores nulos:")
print(df_limpo["Sales_Tratado"].isna().sum())


# %% ETAPA 1.9 - RELATÓRIO DE INCONSISTÊNCIAS

import importlib
import src.limpeza as limpeza

# Recarregar o módulo após alterações
importlib.reload(limpeza)

inconsistencias = limpeza.identificar_inconsistencias(df)

print("=== RELATÓRIO DE INCONSISTÊNCIAS ===")

print(inconsistencias.head(15))

print("\n=== TOTAL DE INCONSISTÊNCIAS ===")
print(len(inconsistencias))

print("\n=== INCONSISTÊNCIAS POR TIPO ===")
print(inconsistencias["Problema"].value_counts())



# %% ETAPA 2.1 - EXPORTAÇÃO PARA EXCEL

from src.exportacao import exportar_relatorio

# Definir caminho de saída
caminho_saida = (
    pasta_projeto
    / "relatorios"
    / "Relatorio_Superstore.xlsx"
)

# Gerar relatório
#arquivo = exportar_relatorio(
    #df_limpo,
    #inconsistencias,
    #caminho_saida
#)

print("=== EXPORTAÇÃO CONCLUÍDA ===")
#print("Arquivo gerado:", arquivo)



# %% ETAPA 2.2 - EXPORTAÇÃO FORMATADA

import importlib
import src.exportacao as exportacao

importlib.reload(exportacao)

#arquivo = exportacao.exportar_relatorio(
    #df_limpo,
    #inconsistencias,
    #caminho_saida
#)

print("Relatório formatado com sucesso!")
#print("Arquivo:", arquivo)



# %% ETAPA 2.3 - INDICADORES COMERCIAIS

from src.indicadores import calcular_indicadores

resumo_geral, resumo_anual = calcular_indicadores(
    df_limpo
)

print("=== RESUMO GERAL ===")
print(resumo_geral.to_string(index=False))

print("\n=== RESUMO ANUAL ===")
print(resumo_anual.to_string(index=False))



# %% ETAPA 2.4 - RELATÓRIO COM INDICADORES

import importlib
import src.exportacao as exportacao

importlib.reload(exportacao)

arquivo = exportacao.exportar_relatorio(
    df_limpo,
    inconsistencias,
    resumo_geral,
    resumo_anual,
    caminho_saida
)

print("Relatório completo gerado!")
print("Arquivo:", arquivo)


# %% ETAPA 2.6 - INDICADORES POR PRODUTO

import importlib
import src.indicadores as indicadores

importlib.reload(indicadores)

resumo_categorias, ranking_produtos = (
    indicadores.calcular_indicadores_produtos(df_limpo)
)

print("=== FATURAMENTO POR CATEGORIA ===")
print(resumo_categorias.to_string(index=False))

print("\n=== TOP 10 PRODUTOS ===")
print(ranking_produtos.head(10).to_string(index=False))

print("\n=== VALIDAÇÃO ===")

total_categorias = resumo_categorias["Faturamento"].sum()
total_geral = df_limpo["Sales_Tratado"].sum()

print("Total categorias:", round(total_categorias, 2))
print("Total geral:", round(total_geral, 2))
print("Diferença:", round(total_geral - total_categorias, 2))


# %% ETAPA 3.2 - TESTE DE CONSOLIDAÇÃO

from pathlib import Path
from src.leitura import consolidar_arquivos

pasta_projeto = Path.cwd()

pasta_arquivos = (
    pasta_projeto
    / "dados_entrada"
    / "arquivos_mensais"
)

df_consolidado = consolidar_arquivos(pasta_arquivos)

print("\n=== DIMENSÕES ===")
print(df_consolidado.shape)

print("\n=== REGISTROS POR ARQUIVO ===")
print(df_consolidado["Arquivo_Origem"].value_counts())

print("\n=== DUPLICIDADES ===")
print(
    "Row IDs duplicados:",
    df_consolidado["Row ID"].duplicated().sum()
)

print("\n=== VALIDAÇÃO ===")
print("Total esperado:", 9800)
print("Total encontrado:", len(df_consolidado))
print("Diferença:", 9800 - len(df_consolidado))


# %%
