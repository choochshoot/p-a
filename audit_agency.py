import os
import re
import json

PROJECT_ROOT = "."
VALID_EXTENSIONS = (".html", ".css", ".js", ".json")
ASSET_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".svg", ".json", ".css", ".js")

absolute_path_pattern = re.compile(r'["\']\/(?!\/)')
base_pattern = re.compile(r'<base\s+href=')
localhost_pattern = re.compile(r'localhost|127\.0\.0\.1')
url_pattern = re.compile(r'(href|src)\s*=\s*["\']([^"\']+)["\']')
css_url_pattern = re.compile(r'url\(["\']?([^"\')]+)["\']?\)')
fetch_pattern = re.compile(r'fetch\(["\']([^"\']+)["\']\)')

missing_files = []
structure_issues = []

def file_exists(path):
    return os.path.exists(os.path.normpath(path))

def scan_file(filepath):
    global missing_files, structure_issues

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Detect base tag
        if base_pattern.search(content):
            structure_issues.append((filepath, "Found <base href> tag"))

        # Detect absolute path
        if absolute_path_pattern.search(content):
            structure_issues.append((filepath, "Absolute path starting with / detected"))

        # Detect localhost
        if localhost_pattern.search(content):
            structure_issues.append((filepath, "Localhost reference detected"))

        # Detect href/src references
        for match in url_pattern.findall(content):
            asset_path = match[1]

            if asset_path.startswith("http"):
                continue
            if asset_path.startswith("#"):
                continue
            if asset_path.startswith("mailto:"):
                continue

            full_path = os.path.join(os.path.dirname(filepath), asset_path)
            full_path = os.path.normpath(full_path)

            if not file_exists(full_path):
                missing_files.append((filepath, asset_path))

        # Detect CSS url(...)
        for match in css_url_pattern.findall(content):
            if match.startswith("http"):
                continue

            full_path = os.path.join(os.path.dirname(filepath), match)
            full_path = os.path.normpath(full_path)

            if not file_exists(full_path):
                missing_files.append((filepath, match))

        # Detect fetch(...)
        for match in fetch_pattern.findall(content):
            if match.startswith("http"):
                continue

            full_path = os.path.join(os.path.dirname(filepath), match)
            full_path = os.path.normpath(full_path)

            if not file_exists(full_path):
                missing_files.append((filepath, match))

    except Exception:
        pass

def scan_json(filepath):
    global missing_files

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        json_str = json.dumps(data)

        paths = re.findall(r'["\']([^"\']+\.(png|jpg|jpeg|webp|svg|json))["\']', json_str)

        for match in paths:
            asset_path = match[0]

            if asset_path.startswith("http"):
                continue

            full_path = os.path.join(PROJECT_ROOT, asset_path)
            full_path = os.path.normpath(full_path)

            if not file_exists(full_path):
                missing_files.append((filepath, asset_path))

    except Exception:
        pass

def main():
    print("\n🔎 Running Agency-Level Deploy Audit...\n")

    for root, dirs, files in os.walk(PROJECT_ROOT):
        for file in files:
            if file.endswith(VALID_EXTENSIONS):
                path = os.path.join(root, file)

                if file.endswith(".json"):
                    scan_json(path)
                else:
                    scan_file(path)

    if structure_issues:
        print("⚠ STRUCTURE ISSUES:\n")
        for issue in structure_issues:
            print(f"{issue[0]}  →  {issue[1]}")
        print()

    if missing_files:
        print("❌ MISSING FILE REFERENCES:\n")
        for missing in missing_files:
            print(f"{missing[0]}  →  {missing[1]}")
        print()

    if not structure_issues and not missing_files:
        print("✔ Audit PASSED. No structural or 404 risks detected.\n")

if __name__ == "__main__":
    main()
