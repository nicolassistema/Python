import generador
import os
import json
import extractor_paginacion

if __name__ == "__main__":
    API_URL = (
        "https://www.cotodigital.com.ar/sitios/cdigi/categoria/catalogo-almac%C3%A9n/_/N-8pub5z"
        "?Nf=product.endDate%7CGTEQ%201.7718912E12%7C%7Cproduct.startDate%7CLTEQ%201.7718912E12"
        "&Nr=AND(product.sDisp_200:1004,product.language:espa%C3%B1ol,OR(product.siteId:CotoDigital))"
        "&format=json"
    )

    scraper = generador.CotoScraper(api_url=API_URL)
    scraper.generar_categorias(verbose=True)



# ----------------------------
# 1) Cargar categorias.json
# ----------------------------
carpeta = "Coto"
archivo = "categorias.json"
ruta = os.path.join(carpeta, archivo)

if not os.path.exists(ruta):
    raise FileNotFoundError(f"No existe el archivo: {ruta}")

with open(ruta, "r", encoding="utf-8") as f:
    datos = json.load(f)

# Armamos la lista (nombre, url) desde el JSON
categorias = []
for item in datos:
    nombre = item.get("nombre")
    url = item.get("url")
    if nombre and url:
        categorias.append((nombre, url))

# ----------------------------
# 2) Recorrer categorías y paginar
# ----------------------------
for nombre, url_cat in categorias:
    try:
        total_pages, urls_json, urls_html = obtener_paginacion_categoria(url_cat)

        print("\n==============================")
        print("Categoría:", nombre)
        print("URL:", url_cat)
        print("Pages:", total_pages)

        if len(urls_json) >= 2:
            print("JSON page2:", urls_json[1])
        else:
            print("JSON page2: (no hay)")

        if len(urls_html) >= 2:
            print("HTML page2:", urls_html[1])
        else:
            print("HTML page2: (no hay)")

        # Acá podrías iterar urls_json para scrapear productos
        # for u in urls_json:
        #     ...

    except Exception as e:
        print("\n❌ Error en categoría:", nombre)
        print("   ", e)