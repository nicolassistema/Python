import bs4 #permite navegar en el texto html y buscar lo que necesitamos
import requests



url_base = 'https://books.toscrape.com/catalogue/page-{}.html'

# print(url_base.format('15'))

#con esto obtengo las urls paginadas
# for num in range(1,11):
#     print(url_base.format(num))



resultado = requests.get(url_base.format('1'))
sopa = bs4.BeautifulSoup(resultado.text, 'lxml')
libros = sopa.select('.product_pod')

ejemplo = libros[0].select('a')[1]['title']
print(ejemplo)



