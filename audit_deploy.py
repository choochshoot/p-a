import os
import re
import json

PROJECT_ROOT = "."
file_extensions = (".html", ".css", ".js", ".json")

patterns = {
    "Absolute path (starts with /)": re.compile(r'["\']\/(?!\/)'),
    "Localhost reference": re.compile(r'localhost|127\.0\.0\.1'),
    "<base href> detected": re.compile(r'<base\s+href='),
    "Absolute fetch": re.compile(r'fetch\(\s*["\']\/'),
}

def scan_text_file(filepath):
    issues = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

            for label, pattern in patterns.items():
                if pattern.search(content):
                    issues.append(label)

    except Exception:
        pass

    return issues

def scan_json_file(filepath):
    issues = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        json_str = json.dumps(data)

        if re.search(r'["\']\/(?!\/)', json_str):
            issues.append("Absolute path in JSON")

        if re.search(r'localhost|127\.0\.0\.1', json_str):
            issues.append("Localhost reference in JSON")

    except Exception:
        pass

    return issues

def main():
    problems_found = False

    print("\n🔎 Running Advanced Deploy Audit...\n")

    for root, dirs, files in os.walk(PROJECT_ROOT):
        for file in files:
            if file.endswith(file_extensions):
                path = os.path.join(root, file)

                if file.endswith(".json"):
                    issues = scan_json_file(path)
                else:
                    issues = scan_text_file(path)

                if issues:
                    problems_found = True
                    print(f"⚠ Issues found in: {path}")
                    for issue in issues:
                        print(f"   - {issue}")
                    print()

    if not problems_found:
        print("✔ Audit passed. No deploy-blocking issues detected.\n")

if __name__ == "__main__":
    main()
