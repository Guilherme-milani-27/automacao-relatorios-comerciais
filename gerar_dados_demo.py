
from pathlib import Path
import random
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
PASTA_DEMO = BASE_DIR / "dados_demo"

random.seed(42)

produtos = [
    ("P001", "Caderno Executivo", "Papelaria"),
    ("P002", "Caneta Premium", "Papelaria"),
    ("P003", "Mouse Sem Fio", "Tecnologia"),
    ("P004", "Teclado USB", "Tecnologia"),
    ("P005", "Cadeira de Escritorio", "Moveis"),
    ("P006", "Mesa Compacta", "Moveis"),
]

def gerar_dados():
    PASTA_DEMO.mkdir(parents=True, exist_ok=True)

    contador = 1

    for ano in range(2022, 2026):
        registros = []

        for i in range(25):
            produto_id, produto_nome, categoria = random.choice(produtos)

            data = pd.Timestamp(
                year=ano,
                month=random.randint(1, 12),
                day=random.randint(1, 28)
            )

            registros.append({
                "Row ID": contador,
                "Order ID": f"PED-{ano}-{i + 1:03d}",
                "Order Date": data.strftime("%d/%m/%Y"),
                "Product ID": produto_id,
                "Product Name": produto_nome,
                "Category": categoria,
                "Sales": round(random.uniform(15, 1500), 2),
                "Postal Code": f"{random.randint(10000, 99999):05d}"
            })

            contador += 1

        df = pd.DataFrame(registros)

        caminho = PASTA_DEMO / f"vendas_{ano}.csv"

        df.to_csv(
            caminho,
            index=False,
            encoding="utf-8-sig"
        )

        print(f"Gerado: {caminho.name} - {len(df)} registros")

    print("\nBase demonstrativa criada com sucesso!")
    print("Total: 100 registros ficticios")


if __name__ == "__main__":
    gerar_dados()
