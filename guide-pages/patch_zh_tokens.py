"""
patch_zh_tokens.py
1. Downloads all live Chinese guide pages that already exist,
   fixes incorrectly-translated brand tokens (e.g. OE->original), saves them.
2. For Chinese pages that don't exist yet (500), downloads the English source
   page and runs it through the translator to create the missing Chinese page.
3. Creates guide-zh-patch.zip ready to deploy.

Usage:  python patch_zh_tokens.py
Output: guide-zh-patch.zip  (upload to /var/www/optimisedeats/guide/)
"""

import re, sys, time, zipfile
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError

# Force UTF-8 output on Windows
sys.stdout.reconfigure(encoding="utf-8")

BASE_URL    = "https://optimisedeats.com/guide/"
ZH_BASE_URL = "https://optimisedeats.com/guide/zh/"
SCRIPT_DIR  = Path(__file__).parent
OUT_DIR     = SCRIPT_DIR / "zh"
PROJECT_DIR = SCRIPT_DIR.parent

# All known PROTECT mappings: real → key (used for both patch and translation)
PROTECT = [
    ("OptimisedEats",   "OE"),
    ("Coles",           "COLES"),
    ("Woolworths",      "WOOLIES"),
    ("Aldi",            "ALDI"),
    ("NHMRC",           "NHMRC"),
    ("mTOR",            "MTOR"),
    ("Vegemite",        "VEG"),
    ("Weston A. Price", "WAP"),
    ("B12",             "B12"),
    ("DHA",             "DHA"),
    ("EPA",             "EPA"),
    ("ALA",             "ALA"),
    ("NRV",             "NRV"),
    ("AUD",             "AUD"),
]

# Known bad Google-translated bracket tokens -> correct value
KNOWN_BAD = {
    "。0E〃":    "OptimisedEats",   # 〔OE〕
    "。手机应用〃": "Weston A. Price",  # 〔手机应用〕
}

# Build static lookup for 〔KEY〕 and [KEY] variants
TOKEN_LOOKUP = {}
for real, key in PROTECT:
    TOKEN_LOOKUP[f"。{key}〃"] = real   # 〔KEY〕
    TOKEN_LOOKUP[f"[{key}]"]           = real
    TOKEN_LOOKUP["{{" + key + "}}"]    = real

# Also add the actual Unicode chars for 〔 〕 directly
LBRACKET = "〔"  # 〔
RBRACKET = "〕"  # 〕
for real, key in PROTECT:
    TOKEN_LOOKUP[f"{LBRACKET}{key}{RBRACKET}"] = real

# Hand-coded known bad translations to catch regardless of bracket type
KNOWN_BAD_SIMPLE = {
    f"{LBRACKET}原稿{RBRACKET}":     "OptimisedEats",   # 〔OE〕 → "original draft"
    f"{LBRACKET}手机应用{RBRACKET}": "Weston A. Price",  # 〔WAP〕 → "mobile app"
    f"{LBRACKET}奥乐齐{RBRACKET}":   "Aldi",             # 〔ALDI〕 → Chinese brand name
    f"[原稿]":                        "OptimisedEats",
    f"[手机应用]":                    "Weston A. Price",
    f"[奥乐齐]":                      "Aldi",
}

# Page slugs — must match actual server paths under /guide/zh/
SLUGS = [
    "",
    "budget-basics",
    "nutrient-gaps",
    "deficiency-symptoms",
    "pre-conception",
    "pregnancy",          # /guide/zh/pregnancy/
    "hidden-hunger",
    "kids",               # /guide/zh/kids/
    "nrv",                # /guide/zh/nrv/
    "arsenal",            # /guide/zh/arsenal/
    "batch-cooking",
    "shopping",           # /guide/zh/shopping/
    "cuisines",           # /guide/zh/cuisines/
    "recipes",
    "foods-for-gaps",     # /guide/zh/foods-for-gaps/
    "macronutrients",
    "daily-habits",
    "absorption",
    "sleep-nutrition",
    "weston-price",
    "life-stages",
    "vegan-nutrition",    # /guide/zh/vegan-nutrition/
    "exercise-nutrition", # /guide/zh/exercise-nutrition/
    "disclaimer",
]

LANG_BANNER_ZH = """\
<div style="background:#f0f9ff;border:1px solid #bae6fd;border-radius:10px;\
padding:10px 16px;margin-bottom:24px;font-size:13px;\
display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap">
  <span style="color:#0369a1">&#127760; &#35821;&#35328; / Language</span>
  <div style="display:flex;gap:12px">
    <a href="../" style="color:#64748b;font-weight:600;text-decoration:none">English</a>
    <span style="color:#16a34a;font-weight:700">&#20013;&#25991;</span>
  </div>
</div>
"""


def fetch(url: str) -> tuple[str | None, int]:
    """Returns (html, status_code). html is None on error."""
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8"), 200
    except HTTPError as e:
        return None, e.code
    except Exception as e:
        print(f"  ERROR: {url} -- {e}")
        return None, 0


def fix_tokens(html: str) -> tuple[str, int]:
    """Replace all known bad/bracket tokens. Returns (fixed_html, replacement_count)."""
    count = 0
    for bad, real in KNOWN_BAD_SIMPLE.items():
        n = html.count(bad)
        if n:
            html = html.replace(bad, real)
            count += n
    for token, real in TOKEN_LOOKUP.items():
        n = html.count(token)
        if n:
            html = html.replace(token, real)
            count += n
    leftovers = re.findall(f"{re.escape(LBRACKET)}[^{re.escape(RBRACKET)}]+{re.escape(RBRACKET)}", html)
    if leftovers:
        print(f"    WARNING: unrecognised bracket tokens still present: {set(leftovers)}")
    return html, count


def translate_from_english(slug: str) -> str | None:
    """
    Download the English page for this slug and translate it to Chinese
    using the same logic as translate_guide_zh.py.
    """
    try:
        from bs4 import BeautifulSoup, NavigableString, Comment
        from deep_translator import GoogleTranslator
    except ImportError:
        print("  ERROR: beautifulsoup4 or deep_translator not installed.")
        print("  Run: pip install beautifulsoup4 deep-translator")
        return None

    url = BASE_URL + (f"{slug}/" if slug else "")
    html, status = fetch(url)
    if html is None:
        print(f"  Cannot fetch English page ({status}): {url}")
        return None

    print(f"  Translating English -> Chinese for: {slug or 'hub'} ...")

    SKIP_TAGS = {"style", "script", "meta", "link"}
    BATCH_MAX = 3000
    DELAY     = 1.5

    translator = GoogleTranslator(source="en", target="zh-CN")

    def protect(text):
        for real, key in PROTECT:
            text = text.replace(real, "{{" + key + "}}")
        return text

    def restore(text):
        for real, key in PROTECT:
            text = text.replace("{{" + key + "}}", real)
            text = text.replace("{{ " + key + " }}", real)
            text = text.replace("[" + key + "]", real)
            text = text.replace(f"{LBRACKET}{key}{RBRACKET}", real)
        return text

    def is_skippable(t):
        t = t.strip()
        if not t: return True
        if re.match(r'^[\d\s\.,\-\+\%\$\(\)\/\:\;\|\*\#\@\!]+$', t): return True
        if t.startswith(('http', '//', 'mailto:')): return True
        if re.search(r'[一-鿿]', t): return True
        if len(t) <= 1: return True
        return False

    def should_skip(node):
        p = node.parent
        while p:
            if p.name in SKIP_TAGS: return True
            p = p.parent
        return False

    soup = BeautifulSoup(html, "html.parser")

    # Collect translatable text nodes
    nodes, texts = [], []
    for node in soup.find_all(string=True):
        if isinstance(node, Comment): continue
        if should_skip(node): continue
        t = node.strip()
        if is_skippable(t): continue
        nodes.append(node)
        texts.append(t)

    # Batch translate
    results = []
    batch, batch_len = [], 0

    def flush():
        nonlocal batch, batch_len
        if not batch: return
        protected = [protect(t) for t in batch]
        joined = "\n".join(protected)
        try:
            translated = translator.translate(joined)
            restored = restore(translated)
            parts = restored.split("\n")
            if len(parts) < len(batch):
                parts += [parts[-1]] * (len(batch) - len(parts))
            results.extend(parts[:len(batch)])
        except Exception as e:
            sys.stderr.write(f"\n  [translate error] {e}\n")
            results.extend(batch)
        batch.clear()
        batch_len = 0
        time.sleep(DELAY)

    for text in texts:
        if batch_len + len(text) + 1 > BATCH_MAX:
            flush()
        batch.append(text)
        batch_len += len(text) + 1
    flush()

    # Apply translations
    for node, zh in zip(nodes, results):
        if zh and zh.strip() and zh.strip() != node.strip():
            node.replace_with(zh.strip())

    # Translate title
    title_tag = soup.find("title")
    if title_tag and title_tag.string:
        base = re.sub(r'\s*[--]\s*OptimisedEats.*$', '', title_tag.string).strip()
        if base and not is_skippable(base):
            zh_title = GoogleTranslator(source="en", target="zh-CN").translate(protect(base))
            zh_title = restore(zh_title)
            title_tag.string = f"{zh_title} -- OptimisedEats"

    # Update lang attribute
    html_tag = soup.find("html")
    if html_tag:
        html_tag["lang"] = "zh-CN"

    # Add language toggle banner at top of <main>
    main = soup.find("main")
    if main:
        is_hub = (slug == "")
        banner = LANG_BANNER_ZH
        if is_hub:
            banner = banner.replace('href="../"', 'href="/guide/"')
        from bs4 import BeautifulSoup as BS
        main.insert(0, BS(banner, "html.parser"))

    # Fix canonical URL
    canon = soup.find("link", rel="canonical")
    if canon and "/guide/" in (canon.get("href") or ""):
        href = canon["href"]
        if "/guide/zh/" not in href:
            canon["href"] = href.replace("/guide/", "/guide/zh/", 1)

    # Update inLanguage in JSON-LD
    for script in soup.find_all("script", type="application/ld+json"):
        if script.string and '"inLanguage"' in script.string:
            script.string = script.string.replace('"en-AU"', '"zh-CN"')

    # Fix related guide links to point to /guide/zh/[slug]/
    related = soup.find("div", class_="related")
    if related:
        for a in related.find_all("a", href=True):
            href = a["href"]
            if href.startswith("/guide/") and "/guide/zh/" not in href:
                slug_part = href.strip("/").replace("guide/", "")
                if slug_part:
                    a["href"] = f"/guide/zh/{slug_part}/"

    time.sleep(DELAY)
    return str(soup)


def patch_page(slug: str):
    """Fetch Chinese page, fix tokens, or translate from English if missing."""
    zh_url = ZH_BASE_URL + (f"{slug}/" if slug else "")
    html, status = fetch(zh_url)
    label = slug or "hub"

    if html is not None:
        # Page exists — fix bad tokens
        fixed, n = fix_tokens(html)
        print(f"  [{label}] {n} token(s) fixed")
    elif status == 500 or status == 404:
        # Page missing — translate from English
        print(f"  [{label}] Chinese page missing (HTTP {status}) -- translating from English...")
        fixed = translate_from_english(slug)
        if fixed is None:
            print(f"  [{label}] SKIPPED (could not generate)")
            return
    else:
        print(f"  [{label}] Unexpected HTTP {status} -- skipping")
        return

    # Save
    if slug:
        out_path = OUT_DIR / slug / "index.html"
    else:
        out_path = OUT_DIR / "index.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(fixed, encoding="utf-8")


def make_zip(zip_path: Path):
    count = 0
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in OUT_DIR.rglob("*"):
            if f.is_file():
                arcname = "zh/" + str(f.relative_to(OUT_DIR)).replace("\\", "/")
                zf.write(f, arcname)
                count += 1
    kb = zip_path.stat().st_size // 1024
    print(f"\nZip: {zip_path.name}  ({kb} KB, {count} files)")


def main():
    print("=" * 60)
    print("Patching Chinese guide pages (fix tokens + generate missing)")
    print("=" * 60)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for slug in SLUGS:
        patch_page(slug)
        time.sleep(0.3)

    zip_path = PROJECT_DIR / "guide-zh-patch.zip"
    make_zip(zip_path)

    print(f"\nDone. Upload guide-zh-patch.zip to server:")
    print("  unzip -o guide-zh-patch.zip -d /var/www/optimisedeats/guide/")


if __name__ == "__main__":
    main()
