import bs4
import requests

url_base = "https://books.toscrape.com/catalogue/page-{}.html"
titulos_rating_alto = []

headers = {"User-Agent": "Mozilla/5.0"}

with requests.Session() as s:
    s.headers.update(headers)

    for pagina in range(1, 51):
        url_pagina = url_base.format(pagina)

        # timeout evita que se “cuelgue” una página
        resultado = s.get(url_pagina, timeout=(5, 15))

        # si falla una página, cortamos y listo
        if resultado.status_code != 200:
            print(f"Página {pagina} devolvió {resultado.status_code}. Corto.")
            break

        sopa = bs4.BeautifulSoup(resultado.text, "lxml")

        libros = sopa.select("article.product_pod")

        for libro in libros:
            # select_one es más rápido que select + len
            if libro.select_one(".star-rating.Four") or libro.select_one(".star-rating.Five"):
                # más directo que libro.select('a')[1]
                titulo_libro = libro.select_one("h3 a")["title"]
                titulos_rating_alto.append(titulo_libro)

print(f"Encontrados: {len(titulos_rating_alto)}")
for t in titulos_rating_alto:
    print(t)