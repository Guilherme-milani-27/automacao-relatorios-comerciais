
# src/status.py

import json
from datetime import datetime
from pathlib import Path


def atualizar_status(
    pasta_projeto,
    id_execucao,
    status,
    mensagem,
    relatorio=None
):
    pasta_status = Path(pasta_projeto) / "logs"
    pasta_status.mkdir(parents=True, exist_ok=True)

    destino = pasta_status / "ultima_execucao.json"

    dados = {
        "id_execucao": id_execucao,
        "data_hora": datetime.now().isoformat(
            timespec="seconds"
        ),
        "status": status,
        "mensagem": mensagem,
        "relatorio": str(relatorio) if relatorio else None
    }

    with open(destino, "w", encoding="utf-8") as arquivo:
        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

    return destino
