import os

"""
====================================================
PULIDO ASESORES — PROJECT AUDIT TOOL
Escanea y muestra la estructura real del proyecto
====================================================
"""

EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "node_modules",
    ".idea",
    ".vscode"
}

EXCLUDE_FILES = {
    ".DS_Store"
}


def scan_directory(path, prefix=""):

    items = sorted(os.listdir(path))

    items = [
        item for item in items
        if item not in EXCLUDE_DIRS
        and item not in EXCLUDE_FILES
    ]

    total = len(items)

    for index, item in enumerate(items):

        full_path = os.path.join(path, item)

        connector = "└── " if index == total - 1 else "├── "

        print(prefix + connector + item)

        if os.path.isdir(full_path):

            extension = "    " if index == total - 1 else "│   "

            scan_directory(full_path, prefix + extension)


def print_header():

    print("""
====================================================
PULIDO ASESORES — PROJECT STRUCTURE AUDIT
====================================================
""")


def print_runtime_notes():

    print("""

====================================================
RUNTIME NOTES
====================================================

CMS:
    python cms/manage_content.py

Servidor local:
    python -m http.server 8000

Abrir navegador:
    http://localhost:8000

El sitio carga contenido desde:
    data/content.json

Render dinámico gestionado por:
    assets/js/app.js

====================================================
""")


def main():

    root = os.getcwd()

    print_header()

    print("PROJECT ROOT:\n")
    print(os.path.basename(root))

    scan_directory(root)

    print_runtime_notes()


if __name__ == "__main__":
    main()