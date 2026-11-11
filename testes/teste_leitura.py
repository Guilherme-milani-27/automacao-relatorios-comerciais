
from pathlib import Path

pasta_projeto = Path(__file__).resolve().parent

arquivo_teste = (
    pasta_projeto
    / "dados_entrada"
    / "arquivos_mensais"
    / "vendas_teste_codificacao.csv"
)

# Bytes inválidos para leitura em UTF-8
arquivo_teste.write_bytes(
    b"\xff\xfe\xfa\xfb"
)

print("Arquivo de teste criado:")
print(arquivo_teste)
