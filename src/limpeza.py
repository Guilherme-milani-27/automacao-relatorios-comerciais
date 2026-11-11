
#  Módulo responsável pela limpeza dos dados

import pandas as pd


def converter_vendas(df):
    """
    Converte a coluna Sales para valores numéricos.

    A regra de múltiplos pontos é provisória
    e específica da base Superstore.
    """

    df = df.copy()

    def converter_valor(valor):
        if pd.isna(valor):
            return float("nan")

        texto = str(valor).strip()

        if texto.count(".") > 1:
            partes = texto.split(".")
            texto = "".join(partes[:-1]) + "." + partes[-1]

        return float(texto)

    df["Sales_Tratado"] = df["Sales"].apply(
        converter_valor
    )

    return df


def identificar_inconsistencias(df):
    """
    Identifica registros que precisam de revisão.
    Retorna um DataFrame com as inconsistências.
    """

    problemas = []

    # Vendas ausentes
    vendas_nulas = df[df["Sales"].isna()]

    for _, linha in vendas_nulas.iterrows():
        problemas.append({
            "Row ID": linha["Row ID"],
            "Coluna": "Sales",
            "Problema": "Valor de venda ausente"
        })

    # CEPs ausentes
    ceps_nulos = df[df["Postal Code"].isna()]

    for _, linha in ceps_nulos.iterrows():
        problemas.append({
            "Row ID": linha["Row ID"],
            "Coluna": "Postal Code",
            "Problema": "CEP ausente"
        })

    # Vendas com múltiplos pontos
    mascara = (
        df["Sales"]
        .astype("string")
        .str.count(r"\.")
        .gt(1)
        .fillna(False)
    )

    vendas_formatacao = df[mascara]

    for _, linha in vendas_formatacao.iterrows():
        problemas.append({
            "Row ID": linha["Row ID"],
            "Coluna": "Sales",
            "Problema": "Formato numérico suspeito"
        })

    return pd.DataFrame(
        problemas,
        columns=["Row ID", "Coluna", "Problema"]
    )
