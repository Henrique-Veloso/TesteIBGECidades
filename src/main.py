import csv
from playwright.sync_api import sync_playwright
import re

LISTA_ESTADOS = [] 
DADOS_RESULTADO = []
MAPA_UFS = {
    "AC": "acre", "AL": "alagoas", "AP": "amapa", "AM": "amazonas", "BA": "bahia", 
    "CE": "ceara", "DF": "distrito-federal", "ES": "espirito-santo", "GO": "goias", 
    "MA": "maranhao", "MT": "mato-grosso", "MS": "mato-grosso-do-sul", "MG": "minas-gerais", 
    "PA": "para", "PB": "paraiba", "PR": "parana", "PE": "pernambuco", "PI": "piaui", 
    "RJ": "rio-de-janeiro", "RN": "rio-grande-do-norte", "RS": "rio-grande-do-sul", 
    "RO": "rondonia", "RR": "roraima", "SC": "santa-catarina", "SP": "sao-paulo", 
    "SE": "sergipe", "TO": "tocantins"
}

def obter_valor_por_rotulo(pagina, rotulo_texto, timeout_ms=15000):
    try:
        localizador_rotulo = pagina.locator(f'text="{rotulo_texto}"').first
        for indice in range(1, 4):
            localizador_container_valor = localizador_rotulo.locator(f'xpath=./following-sibling::div[{indice}]')
            valor_bruto = localizador_container_valor.inner_text(timeout=5000).strip()     
            if valor_bruto and 'N/A' not in valor_bruto and len(valor_bruto) > 1 and 'Comparando' not in valor_bruto:
                valor_limpo = re.search(r'([\d\.\,]+)', valor_bruto.replace('R$', '')).group(1).strip()
                return valor_limpo      
    except Exception as e:
        pass 
    return 'N/A'

def extrair_urls_estados():
    global LISTA_ESTADOS 
    print("Gerando URLs dos 27 estados")
    for sigla_uf, nome_estado in MAPA_UFS.items():
        url_completa = f"https://cidades.ibge.gov.br/brasil/{sigla_uf.lower()}/panorama"
        LISTA_ESTADOS.append((sigla_uf, url_completa))
    LISTA_ESTADOS = list(set(LISTA_ESTADOS))
    print(f"Estados coletados: {len(LISTA_ESTADOS)}")

def extrair_valor(texto_bruto, expressao):
    try:
        match = re.search(expressao, texto_bruto, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    except Exception:
        pass
    return 'N/A'

def extrair_dados_estado(sigla_uf, url_estado):
    global DADOS_RESULTADO
    print(f"Acessando {sigla_uf}")
    dados_atuais = {'UF': sigla_uf}
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)
        pagina = navegador.new_page()
        try:
            pagina.goto(url_estado, timeout=120000)
            print("Renderizando site")
            pagina.wait_for_timeout(15000) 
            conteudo_html = pagina.content()
            texto_painel = re.sub('<[^>]+>', ' ', conteudo_html).replace('\n', ' ')
                    
            populacao_regex = r'População no último censo\s*\[\d{4}\]\s*([\d\.\,]+)\s*pessoas'
            dados_atuais['População no último censo'] = extrair_valor(texto_painel, populacao_regex)
            dados_atuais['Território - Número de municípios'] = extrair_valor(texto_painel, r'Número de municípios\s*\[-\]\s*([\d\.\,]+)\s*municípios')
            renda_regex = r'Rendimento nominal mensal domiciliar per capita\s*\[\d{4}\]\s*([\d\.\,]+)'
            renda_valor = extrair_valor(texto_painel, renda_regex)
            dados_atuais['Trabalho e Rendimento - Renda Per Capita'] = "R$ " + renda_valor if renda_valor != 'N/A' else 'N/A'
            ideb_regex = r'IDEB – Anos iniciais do ensino fundamental \(Rede pública\)\s*\[\d{4}\]\s*([\d\.\,]+)'
            dados_atuais['Educação - IDEB Anos Iniciais'] = extrair_valor(texto_painel, ideb_regex)           
            idh_regex = r'Índice de Desenvolvimento Humano \(IDH\)\s*\[\d{4}\]\s*([\d\.\,]+)'
            dados_atuais['Economia - IDH'] = extrair_valor(texto_painel, idh_regex)          
            esgoto_regex = r'Esgotamento sanitário por rede geral.*?([\d\.\,]+)\s*%'
            dados_atuais['Meio Ambiente - Esgotamento Sanitário (%)'] = extrair_valor(texto_painel, esgoto_regex)
            territorio_area_regex = r'Área da unidade territorial\s*\[\d{4}\]\s*([\d\.\,]+)\s*km²'
            dados_atuais['Território - Área (km²)'] = extrair_valor(texto_painel, territorio_area_regex)

            dados_atuais['Status'] = 'SUCESSO'
            DADOS_RESULTADO.append(dados_atuais)

        except Exception as e:
            dados_atuais['Status'] = f'FALHA: {e}'
            DADOS_RESULTADO.append(dados_atuais)
        navegador.close()

def main():
    extrair_urls_estados()
    for sigla_uf, url_estado in LISTA_ESTADOS: 
        extrair_dados_estado(sigla_uf, url_estado)
    if DADOS_RESULTADO:
        nomes_campos = [
            'UF', 
            'População no último censo', 
            'Território - Número de municípios', 
            'Território - Área (km²)', 
            'Trabalho e Rendimento - Renda Per Capita',
            'Educação - IDEB Anos Iniciais',
            'Economia - IDH',
            'Meio Ambiente - Esgotamento Sanitário (%)',
            'Status'
        ]
        try:
            with open('dados_ibge_estados.csv', 'w', newline='', encoding='utf-8') as arquivo_csv:
                escritor = csv.DictWriter(arquivo_csv, fieldnames=nomes_campos, extrasaction='ignore')
                escritor.writeheader()
                escritor.writerows(DADOS_RESULTADO)
            print("\nDados salvos em 'dados_ibge_estados.csv'.")
        except Exception as e:
            print(f"\nErro: {e}")

if __name__ == "__main__":
    main()