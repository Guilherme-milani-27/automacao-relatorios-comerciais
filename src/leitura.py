
from pathlib import Path
import pandas as pd
from src.validacao import ErroValidacao


COLUNAS_OBRIGATORIAS = [
    "Row ID",
    "Order ID",
    "Order Date",
    "Product ID",
    "Product Name",
    "Category",
    "Sales"
]


def consolidar_arquivos(pasta_entrada):

    pasta_entrada = Path(pasta_entrada)

    arquivos = sorted(
        pasta_entrada.glob("vendas_*.csv")
    )

    if not arquivos:
        raise FileNotFoundError(
            "Nenhum arquivo de vendas encontrado."
        )


    lista_dados = []

    for arquivo in arquivos:

        print(f"\nValidando: {arquivo.name}")

        dados = pd.read_csv(
            arquivo,
            encoding="utf-8-sig",
            dtype={"Postal Code": "string"}
        )

        # Verificar colunas obrigatórias
        colunas_ausentes = [
            coluna
            for coluna in COLUNAS_OBRIGATORIAS
            if coluna not in dados.columns
        ]

        if colunas_ausentes:

            detalhes = [
                {
                    "Arquivo": arquivo.name,
                    "Tipo_Erro": "Coluna ausente",
                    "Detalhes": f"Coluna {coluna} não encontrada"
                }
                for coluna in colunas_ausentes
            ]

            raise ErroValidacao(
                f"Colunas obrigatórias ausentes em {arquivo.name}",
                detalhes
            )

        # Registrar origem e adicionar à lista
        dados["Arquivo_Origem"] = arquivo.name
        lista_dados.append(dados)

        print(
            f"Arquivo validado: {len(dados)} registros"
        )

    # Consolidar depois de ler TODOS os arquivos
    df_consolidado = pd.concat(
        lista_dados,
        ignore_index=True
    )

    
    print("\n=== CONTROLE DE LEITURA ===")
    print("Arquivos encontrados:", len(arquivos))
    print("DataFrames carregados:", len(lista_dados))

    if len(lista_dados) != len(arquivos):
        raise RuntimeError(
            "Nem todos os arquivos foram adicionados à consolidação."
        )

    # Verificar IDs duplicados
    duplicados = df_consolidado[
        df_consolidado["Row ID"].duplicated(
            keep=False
        )
    ]

    
    if not duplicados.empty:

        detalhes = []

        for _, linha in duplicados.iterrows():

            detalhes.append({
                "Arquivo": linha["Arquivo_Origem"],
                "Tipo_Erro": "Registro duplicado",
                "Detalhes": f"Row ID {linha['Row ID']} duplicado"
            })

        raise ErroValidacao(
            "Foram encontrados registros duplicados.",
            detalhes
        )


    print("\n=== CONSOLIDAÇÃO VALIDADA ===")
    print("Arquivos:", len(arquivos))
    print("Registros:", len(df_consolidado))
    print("Duplicidades:", len(duplicados))

    return df_consolidado
