import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlsplit, urlunsplit, quote

import requests


@dataclass
class Categoria:
    nombre: str
    url: str


class CotoScraper:
    """
    Scraper de categorías/subcategorías de Coto (Endeca) basado en JSON.
    Flujo:
      1) Descarga JSON crudo (API_URL) y lo guarda como INPUT_FILE
      2) Extrae subCategories* y construye URLs navegables
      3) Guarda el resultado como OUTPUT_DIR/OUTPUT_FILE
      4) Borra INPUT_FILE (temporal)
    """

    def __init__(
        self,
        api_url: str,
        base: str = "https://www.cotodigital.com.ar/sitios/cdigi",
        input_file: str = "coto_almacen.json",
        output_dir: str = "Coto",
        output_file: str = "categorias.json",
        timeout: Tuple[int, int] = (5, 15),
        headers: Optional[Dict[str, str]] = None,
    ):
        self.api_url = api_url
        self.base = base.rstrip("/")
        self.input_file = input_file
        self.output_dir = output_dir
        self.output_file = output_file
        self.timeout = timeout

        default_headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
            "Accept": "application/json, text/plain, */*",
        }
        if headers:
            default_headers.update(headers)
        self.headers = default_headers

        self.session = requests.Session()
        self.session.headers.update(self.headers)

    # -------------------------------
    # HELPERS URL
    # -------------------------------
    @staticmethod
    def _encode_path_only(url: str) -> str:
        """Encodea SOLO el path (acentos etc), sin tocar query."""
        u = urlsplit(url)
        encoded_path = quote(u.path, safe="/-_~.%")
        return urlunsplit((u.scheme, u.netloc, encoded_path, u.query, u.fragment))

    def _build_url_from_navigation_state(self, nav_state: str) -> str:
        """
        navigationState suele venir como:
          'categoria/catalogo-almacén-.../_/N-xxxx'
        (sin slash inicial). Armamos: base + '/' + nav_state normalizado.
        """
        if not isinstance(nav_state, str) or not nav_state.strip():
            return ""

        ns = nav_state.strip().lstrip("/")
        full = f"{self.base}/{ns}"
        return self._encode_path_only(full)

    # -------------------------------
    # EXTRACTOR
    # -------------------------------
    def _extract_subcategories_urls(self, data: Any) -> List[Dict[str, Any]]:
        """
        Recorre todo el JSON y extrae nodos dentro de subCategories, subCategories2, subCategories3, etc.
        Devuelve lista de dict: {depth, name, url}
        """
        results: List[Dict[str, Any]] = []

        def walk(obj: Any, depth: int = 0):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(k, str) and k.lower().startswith("subcategories") and isinstance(v, list):
                        for child in v:
                            if isinstance(child, dict):
                                name = (child.get("displayName") or child.get("label") or "").strip()
                                nav_state = child.get("navigationState", "")
                                url = self._build_url_from_navigation_state(nav_state)

                                if name and url:
                                    results.append({"depth": depth, "name": name, "url": url})

                                walk(child, depth + 1)
                    else:
                        walk(v, depth)

            elif isinstance(obj, list):
                for item in obj:
                    walk(item, depth)

        walk(data)
        return results

    # -------------------------------
    # IO
    # -------------------------------
    def _output_path(self) -> str:
        return os.path.join(self.output_dir, self.output_file)

    # -------------------------------
    # PASO 1: Descargar JSON crudo
    # -------------------------------
    def _download_raw_json(self) -> Dict[str, Any]:
        """
        Descarga la home para cookies y luego la API_URL (JSON).
        Devuelve el JSON como dict.
        """
        # Entrar a home para cookies
        r1 = self.session.get("https://www.cotodigital.com.ar/", timeout=self.timeout)
        if r1.status_code != 200:
            raise RuntimeError(f"Error al acceder a la home: {r1.status_code}")

        # Pedir JSON de la categoría
        r2 = self.session.get(
            self.api_url,
            headers={"Referer": "https://www.cotodigital.com.ar/"},
            timeout=self.timeout,
        )

        if r2.status_code != 200:
            raise RuntimeError(f"Error API: {r2.status_code} - body: {r2.text[:300]}")

        content_type = r2.headers.get("Content-Type", "")
        if not content_type.startswith("application/json"):
            raise RuntimeError(f"No devolvió JSON. Content-Type: {content_type} - body: {r2.text[:300]}")

        return r2.json()

    def _save_json(self, path: str, data: Any) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load_json(self, path: str) -> Any:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # -------------------------------
    # FUNCIÓN PRINCIPAL PÚBLICA
    # -------------------------------
    def generar_categorias(self, verbose: bool = True) -> List[Categoria]:
        """
        Ejecuta todo el flujo y devuelve la lista final de categorías.
        También guarda OUTPUT_DIR/OUTPUT_FILE y borra el INPUT_FILE temporal.
        """
        # 1) Descargar y guardar crudo
        try:
            raw_data = self._download_raw_json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error de conexión: {e}") from e

        self._save_json(self.input_file, raw_data)
        if verbose:
            print(f"Guardado crudo: {self.input_file}")

        # 2) Procesar (podríamos usar raw_data directo, pero mantenemos el flujo que pediste)
        raw = self._load_json(self.input_file)

        cats = self._extract_subcategories_urls(raw)

        # Deduplicar por URL
        seen = set()
        unique = []
        for c in cats:
            if c["url"] not in seen:
                seen.add(c["url"])
                unique.append(c)

        if verbose:
            print(f"Encontré {len(unique)} categorías/subcategorías (subCategories*)")

        categorias = [Categoria(nombre=c["name"], url=c["url"]) for c in unique]

        # 3) Guardar en carpeta Coto/ (crear si no existe; pisa si existe)
        os.makedirs(self.output_dir, exist_ok=True)
        out_path = self._output_path()

        serializable = [{"nombre": c.nombre, "url": c.url} for c in categorias]
        self._save_json(out_path, serializable)

        if verbose:
            print(f"Archivo final creado: {out_path} ✔")

        # 4) Borrar temporal
        try:
            os.remove(self.input_file)
            if verbose:
                print(f"Archivo temporal eliminado: {self.input_file} ✔")
        except Exception as e:
            if verbose:
                print(f"No se pudo eliminar {self.input_file}: {e}")

        return categorias


