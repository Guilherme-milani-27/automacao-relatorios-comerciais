
from pathlib import Path
import sys

from src.leitura import consolidar_arquivos
from src.limpeza import converter_vendas, identificar_inconsistencias
from src.indicadores import (
    calcular_indicadores,
    calcular_indicadores_produtos,
)
from src.exportacao import exportar_relatorio
from src.validacao_relatorio import validar_relatorio


BASE_DIR = Path(__file__).resolve().parent
PASTA_DEMO = BASE_DIR / "dados_demo"
ARQUIVO_DEMO = BASE_DIR / "relatorios_demo" / "Relatorio_Demonstrativo.xlsx"


def main():
    try:
        print("\n=== EXECUCAO DEMONSTRATIVA ===")

        # 1. Ler e consolidar os CSVs ficticios
        df = consolidar_arquivos(PASTA_DEMO)

        # 2. Tratar os valores de vendas
        df = converter_vendas(df)

        # 3. Identificar inconsistencias
        inconsistencias = identificar_inconsistencias(df)

        # 4. Calcular indicadores
        resumo_geral, resumo_anual = calcular_indicadores(df)

        resumo_categorias, ranking_produtos = (
            calcular_indicadores_produtos(df)
        )

        # 5. Gerar Excel demonstrativo
        destino = exportar_relatorio(
            df_vendas=df,
            df_inconsistencias=inconsistencias,
            resumo_geral=resumo_geral,
            resumo_anual=resumo_anual,
            resumo_categorias=resumo_categorias,
            ranking_produtos=ranking_produtos,
            destino=ARQUIVO_DEMO,
        )

        # 6. Validar estrutura, registros e faturamento
        validar_relatorio(
            caminho=destino,
            registros_esperados=len(df),
            faturamento_esperado=df["Sales_Tratado"].sum(),
        )

        print("\n=== DEMONSTRACAO CONCLUIDA ===")
        print("Registros:", len(df))
        print("Inconsistencias:", len(inconsistencias))
        print(
            "Faturamento: R$",
            f"{df['Sales_Tratado'].sum():.2f}",
        )
        print("Relatorio:", destino)

        return 0

    except Exception as erro:
        print(f"\nERRO NA DEMONSTRACAO: {erro}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
