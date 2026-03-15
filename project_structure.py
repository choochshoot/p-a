"""
====================================================
PULIDO ASESORES — DOCUMENTACIÓN DEL PROYECTO
Arquitectura CMS Modular v2
====================================================

Este archivo describe la estructura del proyecto
y los comandos necesarios para trabajar localmente.

No forma parte del runtime del sitio.
Solo es documentación técnica ejecutable.

Ejecutar:

python project_structure.py

====================================================
"""


def show_structure():

    print("""

===============================
ESTRUCTURA DEL PROYECTO
===============================

project-root
│
├── index.html
│
├── assets
│   ├── css
│   │   ├── base
│   │   │   ├── reset.css
│   │   │   ├── typography.css
│   │   │   └── variables.css
│   │   │
│   │   ├── layout
│   │   │   ├── hero.css
│   │   │   ├── sections.css
│   │   │   ├── grid-extended.css
│   │   │   ├── footer.css
│   │   │   └── menu.css
│   │   │
│   │   ├── components
│   │   │   ├── buttons.css
│   │   │   ├── cards.css
│   │   │   ├── modal.css
│   │   │   └── collapsible.css
│   │   │
│   │   └── styles.css
│   │
│   ├── js
│   │   ├── app.js
│   │   └── lottie-init.js
│   │
│   ├── images
│   │
│   └── lotties
│
├── data
│   └── content.json
│
├── cms
│   └── manage_content.py
│
└── project_structure.py


""")


def show_architecture():

    print("""

===============================
ARQUITECTURA DEL SISTEMA
===============================

El sitio funciona como un CMS dinámico basado en JSON.

FLUJO PRINCIPAL:

manage_content.py
        │
        ▼
data/content.json
        │
        ▼
assets/js/app.js
        │
        ▼
Render dinámico en DOM


TIPOS DE SECCIÓN SOPORTADOS:

- default
- grid
- grid-extended

Planeado:

- profile
- split
- features


VENTAJAS DE ESTA ARQUITECTURA:

✔ No depende de framework
✔ Compatible con GitHub Pages
✔ CMS local en Python
✔ JSON editable
✔ Modular CSS
✔ Escalable


""")


def show_dev_commands():

    print("""

===============================
COMANDOS DE DESARROLLO
===============================

1) Abrir servidor local

python -m http.server 8000


2) Abrir navegador

http://localhost:8000


3) Ejecutar CMS

cd cms
python manage_content.py


4) Salir del CMS

Seleccionar opción 6


5) Detener servidor

CTRL + C


FLUJO RECOMENDADO:

Terminal 1
----------
python -m http.server 8000

Terminal 2
----------
cd cms
python manage_content.py


""")


def show_notes():

    print("""

===============================
NOTAS IMPORTANTES
===============================

1) Nunca abrir index.html directamente
   usando file://

2) Siempre usar servidor local para
   evitar errores de fetch JSON.

3) GitHub Pages funciona porque:

fetch("data/content.json")

usa rutas relativas.


4) No subir:

- .venv
- __pycache__
- logs
- archivos temporales


5) Si agregas nuevas secciones,
   revisa renderSections() en app.js.


""")


def main():

    print("""
====================================================
PULIDO ASESORES — CMS MODULAR
Documentación Técnica del Proyecto
====================================================
""")

    show_structure()
    show_architecture()
    show_dev_commands()
    show_notes()


if __name__ == "__main__":
    main()