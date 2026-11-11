
# src/indicadores.py

import pandas as pd


def calcular_indicadores(df):
    """
    Calcula indicadores comerciais a partir
    dos dados tratados.
    """

    dados = df.copy()

    # Converter datas
    dados["Order Date"] = pd.to_datetime(
        dados["Order Date"],
        format="%d/%m/%Y",
        errors="coerce"
    )

    # Criar coluna de ano
    dados["Ano"] = dados["Order Date"].dt.year

    # Calcular indicadores gerais
    faturamento = dados["Sales_Tratado"].sum()

    total_pedidos = dados["Order ID"].nunique()

    ticket_medio = (
        faturamento / total_pedidos
        if total_pedidos > 0 else 0
    )

    # Criar resumo geral
    resumo_geral = pd.DataFrame({
        "Indicador": [
            "Faturamento Total",
            "Total de Pedidos",
            "Ticket Médio"
        ],
        "Valor": [
            faturamento,
            total_pedidos,
            ticket_medio
        ]
    })

    # Criar resumo anual
    resumo_anual = (
        dados.groupby("Ano", as_index=False)
        .agg(
            Faturamento=("Sales_Tratado", "sum"),
            Pedidos=("Order ID", "nunique")
        )
    )

    resumo_anual["Ticket_Medio"] = (
        resumo_anual["Faturamento"]
        / resumo_anual["Pedidos"]
    )

    return resumo_geral, resumo_anual


def calcular_indicadores_produtos(df):
    """
    Calcula o faturamento por categoria e produto.
    """

    dados = df.copy()

    # 1. Faturamento por categoria
    resumo_categorias = (
        dados.groupby("Category", as_index=False)
        .agg(
            Faturamento=("Sales_Tratado", "sum"),
            Pedidos=("Order ID", "nunique"),
            Produtos=("Product ID", "nunique")
        )
        .sort_values(
            "Faturamento",
            ascending=False
        )
    )

    # 2. Ranking de produtos
    ranking_produtos = (
        dados.groupby(
            ["Product ID", "Product Name"],
            as_index=False
        )
        .agg(
            Faturamento=("Sales_Tratado", "sum"),
            Pedidos=("Order ID", "nunique")
        )
        .sort_values(
            "Faturamento",
            ascending=False
        )
    )

    return resumo_categorias, ranking_produtos
