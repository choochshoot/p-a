import json
import os
from collections import Counter


CONTENT_PATH = "data/content.json"


# ===============================
# ROOT INFO
# ===============================

def show_root():
    print("\n📍 CARPETA RAÍZ DEL PROYECTO\n")
    print(f"Ruta absoluta:\n  {os.getcwd()}")

    print("""
📦 USO EN REPOSITORIO

Este script debe vivir en la raíz del proyecto.

Para integrarlo en otro repo:

1) Copiar carpeta completa del proyecto
2) Mantener estructura:

   /assets
   /data
   /cms
   index.html

3) Ejecutar desde raíz:

   python project_inspector.py

✔ Compatible con GitHub Pages
✔ Usa rutas relativas (data/content.json)
""")


# ===============================
# TREE VIEW
# ===============================

def print_tree(start_path=".", prefix=""):
    items = sorted(os.listdir(start_path))
    pointers = ["├── "] * (len(items) - 1) + ["└── "]

    for pointer, name in zip(pointers, items):
        path = os.path.join(start_path, name)
        print(prefix + pointer + name)

        if os.path.isdir(path):
            extension = "│   " if pointer == "├── " else "    "
            print_tree(path, prefix + extension)


def show_tree():
    print("\n🗂️ ESTRUCTURA DEL PROYECTO\n")
    print(".")
    print_tree(".")


# ===============================
# LOAD JSON
# ===============================

def load_content():
    if not os.path.exists(CONTENT_PATH):
        print("\n❌ content.json no encontrado")
        return None

    with open(CONTENT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ===============================
# SECTIONS ANALYSIS
# ===============================

def analyze_sections(data):
    print("\n🧠 SECCIONES ACTIVAS\n")

    sections = data.get("sections", [])
    types = []
    icons = []

    for s in sections:
        print(f"• {s.get('id')} → {s.get('type')}")
        types.append(s.get("type"))

        for item in s.get("items", []):
            if item.get("icon"):
                icons.append(item.get("icon"))

    print("\n📊 RESUMEN")

    print(f"Total secciones: {len(sections)}")

    print("\nTipos usados:")
    for t, c in Counter(types).items():
        print(f"  - {t}: {c}")

    print("\nIconos usados:")
    for i, c in Counter(icons).items():
        print(f"  - {i}: {c}")


# ===============================
# SYSTEM
# ===============================

def show_system():
    print("\n⚙️ ARQUITECTURA\n")

    print("""
content.json
   ↓
initializeUI()
   ↓
renderSections()
   ↓
sectionRenderers[type]
   ↓
DOM
""")


# ===============================
# COMMANDS
# ===============================

def show_commands():
    print("\n💻 COMANDOS\n")

    print("""
Servidor local:
  python -m http.server 8000

Abrir:
  http://localhost:8000

CMS:
  cd cms
  python manage_content.py

Detener:
  CTRL + C
""")


# ===============================
# MAIN
# ===============================

def main():

    print("""
========================================
PULIDO ASESORES — SYSTEM INSPECTOR
========================================
""")

    show_root()
    show_tree()

    data = load_content()
    if data:
        analyze_sections(data)

    show_system()
    show_commands()


if __name__ == "__main__":
    main()