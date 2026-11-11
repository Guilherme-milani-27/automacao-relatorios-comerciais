
# main.py


from src.leitura import consolidar_arquivos
from src.limpeza import (
    converter_vendas,
    identificar_inconsistencias
)
from src.indicadores import (
    calcular_indicadores,
    calcular_indicadores_produtos
)
from src.exportacao import exportar_relatorio

from src.validacao import ErroValidacao
from src.relatorio_erros import gerar_relatorio_erros

from src.logs import configurar_logger

from time import perf_counter
from uuid import uuid4

from src.historico import registrar_execucao

from src.status import atualizar_status

from config import (
    BASE_DIR,
    PASTA_ENTRADA,
    PASTA_RELATORIOS,
    ARQUIVO_RELATORIO
)


from src.validacao_relatorio import validar_relatorio



def registrar_erro_inesperado(
    logger,
    erro,
    id_execucao,
    inicio,
    pasta_projeto
):
    tempo_total = perf_counter() - inicio

    logger.exception(
        "Execução %s falhou após %.2f segundos: %s",
        id_execucao,
        tempo_total,
        erro
    )

    salvar_status(
        pasta_projeto=pasta_projeto,
        id_execucao=id_execucao,
        inicio=inicio,
        status="ERRO_INESPERADO",
        mensagem=str(erro)
    )

    atualizar_status(
        pasta_projeto,
        id_execucao,
        "ERRO_INESPERADO",
        str(erro)
    )

    print("\n=== FALHA NA AUTOMAÇÃO ===")
    print("Ocorreu um erro inesperado.")
    print("Consulte o arquivo de log para detalhes.")



def salvar_status(
    pasta_projeto,
    id_execucao,
    inicio,
    status,
    arquivos=0,
    registros=0,
    inconsistencias=0,
    mensagem=""
):
    tempo_total = perf_counter() - inicio

    registrar_execucao(
        pasta_projeto=pasta_projeto,
        id_execucao=id_execucao,
        status=status,
        tempo_segundos=tempo_total,
        arquivos=arquivos,
        registros=registros,
        inconsistencias=inconsistencias,
        mensagem=mensagem
    )


    
def main():

    inicio = perf_counter()
    id_execucao = uuid4().hex[:8]

    # 1. Definir caminhos
    pasta_projeto = BASE_DIR

    logger = configurar_logger(pasta_projeto)

    logger.info(
        "Iniciando execução %s",
        id_execucao
    )

    atualizar_status(
        pasta_projeto,
        id_execucao,
        "EM_EXECUCAO",
        "Processamento iniciado"
    )

    pasta_entrada = PASTA_ENTRADA

    saida = ARQUIVO_RELATORIO

    # 2. Consolidar arquivos
    logger.info("Iniciando leitura e consolidação dos arquivos")
    print("\n[1/5] Consolidando arquivos...")
    
    try:
        df = consolidar_arquivos(pasta_entrada)
        logger.info(
            "Consolidação concluída: %s arquivos e %s registros",
            df["Arquivo_Origem"].nunique(),
            len(df)
        )
        

    except ErroValidacao as erro:

        destino_erros = PASTA_RELATORIOS / "Relatorio_Erros.xlsx"

        gerar_relatorio_erros(
            erro.detalhes,
            destino_erros
        )

        logger.error(
            "Falha de validação: %s | Relatório: %s",
            erro,
            destino_erros
        )

        print("\n=== ERRO DE VALIDAÇÃO ===")
        print(erro)
        print("Relatório de erros:", destino_erros)
        print("Processamento interrompido.")

        
        tempo_total = perf_counter() - inicio

        logger.warning(
            "Execução %s interrompida após %.2f segundos",
            id_execucao,
            tempo_total
        )

        
        salvar_status(
            pasta_projeto=pasta_projeto,
            id_execucao=id_execucao,
            inicio=inicio,
            status="ERRO_VALIDACAO",
            mensagem=str(erro)
        )

        atualizar_status(
            pasta_projeto,
            id_execucao,
            "ERRO_VALIDACAO",
            str(erro)
        )

        return 1

    
    except Exception as erro:

        registrar_erro_inesperado(
            logger,
            erro,
            id_execucao,
            inicio,
            pasta_projeto
        )

        return 1



    
    # 3. Tratar, auditar e calcular indicadores
    try:
        print("\n[2/5] Tratando vendas...")
        df_limpo = converter_vendas(df)

        print("\n[3/5] Identificando inconsistências...")
        inconsistencias = identificar_inconsistencias(df)

        logger.info(
            "Auditoria concluída: %s inconsistências",
            len(inconsistencias)
        )

        print("\n[4/5] Calculando indicadores...")

        resumo_geral, resumo_anual = calcular_indicadores(
            df_limpo
        )

        resumo_categorias, ranking_produtos = (
            calcular_indicadores_produtos(df_limpo)
        )

    except Exception as erro:
        registrar_erro_inesperado(
            logger,
            erro,
            id_execucao,
            inicio,
            pasta_projeto
        )
        return 1


    
    # 5. Exportar e validar relatório
    print("\n[5/5] Gerando Excel...")

    try:
        exportar_relatorio(
            df_vendas=df_limpo,
            df_inconsistencias=inconsistencias,
            resumo_geral=resumo_geral,
            resumo_anual=resumo_anual,
            resumo_categorias=resumo_categorias,
            ranking_produtos=ranking_produtos,
            destino=saida
        )

        logger.info(
            "Iniciando validação do relatório Excel"
        )

        
        validar_relatorio(
            caminho=saida,
            registros_esperados=len(df_limpo),
            faturamento_esperado=df_limpo["Sales_Tratado"].sum()
        )


        logger.info(
            "Relatório Excel validado com sucesso"
        )

    except Exception as erro:
        registrar_erro_inesperado(
            logger,
            erro,
            id_execucao,
            inicio,
            pasta_projeto
        )
        return 1

    logger.info(
        "Relatório comercial gerado: %s",
        saida
    )

    
    salvar_status(
        pasta_projeto=pasta_projeto,
        id_execucao=id_execucao,
        inicio=inicio,
        status="SUCESSO",
        arquivos=df["Arquivo_Origem"].nunique(),
        registros=len(df),
        inconsistencias=len(inconsistencias),
        mensagem="Relatório comercial gerado"
    )

    atualizar_status(
        pasta_projeto,
        id_execucao,
        "SUCESSO",
        "Relatório comercial gerado",
        relatorio=saida
    )

    logger.info("Automação finalizada com sucesso")

    print("\n=== AUTOMAÇÃO CONCLUÍDA ===")
    print(
    "Arquivos consolidados:",
    df["Arquivo_Origem"].nunique()
    )
    print("Registros processados:", len(df))
    print("Inconsistências:", len(inconsistencias))
    print("Relatório:", saida)

    
    tempo_total = perf_counter() - inicio

    logger.info(
        "Execução %s finalizada em %.2f segundos",
        id_execucao,
        tempo_total
    )

    print(
        f"Tempo de execução: {tempo_total:.2f} segundos"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())