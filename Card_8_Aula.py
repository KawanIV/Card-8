# importar a biblioteca
from bs4 import BeautifulSoup
import requests
import time

print('Coloque algum requisito que você não tem familiaridade')
filtro_requisitos = input('>')
print(f'Removido {filtro_requisitos}')

def procura_trabalho():
	html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation=').text
	soup = BeautifulSoup(html_text, 'lxml')
	jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')
	for index, job in enumerate(jobs):
		locais = job.find('li', class_ = 'srp-zindex location-tru').text
		if 'Ahmedabad' in locais:
			empresa = job.find('h3', class_ = 'joblist-comp-name').text.replace(' ','')
			requisitos = (job.find('div', class_='more-skills-sections')).get_text(' ',strip=True)
			informacoes = (job.find('a', class_='posoverlay_srp')).get('href')
			if filtro_requisitos not in requisitos:
				with open(f'arquivos/{index}.txt','w') as f:	
					f.write(f"Empresa: {empresa.strip()} \n")
					f.write(f"Requisitos: {requisitos.strip()} \n")
					f.write(f"Informações: {informacoes} \n")
				print(f'Arquivo salvo: {index}')

if __name__ == '__main__':
	while True:
		procura_trabalho()
		tempo_espera = 10
		print(f'Esperando {tempo_espera} segundos...')
		time.sleep(tempo_espera)
