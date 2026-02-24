import math
import requests


class CotoPaginador:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
            "Referer": "https://www.cotodigital.com.ar/",
        })

    def _find_results_list(self, data):
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

    def _fetch_first_json(self, url_categoria: str):
        # cookies
        self.session.get("https://www.cotodigital.com.ar/", timeout=(10, 30)).raise_for_status()

        # JSON page 1
        r = self.session.get(url_categoria + "?format=json", timeout=(10, 30))
        r.raise_for_status()
        return r.json()

    def _build_api_url(self, nav_state: str, offset: int, rpp: int) -> str:
        ns = nav_state
        ns = ns.replace("{offset}", str(offset)).replace("{recordsPerPage}", str(rpp))
        ns = ns.replace("%7Boffset%7D", str(offset)).replace("%7BrecordsPerPage%7D", str(rpp))
        ns = ns.replace("%257Boffset%257D", str(offset)).replace("%257BrecordsPerPage%257D", str(rpp))

        if ns.startswith("/"):
            return "https://www.cotodigital.com.ar/sitios/cdigi/categoria" + ns
        return ns

    def _api_to_friendly_html(self, url_categoria: str, api_url: str) -> str:
        if "?" not in api_url:
            return url_categoria

        query = api_url.split("?", 1)[1]

        # quitar format=json para ver HTML
        query_parts = [p for p in query.split("&") if not p.startswith("format=")]
        query = "&".join(query_parts)

        # encodear "=" como %3D, pero dejar "&"
        query = query.replace("=", "%3D")

        return url_categoria + "%3F" + query

    # ✅ MÉTODO PÚBLICO (lo que vas a usar desde el main)
    def obtener_paginacion_categoria(self, url_categoria: str, devolver_html_friendly: bool = True):

        data = self._fetch_first_json(url_categoria)

        rl = self._find_results_list(data)
        if not rl:
            raise ValueError("No se encontró el bloque de paginación en el JSON.")

        total = int(rl["totalNumRecs"])
        rpp = int(rl["recsPerPage"])
        total_pages = math.ceil(total / rpp)
        nav_state = rl["pagingActionTemplate"]["navigationState"]

        #urls_json = []
        urls_html = []

        for page in range(1, total_pages + 1):
            offset = (page - 1) * rpp
            api_url = self._build_api_url(nav_state, offset, rpp)
            #urls_json.append(api_url)

            if devolver_html_friendly:
                urls_html.append(self._api_to_friendly_html(url_categoria, api_url))

        if devolver_html_friendly:
            #return total_pages, urls_json, urls_html
            return total_pages, urls_html

        #return total_pages, urls_json
        return total_pages