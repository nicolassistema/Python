import bs4 #permite navegar en el texto html y buscar lo que necesitamos
import requests


resultado = requests.get('https://books.toscrape.com/')

sopa = bs4.BeautifulSoup(resultado.text, 'lxml')

#print(sopa.select('p')[0].get_text())


#columna_lateral = sopa.select('div ol li article div a')

columna_lateral = sopa.select('div ol li h3 a')

for p in columna_lateral:
    print(p.getText())


