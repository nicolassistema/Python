import json
import re
import time
from typing import Any, Optional, Tuple
import requests


class CotoProductoExtractor:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
            "Referer": "https://www.cotodigital.com.ar/",
        })

    # =========================================================
    # NETWORK
    # =========================================================

    def fetch_json(self, url_api: str):
        # Activar cookies
        self.session.get("https://www.cotodigital.com.ar/")

        for _ in range(3):
            try:
                r = self.session.get(url_api, timeout=(10, 30))
                r.raise_for_status()
                return r.json()
            except Exception:
                time.sleep(0.7)

        raise Exception(f"No se pudo obtener JSON: {url_api}")

    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def _friendly_to_api_url(url_friendly: str) -> str:
        """
        Convierte URL HTML encoded (%3F %3D) a URL API real
        y asegura que tenga format=json.
        """
        u = url_friendly.replace("%3F", "?").replace("%3D", "=")

        if "?" not in u:
            return u + "?format=json"

        if "format=json" in u:
            return u

        return u + "&format=json"

    @staticmethod
    def _parse_price_any(value: Any) -> Optional[float]:
        """
        Convierte "$8.121,74" o "$8121.74c/u" o "12182.000000" en float
        """
        if value is None:
            return None

        if isinstance(value, (int, float)):
            return float(value)

        s = str(value).strip()
        if not s:
            return None

        s = re.sub(r"[^\d\.,]", "", s)

        if "," in s and "." in s:
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", ".")

        try:
            return float(s)
        except ValueError:
            return None

    @staticmethod
    def _promo_from_descuentos(attrs: dict) -> Tuple[Optional[float], Optional[str]]:
        """
        Devuelve (precio_descuento, detalle_promo) desde product.dtoDescuentos (si existe).
        """
        dd = attrs.get("product.dtoDescuentos")
        if not isinstance(dd, list) or not dd:
            return None, None

        raw = dd[0]
        if not raw:
            return None, None

        try:
            arr = json.loads(raw) if isinstance(raw, str) else raw
            if not (isinstance(arr, list) and arr):
                return None, None

            d0 = arr[0] if isinstance(arr[0], dict) else None
            if not d0:
                return None, None

            precio_desc = (
                d0.get("precioDescuento")
                or d0.get("precio")
                or d0.get("precioPromo")
            )
            precio_desc = CotoProductoExtractor._parse_price_any(precio_desc)

            detalle = (
                d0.get("leyenda")
                or d0.get("descripcion")
                or d0.get("texto")
                or d0.get("detalle")
            )
            if isinstance(detalle, str):
                detalle = detalle.strip()
            else:
                detalle = None

            return precio_desc, detalle
        except Exception:
            return None, None

    @staticmethod
    def _buscar_detalle_promo_en_attrs(attrs: dict) -> Optional[str]:
        """
        Fallback robusto: busca texto promo dentro de cualquier attribute.
        Útil cuando en HTML se ve 'PRECIO CON 3X2' pero en JSON está en otra key.
        """
        if not isinstance(attrs, dict):
            return None

        patrones = [
            "PRECIO CON",
            "3X2",
            "2X1",
            "LLEVANDO",
            "OFERTA",
            "EXCLUSIVO",
            "DESCUENTO",
            "PROMO",
            "AHORR",
            "CUOTAS",
        ]

        def es_promo_texto(s: str) -> bool:
            up = s.upper()
            return any(p in up for p in patrones)

        for _, v in attrs.items():
            if isinstance(v, list):
                for item in v:
                    if isinstance(item, str):
                        txt = item.strip()
                        if len(txt) >= 4 and es_promo_texto(txt):
                            return txt
            elif isinstance(v, str):
                txt = v.strip()
                if len(txt) >= 4 and es_promo_texto(txt):
                    return txt

        return None

    @staticmethod
    def _find_records_list(data: Any):
        stack = [data]
        while stack:
            cur = stack.pop()
            if isinstance(cur, dict):
                if "records" in cur and isinstance(cur["records"], list):
                    return cur
                stack.extend(cur.values())
            elif isinstance(cur, list):
                stack.extend(cur)
        return None

    # =========================================================
    # PARSER
    # =========================================================

    def extract_productos_from_json(self, data: Any):
        block = self._find_records_list(data)
        if not block:
            return []

        productos = []

        for rec in block.get("records", []):
            attrs = rec.get("attributes", {}) if isinstance(rec, dict) else {}

            # subnivel (a veces hay datos ahí)
            sub_attrs = None
            if isinstance(rec, dict) and isinstance(rec.get("records"), list) and rec["records"]:
                sub = rec["records"][0]
                if isinstance(sub, dict):
                    sub_attrs = sub.get("attributes", {})

            # -------------------------
            # ID (producto)
            # -------------------------
            producto_id = None
            for a in [sub_attrs, attrs]:
                if not isinstance(a, dict):
                    continue
                for k in ("product.repositoryId", "repositoryId", "product.id"):
                    v = a.get(k)
                    if isinstance(v, list) and v:
                        producto_id = str(v[0]).strip()
                        break
                    if isinstance(v, str) and v.strip():
                        producto_id = v.strip()
                        break
                if producto_id:
                    break

            # -------------------------
            # Nombre
            # -------------------------
            nombre = None
            for a in [sub_attrs, attrs]:
                if not isinstance(a, dict):
                    continue
                for k in ("product.displayName", "product.name", "displayName", "name"):
                    v = a.get(k)
                    if isinstance(v, list) and v:
                        nombre = str(v[0]).strip()
                        break
                    if isinstance(v, str) and v.strip():
                        nombre = v.strip()
                        break
                if nombre:
                    break

            # -------------------------
            # Precio regular (sin promo)
            # -------------------------
            precio_regular = None
            for a in [sub_attrs, attrs]:
                if not isinstance(a, dict):
                    continue
                ap = a.get("sku.activePrice")
                if isinstance(ap, list) and ap:
                    precio_regular = self._parse_price_any(ap[0])
                    if precio_regular is not None:
                        break

            # -------------------------
            # Promo (precio + detalle)
            # -------------------------
            precio_descuento = None
            detalle_promo = None

            # 1) desde dtoDescuentos
            for a in [sub_attrs, attrs]:
                if not isinstance(a, dict):
                    continue
                precio_descuento, detalle_promo = self._promo_from_descuentos(a)
                if precio_descuento is not None or detalle_promo:
                    break

            # 2) fallback: buscar texto promo en cualquier attribute
            if not detalle_promo:
                for a in [sub_attrs, attrs]:
                    detalle_promo = self._buscar_detalle_promo_en_attrs(a)
                    if detalle_promo:
                        break

            if nombre:
                productos.append({
                    "id": producto_id,
                    "nombre": nombre,
                    "precio_descuento": precio_descuento,
                    "precio_regular": precio_regular,
                    "detalle_promo": detalle_promo
                })

        return productos

    # =========================================================
    # PUBLIC
    # =========================================================

    def scrape_url_paginada(self, url_friendly: str):
        url_api = self._friendly_to_api_url(url_friendly)
        data = self.fetch_json(url_api)
        return self.extract_productos_from_json(data)