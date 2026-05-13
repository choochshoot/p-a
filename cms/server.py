from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import argparse
import json
import mimetypes
import re
import shutil
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "content.json"
IMAGES_DIR = ROOT / "assets" / "images"
ALLOWED_SECTION_TYPES = {
    "default",
    "grid",
    "grid-extended",
    "cards-premium",
    "cards-special",
    "services-feature",
}


def slugify_filename(value):
    stem = Path(value).stem.lower()
    suffix = Path(value).suffix.lower()
    stem = re.sub(r"[^a-z0-9]+", "-", stem).strip("-") or "imagen"
    suffix = suffix if suffix in {".jpg", ".jpeg", ".png", ".webp", ".svg", ".gif"} else ".webp"
    return f"{stem}{suffix}"


def backup_content():
    backup_dir = ROOT / "data" / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    shutil.copy2(DATA_PATH, backup_dir / f"content-{stamp}.json")


def json_response(handler, status, payload):
    body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def validate_asset_path(value, allow_empty=True):
    if value in (None, ""):
        return allow_empty
    if not isinstance(value, str):
        return False
    if value.startswith("/") or "://" in value or ".." in value.replace("\\", "/"):
        return False
    return value.startswith(("assets/", "data/"))


def validate_content(data):
    errors = []

    if not isinstance(data, dict):
        return ["El contenido debe ser un objeto JSON."]

    hero = data.get("hero", {})
    if hero:
        for key in ("background", "logo"):
            if not validate_asset_path(hero.get(key)):
                errors.append(f"Hero: la ruta '{key}' debe ser relativa y empezar con assets/.")

    sections = data.get("sections")
    if not isinstance(sections, list):
        errors.append("sections debe ser una lista.")
        return errors

    seen_ids = set()
    for index, section in enumerate(sections, start=1):
        label = section.get("id") or f"seccion {index}"
        section_id = section.get("id")
        section_type = section.get("type")

        if not section_id:
            errors.append(f"{label}: falta id.")
        elif section_id in seen_ids:
            errors.append(f"{label}: id duplicado.")
        seen_ids.add(section_id)

        if section_type not in ALLOWED_SECTION_TYPES:
            errors.append(f"{label}: type no soportado ({section_type}).")

        if not section.get("title"):
            errors.append(f"{label}: falta title.")

        if not validate_asset_path(section.get("image")):
            errors.append(f"{label}: image debe ser una ruta relativa assets/...")

        if not validate_asset_path(section.get("lottie")):
            errors.append(f"{label}: lottie debe ser una ruta relativa assets/...")

        for img in section.get("gallery") or []:
            if not validate_asset_path(img):
                errors.append(f"{label}: gallery contiene una ruta invalida.")

    return errors


def parse_multipart(headers, body):
    content_type = headers.get("Content-Type", "")
    match = re.search(r"boundary=(?P<boundary>[^;]+)", content_type)
    if not match:
        return {}

    boundary = match.group("boundary").strip('"').encode("utf-8")
    parts = {}

    for raw_part in body.split(b"--" + boundary):
        raw_part = raw_part.strip()
        if not raw_part or raw_part == b"--":
            continue

        if raw_part.endswith(b"--"):
            raw_part = raw_part[:-2].strip()

        header_blob, _, value = raw_part.partition(b"\r\n\r\n")
        if not value:
            continue

        value = value.rstrip(b"\r\n")
        header_text = header_blob.decode("utf-8", errors="replace")
        disposition = next(
            (line for line in header_text.split("\r\n") if line.lower().startswith("content-disposition")),
            "",
        )

        name_match = re.search(r'name="([^"]+)"', disposition)
        if not name_match:
            continue

        filename_match = re.search(r'filename="([^"]*)"', disposition)
        parts[name_match.group(1)] = {
            "filename": filename_match.group(1) if filename_match else None,
            "value": value,
        }

    return parts


class CMSHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/cms":
            self.send_response(302)
            self.send_header("Location", "/cms/")
            self.end_headers()
            return

        if parsed.path == "/api/content":
            if not DATA_PATH.exists():
                json_response(self, 404, {"ok": False, "error": "data/content.json no existe."})
                return
            with DATA_PATH.open("r", encoding="utf-8") as file:
                json_response(self, 200, {"ok": True, "content": json.load(file)})
            return

        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/content":
            self.save_content()
            return

        if parsed.path == "/api/upload":
            self.upload_asset()
            return

        json_response(self, 404, {"ok": False, "error": "Endpoint no encontrado."})

    def save_content(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)

        try:
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            json_response(self, 400, {"ok": False, "error": "JSON invalido."})
            return

        content = payload.get("content")
        errors = validate_content(content)
        if errors:
            json_response(self, 422, {"ok": False, "errors": errors})
            return

        backup_content()
        with DATA_PATH.open("w", encoding="utf-8", newline="\n") as file:
            json.dump(content, file, ensure_ascii=False, indent=2)
            file.write("\n")

        json_response(self, 200, {"ok": True, "message": "Contenido guardado."})

    def upload_asset(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        form = parse_multipart(self.headers, body)
        field = form.get("file")

        if field is None or not field.get("filename"):
            json_response(self, 400, {"ok": False, "error": "Selecciona una imagen."})
            return

        folder = "cms"
        folder_value = form.get("folder", {}).get("value", b"").decode("utf-8", errors="ignore")
        if folder_value:
            folder = re.sub(r"[^a-z0-9/-]+", "-", folder_value.lower()).strip("/-") or "cms"

        target_dir = (IMAGES_DIR / folder).resolve()
        if not str(target_dir).startswith(str(IMAGES_DIR.resolve())):
            json_response(self, 400, {"ok": False, "error": "Carpeta invalida."})
            return

        target_dir.mkdir(parents=True, exist_ok=True)
        filename = slugify_filename(field["filename"])
        target = target_dir / filename

        counter = 2
        while target.exists():
            target = target_dir / f"{Path(filename).stem}-{counter}{Path(filename).suffix}"
            counter += 1

        with target.open("wb") as output:
            output.write(field["value"])

        relative_path = target.relative_to(ROOT).as_posix()
        json_response(self, 200, {"ok": True, "path": relative_path})

    def guess_type(self, path):
        kind, encoding = mimetypes.guess_type(path)
        if kind == "text/javascript":
            kind = "application/javascript"
        return kind or super().guess_type(path)


def main():
    parser = argparse.ArgumentParser(description="CMS local para Pulido Asesores")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8020, type=int)
    args = parser.parse_args()

    if not DATA_PATH.exists():
        print(f"No se encontro {DATA_PATH}", file=sys.stderr)
        return 1

    server = ThreadingHTTPServer((args.host, args.port), CMSHandler)
    print(f"CMS local: http://{args.host}:{args.port}/cms/")
    print(f"Vista del sitio: http://{args.host}:{args.port}/")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
