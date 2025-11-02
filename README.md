# Extrator de Dados do IBGE Cidades 

## Descrição do Projeto

Este projeto é um scraper de dados robusto desenvolvido em Python utilizando a biblioteca Playwright. O objetivo é simular um processo de Automação de Processos para extrair informações socioeconômicas e demográficas de todas as 27 Unidades da Federação diretamente do site oficial do IBGE Cidades (https://cidades.ibge.gov.br/).

## Requisitos e Tecnologias

| Categoria | Componente | Função no Projeto |
| :--- | :--- | :--- |
| **Linguagem** | Python | Linguagem principal do desenvolvimento. |
| **Automação** | Playwright | Motor essencial para navegação, renderização e execução do JavaScript (JS). |
| **Limpeza/Parsing** | `re` (Regex) | Utilizado para a limpeza e extração de valores numéricos de alta precisão do texto bruto (HTML). |
| **Exportação** | `csv` (Módulo Nativo) | Utilizado para gerar o arquivo final no formato tabular ("planilha"), sem dependências externas. |

## Dados Coletados

O script foi desenhado para extrair os principais indicadores das 6 categorias a nível estadual para todas as 27 UFs:

| Categoria Principal | Dado Específico Extraído |
| :--- | :--- |
| **População** | População no último censo |
| **Território** | Número de municípios e Área total (km²) |
| **Trabalho e Rendimento** | Rendimento nominal mensal domiciliar |
| **Educação** | IDEB – Anos Iniciais do ensino fundamental |
| **Economia** | Índice de Desenvolvimento Humano (IDH) |
| **Meio Ambiente** | Esgotamento sanitário por rede geral (%) |

## Como Executar

### 1. Configuração do Ambiente

Crie e ative um ambiente virtual para isolar as dependências do projeto:

```bash
python -m venv venv
```

```bash
source venv/bin/activate
```

```bash
pip install playwright
```

```bash
playwright install
```

### 2. Execução do Script

```bash
python src/main.py
```

### 3. Resultado Esperado

O script fará a extração de dados para os 27 estados. Ao finalizar, o resultado será salvo no seguinte arquivo:

Arquivo de Saída: `dados_ibge_estados.csv`