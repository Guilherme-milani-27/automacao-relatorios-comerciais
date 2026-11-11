
# src/logs.py

import logging
from pathlib import Path
from datetime import datetime


def configurar_logger(pasta_projeto):

    pasta_logs = Path(pasta_projeto) / "logs"
    pasta_logs.mkdir(parents=True, exist_ok=True)

    data_atual = datetime.now().strftime("%Y-%m-%d")

    arquivo_log = (
        pasta_logs / f"automacao_{data_atual}.log"
    )

    logger = logging.getLogger("ProjetoB")
    logger.setLevel(logging.INFO)

    # Evitar handlers duplicados
    if logger.handlers:
        return logger

    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Registrar mensagens em arquivo
    handler_arquivo = logging.FileHandler(
        arquivo_log,
        encoding="utf-8"
    )
    handler_arquivo.setFormatter(formato)

    # Exibir mensagens no terminal
    handler_terminal = logging.StreamHandler()
    handler_terminal.setFormatter(formato)

    logger.addHandler(handler_arquivo)
    logger.addHandler(handler_terminal)

    return logger
