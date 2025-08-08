import requests
from bs4 import BeautifulSoup
from itertools import zip_longest
import re
import time
import os
import sys # Para codificação UTF-8 na saída
import csv # Para lidar com o formato Nome;Link
# Parte do pandas
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configuração
URL = "https://www.chumpower.com/en/products.html"
PASTA_DADOS = r"C:\Users\Usuario\Zoho WorkDrive (BMG Peças e Serviços)\My Folders\Dados - BMT\Arquivos PC\Trampo\ATIVO\137. Monitoramento da Concorrência\Chunpower"
NOME_ARQUIVO = "produtos_chumpower_anteriores.txt" # Agora conterá Nome;Link
ARQUIVO_PRODUTOS_ANTERIORES = os.path.join(PASTA_DADOS, NOME_ARQUIVO)
ENCODING = 'utf-8'
# Separador para o arquivo Nome;Link
SEPARADOR = ';'
# Configuração do Selenium
chrome_options = Options()


# Scraping
def fazer_scraping():
    produtos_encontrados = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    response = requests.get(URL, headers=headers, timeout=21)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    
    soup = BeautifulSoup(response.text, 'html.parser')
    lista_produtos_div = soup.find('div', class_='pdt-list')
    produtos_html = lista_produtos_div.find_all('a', class_='item fs-16 p-35 p-lg-20 p-sm-15 bg-lightergray')
    
    for produto_tag_a in produtos_html:
        link = produto_tag_a.get('href')
        nome_div = produto_tag_a.find('div', class_='color-sec-color f-900')
        nome = nome_div.get_text(strip=True)
        produtos_encontrados.append({'Item': nome, 'Link': link})
    
    return produtos_encontrados

# Comparação e Exportação
def comparar_e_exportar(produtos_encontrados):
    arquivo_novo = sorted([produto['Item'] for produto in produtos_encontrados])
    
    nomes = set()
    with open(ARQUIVO_PRODUTOS_ANTERIORES, mode='r', encoding=ENCODING, newline='') as f:
        reader = csv.reader(f, delimiter=SEPARADOR)
        for linha in reader:
            nomes.add(linha[0].strip())
    
    arquivo_antigo = list(sorted(nomes))
    tem_diferencas = any(item_antigo != item_novo for item_antigo, item_novo in zip_longest(arquivo_antigo, arquivo_novo, fillvalue="(vazio)"))
    
    if tem_diferencas:
        with open(ARQUIVO_PRODUTOS_ANTERIORES, "w", encoding=ENCODING) as arquivo:
            for produto in produtos_encontrados:
                arquivo.write(f"{produto['Item']}{SEPARADOR}{produto['Link']}\n")
        print(f"Diferenças encontradas. Lista exportada para '{NOME_ARQUIVO}'.")
    else:
        print("Nenhuma diferença encontrada.")




def acessar_links(produtos_encontrados):
	todas_tabelas = []
	links = sorted([produto['Link'] for produto in produtos_encontrados])
	nome = sorted([produto['Item'] for produto in produtos_encontrados])
	# Chama o navegador (Chrome)
	service = Service(ChromeDriverManager().install()) # Instala/gerencia o driver
	driver = webdriver.Chrome(service=service, options=chrome_options)
	for link, nom in zip(links, nome):
		print(f"Acessando {link} com Selenium...")
		driver.get(link)
		time.sleep(5)
		print("Obtendo HTML...")
		html_da_pagina = driver.page_source
		print("Processando HTML com Pandas...")
		lista_tabelas = pd.read_html(html_da_pagina)
		todas_tabelas.extend(lista_tabelas)  # Adicionar a lista consolidada
    
	# Exportação ajustada (única alteração)
	if todas_tabelas:
		with pd.ExcelWriter('tabelas_consolidadas.xlsx') as writer:
			for i, (tabela, nom) in enumerate(zip(todas_tabelas, nome * len(todas_tabelas)), start=1):
				 # Ajusta o nome
				nome_sanitizado = re.sub(r'[\\/*?\[\]:]', '_', str(nom))
				nome_aba = f"{nome_sanitizado}_{i}"[:31]
				tabela.to_excel(writer, sheet_name=nome_aba, index=False)
		print("\nTabelas exportadas")
	else:
		print("\nNenhuma tabela encontrada para exportação (erro)")
    
	print("Fechando...")
	driver.quit()
	return todas_tabelas

# Parte do main
if __name__ == "__main__":
	# Verifica se o arquivo existe, caso contrário cria um fake
	if not os.path.exists(ARQUIVO_PRODUTOS_ANTERIORES):
		with open(ARQUIVO_PRODUTOS_ANTERIORES, 'w', encoding=ENCODING, newline='') as f:
			f.write(f"Produto Fake{SEPARADOR}https://www.exemplo.com/fake\n")
		print(f"Arquivo {NOME_ARQUIVO} não encontrado. Criado um arquivo inicial com dados fake.")
	produtos = fazer_scraping()
	comparar_e_exportar(produtos)
	acessar_links(produtos)
