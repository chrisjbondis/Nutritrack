"""
translate_guide_zh.py
Translates all generated guide HTML pages from English to Simplified Chinese.

Source:  guide-pages/[page]/index.html  (and guide-pages/index.html for hub)
Output:  guide-pages/zh/[page]/index.html  (and guide-pages/zh/index.html)

The zip is then deployed to /var/www/optimisedeats/guide/zh/ on the server.

Usage:  python translate_guide_zh.py
        python translate_guide_zh.py --page life-stages   (single page)
"""

import re, time, sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment
from deep_translator import GoogleTranslator

# ── Config ─────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent          # guide-pages/
ZH_DIR     = BASE_DIR / "zh"               # guide-pages/zh/
BATCH_MAX  = 3000                           # chars per Google Translate call
DELAY      = 1.5                            # seconds between API calls

# Tags whose text we NEVER translate
SKIP_TAGS  = {"style", "script", "meta", "link"}

# Attribute values we translate
TRANSLATE_ATTRS = {
    "title": True,     # <title> tag  (handled separately)
    "content": True,   # <meta content="...">
}

# Strings to protect from translation (token → original)
# Using {{DOUBLE_CURLY}} format — Google Translate treats these as template
# placeholders and leaves them untouched, unlike 〔bracket〕 tokens which
# Google sometimes translates as abbreviations.
PROTECT = [
    ("OptimisedEats",   "{{OE}}"),
    ("Coles",           "{{COLES}}"),
    ("Woolworths",      "{{WOOLIES}}"),
    ("Aldi",            "{{ALDI}}"),
    ("NHMRC",           "{{NHMRC}}"),
    ("mTOR",            "{{MTOR}}"),
    ("Vegemite",        "{{VEG}}"),
    ("Weston A. Price", "{{WAP}}"),
    ("B12",             "{{B12}}"),
    ("DHA",             "{{DHA}}"),
    ("EPA",             "{{EPA}}"),
    ("ALA",             "{{ALA}}"),
    ("NRV",             "{{NRV}}"),
    ("AUD",             "{{AUD}}"),
]

# Language toggle banner — injected at the top of <main> in Chinese pages
LANG_BANNER_ZH = """\
<div style="background:#f0f9ff;border:1px solid #bae6fd;border-radius:10px;\
padding:10px 16px;margin-bottom:24px;font-size:13px;\
display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap">
  <span style="color:#0369a1">&#127760; 语言 / Language</span>
  <div style="display:flex;gap:12px">
    <a href="../" style="color:#64748b;font-weight:600;text-decoration:none">English</a>
    <span style="color:#16a34a;font-weight:700">中文</span>
  </div>
</div>
"""

# Language toggle for English pages (points to zh/ sibling)
LANG_BANNER_EN = """\
<div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;\
padding:10px 16px;margin-bottom:24px;font-size:13px;\
display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap">
  <span style="color:#166534">&#127760; Language / 语言</span>
  <div style="display:flex;gap:12px">
    <span style="color:#16a34a;font-weight:700">English</span>
    <a href="zh/" style="color:#64748b;font-weight:600;text-decoration:none">中文</a>
  </div>
</div>
"""

translator = GoogleTranslator(source="en", target="zh-CN")


# ── Translation helpers ────────────────────────────────────────────────────────

def protect(text: str) -> str:
    for real, token in PROTECT:
        text = text.replace(real, token)
    return text

def restore(text: str) -> str:
    for real, token in PROTECT:
        text = text.replace(token, real)
        # Google sometimes inserts spaces inside {{ }} — handle e.g. "{{ OE }}"
        inner = token[2:-2]  # strip the {{ }}
        for space in ("", " "):
            text = text.replace(f"{{ {space}{inner}{space} }}", real)
            text = text.replace(f"{{{{{space}{inner}{space}}}}}", real)
        # Legacy: old 〔bracket〕 tokens still present on server — restore those too
        bracket_token = f"〔{inner}〕"
        text = text.replace(bracket_token, real)
    return text

def is_skippable(text: str) -> bool:
    """True for strings that don't need translation."""
    t = text.strip()
    if not t:
        return True
    # Pure numbers / punctuation / symbols
    if re.match(r'^[\d\s\.,\-\+\%\$\(\)\/\:\;\|\*\#\@\!]+$', t):
        return True
    # URLs
    if t.startswith(('http', '//', 'mailto:')):
        return True
    # Already Chinese
    if re.search(r'[一-鿿]', t):
        return True
    # Very short meaningless strings
    if len(t) <= 1:
        return True
    # Pure emoji / symbol
    if re.match(r'^[\U0001F000-\U0001FFFF☀-➿\s]+$', t):
        return True
    return False

def should_skip_node(node) -> bool:
    """True if this node is inside a skip tag."""
    parent = node.parent
    while parent:
        if parent.name in SKIP_TAGS:
            return True
        parent = parent.parent
    return False

def collect_nodes(soup):
    """Return list of (NavigableString, str) for all translatable text nodes."""
    results = []
    for node in soup.find_all(string=True):
        if isinstance(node, Comment):
            continue
        if should_skip_node(node):
            continue
        text = node.strip()
        if is_skippable(text):
            continue
        results.append((node, text))
    return results

def batch_translate(texts: list[str]) -> list[str]:
    """
    Translate a list of strings using newline batching.
    Returns list of translated strings (same length as input).
    """
    if not texts:
        return []

    results = []
    batch, batch_len = [], 0

    def flush_batch():
        nonlocal batch, batch_len
        if not batch:
            return
        protected = [protect(t) for t in batch]
        joined = "\n".join(protected)
        try:
            translated = translator.translate(joined)
            restored = restore(translated)
            parts = restored.split("\n")
            # Align: if translation collapsed lines, distribute best-effort
            if len(parts) < len(batch):
                # Pad with last part
                parts += [parts[-1]] * (len(batch) - len(parts))
            results.extend(parts[:len(batch)])
        except Exception as e:
            sys.stderr.write(f"\n  [translate error] {e}\n")
            results.extend(batch)  # keep originals on error
        batch.clear()
        batch_len = 0
        time.sleep(DELAY)

    for text in texts:
        tlen = len(text)
        if batch_len + tlen + 1 > BATCH_MAX:
            flush_batch()
        batch.append(text)
        batch_len += tlen + 1

    flush_batch()
    return results


# ── Per-page translation ───────────────────────────────────────────────────────

def translate_meta_tags(soup):
    """Translate <title> and key <meta> content values."""
    # <title>
    title_tag = soup.find("title")
    if title_tag and title_tag.string:
        orig = title_tag.string
        base = re.sub(r'\s*[—\-–]\s*OptimisedEats.*$', '', orig).strip()
        if base and not is_skippable(base):
            zh_base = batch_translate([base])
            if zh_base:
                title_tag.string = f"{zh_base[0]} — OptimisedEats"

    # <meta name="description"> and og:description, og:title, keywords
    meta_to_translate = []
    for meta in soup.find_all("meta"):
        name = (meta.get("name") or meta.get("property") or "").lower()
        if name in ("description", "keywords", "og:title", "og:description"):
            content = meta.get("content", "")
            if content and not is_skippable(content):
                meta_to_translate.append((meta, content))

    if meta_to_translate:
        zh_values = batch_translate([c for _, c in meta_to_translate])
        for (meta, _), zh in zip(meta_to_translate, zh_values):
            meta["content"] = zh

    # lang attribute
    html_tag = soup.find("html")
    if html_tag:
        html_tag["lang"] = "zh-CN"

    # canonical URL: /guide/[page]/ → /guide/zh/[page]/
    canon = soup.find("link", rel="canonical")
    if canon and "/guide/" in (canon.get("href") or ""):
        href = canon["href"]
        if "/guide/zh/" not in href:
            canon["href"] = href.replace("/guide/", "/guide/zh/", 1)

    # JSON-LD: update inLanguage
    for script in soup.find_all("script", type="application/ld+json"):
        if script.string and '"inLanguage"' in script.string:
            script.string = script.string.replace('"en-AU"', '"zh-CN"')


def add_lang_toggle(soup, is_hub=False):
    """Inject language banner at top of <main>."""
    main = soup.find("main")
    if not main:
        return
    # Hub page: the "English" link goes to /guide/ not ../
    banner = LANG_BANNER_ZH
    if is_hub:
        banner = banner.replace('href="../"', 'href="/guide/"')
    toggle = BeautifulSoup(banner, "html.parser")
    main.insert(0, toggle)


def fix_zh_internal_links(soup):
    """
    In zh/ pages, update related guide links to point to /guide/zh/[page]/
    but keep breadcrumb, header, footer links pointing to the English site.
    """
    # Related links section: update to zh/ siblings
    related = soup.find("div", class_="related")
    if related:
        for a in related.find_all("a", href=True):
            href = a["href"]
            if href.startswith("/guide/") and "/guide/zh/" not in href:
                slug = href.strip("/").replace("guide/", "")
                if slug:
                    a["href"] = f"/guide/zh/{slug}/"


def translate_page(slug: str, html_path: Path, out_path: Path):
    """Translate one page and write the Chinese version."""
    is_hub = (slug == "")
    label = "hub" if is_hub else slug

    html = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # Collect text nodes
    node_pairs = collect_nodes(soup)
    texts = [t for _, t in node_pairs]
    nodes = [n for n, _ in node_pairs]

    print(f"  {label}: {len(texts)} strings to translate...", end=" ", flush=True)

    # Translate body text
    translated = batch_translate(texts)

    # Replace text nodes in-place
    replaced = 0
    for node, zh in zip(nodes, translated):
        if zh and zh.strip() and zh.strip() != node.strip():
            node.replace_with(zh.strip())
            replaced += 1

    # Translate meta / title
    translate_meta_tags(soup)

    # Add language toggle banner
    add_lang_toggle(soup, is_hub=is_hub)

    # Fix internal links in related-links section
    fix_zh_internal_links(soup)

    # Write output
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(str(soup), encoding="utf-8")

    print(f"done ({replaced} replaced)")


# ── Add EN toggle to English pages ────────────────────────────────────────────

def add_en_toggle_to_english_pages(slugs_with_zh: list[str]):
    """
    Add a 'Switch to 中文' toggle to each English guide page that now has a
    Chinese counterpart. Uses absolute paths so the link is always correct
    regardless of where the page sits in the URL hierarchy.
    Skips only if the correct absolute link is already present.
    Replaces any existing banner that has the old relative href="zh/" link.
    """
    print("\nAdding ZH toggle to English pages...")
    for slug in slugs_with_zh:
        if slug == "":
            path = BASE_DIR / "index.html"
            zh_href = "/guide/zh/"
        else:
            path = BASE_DIR / slug / "index.html"
            zh_href = f"/guide/zh/{slug}/"
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")
        # Already has the correct absolute link — nothing to do
        if f'href="{zh_href}"' in html:
            print(f"  (already correct): {slug or 'hub'}")
            continue
        soup = BeautifulSoup(html, "html.parser")
        main = soup.find("main")
        if not main:
            continue
        # Remove any existing (wrong) banner — identified by its background colour
        for existing in main.find_all("div", style=True):
            if "f0fdf4" in (existing.get("style") or ""):
                existing.decompose()
                break
        # Build banner with the correct absolute zh link
        banner = LANG_BANNER_EN.replace('href="zh/"', f'href="{zh_href}"')
        toggle = BeautifulSoup(banner, "html.parser")
        main.insert(0, toggle)
        path.write_text(str(soup), encoding="utf-8")
        print(f"  + EN toggle: {slug or 'hub'}")


# ── Deploy zip ────────────────────────────────────────────────────────────────

def make_deploy_zip():
    """Create guide-zh-deploy.zip from the zh/ directory."""
    import zipfile
    zip_path = BASE_DIR.parent / "guide-zh-deploy.zip"
    count = 0
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in ZH_DIR.rglob("*"):
            if f.is_file():
                arcname = "zh/" + str(f.relative_to(ZH_DIR)).replace("\\", "/")
                zf.write(f, arcname)
                count += 1
        # Also include English pages (with the new toggle banners)
        for f in BASE_DIR.rglob("index.html"):
            if "zh" not in str(f).replace("\\", "/"):
                rel = str(f.relative_to(BASE_DIR)).replace("\\", "/")
                zf.write(f, rel)
                count += 1
    kb = zip_path.stat().st_size // 1024
    print(f"\nDeploy zip: {zip_path.name}  ({kb} KB, {count} files)")
    return zip_path


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # Optional: single page mode
    single = None
    if "--page" in sys.argv:
        idx = sys.argv.index("--page")
        single = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None

    # Build list of pages to translate
    # Hub: BASE_DIR/index.html → ZH_DIR/index.html
    # Pages: BASE_DIR/[slug]/index.html → ZH_DIR/[slug]/index.html
    all_pages = []  # list of (slug, src_path, out_path)

    hub_src = BASE_DIR / "index.html"
    if hub_src.exists():
        all_pages.append(("", hub_src, ZH_DIR / "index.html"))

    for src in sorted(BASE_DIR.rglob("*/index.html")):
        rel = src.relative_to(BASE_DIR)
        parts = rel.parts
        if len(parts) != 2:
            continue
        slug = parts[0]
        if slug == "zh":
            continue  # skip existing zh output
        out = ZH_DIR / slug / "index.html"
        all_pages.append((slug, src, out))

    if single:
        all_pages = [(s, src, out) for s, src, out in all_pages if s == single]
        if not all_pages:
            print(f"Page not found: {single}")
            return

    print("=" * 60)
    print("OptimisedEats Guide  EN -> Simplified Chinese (zh-CN)")
    print("=" * 60)
    print(f"Translating {len(all_pages)} pages...\n")

    done_slugs = []
    for slug, src, out in all_pages:
        try:
            translate_page(slug, src, out)
            done_slugs.append(slug)
        except Exception as e:
            print(f"\n  ERROR on {slug}: {e}")

    # Add English toggles to source pages
    if not single:
        add_en_toggle_to_english_pages(done_slugs)

    # Make deploy zip
    if not single:
        make_deploy_zip()

    zh_pages = list(ZH_DIR.rglob("index.html"))
    print(f"\nDone!  {len(zh_pages)} Chinese pages in guide-pages/zh/")
    print("Deploy zip: guide-zh-deploy.zip")
    print("Server path: /var/www/optimisedeats/guide/zh/")


if __name__ == "__main__":
    main()
