"""
add_hreflang.py
Adds hreflang alternate link tags to all English and Chinese guide pages.
Run this once after translate_guide_zh.py, or whenever pages are regenerated.

What it adds to <head>:
  English page at /guide/[slug]/:
    <link rel="alternate" hreflang="en"      href="https://optimisedeats.com/guide/[slug]/"/>
    <link rel="alternate" hreflang="zh-Hans" href="https://optimisedeats.com/guide/zh/[slug]/"/>
    <link rel="alternate" hreflang="x-default" href="https://optimisedeats.com/guide/[slug]/"/>

  Chinese page at /guide/zh/[slug]/:
    <link rel="alternate" hreflang="zh-Hans" href="https://optimisedeats.com/guide/zh/[slug]/"/>
    <link rel="alternate" hreflang="en"      href="https://optimisedeats.com/guide/[slug]/"/>
    <link rel="alternate" hreflang="x-default" href="https://optimisedeats.com/guide/[slug]/"/>
"""

import zipfile
from pathlib import Path
from bs4 import BeautifulSoup

BASE    = Path(__file__).parent
ZH_DIR  = BASE / "zh"
BASE_URL = "https://optimisedeats.com/guide"

def hreflang_tags(en_url: str, zh_url: str) -> str:
    return (
        f'<link rel="alternate" hreflang="en" href="{en_url}"/>\n'
        f'<link rel="alternate" hreflang="zh-Hans" href="{zh_url}"/>\n'
        f'<link rel="alternate" hreflang="x-default" href="{en_url}"/>\n'
    )

def already_has_hreflang(soup) -> bool:
    return bool(soup.find("link", rel="alternate", hreflang=True))

def add_to_page(path: Path, en_url: str, zh_url: str):
    html = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    if already_has_hreflang(soup):
        return False  # already done

    head = soup.find("head")
    if not head:
        return False

    canon = head.find("link", rel="canonical")
    tags_html = hreflang_tags(en_url, zh_url)
    tags_soup = BeautifulSoup(tags_html, "html.parser")

    if canon:
        # Insert after canonical
        for tag in reversed(list(tags_soup.children)):
            if hasattr(tag, 'name') and tag.name:
                canon.insert_after(tag)
    else:
        # Append to head
        head.append(tags_soup)

    path.write_text(str(soup), encoding="utf-8")
    return True


def main():
    # Find all English pages (not in zh/)
    en_pages = []
    hub = BASE / "index.html"
    if hub.exists():
        en_pages.append(("", hub))
    for p in sorted(BASE.rglob("*/index.html")):
        rel = p.relative_to(BASE)
        parts = rel.parts
        if len(parts) == 2 and parts[0] != "zh":
            en_pages.append((parts[0], p))

    print(f"Adding hreflang to {len(en_pages)} English + {len(en_pages)} Chinese pages...")

    updated_en, updated_zh = 0, 0
    for slug, en_path in en_pages:
        if slug == "":
            en_url = f"{BASE_URL}/"
            zh_url = f"{BASE_URL}/zh/"
            zh_path = ZH_DIR / "index.html"
        else:
            en_url = f"{BASE_URL}/{slug}/"
            zh_url = f"{BASE_URL}/zh/{slug}/"
            zh_path = ZH_DIR / slug / "index.html"

        # English page
        if add_to_page(en_path, en_url, zh_url):
            updated_en += 1

        # Chinese page
        if zh_path.exists():
            if add_to_page(zh_path, en_url, zh_url):
                updated_zh += 1

    print(f"Updated: {updated_en} EN pages, {updated_zh} ZH pages")

    # Rebuild deploy zip with everything
    zip_path = BASE.parent / "guide-zh-deploy.zip"
    count = 0
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        # Chinese pages
        for f in ZH_DIR.rglob("*"):
            if f.is_file():
                arcname = "zh/" + str(f.relative_to(ZH_DIR)).replace("\\", "/")
                zf.write(f, arcname)
                count += 1
        # English pages (updated with hreflang)
        for f in BASE.rglob("index.html"):
            if "zh" not in str(f).replace("\\", "/"):
                rel = str(f.relative_to(BASE)).replace("\\", "/")
                zf.write(f, rel)
                count += 1

    kb = zip_path.stat().st_size // 1024
    print(f"Deploy zip: guide-zh-deploy.zip  ({kb} KB, {count} files)")


if __name__ == "__main__":
    main()
