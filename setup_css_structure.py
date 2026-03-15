import os

base_path = "assets/css"

structure = {
    "base": ["reset.css", "variables.css", "typography.css"],
    "layout": ["hero.css", "sections.css", "footer.css"],
    "components": ["buttons.css", "cards.css", "modal.css"],
    "effects": ["background.css", "animations.css"]
}

for folder, files in structure.items():
    folder_path = os.path.join(base_path, folder)
    os.makedirs(folder_path, exist_ok=True)

    for file in files:
        file_path = os.path.join(folder_path, file)
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"/* {file} */\n")
            print(f"Created: {file_path}")

print("\n✔ CSS structure created successfully.")
