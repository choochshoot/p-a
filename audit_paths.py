import os
import re

PROJECT_ROOT = "."

absolute_pattern = re.compile(r'(href|src|url|fetch)\(\s*["\']\/')

def scan_file(filepath):
    issues = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

            matches = absolute_pattern.findall(content)
            if matches:
                issues.append(filepath)

    except:
        pass

    return issues

def main():
    problematic_files = []

    for root, dirs, files in os.walk(PROJECT_ROOT):
        for file in files:
            if file.endswith((".html", ".css", ".js")):
                path = os.path.join(root, file)
                issues = scan_file(path)
                if issues:
                    problematic_files.extend(issues)

    if problematic_files:
        print("\n⚠ Se encontraron rutas absolutas en:")
        for f in problematic_files:
            print(f"- {f}")
    else:
        print("\n✔ No se encontraron rutas absolutas. Todo es relativo.")

if __name__ == "__main__":
    main()
