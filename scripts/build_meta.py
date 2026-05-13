from html import escape
from pathlib import Path
import json
import re


ROOT = Path(__file__).resolve().parents[1]
CONTENT_PATH = ROOT / "data" / "content.json"
SITE_CONFIG_PATH = ROOT / "data" / "site-config.json"
INDEX_PATH = ROOT / "index.html"


def load_content():
    with CONTENT_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_site_config():
    if not SITE_CONFIG_PATH.exists():
        return {}
    with SITE_CONFIG_PATH.open("r", encoding="utf-8") as file:
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


def valid_gtm_id(gtm_id):
    return bool(re.match(r"^GTM-[A-Z0-9]+$", gtm_id or "")) and gtm_id != "GTM-XXXXXXX"


def build_gtm_head(gtm_id):
    return f"""<!-- Google Tag Manager -->
<script>
(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{gtm_id}');
</script>
<!-- End Google Tag Manager -->"""


def build_gtm_body(gtm_id):
    return f"""<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={escape(gtm_id, quote=True)}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""


def sync_gtm(html, analytics):
    head_start = "<!-- GTM HEAD START -->"
    head_end = "<!-- GTM HEAD END -->"
    body_start = "<!-- GTM BODY START -->"
    body_end = "<!-- GTM BODY END -->"

    gtm_id = analytics.get("gtmId", "")
    enabled = analytics.get("enabled") is True and valid_gtm_id(gtm_id)
    head_block = f"{head_start}\n{build_gtm_head(gtm_id) if enabled else ''}\n{head_end}"
    body_block = f"{body_start}\n{build_gtm_body(gtm_id) if enabled else ''}\n{body_end}"

    html = re.sub(
        rf"{re.escape(head_start)}.*?{re.escape(head_end)}",
        head_block,
        html,
        flags=re.DOTALL,
    ) if head_start in html else html.replace("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">", "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n\n" + head_block, 1)

    html = re.sub(
        rf"{re.escape(body_start)}.*?{re.escape(body_end)}",
        body_block,
        html,
        flags=re.DOTALL,
    ) if body_start in html else html.replace("<body>", "<body>\n" + body_block, 1)

    return html


def sync_analytics_script(html):
    marker = '<script src="assets/js/analytics.js" defer></script>'
    if marker in html:
        return html
    return html.replace(
        '<script type="module" src="assets/js/app.js"></script>',
        '<script type="module" src="assets/js/app.js"></script>\n<script src="assets/js/analytics.js" defer></script>',
        1,
    )


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
    site_config = load_site_config()
    meta = content.get("meta", {})
    hero = content.get("hero", {})
    title = meta.get("title", "Pulido Asesores")
    description = meta.get("description", "")
    keywords = meta.get("keywords", "")
    site_url = meta.get("url", "")

    html = INDEX_PATH.read_text(encoding="utf-8")
    html = sync_gtm(html, site_config.get("analytics", {}))

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
    html = sync_analytics_script(html)

    INDEX_PATH.write_text(html, encoding="utf-8", newline="\n")
    print("Meta tags y analytics sincronizados desde data/content.json y data/site-config.json")


if __name__ == "__main__":
    main()
