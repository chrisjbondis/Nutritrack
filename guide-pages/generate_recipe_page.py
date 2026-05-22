"""Generate the full recipe index page for the guide hub.
Reads recipes_extracted.json (generated from budget-nutrition-app-LATEST.jsx).
"""
import json, pathlib

BASE = pathlib.Path(__file__).parent
PROJECT = BASE.parent
CSS = (BASE / "_shared.css").read_text(encoding="utf-8")

recipes = json.loads((PROJECT / "recipes_extracted.json").read_text(encoding="utf-8"))

# Derive vegetarian: no meat/fish tags present
MEAT_TAGS = {"sardine", "kangaroo", "chicken", "organ-meat"}
for r in recipes:
    tag_set = set(r["tags"])
    if not tag_set & MEAT_TAGS:
        if "vegetarian" not in tag_set:
            r["tags"].append("vegetarian")
    # vegan is a subset of vegetarian
    if "vegan" in tag_set and "vegetarian" not in r["tags"]:
        r["tags"].append("vegetarian")

EXTRA_CSS = """
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
"""

TYPE_LABELS = {
    "breakfast": ("Breakfasts", "🌅"),
    "lunch": ("Lunches", "☀️"),
    "dinner": ("Dinners", "🌙"),
    "snack": ("Snacks & Extras", "🍿"),
}

TAG_LABELS = {
    "vegetarian": "Veggie",
    "vegan": "Vegan",
    "sardine": "Sardines",
    "kangaroo": "Roo",
    "chicken": "Chicken",
    "organ-meat": "Organ",
    "kid-friendly": "Kids",
    "quick": "Quick",
    "high-protein": "High Protein",
    "freezer": "Freezer",
    "pregnancy-safe": "Pregnancy",
    "omega-3": "Omega-3",
    "iron": "Iron-rich",
}

FILTER_TAGS = ["vegetarian","vegan","sardine","kangaroo","chicken","organ-meat",
               "kid-friendly","quick","high-protein","freezer","pregnancy-safe","omega-3","iron"]

def render_tag(tag):
    label = TAG_LABELS.get(tag, tag.replace("-", " ").title())
    css_class = f"recipe-tag {tag}" if tag in ("sardine","kangaroo","organ-meat","vegan","vegetarian","kid-friendly","high-protein","quick") else "recipe-tag"
    return f'<span class="{css_class}">{label}</span>'

def render_card(r):
    show_tags = [t for t in r["tags"] if t in TAG_LABELS]
    tags_html = "".join(render_tag(t) for t in show_tags)
    tags_section = f'<div class="recipe-tags">{tags_html}</div>' if tags_html else ""
    return f"""<div class="recipe-card">
  <div style="font-size:26px">{r["emoji"]}</div>
  <div class="recipe-title">{r["name"]}</div>
  <div class="recipe-meta">
    <span class="recipe-cost">${r["cost"]:.2f}/serve</span>
    <span>&#183;</span>
    <span>{r["time"]} min</span>
  </div>
  <div class="recipe-desc">{r["desc"]}</div>
  {tags_section}
</div>"""

# Build filter JS
filter_js = """
<script>
function filterRecipes(tag) {
  var cards = document.querySelectorAll('.recipe-card');
  var btns = document.querySelectorAll('.filter-btn');
  btns.forEach(function(b){ b.classList.toggle('active', b.dataset.tag === tag); });
  cards.forEach(function(c){
    if (tag === 'all') { c.style.display=''; return; }
    var tags = c.dataset.tags || '';
    c.style.display = tags.indexOf(tag) !== -1 ? '' : 'none';
  });
  // Hide/show section headers based on visible cards
  document.querySelectorAll('.meal-section').forEach(function(section){
    var visible = section.querySelectorAll('.recipe-card:not([style*="none"])').length;
    section.style.display = visible ? '' : 'none';
  });
}
</script>
"""

# Build body
sections_html = ""
for mtype, (label, emoji) in TYPE_LABELS.items():
    type_recipes = [r for r in recipes if r["type"] == mtype]
    type_recipes.sort(key=lambda r: r["cost"])
    cards = ""
    for r in type_recipes:
        tag_str = " ".join(r["tags"])
        card = render_card(r).replace('<div class="recipe-card">', f'<div class="recipe-card" data-tags="{tag_str}">')
        cards += card + "\n"
    sections_html += f"""<div class="meal-section">
<div class="section-header">{emoji} {label} <span class="recipe-count">({len(type_recipes)} recipes)</span></div>
<div class="recipe-grid">
{cards}</div>
</div>
"""

filter_buttons = '<a class="filter-btn active" data-tag="all" href="javascript:void(0)" onclick="filterRecipes(\'all\')">All recipes</a>\n'
for tag in FILTER_TAGS:
    label = TAG_LABELS[tag]
    filter_buttons += f'<a class="filter-btn" data-tag="{tag}" href="javascript:void(0)" onclick="filterRecipes(\'{tag}\')">{label}</a>\n'

body_html = f"""
<h1>Budget Recipe Index</h1>
<p class="lead">All 106 budget-optimised recipes from the OptimisedEats app — sorted by meal type and cost. Each recipe is built around affordable, nutrient-dense ingredients with real prices from Australian supermarkets.</p>

<div class="highlight-box">
  <h3>How recipes are costed</h3>
  <p>Costs are per serve based on current Coles / Woolworths / Aldi pricing. Pantry staples (oil, salt, spices) are included at pro-rated costs. Prices are approximate and vary by store and season.</p>
</div>

<h2 style="margin-top:24px">Filter by type</h2>
<div class="filter-bar">
{filter_buttons}</div>

{sections_html}

<div class="cta-box">
  <h2>Build a full week's meal plan</h2>
  <p>The free app lets you add these recipes to a weekly planner, tracks your nutrient coverage across the household, and generates a shopping list — all in one place.</p>
  <a class="cta-btn" href="/">Open the free app</a>
</div>

{filter_js}
"""

ALL_RELATED = [
    ("Budget Basics", "/guide/budget-basics/"),
    ("Nutrient Gaps", "/guide/nutrient-gaps/"),
    ("Budget Arsenal", "/guide/arsenal/"),
    ("Pregnancy Nutrition", "/guide/pregnancy/"),
    ("Kids & Toddlers", "/guide/kids/"),
    ("Batch Cooking", "/guide/batch-cooking/"),
]

related = "".join(f'<a class="related-link" href="{h}">{l}</a>' for l,h in ALL_RELATED)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>106 Budget Nutrition Recipes — OptimisedEats</title>
<meta name="description" content="106 budget-optimised recipes for Australian families — breakfasts, lunches, dinners and snacks built around sardines, eggs, lentils, kangaroo and other cheap nutrient-dense foods. All under $5 per serve.">
<meta name="keywords" content="budget recipes Australia, cheap healthy recipes, lentil recipes, sardine recipes, egg recipes cheap, kangaroo recipes, family meal ideas Australia">
<link rel="canonical" href="https://optimisedeats.com/guide/recipes/">
<meta property="og:title" content="106 Budget Nutrition Recipes — OptimisedEats">
<meta property="og:description" content="106 budget-optimised recipes for Australian families — all under $5 per serve.">
<meta property="og:url" content="https://optimisedeats.com/guide/recipes/">
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
  <a href="/">Home</a><span>&#8250;</span><a href="/guide/">Nutrition Guide</a><span>&#8250;</span>Recipe Index
</div>
<main>
{body_html}
<div class="related">
  <h2>More guides</h2>
  <div class="related-grid">{related}</div>
</div>
</main>
<footer class="site-footer">
  <p>&#169; 2025 OptimisedEats &middot; Free nutrition planning for Australians &amp; New Zealanders &middot; <a href="/">Open App</a></p>
  <p style="margin-top:6px;font-size:11px;color:#cbd5e1">Prices are approximate based on current supermarket pricing and may vary. For general educational purposes only.</p>
</footer>
</body>
</html>"""

out = BASE / "recipes" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(html, encoding="utf-8")
print(f"DONE guide/recipes/index.html ({len(recipes)} recipes)")
