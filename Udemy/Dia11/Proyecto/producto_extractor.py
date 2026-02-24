import re
import time
from typing import List, Dict, Optional, Tuple, Any
from urllib.parse import urlparse

import requests


class CotoProductoExtractor:
    def __init__(self, session: Optional[requests.Session] = None):
        self.session = session or requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
            "Referer": "https://www.cotodigital.com.ar/",
        })

    # ----------------------------
    # Helpers
    # ----------------------------
    @staticmethod
    def _friendly_to_api_url(url_friendly: str) -> str:
        """
        Convierte una URL friendly (con %3F y %3D) a una URL normal con query,
        y asegura format=json.
        """
        u = url_friendly.replace("%3F", "?").replace("%3D", "=")

        # si quedó sin '?', no hay query; igual le agregamos format=json
        if "?" not in u:
            return u + "?format=json"

        # si ya tiene format=json no agregamos
        if "format=json" in u:
            return u

        # agregar format=json al final (con &)
        if u.endswith("&") or u.endswith("?"):
            return u + "format=json"
        return u + "&format=json"

    @staticmethod
    def _parse_price_any(value: Any) -> Optional[float]:
        """
        Convierte distintos formatos a float.
        - "$8.121,74" -> 8121.74
        - "12182" -> 12182.0
        - 12182 -> 12182.0
        """
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)

        s = str(value).strip()
        if not s:
            return None

        # dejar solo dígitos/puntos/comas
        s = re.sub(r"[^\d\.,]", "", s)
        if not s:
            return None

        # AR: '.' miles, ',' decimales
        s = s.replace(".", "").replace(",", ".")
        try:
            return float(s)
        except ValueError:
            return None

    def _find_records_list(self, data: Any) -> Optional[Dict]:
        """
        Busca recursivamente un bloque que contenga records + totalNumRecs/recsPerPage,
        típico de la respuesta de Coto.
        """
        stack = [data]
        while stack:
            cur = stack.pop()
            if isinstance(cur, dict):
                # patrón típico
                if "records" in cur and isinstance(cur["records"], list):
                    return cur
                stack.extend(cur.values())
            elif isinstance(cur, list):
                stack.extend(cur)
        return None

    # ----------------------------
    # Networking
    # ----------------------------
    def fetch_json(self, url_api_json: str, timeout: Tuple[int, int] = (10, 30), retries: int = 3) -> Any:
        # cookies
        self.session.get("https://www.cotodigital.com.ar/", timeout=timeout)

        last_exc = None
        for i in range(retries):
            try:
                r = self.session.get(url_api_json, timeout=timeout)
                r.raise_for_status()
                return r.json()
            except Exception as e:
                last_exc = e
                time.sleep(0.8 * (i + 1))
        raise last_exc

    # ----------------------------
    # Parsing (JSON)
    # ----------------------------
    def extract_nombre_precio_from_json(self, data: Any) -> List[Dict]:
        """
        Devuelve lista de productos con:
          - nombre
          - precio (float o None)
        """
        block = self._find_records_list(data)
        if not block:
            return []

        productos = []
        for rec in block.get("records", []):
            # Endeca suele traer "attributes"
            attrs = rec.get("attributes", {}) if isinstance(rec, dict) else {}

            # nombre: suele venir como lista en product.displayName
            nombre = None
            for k in ("product.displayName", "product.name", "displayName", "name"):
                v = attrs.get(k)
                if isinstance(v, list) and v:
                    nombre = str(v[0]).strip()
                    break
                if isinstance(v, str) and v.strip():
                    nombre = v.strip()
                    break

            # precio: intentamos varias claves comunes
            precio = None
            for k in (
                "product.salePrice",
                "product.promoPrice",
                "product.listPrice",
                "sku.salePrice",
                "sku.listPrice",
                "price",
            ):
                v = attrs.get(k)
                if isinstance(v, list) and v:
                    precio = self._parse_price_any(v[0])
                    if precio is not None:
                        break
                else:
                    precio = self._parse_price_any(v)
                    if precio is not None:
                        break

            if nombre:
                productos.append({
                    "nombre": nombre,
                    "precio": precio
                })

        return productos

    # ----------------------------
    # Public API
    # ----------------------------
    def scrape_url_paginada(self, url_paginada_html_friendly: str) -> List[Dict]:
        url_api = self._friendly_to_api_url(url_paginada_html_friendly)
        data = self.fetch_json(url_api)
        return self.extract_nombre_precio_from_json(data)