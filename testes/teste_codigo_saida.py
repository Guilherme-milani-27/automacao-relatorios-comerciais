
import sys
from unittest.mock import patch

import main


def simular_falha(*args, **kwargs):
    raise RuntimeError("Falha simulada para teste")


with patch(
    "main.consolidar_arquivos",
    side_effect=simular_falha
):
    codigo_saida = main.main()

print("\n=== RESULTADO DO TESTE ===")
print("Código de saída:", codigo_saida)

sys.exit(codigo_saida)
