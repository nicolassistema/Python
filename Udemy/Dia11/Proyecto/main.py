import generador
import os
import json
from extractor_paginacion import CotoPaginador
from logger_config import configurar_logger
from producto_extractor import CotoProductoExtractor

# 🔥 Topeador (None = sin límite)
LIMITE_CATEGORIAS = 3   # cambiar a None para procesar todas


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
    # Configuración de logging
    # ----------------------------
    log = configurar_logger("log_coto")

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

    categorias = []
    for item in datos:
        nombre = item.get("nombre")
        url = item.get("url")
        if nombre and url:
            categorias.append((nombre, url))

    # 🔥 Aplicar tope
    if LIMITE_CATEGORIAS is not None:
        categorias = categorias[:LIMITE_CATEGORIAS]

    # ----------------------------
    # 2) Recorrer categorías y generar paginación
    # ----------------------------
    paginador = CotoPaginador()
    salida_final = []

    for index, (nombre, url_cat) in enumerate(categorias, start=1):
        try:
            log.info("***************************************************")
            log.info("Procesando %s/%s -> %s", index, len(categorias), nombre)

            total_pages, urls_html = paginador.obtener_paginacion_categoria(
                url_cat,
                devolver_html_friendly=True
            )

            if total_pages and total_pages > 0:
                salida_final.append({
                    "categoria": nombre,
                    "url_categoria": url_cat,
                    "total_pages": total_pages,
                    "urls_paginadas_html": urls_html
                })
                log.info("✅ %s: %s páginas", nombre, total_pages)
            else:
                log.info("ℹ️ %s: no tiene páginas (0)", nombre)

        except Exception as e:
            log.error("❌ Error en categoría: %s", nombre)
            log.error("Detalle: %s", e)

            salida_final.append({
                "categoria": nombre,
                "url_categoria": url_cat,
                "error": str(e)
            })

    # ----------------------------
    # 3) Guardar JSON único final (paginación)
    # ----------------------------
    ruta_out = os.path.join("Coto", "categorias_paginadas.json")
    with open(ruta_out, "w", encoding="utf-8") as f:
        json.dump(salida_final, f, ensure_ascii=False, indent=2)

    # ----------------------------
    # 4) Eliminar categorias.json
    # ----------------------------
    try:
        if os.path.exists(ruta):
            os.remove(ruta)
            log.info("🗑 Archivo eliminado: %s ✔", ruta)
    except Exception as e:
        log.error("❌ No se pudo eliminar categorias.json: %s", e)

    log.info("📦 JSON final generado en: %s", ruta_out)

    # =========================================================
    # 5) Cargar categorias_paginadas.json y armar lista resumida
    # =========================================================
    lista_categorias_paginas = []

    try:
        with open(ruta_out, "r", encoding="utf-8") as f:
            data_paginadas = json.load(f)

        for item in data_paginadas:
            nombre_cat = item.get("categoria")
            urls = item.get("urls_paginadas_html", [])

            if nombre_cat and urls:
                lista_categorias_paginas.append((nombre_cat, urls))

        log.info("📌 Lista resumida creada: %s categorías con URLs", len(lista_categorias_paginas))

    except Exception as e:
        log.error("❌ No se pudo cargar/armar lista desde categorias_paginadas.json: %s", e)

    # =========================================================
    # 6) Scrape HTML de cada URL paginada -> nombre + precio
    # =========================================================
    extractor = CotoProductoExtractor()  # usa su propia session interna

    productos_por_categoria = []  # salida final

    for cat_index, (categoria, urls_paginas) in enumerate(lista_categorias_paginas, start=1):
        log.info("📦 Scrapeando categoría %s/%s: %s (páginas: %s)",
                 cat_index, len(lista_categorias_paginas), categoria, len(urls_paginas))

        productos_categoria = []

        for page_index, url_page in enumerate(urls_paginas, start=1):
            try:
                productos = extractor.scrape_url_paginada(url_page)

                log.info("   Página %s/%s -> productos: %s",
                         page_index, len(urls_paginas), len(productos))

                # guardamos los productos de esa página
                productos_categoria.extend(productos)

            except Exception as e:
                log.error("❌ Error scrapeando %s (página %s/%s): %s",
                          categoria, page_index, len(urls_paginas), e)

        # guardamos por categoría
        productos_por_categoria.append({
            "categoria": categoria,
            "total_urls": len(urls_paginas),
            "total_productos": len(productos_categoria),
            "productos": productos_categoria
        })

    # ----------------------------
    # 7) Guardar productos (nombre + precio)
    # ----------------------------
    ruta_productos = os.path.join("Coto", "productos_nombre_precio.json")
    with open(ruta_productos, "w", encoding="utf-8") as f:
        json.dump(productos_por_categoria, f, ensure_ascii=False, indent=2)

    log.info("✅ Productos guardados en: %s", ruta_productos)