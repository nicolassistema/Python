import requests
import json

page_url = "https://www.cotodigital.com.ar/sitios/cdigi/categoria/catalogo-almac%C3%A9n/_/N-8pub5z?Nf=product.endDate%7CGTEQ%201.7718912E12%7C%7Cproduct.startDate%7CLTEQ%201.7718912E12&Nr=AND(product.sDisp_200:1004,product.language:espa%C3%B1ol,OR(product.siteId:CotoDigital))&format=json"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
    "Accept": "application/json, text/plain, */*",
}

s = requests.Session()
s.headers.update(headers)

# 1️⃣ Entramos a la home para obtener cookies
r1 = s.get("https://www.cotodigital.com.ar/", timeout=(5, 15))
print("base status:", r1.status_code)

# 2️⃣ Llamamos a la API
r2 = s.get(
    page_url,
    headers={"Referer": "https://www.cotodigital.com.ar/"},
    timeout=(5, 15)
)

print("api status:", r2.status_code)

# 3️⃣ Verificamos que la respuesta sea JSON
content_type = r2.headers.get("Content-Type", "")

if r2.status_code == 200 and "application/json" in content_type:
    print("La respuesta es JSON válido ✔")

    try:
        data = r2.json()  # Convertimos a dict de Python

        # Guardamos el JSON
        with open("coto_almacen.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print("Guardado: coto_almacen.json")

    except json.JSONDecodeError:
        print("La respuesta dice ser JSON pero no pudo decodificarse ❌")

else:
    print("La respuesta NO es JSON ❌")
    print("Content-Type recibido:", content_type)
    print("Primeros 500 caracteres de la respuesta:")
    print(r2.text[:500])