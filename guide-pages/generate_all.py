"""
Master guide generator — regenerates ALL pages with consistent cross-links.
Run this whenever any page changes, then deploy guide-all-deploy.zip.
"""
import json, pathlib, zipfile, re

BASE = pathlib.Path(__file__).parent
PROJECT = BASE.parent
CSS = (BASE / "_shared.css").read_text(encoding="utf-8")

EXTRA_CSS = """
.nutrient-section{margin:28px 0;padding:22px 24px;background:#fff;border:1px solid #e2e8f0;border-radius:12px}
.nutrient-section h2,.nutrient-section h3{border-top:none;margin-top:0;padding-top:0}
.stage-bar{display:flex;gap:0;margin:14px 0;border-radius:10px;overflow:hidden}
.stage{flex:1;padding:10px 12px;font-size:12px;line-height:1.4}
.stage strong{display:block;font-size:13px;margin-bottom:2px}
.stage-1{background:#fef9c3;color:#854d0e}
.stage-2{background:#fed7aa;color:#9a3412}
.stage-3{background:#fecaca;color:#991b1b}
.impact-box{display:flex;gap:12px;padding:10px 0;border-bottom:1px solid #f1f5f9;align-items:flex-start}
.impact-box:last-child{border-bottom:none}
.impact-icon{font-size:22px;flex-shrink:0}
.partner-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:16px 0}
@media(max-width:600px){.partner-grid{grid-template-columns:1fr}}
.partner-card{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:18px}
.partner-card h3{margin-top:0;border-top:none;padding-top:0;font-size:16px}
.partner-female{border-top:3px solid #ec4899}
.partner-male{border-top:3px solid #3b82f6}
.callout{background:#f0fdf4;border-left:4px solid #16a34a;padding:14px 18px;border-radius:0 8px 8px 0;margin:16px 0}
.callout-red{background:#fef2f2;border-left:4px solid #dc2626;padding:14px 18px;border-radius:0 8px 8px 0;margin:16px 0}
.gap-stat{display:inline-block;background:#fef2f2;color:#dc2626;font-weight:800;font-size:13px;padding:2px 10px;border-radius:20px;margin-left:8px;vertical-align:middle}
.absorption-rule{display:flex;gap:12px;align-items:flex-start;padding:10px 0;border-bottom:1px solid #f1f5f9}
.absorption-rule:last-child{border-bottom:none}
.absorption-icon{font-size:22px;flex-shrink:0;margin-top:2px}
.stack-item{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #f1f5f9;gap:12px}
.stack-item:last-child{border-bottom:none}
.stack-food{font-weight:700;color:#0f172a;font-size:14px}
.stack-detail{font-size:13px;color:#64748b}
.stack-cost{font-weight:700;color:#16a34a;font-size:14px;white-space:nowrap}
.tier-badge{display:inline-block;padding:2px 10px;border-radius:20px;font-size:11px;font-weight:800;margin-right:6px}
.tier1{background:#fef3c7;color:#92400e}
.tier2{background:#dbeafe;color:#1e40af}
.tier3{background:#f0fdf4;color:#166534}
.filter-bar{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0 24px}
.filter-btn{background:#f1f5f9;border:1px solid #e2e8f0;color:#475569;font-size:12px;font-weight:700;padding:5px 13px;border-radius:20px;cursor:pointer;text-decoration:none;white-space:nowrap}
.filter-btn:hover,.filter-btn.active{background:#16a34a;color:#fff;border-color:#16a34a;text-decoration:none}
.recipe-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px;margin:0 0 32px}
.recipe-card{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:16px;display:flex;flex-direction:column;gap:6px}
.recipe-card:hover{box-shadow:0 4px 16px rgba(0,0,0,.07)}
.recipe-title{font-size:15px;font-weight:700;color:#0f172a;line-height:1.3}
.recipe-meta{display:flex;gap:10px;font-size:12px;color:#64748b;align-items:center}
.recipe-cost{color:#16a34a;font-weight:700}
.recipe-desc{font-size:13px;color:#475569;line-height:1.5}
.recipe-tags{display:flex;flex-wrap:wrap;gap:4px;margin-top:2px}
.recipe-tag{font-size:10px;font-weight:700;padding:1px 7px;border-radius:10px;background:#f0fdf4;color:#166534}
.recipe-tag.sardine{background:#eff6ff;color:#1d4ed8}
.recipe-tag.kangaroo{background:#fff7ed;color:#c2410c}
.recipe-tag.organ-meat{background:#fdf2f8;color:#86198f}
.recipe-tag.vegan{background:#f0fdf4;color:#166534}
.recipe-tag.vegetarian{background:#ecfdf5;color:#065f46}
.recipe-tag.kid-friendly{background:#fffbeb;color:#92400e}
.recipe-tag.high-protein{background:#eff6ff;color:#1e40af}
.recipe-tag.quick{background:#fff7ed;color:#9a3412}
.section-header{font-size:20px;font-weight:800;color:#0f172a;margin:32px 0 12px;padding-bottom:8px;border-bottom:2px solid #f1f5f9;display:flex;align-items:center;gap:10px}
.recipe-count{font-size:13px;font-weight:400;color:#94a3b8}
.nrv-note{font-size:12px;color:#94a3b8;font-style:italic;margin-top:4px}
.data-table th{font-size:12px}
.data-table td{font-size:13px}
.data-table td:not(:first-child){text-align:center}
.data-table th:not(:first-child){text-align:center}
.app-link-box{background:linear-gradient(135deg,#f0fdf4,#dcfce7);border:1px solid #86efac;border-radius:12px;padding:16px 20px;margin:24px 0;display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}
.app-link-box p{margin:0;font-size:14px;color:#166534}
.app-link-btn{background:#16a34a;color:#fff;padding:8px 18px;border-radius:8px;font-weight:700;font-size:13px;white-space:nowrap;text-decoration:none}
.app-link-btn:hover{background:#15803d;text-decoration:none}
"""

# ── ALL PAGES REGISTRY ────────────────────────────────────────────────────────
ALL_PAGES = [
    ("Budget Basics",            "/guide/budget-basics/",        "💰"),
    ("Nutrient Gaps",            "/guide/nutrient-gaps/",        "⚠️"),
    ("Deficiency Symptoms",      "/guide/deficiency-symptoms/",  "🩺"),
    ("Pre-Conception",           "/guide/pre-conception/",       "👶"),
    ("Pregnancy Nutrition",      "/guide/pregnancy/",            "🤰"),
    ("Hidden Hunger",            "/guide/hidden-hunger/",        "🍟"),
    ("Kids &amp; Toddlers",      "/guide/kids/",                 "🧒"),
    ("NRV Reference Tables",     "/guide/nrv/",                  "📊"),
    ("Budget Arsenal",           "/guide/arsenal/",              "🏆"),
    ("Batch Cooking",            "/guide/batch-cooking/",        "🍲"),
    ("Smart Shopping",           "/guide/shopping/",             "🛒"),
    ("World Cuisines",           "/guide/cuisines/",             "🌏"),
    ("106 Recipes",              "/guide/recipes/",              "🍳"),
    ("Which Foods Fill Gaps",    "/guide/foods-for-gaps/",       "🎯"),
    ("Macronutrients",           "/guide/macronutrients/",       "💪"),
    ("5 Daily Habits",           "/guide/daily-habits/",         "✅"),
    ("Absorption Tips",          "/guide/absorption/",           "🔬"),
    ("Sleep &amp; Nutrition",    "/guide/sleep-nutrition/",      "😴"),
    ("Weston A. Price",          "/guide/weston-price/",         "📜"),
    ("Nutrient Gaps by Life Stage", "/guide/life-stages/",       "👥"),
    ("Vegan &amp; Plant-Based",  "/guide/vegan-nutrition/",      "🌱"),
    ("Exercise &amp; Nutrition", "/guide/exercise-nutrition/",   "🏃"),
    ("Disclaimer",               "/guide/disclaimer/",           "📋"),
]

def other_related(current_path):
    return [(l, h) for l, h, _ in ALL_PAGES if h != current_path]

# ── SHARED TEMPLATE ───────────────────────────────────────────────────────────
def shell(title, desc, keywords, breadcrumb_label, canonical, body_html, related_links):
    related = "".join(f'<a class="related-link" href="{h}">{l}</a>' for l, h in related_links)
    jsonld = f'''{{"@context":"https://schema.org","@type":"Article","headline":"{title}","description":"{desc}","url":"https://optimisedeats.com{canonical}","author":{{"@type":"Person","name":"Chris","url":"https://optimisedeats.com/guide/disclaimer/"}},"publisher":{{"@type":"Organization","name":"OptimisedEats","url":"https://optimisedeats.com"}},"inLanguage":"en-AU"}}'''
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<link rel="canonical" href="https://optimisedeats.com{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://optimisedeats.com{canonical}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="OptimisedEats">
<meta name="author" content="Chris — OptimisedEats">
<script type="application/ld+json">{jsonld}</script>
<style>{CSS}{EXTRA_CSS}</style>
</head>
<body>
<header class="site-header">
  <div class="site-header-inner">
    <a class="logo" href="/"><span>Optimised</span>Eats</a>
    <a class="header-cta" href="/">Open Free App</a>
  </div>
</header>
<div class="breadcrumb">
  <a href="/">Home</a><span>&#8250;</span><a href="/guide/">Nutrition Guide</a><span>&#8250;</span>{breadcrumb_label}
</div>
<main>
{body_html}
<div class="related">
  <h2>More guides</h2>
  <div class="related-grid">{related}</div>
</div>
</main>
<footer class="site-footer">
  <p>&#169; 2025 OptimisedEats &middot; Free nutrition planning for Australians &amp; New Zealanders &middot; <a href="/">Open App</a> &middot; <a href="/guide/">All Guides</a> &middot; <a href="/budget-nutrition-guide.pdf" download>PDF</a> &middot; <a href="/budget-nutrition-ebook.epub" download>EPUB</a></p>
  <p style="margin-top:6px;font-size:11px;color:#cbd5e1">Based on NHMRC Australian Nutrient Reference Values and peer-reviewed research. General educational purposes only &mdash; not a substitute for personalised medical advice.</p>
</footer>
</body>
</html>"""

def app_link(text="Track this in the free app"):
    return f"""<div class="app-link-box">
  <p>&#128247; <strong>{text}</strong> &mdash; enter your household members and see how your meals measure up against their exact targets.</p>
  <a class="app-link-btn" href="/">Open free app</a>
</div>"""

# ── RE-RUN OTHER GENERATORS (they write their own files first) ────────────────
import subprocess, sys
for script in ["generate_pages.py", "generate_technical_pages.py", "generate_new_pages.py", "generate_extra_pages.py", "generate_life_exercise_pages.py"]:
    result = subprocess.run([sys.executable, str(BASE / script)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(result.stdout.strip())
    if result.returncode != 0:
        print("STDERR:", result.stderr[:300])

# ── HUB INDEX (written AFTER subprocesses so it can't be overwritten) ─────────
hub_cards = ""
for label, href, emoji in ALL_PAGES:
    descs = {
        "/guide/budget-basics/": "The cheapest nutrient-dense foods in Australia. How to eat well for $7&ndash;12/day.",
        "/guide/nutrient-gaps/": "60% calcium, 48% zinc, 47% iron, 31% magnesium, 21% Vit D. Full food tables with costs.",
        "/guide/deficiency-symptoms/": "What falling short actually does &mdash; the 3-stage iron progression, Vit D and depression, DHA and postpartum.",
        "/guide/pre-conception/": "Both partners need to prepare. Zinc for sperm, folate for neural tubes, DHA for brain. 6 months before.",
        "/guide/pregnancy/": "Folate, iron, iodine and DHA needs &mdash; and the cheapest foods to meet them.",
        "/guide/hidden-hunger/": "Ultra-processed foods and children &mdash; the 2.57&times; deficiency risk, dopamine hijacking, ARFID, and what it does to developing brains.",
        "/guide/kids/": "Iron for brain development, calcium for bones, omega-3 for focus. Practical meals kids eat.",
        "/guide/nrv/": "Complete NHMRC reference tables for all demographics &mdash; children through elderly, pregnancy and lactation.",
        "/guide/arsenal/": "Tier 1/2/3 ranked system &mdash; the most nutrient-dense affordable foods in Australian supermarkets.",
        "/guide/batch-cooking/": "Cook once, eat all week. Freezer meals that slash your food bill without sacrificing nutrition.",
        "/guide/shopping/": "Unit pricing, frozen vs fresh, Aldi vs Woolworths, and what&rsquo;s never worth buying.",
        "/guide/cuisines/": "Mediterranean, Indian, Asian and Middle Eastern meals that are naturally cheap and nutritious.",
        "/guide/recipes/": "All 106 budget-optimised recipes &mdash; filterable by meal type, dietary preference and nutritional focus.",
        "/guide/disclaimer/": "About the author, sources used (NHMRC, ABS, USDA), methodology, and why this is general information &mdash; not medical advice.",
        "/guide/foods-for-gaps/": "A food-to-nutrient lookup table. Find the cheapest whole foods for every major gap: iron, calcium, zinc, B12, folate, omega-3 and more.",
        "/guide/macronutrients/": "AMDR ranges, energy requirements, protein RDA by age and sex, fibre and water targets. Complete reference tables from NHMRC and NASEM.",
        "/guide/daily-habits/": "Five daily habits that cover the most common Australian deficiencies &mdash; on a $47/week food budget. Plus weekly habits for the rest.",
        "/guide/absorption/": "Iron + Vitamin C, fat-soluble vitamins and fat, calcium timing, tea and coffee blocking, phytates and oxalates. Absorption rules that double what you get.",
        "/guide/sleep-nutrition/": "Magnesium, iron, Vitamin D and B vitamins all directly affect sleep. The nutritional causes of poor sleep &mdash; and what to eat about it.",
        "/guide/weston-price/": "Dr Price documented traditional diet communities in the 1930s. Vitamin K2, Activator X, pre-conception nutrition &mdash; and what modern science confirms.",
        "/guide/life-stages/": "Children, teenagers, adult women, adult men, and older adults each miss different nutrients. Includes the protein synthesis problem that affects everyone over 65.",
        "/guide/vegan-nutrition/": "B12 is mandatory. Iron, zinc and omega-3 need active strategies. Calcium and iodine need specific choices. The complete plant-based nutrient guide.",
        "/guide/exercise-nutrition/": "How being active changes what you need to eat. Protein timing, iron losses, magnesium in sweat, sarcopenia, and fuelling activity on a real budget.",
    }
    d = descs.get(href, "")
    hub_cards += f"""  <a class="card" href="{href}">
    <div class="card-icon">{emoji}</div>
    <div class="card-title">{label}</div>
    <div class="card-desc">{d}</div>
  </a>\n"""

hub_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Free Budget Nutrition Guide &mdash; OptimisedEats</title>
<meta name="description" content="Evidence-based nutrition guides for Australians and New Zealanders on a budget. Nutrient gaps, pre-conception, pregnancy, kids, recipes, NRV tables and more.">
<meta name="keywords" content="budget nutrition Australia, cheap healthy eating, family meal planning Australia, nutrient reference values, pre-conception nutrition">
<link rel="canonical" href="https://optimisedeats.com/guide/">
<meta property="og:title" content="Free Budget Nutrition Guide &mdash; OptimisedEats">
<meta property="og:description" content="20 evidence-based nutrition guides for Australians and New Zealanders.">
<meta property="og:url" content="https://optimisedeats.com/guide/">
<style>{CSS}{EXTRA_CSS}</style>
</head>
<body>
<header class="site-header">
  <div class="site-header-inner">
    <a class="logo" href="/"><span>Optimised</span>Eats</a>
    <a class="header-cta" href="/">Open Free App</a>
  </div>
</header>
<div class="breadcrumb"><a href="/">Home</a><span>&#8250;</span>Nutrition Guide</div>
<main>
<h1>Free Budget Nutrition Guide</h1>
<p class="lead">Evidence-based nutrition for Australians and New Zealanders on a real budget &mdash; covering every life stage, every common deficiency, and every meal type.</p>
<div class="card-grid">
{hub_cards}</div>
<div class="highlight-box">
  <h3>&#127462;&#127482; Built for Australian &amp; NZ prices</h3>
  <p>All food costs use current Coles / Woolworths / Aldi pricing. Our free app lets you build a full week&rsquo;s meal plan for your family&rsquo;s exact ages, sex, and dietary needs &mdash; and tracks all 17 nutrients automatically.</p>
  <p><a href="/">Try the free meal planner &rarr;</a></p>
</div>
<div style="background:linear-gradient(135deg,#f0fdf4,#dcfce7);border:1px solid #86efac;border-radius:12px;padding:20px 24px;margin:24px 0">
  <div style="font-size:15px;font-weight:800;color:#166534;margin-bottom:8px">&#11015; Download the complete guide &mdash; free</div>
  <div style="font-size:13px;color:#374151;margin-bottom:14px">All 26 topics in one file. Print it, read it offline, or load it on your e-reader. Free forever.</div>
  <div style="display:flex;gap:12px;flex-wrap:wrap">
    <a href="/budget-nutrition-guide.pdf" download style="background:#16a34a;color:#fff;padding:10px 20px;border-radius:8px;font-weight:700;font-size:13px;white-space:nowrap;text-decoration:none">&#128196; Download PDF</a>
    <a href="/budget-nutrition-ebook.epub" download style="background:#0f766e;color:#fff;padding:10px 20px;border-radius:8px;font-weight:700;font-size:13px;white-space:nowrap;text-decoration:none">&#128218; Download EPUB (e-reader)</a>
  </div>
</div>
<div class="related">
  <h2>Jump to a guide</h2>
  <div class="related-grid">{"".join(f'<a class="related-link" href="{h}">{l}</a>' for l,h,_ in ALL_PAGES)}</div>
</div>
</main>
<footer class="site-footer">
  <p>&#169; 2025 OptimisedEats &middot; <a href="/">Open App</a> &middot; <a href="/guide/">All Guides</a></p>
  <p style="margin-top:6px;font-size:11px;color:#cbd5e1">General educational purposes only. Not a substitute for personalised medical or dietary advice.</p>
</footer>
</body>
</html>"""

(BASE / "index.html").write_text(hub_html, encoding="utf-8")
print("DONE guide/index.html")

# ── IMPORT BODIES FROM EXISTING GENERATORS ────────────────────────────────────
# Rather than duplicate, just re-run the other scripts and collect their output,
# then rewrite with updated shells (consistent footer, related links, app-link boxes).
# We achieve this by importing bodies as strings here.

# ── RECIPES PAGE (regenerated with full recipe data) ──────────────────────────
recipes = json.loads((PROJECT / "recipes_extracted.json").read_text(encoding="utf-8"))

MEAT_TAGS = {"sardine", "kangaroo", "chicken", "organ-meat"}
for r in recipes:
    tag_set = set(r["tags"])
    if not tag_set & MEAT_TAGS and "vegetarian" not in tag_set:
        r["tags"].append("vegetarian")
    if "vegan" in tag_set and "vegetarian" not in r["tags"]:
        r["tags"].append("vegetarian")

TAG_LABELS = {
    "vegetarian":"Veggie","vegan":"Vegan","sardine":"Sardines","kangaroo":"Roo",
    "chicken":"Chicken","organ-meat":"Organ","kid-friendly":"Kids","quick":"Quick",
    "high-protein":"High Protein","freezer":"Freezer","pregnancy-safe":"Pregnancy",
    "omega-3":"Omega-3","iron":"Iron-rich",
}
FILTER_TAGS = list(TAG_LABELS.keys())
TYPE_LABELS = {"breakfast":("Breakfasts","&#127749;"),"lunch":("Lunches","&#9728;&#65039;"),
               "dinner":("Dinners","&#127769;"),"snack":("Snacks","&#127871;")}

def tag_html(tag):
    label = TAG_LABELS.get(tag, tag.replace("-"," ").title())
    cls = f"recipe-tag {tag}" if tag in ("sardine","kangaroo","organ-meat","vegan","vegetarian","kid-friendly","high-protein","quick") else "recipe-tag"
    return f'<span class="{cls}">{label}</span>'

def recipe_card(r):
    show = [t for t in r["tags"] if t in TAG_LABELS]
    tags = "".join(tag_html(t) for t in show)
    tag_sec = f'<div class="recipe-tags">{tags}</div>' if tags else ""
    return f'<div class="recipe-card" data-tags="{" ".join(r["tags"])}">\n  <div style="font-size:26px">{r["emoji"]}</div>\n  <div class="recipe-title">{r["name"]}</div>\n  <div class="recipe-meta"><span class="recipe-cost">${r["cost"]:.2f}/serve</span><span>&#183;</span><span>{r["time"]} min</span></div>\n  <div class="recipe-desc">{r["desc"]}</div>\n  {tag_sec}\n</div>'

sections_html = ""
for mtype,(label,emoji) in TYPE_LABELS.items():
    recs = sorted([r for r in recipes if r["type"]==mtype], key=lambda r: r["cost"])
    cards = "\n".join(recipe_card(r) for r in recs)
    sections_html += f'<div class="meal-section"><div class="section-header">{emoji} {label} <span class="recipe-count">({len(recs)} recipes)</span></div><div class="recipe-grid">{cards}</div></div>\n'

filter_btns = '<a class="filter-btn active" data-tag="all" href="javascript:void(0)" onclick="filterRecipes(\'all\')">All recipes</a>\n'
for tag in FILTER_TAGS:
    filter_btns += f'<a class="filter-btn" data-tag="{tag}" href="javascript:void(0)" onclick="filterRecipes(\'{tag}\')">{TAG_LABELS[tag]}</a>\n'

filter_js = """<script>
function filterRecipes(tag){
  document.querySelectorAll('.filter-btn').forEach(function(b){b.classList.toggle('active',b.dataset.tag===tag);});
  document.querySelectorAll('.recipe-card').forEach(function(c){
    c.style.display=(tag==='all'||(' '+c.dataset.tags+' ').indexOf(' '+tag+' ')!==-1)?'':'none';
  });
  document.querySelectorAll('.meal-section').forEach(function(s){
    s.style.display=s.querySelectorAll('.recipe-card:not([style*="none"])').length?'':'none';
  });
}
</script>"""

recipes_body = f"""<h1>Budget Recipe Index</h1>
<p class="lead">All 106 budget-optimised recipes from the OptimisedEats app &mdash; sorted by meal type and cost per serve. Filter by dietary preference or nutritional focus.</p>
<div class="highlight-box"><h3>How recipes are costed</h3><p>Per serve, based on current Coles / Woolworths / Aldi pricing. Pantry staples included at pro-rated costs. Prices vary by store and season.</p></div>
{app_link("Build a weekly plan with these recipes")}
<h2 style="margin-top:24px">Filter by type</h2>
<div class="filter-bar">{filter_btns}</div>
{sections_html}
<div class="cta-box"><h2>Build a full week&rsquo;s meal plan</h2><p>Add these recipes to a weekly planner, track nutrient coverage across your household, and generate a shopping list.</p><a class="cta-btn" href="/">Open the free app</a></div>
{filter_js}"""

p = BASE / "recipes"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(shell(
    "106 Budget Nutrition Recipes &mdash; OptimisedEats",
    "106 budget-optimised recipes for Australian families. Breakfasts, lunches, dinners and snacks built around sardines, eggs, lentils, kangaroo and other cheap nutrient-dense foods.",
    "budget recipes Australia, cheap healthy recipes, lentil recipes, sardine recipes, kangaroo recipes, family meal ideas Australia",
    "106 Recipes", "/guide/recipes/", recipes_body, other_related("/guide/recipes/")
), encoding="utf-8")
print("DONE guide/recipes/index.html")

# ── SITEMAP ───────────────────────────────────────────────────────────────────
import datetime
today = datetime.date.today().isoformat()

sitemap_urls = ["https://optimisedeats.com/", "https://optimisedeats.com/guide/"] + \
    [f"https://optimisedeats.com{h}" for _,h,_ in ALL_PAGES]

sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in sitemap_urls:
    priority = "1.0" if url == "https://optimisedeats.com/" else "0.9" if url == "https://optimisedeats.com/guide/" else "0.8"
    sitemap_xml += f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{priority}</priority>\n  </url>\n"
sitemap_xml += "</urlset>"

(PROJECT / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")
print(f"DONE sitemap.xml ({len(sitemap_urls)} URLs)")

# ── ZIP EVERYTHING FOR DEPLOY ─────────────────────────────────────────────────
out = PROJECT / "guide-all-deploy.zip"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
    for f in BASE.rglob("*.html"):
        arcname = f.relative_to(BASE)
        zf.write(f, arcname)
    zf.write(PROJECT / "sitemap.xml", "sitemap.xml")  # for root deploy

print(f"DONE guide-all-deploy.zip ({round(out.stat().st_size/1024)}KB)")
print(f"Total pages: {len(list(BASE.rglob('*.html')))}")
