import json
import os
import re
import unicodedata

DATA_PATH = os.path.join("data", "content.json")

# ==========================================
# UTILITIES
# ==========================================

def slugify(text):
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def load_data():
    if not os.path.exists(DATA_PATH):
        print("content.json no encontrado.")
        exit()

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("✔ Cambios guardados correctamente.\n")


def yes_no(question):
    return input(f"{question} (y/n): ").lower() == "y"


def list_sections(data):
    print("\n=== SECCIONES ===")
    for i, s in enumerate(data.get("sections", [])):
        map_label = "🗺️" if s.get("map") else ""
        print(f"{i+1}) {s.get('title')} (ID: {s.get('id')}) {map_label}")


# ==========================================
# HERO
# ==========================================

def edit_hero(data):
    hero = data.get("hero", {})

    print("\n=== EDITANDO HERO ===")

    hero["enabled"] = yes_no("¿Activar Hero?")

    new_title = input(f"Título ({hero.get('title', '')}): ")
    if new_title:
        hero["title"] = new_title

    if yes_no("¿Modificar texto?"):
        print("Escribe el nuevo texto (multilínea). Escribe END para terminar:")

        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)

        hero["text"] = "\n".join(lines)


    

    new_sub = input(f"Subtítulo ({hero.get('subtitle', '')}): ")
    if new_sub:
        hero["subtitle"] = new_sub

    new_bg = input(f"Background ({hero.get('background', '')}): ")
    if new_bg:
        hero["background"] = new_bg

    new_logo = input(f"Logo ({hero.get('logo', '')}): ")
    if new_logo:
        hero["logo"] = new_logo

    if yes_no("¿Configurar CTA Hero?"):
        hero["cta"] = {
            "enabled": yes_no("¿Activar botón?"),
            "text": input("Texto botón: "),
            "url": input("URL botón: ")
        }
    else:
        hero["cta"] = None

    data["hero"] = hero
    save_data(data)


# ==========================================
# CREATE SECTION
# ==========================================

def create_section(data):

    print("\n=== CREAR NUEVA SECCIÓN ===")

    section_type = input("Tipo (default/grid/grid-extended): ")

    if section_type not in ["default", "grid", "grid-extended"]:
        print("Tipo inválido. Usa 'default' o 'grid'.")
        return

    # ---------- ID + SLUGIFY ----------
    raw_id = input("ID interno (puede tener espacios): ").strip()

    if not raw_id:
        print("El ID no puede estar vacío.")
        return

    section_id = slugify(raw_id)

    existing_ids = [s.get("id") for s in data.get("sections", [])]
    if section_id in existing_ids:
        print(f"⚠ Ya existe una sección con ID '{section_id}'.")
        return

    print(f"ID generado automáticamente: {section_id}")

    # ---------- TEXTO MULTILÍNEA ----------
    print("Escribe el texto (líneas múltiples). Escribe END para terminar:")
    lines = []

    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    section_text = "\n".join(lines)

    # ---------- DICCIONARIO ----------
    section = {
        "enabled": True,
        "id": section_id,
        "type": section_type,
        "title": input("Título sección: "),
        "text": section_text,
        "map": False,
        "cta": None
    }

    # Imagen solo para default
    if section_type == "default":
        if yes_no("¿Agregar imagen principal?"):
            section["image"] = input("Ruta imagen (ej: assets/images/file.webp): ")
        else:
            section["image"] = None

    # Quote solo para default
    if section_type == "default":
        if yes_no("¿Agregar quote?"):
            section["quote"] = {
                "text": input("Texto quote: "),
                "author": input("Autor quote: ")
            }
        else:
            section["quote"] = None


    # GRID EXTENSION
    if section_type == "grid":
        section["items"] = []
        count = int(input("¿Cuántos items grid?: "))
        for i in range(count):
            section["items"].append({
                "lottie": input("Ruta lottie: "),
                "title": input("Título item: "),
                "text": input("Texto item: ")
            })

    # GRID EXTENDED (NUEVO TIPO PREMIUM)
    if section_type == "grid-extended":
        section["subtitle"] = input("Subtítulo sección: ")

        section["items"] = []
        count = int(input("¿Cuántos items grid-extended?: "))

        for i in range(count):
            section["items"].append({
                "number": input("Número (ej: 01): "),
                "title": input("Título item: "),
                "description": input("Descripción item: "),
                "icon": input("Ruta lottie: "),
                "link": input("Link (opcional): ") or None
            })

    # Mapa
    if yes_no("¿Activar mapa?"):
        section["map"] = True

    # CTA
    if yes_no("¿Agregar botón CTA?"):
        section["cta"] = {
            "text": input("Texto botón: "),
            "url": input("URL botón: ")
        }

    data["sections"].append(section)
    save_data(data)


# ==========================================
# EDIT SECTION
# ==========================================

def edit_section(data):

    if not data.get("sections"):
        print("No hay secciones creadas.")
        return

    list_sections(data)

    try:
        index = int(input("Número a editar: ")) - 1
        section = data["sections"][index]
    except:
        print("Selección inválida.")
        return

    print("\n=== EDITANDO SECCIÓN ===")

    new_title = input(f"Título ({section.get('title')}): ")
    if new_title:
        section["title"] = new_title
    
    # SUBTITLE (solo para grid-extended)
    if section.get("type") == "grid-extended":
        current_sub = section.get("subtitle", "")
        new_sub = input(f"Subtítulo ({current_sub}): ")
        if new_sub:
            section["subtitle"] = new_sub        

    # TEXT (solo para default y grid)
    if section.get("type") in ["default", "grid"]:
        if yes_no("¿Modificar texto?"):
            print("Escribe el nuevo texto (multilínea). Escribe END para terminar:")

            lines = []
            while True:
                line = input()
                if line.strip() == "END":
                    break
                lines.append(line)

            section["text"] = "\n".join(lines)



    if yes_no("¿Cambiar estado enabled?"):
        section["enabled"] = yes_no("¿Activar sección?")

    # Imagen (solo default)
    if section.get("type") == "default":
        if yes_no("¿Modificar imagen?"):
            section["image"] = input("Nueva ruta imagen (vacío para eliminar): ") or None

    # Quote (solo default)
    if section.get("type") == "default":
        if yes_no("¿Modificar quote?"):
            if yes_no("¿Activar quote?"):
                section["quote"] = {
                    "text": input("Texto quote: "),
                    "author": input("Autor: ")
                }
            else:
                section["quote"] = None

    # Grid items
    if section.get("type") == "grid":
        if yes_no("¿Modificar items del grid?"):
            section["items"] = []
            count = int(input("¿Cuántos items?: "))
            for i in range(count):
                section["items"].append({
                    "lottie": input("Ruta lottie: "),
                    "title": input("Título item: "),
                    "text": input("Texto item: ")
                })
    # GRID EXTENDED ITEMS
    if section.get("type") == "grid-extended":
        if yes_no("¿Modificar items grid-extended?"):
            section["items"] = []
            count = int(input("¿Cuántos items?: "))
            for i in range(count):
                section["items"].append({
                    "number": input("Número (ej: 01): "),
                    "title": input("Título item: "),
                    "description": input("Descripción item: "),
                    "icon": input("Ruta lottie: "),
                    "link": input("Link (opcional): ") or None
                })                

    # Mapa
    if yes_no("¿Modificar mapa?"):
        section["map"] = yes_no("¿Activar mapa?")

    # CTA
    if yes_no("¿Modificar CTA?"):
        if yes_no("¿Activar botón?"):
            section["cta"] = {
                "text": input("Texto botón: "),
                "url": input("URL botón: ")
            }
        else:
            section["cta"] = None

    save_data(data)


# ==========================================
# DELETE SECTION
# ==========================================

def delete_section(data):

    if not data.get("sections"):
        print("No hay secciones.")
        return

    list_sections(data)

    try:
        index = int(input("Número a eliminar: ")) - 1
        deleted = data["sections"].pop(index)
        print(f"Sección '{deleted.get('title')}' eliminada.")
        save_data(data)
    except:
        print("Selección inválida.")

# ==========================================
# MOVE SECTION (CMS 1.2 - Advanced Reorder)
# ==========================================

def move_section(data):

    if not data.get("sections"):
        print("No hay secciones.")
        return

    list_sections(data)

    try:
        current_index = int(input("Número de sección a mover: ")) - 1

        if current_index < 0 or current_index >= len(data["sections"]):
            print("Número inválido.")
            return

        new_position = int(input("Mover a posición número: ")) - 1

        if new_position < 0 or new_position >= len(data["sections"]):
            print("Posición destino inválida.")
            return

        section = data["sections"].pop(current_index)
        data["sections"].insert(new_position, section)

        save_data(data)
        print("Sección movida correctamente.\n")

    except:
        print("Selección inválida.")



# ==========================================
# MAIN MENU
# ==========================================

def main():

    data = load_data()

    while True:

        print("""
========= CMS PULIDO ASESORES =========
1) Editar Hero
2) Crear Sección
3) Editar Sección
4) Eliminar Sección
5) Mover Sección
6) Salir
""")

        option = input("Selecciona opción: ")

        if option == "1":
            edit_hero(data)

        elif option == "2":
            create_section(data)

        elif option == "3":
            edit_section(data)

        elif option == "4":
            delete_section(data)

        elif option == "5":
            move_section(data)

        elif option == "6":
            print("Saliendo...")
            break


        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
