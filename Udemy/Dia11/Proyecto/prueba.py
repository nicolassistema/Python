import math
import requests
from pip._internal.utils import urls

URL_CATEGORIA = "https://www.cotodigital.com.ar/sitios/cdigi/categoria/catalogo-almac%C3%A9n-golosinas/_/N-1y5dh9i"

def get_session():
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
        "Referer": "https://www.cotodigital.com.ar/",
    })
    return s

def find_results_list(data):
    stack = [data]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            if ("totalNumRecs" in cur and "recsPerPage" in cur
                and isinstance(cur.get("pagingActionTemplate"), dict)
                and "navigationState" in cur["pagingActionTemplate"]):
                return cur
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)
    return None

def fetch_first_json(s, url_categoria):
    s.get("https://www.cotodigital.com.ar/", timeout=(10, 30)).raise_for_status()
    r = s.get(url_categoria + "?format=json", timeout=(10, 30))
    r.raise_for_status()
    return r.json()

def navstate_to_friendly_url(url_categoria: str, nav_state: str, offset: int, rpp: int) -> str:
    """
    nav_state suele venir como:
      "/catalogo.../_/N-1y5dh9i?Nf=...&No={offset}&Nrpp={recordsPerPage}&format=json"
    Queremos:
      "<url_categoria>%3FNf%3D...&No%3D24&Nrpp%3D24"
    """
    # 1) reemplazo placeholders (si vinieran como {offset} o como %7Boffset%7D, etc.)
    ns = nav_state
    ns = ns.replace("{offset}", str(offset)).replace("{recordsPerPage}", str(rpp))
    ns = ns.replace("%7Boffset%7D", str(offset)).replace("%7BrecordsPerPage%7D", str(rpp))
    ns = ns.replace("%257Boffset%257D", str(offset)).replace("%257BrecordsPerPage%257D", str(rpp))

    # 2) ns puede venir con "/catalogo.../N-xxx?...."
    # nos quedamos SOLO con la parte de query después del "?"
    if "?" in ns:
        query = ns.split("?", 1)[1]
    else:
        query = ""

    # 3) sacar format=json para que al abrir en navegador se vea la página HTML
    # (si lo querés igual, comentá esta línea)
    parts = [p for p in query.split("&") if not p.startswith("format=")]
    query = "&".join(parts)

    # 4) encodear “a la manera Coto”:
    # - el '?' va como %3F
    # - cada '=' va como %3D
    # - pero los '&' quedan sin encodear
    query = query.replace("=", "%3D")

    # 5) URL final friendly
    return url_categoria + "%3F" + query

def main():
    s = get_session()
    data = fetch_first_json(s, URL_CATEGORIA)

    rl = find_results_list(data)
    total = int(rl["totalNumRecs"])
    rpp = int(rl["recsPerPage"])
    total_pages = math.ceil(total / rpp)
    nav_state = rl["pagingActionTemplate"]["navigationState"]

    print("total_pages:", total_pages)

    urls = []
    for page in range(1, total_pages + 1):
        offset = (page - 1) * rpp
        friendly = navstate_to_friendly_url(URL_CATEGORIA, nav_state, offset, rpp)
        urls.append(friendly)

    # muestra ejemplo
    print("\nEjemplo página 1:\n", urls[0])
    print("\nEjemplo página 2:\n", urls[1])
    print("\nEjemplo última:\n", urls[-1])

    # with open("urls_html_friendly.txt", "w", encoding="utf-8") as f:
    #     f.write("\n".join(urls))
    #
    # print("\n✅ Guardado: urls_html_friendly.txt")
    lista_urls = []
    for url in urls:
        lista_urls.append(url)

    for url in lista_urls:
        print("url:", url)



    #print("\n".join(urls))

if __name__ == "__main__":
    main()