
# src/exportacao.py

from pathlib import Path
import pandas as pd

from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter


def formatar_planilha(ws):
    """
    Aplica formatação profissional à planilha.
    """

    # Formatar cabeçalho
    for celula in ws[1]:
        celula.fill = PatternFill(
            start_color="17365D",
            end_color="17365D",
            fill_type="solid"
        )

        celula.font = Font(
            color="FFFFFF",
            bold=True
        )

        celula.alignment = Alignment(
            horizontal="center"
        )

    # Congelar primeira linha
    ws.freeze_panes = "A2"

    # Adicionar filtros
    ws.auto_filter.ref = ws.dimensions

    # Ajustar largura das colunas
    for coluna in ws.columns:
        letra = get_column_letter(coluna[0].column)

        maior_tamanho = max(
            len(str(celula.value))
            if celula.value is not None else 0
            for celula in coluna
        )

        ws.column_dimensions[letra].width = min(
            maior_tamanho + 3,
            45
        )

    # Formatar valores numéricos de vendas
    for celula in ws[1]:
        if celula.value == "Sales_Tratado":
            indice_coluna = celula.column

            for linha in ws.iter_rows(
                min_row=2,
                min_col=indice_coluna,
                max_col=indice_coluna
            ):
                linha[0].number_format = '#,##0.000'

def exportar_relatorio(
    df_vendas,
    df_inconsistencias,
    resumo_geral,
    resumo_anual,
    resumo_categorias,
    ranking_produtos,
    destino
):

    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(destino, engine="openpyxl") as writer:

        resumo_geral.to_excel(
            writer,
            sheet_name="Resumo_Geral",
            index=False
        )

        resumo_anual.to_excel(
            writer,
            sheet_name="Resumo_Anual",
            index=False
        )

        df_vendas.to_excel(
            writer,
            sheet_name="Vendas_Tratadas",
            index=False
        )

        df_inconsistencias.to_excel(
            writer,
            sheet_name="Inconsistencias",
            index=False
        )

        
        resumo_categorias.to_excel(
            writer,
            sheet_name="Resumo_Categorias",
            index=False
        )

        ranking_produtos.to_excel(
            writer,
            sheet_name="Ranking_Produtos",
            index=False
        )

        # Formatar todas as abas
        for ws in writer.book.worksheets:
            formatar_planilha(ws)

        # Formatar valores do resumo geral
        ws_geral = writer.book["Resumo_Geral"]

        for linha in range(2, ws_geral.max_row + 1):
            indicador = ws_geral.cell(linha, 1).value
            celula = ws_geral.cell(linha, 2)

            if indicador == "Total de Pedidos":
                celula.number_format = '#,##0'
            else:
                celula.number_format = '"R$" #,##0.00'

        # Formatar indicadores anuais
        ws_anual = writer.book["Resumo_Anual"]

        for linha in range(2, ws_anual.max_row + 1):
            ws_anual.cell(linha, 2).number_format = '"R$" #,##0.00'
            ws_anual.cell(linha, 3).number_format = '#,##0'
            ws_anual.cell(linha, 4).number_format = '"R$" #,##0.00'
        
        # Formatar faturamento por categoria
        ws_cat = writer.book["Resumo_Categorias"]

        for linha in range(2, ws_cat.max_row + 1):
            ws_cat.cell(linha, 2).number_format = '"R$" #,##0.00'
            ws_cat.cell(linha, 3).number_format = '#,##0'
            ws_cat.cell(linha, 4).number_format = '#,##0'

        # Formatar ranking de produtos
        ws_prod = writer.book["Ranking_Produtos"]

        for linha in range(2, ws_prod.max_row + 1):
            ws_prod.cell(linha, 3).number_format = '"R$" #,##0.00'
            ws_prod.cell(linha, 4).number_format = '#,##0'

    return destino
