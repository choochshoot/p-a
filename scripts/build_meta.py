from html import escape
from pathlib import Path
import json
import re


ROOT = Path(__file__).resolve().parents[1]
CONTENT_PATH = ROOT / "data" / "content.json"
INDEX_PATH = ROOT / "index.html"


def load_content():
    with CONTENT_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def absolute_url(path, base_url):
    if not path:
        return ""
    if re.match(r"^https?://", path, re.IGNORECASE):
        return path
    return f"{base_url.rstrip('/')}/{path.lstrip('/')}"


def tag(name, attrs):
    pairs = " ".join(
        f'{key}="{escape(str(value), quote=True)}"'
        for key, value in attrs.items()
        if value is not None
    )
    return f"<{name} {pairs}>"


def replace_tag(html, pattern, replacement):
    updated, count = re.subn(pattern, replacement, html, count=1, flags=re.IGNORECASE)
    if count:
        return updated
    return html


def upsert_meta_block(html, block):
    start_marker = "<!-- Open Graph -->"
    end_marker = "<!-- Preload CSS -->"

    pattern = re.compile(
        rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}",
        re.DOTALL | re.IGNORECASE,
    )

    replacement = f"{start_marker}\n{block}\n\n{end_marker}"
    updated, count = pattern.subn(replacement, html, count=1)
    if count:
        return updated

    return html.replace(end_marker, replacement, 1)


def build_meta_block(meta, hero):
    title = meta.get("title", "")
    description = meta.get("description", "")
    site_url = meta.get("url", "")
    image = absolute_url(meta.get("image") or hero.get("background"), site_url)
    image_type = "image/webp" if image.lower().endswith(".webp") else None

    lines = [
        tag("meta", {"property": "og:type", "content": "website"}),
        tag("meta", {"property": "og:site_name", "content": "Pulido Asesores"}),
        tag("meta", {"property": "og:title", "id": "ogTitle", "content": title}),
        tag("meta", {"property": "og:description", "id": "ogDescription", "content": description}),
        tag("meta", {"property": "og:image", "id": "ogImage", "content": image}),
        tag("meta", {"property": "og:image:secure_url", "id": "ogImageSecure", "content": image}),
        tag("meta", {"property": "og:image:type", "content": image_type}),
        tag("meta", {"property": "og:image:alt", "content": "Pulido Asesores"}),
        tag("meta", {"property": "og:url", "id": "ogUrl", "content": site_url}),
        "",
        tag("meta", {"name": "twitter:card", "content": "summary_large_image"}),
        tag("meta", {"name": "twitter:title", "id": "twitterTitle", "content": title}),
        tag("meta", {"name": "twitter:description", "id": "twitterDescription", "content": description}),
        tag("meta", {"name": "twitter:image", "id": "twitterImage", "content": image}),
    ]

    return "\n".join(line for line in lines if line is not None)


def main():
    content = load_content()
    meta = content.get("meta", {})
    hero = content.get("hero", {})
    title = meta.get("title", "Pulido Asesores")
    description = meta.get("description", "")
    keywords = meta.get("keywords", "")
    site_url = meta.get("url", "")

    html = INDEX_PATH.read_text(encoding="utf-8")

    html = replace_tag(
        html,
        r"<title\b[^>]*>.*?</title>",
        f'<title id="metaTitle">{escape(title)}</title>',
    )
    html = replace_tag(
        html,
        r'<meta\s+name="description"\s+id="metaDescription"[^>]*>',
        tag("meta", {"name": "description", "id": "metaDescription", "content": description}),
    )
    html = replace_tag(
        html,
        r'<meta\s+name="keywords"\s+id="metaKeywords"[^>]*>',
        tag("meta", {"name": "keywords", "id": "metaKeywords", "content": keywords}),
    )
    html = replace_tag(
        html,
        r'<link\s+rel="canonical"\s+id="canonicalUrl"[^>]*>',
        tag("link", {"rel": "canonical", "id": "canonicalUrl", "href": site_url}),
    )
    html = upsert_meta_block(html, build_meta_block(meta, hero))

    INDEX_PATH.write_text(html, encoding="utf-8", newline="\n")
    print("Meta tags sincronizados desde data/content.json")


if __name__ == "__main__":
    main()
