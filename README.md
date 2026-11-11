
# Automação de Relatórios Comerciais com Python

Projeto de automação desenvolvido em Python para consolidar
arquivos CSV, tratar dados comerciais, identificar inconsistências
e gerar relatórios gerenciais em Excel.

## Objetivo

Reduzir o trabalho manual de consolidação de dados e
oferecer relatórios comerciais com verificações automáticas
de integridade e consistência financeira.

## Tecnologias

- Python
- Pandas
- OpenPyXL
- Excel

## Funcionalidades

- Leitura e consolidação de múltiplos arquivos CSV
- Identificação de registros duplicados
- Tratamento e padronização de valores de vendas
- Auditoria de inconsistências
- Cálculo de indicadores comerciais
- Geração automática de relatórios Excel
- Validação de estrutura e quantidade de registros
- Conciliação financeira entre os dados e o relatório
- Registro de logs e histórico de execuções
- Tratamento de erros

## Estrutura do projeto

```text
Projeto_B_Automacao_Relatorios/
├── dados_entrada/
│   └── arquivos_mensais/
├── logs/
├── relatorios/
├── src/
│   ├── leitura.py
│   ├── limpeza.py
│   ├── indicadores.py
│   ├── exportacao.py
│   ├── validacao.py
│   └── validacao_relatorio.py
├── config.py
├── main.py
├── preparar_dados.py
├── requirements.txt
└── README.md
```

## Instalação

Requisitos: Python e pip instalados.

Crie um ambiente virtual:

```powershell
py -m venv .venv
```

Instale as dependências:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Como executar

Coloque os arquivos CSV na pasta:

`dados_entrada/arquivos_mensais/`

Execute:

```powershell
.\.venv\Scripts\python.exe main.py
```

## Relatório gerado

O arquivo principal é salvo em:

`relatorios/Relatorio_Consolidado.xlsx`

Ele contém seis abas:

1. Resumo_Geral
2. Resumo_Anual
3. Vendas_Tratadas
4. Inconsistencias
5. Resumo_Categorias
6. Ranking_Produtos

## Validações automáticas

O sistema verifica:

- Quantidade de arquivos e registros processados
- Existência de duplicidades
- Inconsistências nos dados
- Estrutura do relatório Excel
- Quantidade de vendas exportadas
- Correspondência entre o faturamento calculado
  e o faturamento registrado no Excel

Se a validação do relatório falhar, a execução não será
registrada como concluída com sucesso.

## Resultados do projeto

Teste realizado com a base Superstore:

- Arquivos consolidados: 4
- Registros processados: 9.800
- Faturamento validado: R$ 2.261.536,78
- Inconsistências identificadas: 11

Os resultados apresentados correspondem à base de
demonstração utilizada durante o desenvolvimento.

## Próximas melhorias

- Interface simplificada para execução
- Testes automatizados
- Otimização do desempenho
- Suporte a diferentes layouts de arquivos CSV

## Autor

Projeto desenvolvido para demonstração de competências
em Python, automação de processos e análise de dados.

## Demonstração com dados fictícios

Este projeto disponibiliza uma base demonstrativa com 100 registros fictícios de vendas, distribuídos em quatro arquivos CSV referentes aos anos de 2022 a 2025.

A demonstração permite testar a automação sem utilizar informações comerciais reais.

### Executando a demonstração

**1. Instale as dependências:**

```bash
python -m pip install -r requirements.txt
```

**2. Execute a demonstração:**

```bash
python executar_demo.py
```

O programa realizará automaticamente:

- Leitura e consolidação dos arquivos CSV.
- Tratamento dos valores de vendas.
- Identificação de inconsistências.
- Cálculo dos indicadores comerciais.
- Exportação do relatório Excel.
- Validação da estrutura e do faturamento.

### Resultado esperado

| Indicador | Resultado |
|---|---|
| Arquivos processados | 4 |
| Registros | 100 |
| Faturamento | R$ 76.487,10 |
| Inconsistências | 0 |
| Abas do relatório | 6 |

O arquivo será gerado em:

`relatorios_demo/Relatorio_Demonstrativo.xlsx`

### Gerando novamente os dados fictícios

Para recriar os arquivos CSV demonstrativos:

```bash
python gerar_dados_demo.py
```

Os arquivos serão gerados na pasta `dados_demo/`.

**Observação:** os dados são inteiramente fictícios e utilizados exclusivamente para demonstração das funcionalidades da automação.