from pathlib import Path
from openpyxl import load_workbook
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


ABAS_ESPERADAS = [
    "Resumo_Geral",
    "Resumo_Anual",
    "Vendas_Tratadas",
    "Inconsistencias",
    "Resumo_Categorias",
    "Ranking_Produtos"
]


def validar_relatorio(
    caminho,
    registros_esperados,
    faturamento_esperado=None
):
    caminho = Path(caminho)

    if not caminho.is_file():
        raise FileNotFoundError(
            f"Relatório não encontrado: {caminho}"
        )

    wb = load_workbook(
        caminho,
        read_only=True,
        data_only=True
    )

    try:
        abas_encontradas = wb.sheetnames

        abas_faltantes = [
            aba for aba in ABAS_ESPERADAS
            if aba not in abas_encontradas
        ]

        if abas_faltantes:
            raise ValueError(
                f"Abas ausentes: {abas_faltantes}"
            )

        # Validar se as abas possuem dados
        for nome_aba in ABAS_ESPERADAS:
            ws = wb[nome_aba]

            # A aba Inconsistencias pode estar vazia,
            # contendo apenas o cabeçalho
            minimo_linhas = (
                1 if nome_aba == "Inconsistencias"
                else 2
            )

            if ws.max_row < minimo_linhas:
                raise ValueError(
                    f"A aba '{nome_aba}' não possui "
                    "a quantidade mínima de linhas."
                )

        # Conferir quantidade de vendas
        ws_vendas = wb["Vendas_Tratadas"]
        registros = ws_vendas.max_row - 1

        
        if registros != registros_esperados:
            raise ValueError(
                f"Quantidade de registros divergente. "
                f"Esperado: {registros_esperados} | "
                f"Encontrado: {registros}"
            )

        
        # Validar faturamento da aba Vendas_Tratadas
        if faturamento_esperado is not None:

            cabecalho = [
                celula.value
                for celula in ws_vendas[1]
            ]

            if "Sales_Tratado" not in cabecalho:
                raise ValueError(
                    "Coluna Sales_Tratado não encontrada "
                    "na aba Vendas_Tratadas."
                )

            indice_vendas = cabecalho.index("Sales_Tratado")

            total_excel = Decimal("0")

            for linha in ws_vendas.iter_rows(
                min_row=2,
                values_only=True
            ):
                valor = linha[indice_vendas]

                if valor is not None:
                    try:
                        total_excel += Decimal(str(valor))
                    except InvalidOperation:
                        raise ValueError(
                            f"Valor de venda inválido: {valor}"
                        )

            # Padronizar os totais para duas casas decimais
            total_excel = total_excel.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )

            total_python = Decimal(
                str(faturamento_esperado)
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )

            diferenca = abs(total_excel - total_python)

            if diferenca != Decimal("0.00"):
                raise ValueError(
                    "Divergência financeira detectada. "
                    f"Python: {total_python:.2f} | "
                    f"Excel: {total_excel:.2f} | "
                    f"Diferença: {diferenca:.2f}"
                )


            print(
                f"Faturamento validado: "
                f"R$ {total_excel:,.2f}"
            )

        print("\n=== VALIDAÇÃO DO RELATÓRIO ===")
        print("Arquivo:", caminho.name)
        print("Abas verificadas:", len(ABAS_ESPERADAS))
        print("Registros de vendas:", registros)
        print("Estrutura validada com sucesso!")

    finally:
        wb.close()

