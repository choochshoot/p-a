# CMS local

Editor visual local para modificar `data/content.json` sin tocar `index.html` ni el render principal del sitio.

## Abrir el CMS

Desde la terminal del proyecto:

```powershell
python cms/server.py --port 8020
```

Luego abre:

```text
http://127.0.0.1:8020/cms/
```

Si el puerto `8020` ya esta ocupado, usa otro:

```powershell
python cms/server.py --port 8030
```

Y abre:

```text
http://127.0.0.1:8030/cms/
```

## Que puede editar

- Hero: titulo, subtitulo, CTA, imagen de fondo y logo.
- Secciones: titulo, texto, tipo, menu, visibilidad, imagen, lottie, items, galeria, quote y CTA.
- Orden de secciones con botones de subir/bajar.
- Nuevas secciones usando tipos ya soportados por `assets/js/app.js`.
- Imagenes locales, guardadas dentro de `assets/images`.

## Seguridad del flujo

Antes de guardar, el servidor valida ids duplicados, tipos de seccion soportados y rutas relativas. Cada guardado crea un respaldo local en `data/backups/`.
