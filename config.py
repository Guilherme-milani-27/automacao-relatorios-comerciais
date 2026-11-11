
from pathlib import Path

# Diretório principal do projeto
BASE_DIR = Path(__file__).resolve().parent

# Diretórios utilizados pela automação
PASTA_ENTRADA = BASE_DIR / "dados_entrada" / "arquivos_mensais"
PASTA_RELATORIOS = BASE_DIR / "relatorios"
PASTA_LOGS = BASE_DIR / "logs"

# Arquivos de saída
ARQUIVO_RELATORIO = (
    PASTA_RELATORIOS / "Relatorio_Consolidado.xlsx"
)

ARQUIVO_HISTORICO = (
    PASTA_LOGS / "historico_execucoes.csv"
)

ARQUIVO_STATUS = (
    PASTA_LOGS / "ultima_execucao.json"
)

# Criar diretórios de saída, caso não existam
PASTA_RELATORIOS.mkdir(parents=True, exist_ok=True)
PASTA_LOGS.mkdir(parents=True, exist_ok=True)
