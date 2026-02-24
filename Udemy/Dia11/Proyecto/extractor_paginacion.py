import math
import requests


def _get_session():
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
        "Referer": "https://www.cotodigital.com.ar/",
    })
    return s


def _find_results_list(data):
    stack = [data]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            if (
                "totalNumRecs" in cur
                and "recsPerPage" in cur
                and isinstance(cur.get("pagingActionTemplate"), dict)
                and "navigationState" in cur["pagingActionTemplate"]
            ):
                return cur
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)
    return None


def _fetch_first_json(session, url_categoria: str):
    # cookies
    session.get("https://www.cotodigital.com.ar/", timeout=(10, 30)).raise_for_status()

    # JSON page 1
    r = session.get(url_categoria + "?format=json", timeout=(10, 30))
    r.raise_for_status()
    return r.json()


def _build_api_url(nav_state: str, offset: int, rpp: int) -> str:
    """
    Devuelve URL JSON real (API) usando navigationState
    """
    ns = nav_state
    ns = ns.replace("{offset}", str(offset)).replace("{recordsPerPage}", str(rpp))
    ns = ns.replace("%7Boffset%7D", str(offset)).replace("%7BrecordsPerPage%7D", str(rpp))
    ns = ns.replace("%257Boffset%257D", str(offset)).replace("%257BrecordsPerPage%257D", str(rpp))

    # La navigationState suele empezar con "/catalogo..."; cuelga de /sitios/cdigi/categoria
    if ns.startswith("/"):
        return "https://www.cotodigital.com.ar/sitios/cdigi/categoria" + ns
    return ns


def _api_to_friendly_html(url_categoria: str, api_url: str) -> str:
    """
    Convierte la API URL (?No=..&Nrpp=..&format=json) a friendly HTML con %3F y No%3D...
    y sin format=json (para que muestre HTML en navegador).
    """
    # api_url trae ".../N-xxx?A=1&B=2&format=json"
    if "?" not in api_url:
        return url_categoria

    query = api_url.split("?", 1)[1]

    # quitar format=json para ver HTML
    query_parts = [p for p in query.split("&") if not p.startswith("format=")]
    query = "&".join(query_parts)

    # encodear "=" como %3D, pero dejar "&"
    query = query.replace("=", "%3D")

    return url_categoria + "%3F" + query


def obtener_paginacion_categoria(url_categoria: str, devolver_html_friendly: bool = True):
    """
    Le pasás UNA URL de categoría y te devuelve:

    - total_pages
    - urls_json (siempre)
    - urls_html (opcional, friendly para navegador)

    Uso típico: por cada categoría, llamás a esto y recorrés urls_json para scrapear.
    """

    session = _get_session()
    data = _fetch_first_json(session, url_categoria)

    rl = _find_results_list(data)
    if not rl:
        raise ValueError("No se encontró el bloque de paginación en el JSON.")

    total = int(rl["totalNumRecs"])
    rpp = int(rl["recsPerPage"])
    total_pages = math.ceil(total / rpp)
    nav_state = rl["pagingActionTemplate"]["navigationState"]

    urls_json = []
    urls_html = []

    for page in range(1, total_pages + 1):
        offset = (page - 1) * rpp

        api_url = _build_api_url(nav_state, offset, rpp)
        urls_json.append(api_url)

        if devolver_html_friendly:
            urls_html.append(_api_to_friendly_html(url_categoria, api_url))

    if devolver_html_friendly:
        return total_pages, urls_json, urls_html

    return total_pages, urls_json