
# src/relatorio_erros.py

from pathlib import Path
import pandas as pd

from openpyxl.styles import Font, PatternFill


def gerar_relatorio_erros(detalhes, destino):

    destino = Path(destino)
    destino.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df_erros = pd.DataFrame(detalhes)

    with pd.ExcelWriter(
        destino,
        engine="openpyxl"
    ) as writer:

        df_erros.to_excel(
            writer,
            sheet_name="Erros_Validacao",
            index=False
        )

        ws = writer.book["Erros_Validacao"]

        # Formatar cabeçalho
        for celula in ws[1]:
            celula.fill = PatternFill(
                start_color="9C0006",
                end_color="9C0006",
                fill_type="solid"
            )

            celula.font = Font(
                color="FFFFFF",
                bold=True
            )

        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions

        # Ajustar largura das colunas
        for coluna in ws.columns:
            letra = coluna[0].column_letter

            largura = max(
                len(str(celula.value))
                if celula.value is not None else 0
                for celula in coluna
            )

            ws.column_dimensions[letra].width = min(
                largura + 3,
                60
            )

    return destino
