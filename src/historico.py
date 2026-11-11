
# src/historico.py

import csv
from pathlib import Path
from datetime import datetime


def registrar_execucao(
    pasta_projeto,
    id_execucao,
    status,
    tempo_segundos,
    arquivos=0,
    registros=0,
    inconsistencias=0,
    mensagem=""
):

    pasta_historico = Path(pasta_projeto) / "logs"
    pasta_historico.mkdir(parents=True, exist_ok=True)

    arquivo = pasta_historico / "historico_execucoes.csv"

    colunas = [
        "Data_Hora",
        "ID_Execucao",
        "Status",
        "Tempo_Segundos",
        "Arquivos",
        "Registros",
        "Inconsistencias",
        "Mensagem"
    ]

    registro = {
        "Data_Hora": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "ID_Execucao": id_execucao,
        "Status": status,
        "Tempo_Segundos": round(tempo_segundos, 2),
        "Arquivos": arquivos,
        "Registros": registros,
        "Inconsistencias": inconsistencias,
        "Mensagem": mensagem
    }

    novo_arquivo = (
        not arquivo.exists()
        or arquivo.stat().st_size == 0
    )

    with open(
        arquivo,
        mode="a",
        newline="",
        encoding="utf-8-sig"
    ) as f:

        escritor = csv.DictWriter(
            f,
            fieldnames=colunas,
            delimiter=";"
        )

        if novo_arquivo:
            escritor.writeheader()

        escritor.writerow(registro)

    return arquivo
