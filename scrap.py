# importar a biblioteca
from bs4 import BeautifulSoup
# Abrir arquivo html local, primeiro definimos o caminho e o nome do arquivo,  o segundo é o metodo
# que vc vai aplicar nesse arquivo html (ler, escrever , os dois) para apenas ler use o comando 'r'.
with open('Curso.html', 'r') as html_file:
	content = html_file.read()# o read lê o html
# Agora podemos usar o beautifulsoup para ler o html e trabalhar com um objeto python
# ao invés de usar o objeto html.
	soup = BeautifulSoup(content, 'lxml') # Primeiro é definido a variavel que ele vai ler e o método
	card_cursos = soup.find_all('div',class_='card')
	for curso in card_cursos:
		nome_curso = curso.h5.text
		preço_curso = curso.a.text.split()[-1]
		print(nome_curso)
		print(preço_curso)
