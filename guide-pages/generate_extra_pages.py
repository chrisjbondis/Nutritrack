"""Generate 6 additional guide pages from the book content."""
import pathlib

BASE = pathlib.Path(__file__).parent
CSS = (BASE / "_shared.css").read_text(encoding="utf-8")

EXTRA_CSS = """
.nutrient-section{margin:28px 0;padding:22px 24px;background:#fff;border:1px solid #e2e8f0;border-radius:12px}
.nutrient-section h2,.nutrient-section h3{border-top:none;margin-top:0;padding-top:0}
.callout{background:#f0fdf4;border-left:4px solid #16a34a;padding:14px 18px;border-radius:0 8px 8px 0;margin:16px 0}
.callout-amber{background:#fffbeb;border-left:4px solid #f59e0b;padding:14px 18px;border-radius:0 8px 8px 0;margin:16px 0}
.callout-red{background:#fef2f2;border-left:4px solid #dc2626;padding:14px 18px;border-radius:0 8px 8px 0;margin:16px 0}
.callout-blue{background:#eff6ff;border-left:4px solid #3b82f6;padding:14px 18px;border-radius:0 8px 8px 0;margin:16px 0}
.habit-item{display:flex;gap:14px;align-items:flex-start;padding:14px 0;border-bottom:1px solid #f1f5f9}
.habit-item:last-child{border-bottom:none}
.habit-num{font-size:22px;font-weight:900;color:#16a34a;flex-shrink:0;min-width:32px}
.habit-body{flex:1}
.habit-title{font-weight:700;color:#0f172a;font-size:15px;margin-bottom:3px}
.habit-detail{font-size:13px;color:#475569;line-height:1.5}
.habit-cost{display:inline-block;background:#f0fdf4;color:#166534;font-weight:700;font-size:12px;padding:1px 9px;border-radius:20px;margin-top:4px}
.absorption-row{display:flex;gap:12px;align-items:flex-start;padding:12px 0;border-bottom:1px solid #f1f5f9}
.absorption-row:last-child{border-bottom:none}
.absorption-icon{font-size:22px;flex-shrink:0}
.foods-table{width:100%;border-collapse:collapse;font-size:13px;margin:16px 0}
.foods-table th{background:#1e3a5f;color:#fff;padding:10px 12px;text-align:left;font-size:12px;font-weight:700}
.foods-table td{padding:9px 12px;border-bottom:1px solid #f1f5f9;vertical-align:top}
.foods-table tr:nth-child(even) td{background:#f8fafc}
.foods-table .primary{font-weight:700;color:#0f172a}
.foods-table .secondary{color:#475569}
.nutrient-label{font-weight:700;color:#1e3a5f}
.sleep-stat{display:inline-block;background:#eff6ff;color:#1d4ed8;font-weight:800;font-size:13px;padding:2px 10px;border-radius:20px;margin-left:6px}
.price-tag{font-weight:700;color:#16a34a;white-space:nowrap}
.data-table{width:100%;border-collapse:collapse;font-size:13px;margin:12px 0}
.data-table th{background:#f1f5f9;color:#374151;padding:8px 10px;text-align:left;font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.3px}
.data-table td{padding:8px 10px;border-bottom:1px solid #f1f5f9;vertical-align:top}
.data-table th:not(:first-child),.data-table td:not(:first-child){text-align:center}
.app-link-box{background:linear-gradient(135deg,#f0fdf4,#dcfce7);border:1px solid #86efac;border-radius:12px;padding:16px 20px;margin:24px 0;display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}
.app-link-box p{margin:0;font-size:14px;color:#166534}
.app-link-btn{background:#16a34a;color:#fff;padding:8px 18px;border-radius:8px;font-weight:700;font-size:13px;white-space:nowrap;text-decoration:none}
.wap-quote{background:#fdf6e3;border-left:4px solid #d97706;padding:14px 18px;border-radius:0 8px 8px 0;margin:16px 0;font-style:italic;color:#78350f}
"""

ALL_RELATED = [
    ("Budget Basics",           "/guide/budget-basics/"),
    ("Nutrient Gaps",           "/guide/nutrient-gaps/"),
    ("Deficiency Symptoms",     "/guide/deficiency-symptoms/"),
    ("Pre-Conception",          "/guide/pre-conception/"),
    ("Pregnancy Nutrition",     "/guide/pregnancy/"),
    ("Hidden Hunger",           "/guide/hidden-hunger/"),
    ("Kids &amp; Toddlers",     "/guide/kids/"),
    ("NRV Reference Tables",    "/guide/nrv/"),
    ("Budget Arsenal",          "/guide/arsenal/"),
    ("Batch Cooking",           "/guide/batch-cooking/"),
    ("Smart Shopping",          "/guide/shopping/"),
    ("World Cuisines",          "/guide/cuisines/"),
    ("106 Recipes",             "/guide/recipes/"),
    ("Disclaimer",              "/guide/disclaimer/"),
    ("Which Foods Fill Gaps",   "/guide/foods-for-gaps/"),
    ("Macronutrients",          "/guide/macronutrients/"),
    ("5 Daily Habits",          "/guide/daily-habits/"),
    ("Absorption Tips",         "/guide/absorption/"),
    ("Sleep &amp; Nutrition",   "/guide/sleep-nutrition/"),
    ("Weston A. Price",         "/guide/weston-price/"),
]

def related_for(current_path):
    return [(l, h) for l, h in ALL_RELATED if h != current_path]

def page(title, desc, keywords, breadcrumb_label, canonical, body_html, related_links):
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
<meta name="author" content="Chris &mdash; OptimisedEats">
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
  <p>&#169; 2025 OptimisedEats &middot; Free nutrition planning for Australians &amp; New Zealanders &middot; <a href="/">Open App</a> &middot; <a href="/guide/">All Guides</a> &middot; <a href="/budget-nutrition-guide.pdf" download>Download PDF</a></p>
  <p style="margin-top:6px;font-size:11px;color:#cbd5e1">Based on NHMRC Australian Nutrient Reference Values and peer-reviewed research. General educational purposes only &mdash; not a substitute for personalised medical advice.</p>
</footer>
</body>
</html>"""

def app_link(text="Track this in the free app"):
    return f"""<div class="app-link-box">
  <p>&#128247; <strong>{text}</strong> &mdash; enter your household members and see how your meals measure up against their exact targets.</p>
  <a class="app-link-btn" href="/">Open free app</a>
</div>"""

# ── PAGE 1: WHICH FOODS FILL WHICH GAPS ───────────────────────────────────────
foods_rows = [
    ("Protein",         "Eggs, lentils, beans, milk, liver",                    "Oats, rice, peanut butter, canned fish"),
    ("Fibre",           "Lentils, oats, beans, brown rice",                     "Potatoes, bananas, cabbage, vegetables"),
    ("Vitamin A",       "Liver (retinol), carrots, sweet potato, spinach",      "Canned tomatoes, eggs"),
    ("Vitamin B12",     "Liver, sardines, eggs, milk",                          "Canned tuna, fortified cereal"),
    ("Folate (B9)",     "Liver, lentils, spinach, canned beans",                "Fortified cereal, cabbage, eggs"),
    ("Vitamin C",       "Cabbage, potatoes, canned tomatoes, broccoli",         "Bananas, spinach, seasonal citrus"),
    ("Vitamin D",       "Sardines, eggs, fortified milk",                       "Sunlight exposure (free!)"),
    ("Vitamin K",       "Spinach / kale, cabbage, broccoli",                    "Eggs, olive oil"),
    ("Calcium",         "Milk, sardines (with bones), fortified cereal",        "Cabbage, canned beans, cheese"),
    ("Iron",            "Liver, lentils, beans, spinach",                       "Fortified cereal, oats, eggs"),
    ("Zinc",            "Liver, beans, lentils, eggs",                          "Oats, pumpkin seeds, milk"),
    ("Magnesium",       "Lentils, spinach, brown rice, pumpkin seeds",          "Oats, bananas, canned beans"),
    ("Potassium",       "Potatoes, lentils, bananas, beans",                    "Spinach, milk, canned tomatoes"),
    ("Omega-3 DHA/EPA", "Sardines, canned salmon",                              "Omega-3 enriched eggs"),
    ("Choline",         "Liver, eggs",                                          "Beans, milk, potatoes"),
    ("Iodine",          "Milk, eggs, sardines, iodised salt",                   "Seaweed (small amounts)"),
]

foods_table_html = """<table class="foods-table">
<thead><tr><th>Nutrient</th><th>Primary Budget Sources</th><th>Secondary Sources</th></tr></thead>
<tbody>"""
for nutrient, primary, secondary in foods_rows:
    foods_table_html += f"""<tr>
  <td><span class="nutrient-label">{nutrient}</span></td>
  <td class="primary">{primary}</td>
  <td class="secondary">{secondary}</td>
</tr>"""
foods_table_html += "</tbody></table>"

foods_body = f"""<h1>Which Foods Fill Which Nutrient Gaps?</h1>
<p class="lead">A practical food-to-nutrient lookup matrix. Use this to make sure your weekly meals cover all major targets &mdash; without needing a nutrition degree.</p>

<div class="callout">
  <strong>How to use this table:</strong> Find a nutrient you need more of &mdash; then look left for the cheapest whole-food sources. Primary sources give the highest amount per dollar. Secondary sources are useful top-ups.
</div>

{foods_table_html}

<h2>Budget shortcuts &mdash; the foods that appear most often</h2>
<div class="nutrient-section">
  <div class="habit-item">
    <div class="habit-num">&#129351;</div>
    <div class="habit-body">
      <div class="habit-title">Liver &mdash; the most complete budget food</div>
      <div class="habit-detail">Appears in: Vitamin A, B12, Folate, Iron, Zinc, Choline. One 100g serve of chicken liver covers your weekly B12, daily Vitamin A, and over 50% of your iron target &mdash; for under $1.50. Hidden in bolognese or stir-fry, most families don&rsquo;t notice.</div>
      <span class="habit-cost">~$1.50 per serve</span>
    </div>
  </div>
  <div class="habit-item">
    <div class="habit-num">&#129408;</div>
    <div class="habit-body">
      <div class="habit-title">Eggs &mdash; appear in 8 out of 16 nutrients</div>
      <div class="habit-detail">B12, Vitamin A, Vitamin D, Vitamin K, Calcium, Iron, Zinc, Choline. Two eggs a day covers a meaningful chunk of most fat-soluble vitamin needs and provides 12g complete protein.</div>
      <span class="habit-cost">~$0.60 per 2 eggs</span>
    </div>
  </div>
  <div class="habit-item">
    <div class="habit-num">&#129419;</div>
    <div class="habit-body">
      <div class="habit-title">Sardines (canned, with bones) &mdash; the best value omega-3 source</div>
      <div class="habit-detail">B12, Vitamin D, Calcium, Omega-3. The bones are edible and provide calcium equivalent to a glass of milk. One tin twice a week covers your weekly omega-3 and Vitamin D targets.</div>
      <span class="habit-cost">~$1.80 per tin</span>
    </div>
  </div>
  <div class="habit-item">
    <div class="habit-num">&#129368;</div>
    <div class="habit-body">
      <div class="habit-title">Lentils &mdash; the most versatile plant source</div>
      <div class="habit-detail">Protein, Fibre, Folate, Iron, Zinc, Magnesium, Potassium. A 400g can of lentils provides roughly 25g protein and 16g fibre for under $1.50. Combine with Vitamin C (lemon, tomato, capsicum) to triple iron absorption.</div>
      <span class="habit-cost">~$1.40 per 400g tin</span>
    </div>
  </div>
</div>

<h2>The absorption rules you can&rsquo;t ignore</h2>
<div class="callout">
  <strong>Iron + Vitamin C:</strong> Always consume iron-rich foods (lentils, spinach, fortified cereal) with a Vitamin C source &mdash; lemon juice, capsicum, tomato. Can triple absorption.
</div>
<div class="callout">
  <strong>Fat-soluble vitamins (A, D, E, K):</strong> Always eat with some fat &mdash; cook vegetables in olive oil or serve alongside eggs. Without fat, beta-carotene from carrots/sweet potato is barely absorbed.
</div>
<div class="callout-amber">
  <strong>Tea and coffee:</strong> Wait 1 hour before or after meals. Tannins reduce iron absorption by 60&ndash;90% when consumed with plant-iron foods.
</div>
<p>See the full <a href="/guide/absorption/">Nutrient Absorption Tips guide</a> for detailed rules.</p>

{app_link("See if your week covers all these nutrients")}

<div class="cta-box">
  <h2>See your household&rsquo;s specific targets</h2>
  <p>Add your family members to the free app &mdash; it calculates exact targets for each person&rsquo;s age and sex, then tracks nutrient coverage across your weekly meals.</p>
  <a class="cta-btn" href="/">Open the free app</a>
</div>

<p style="font-size:12px;color:#94a3b8;margin-top:24px">Sources: NHMRC Australian Nutrient Reference Values (2006, updated 2017) &middot; USDA FoodData Central &middot; Nutrient data based on standard serve sizes from Australian supermarkets.</p>"""

p = BASE / "foods-for-gaps"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "Which Foods Fill Which Nutrient Gaps? &mdash; OptimisedEats",
    "A practical food-to-nutrient lookup table for Australians. Find the cheapest whole foods for every major nutrient: iron, calcium, zinc, B12, folate, omega-3 and more.",
    "which foods have iron Australia, calcium sources budget, best zinc foods, B12 foods, folate foods Australia, cheap nutrient dense foods",
    "Which Foods Fill Gaps", "/guide/foods-for-gaps/", foods_body, related_for("/guide/foods-for-gaps/")
), encoding="utf-8")
print("DONE guide/foods-for-gaps/index.html")


# ── PAGE 2: MACRONUTRIENTS ────────────────────────────────────────────────────
macro_body = """<h1>Macronutrient Requirements by Age &amp; Sex</h1>
<p class="lead">Protein, carbohydrate, fat, fibre, and water targets for every life stage &mdash; based on Australian NHMRC and US NASEM reference values.</p>

<div class="callout-blue">
  <strong>What are macronutrients?</strong> They&rsquo;re the nutrients your body needs in large quantities: protein, carbohydrates, and fat &mdash; plus fibre and water. Unlike micronutrients (vitamins and minerals), they&rsquo;re measured in grams rather than micrograms.
</div>

<h2>Acceptable Macronutrient Distribution Ranges (AMDR)</h2>
<p>These are the recommended ranges for each macronutrient as a percentage of total daily energy. Staying within these ranges is associated with adequate micronutrient intake and reduced chronic disease risk.</p>
<table class="data-table">
<thead><tr><th>Age Group</th><th>Protein</th><th>Carbohydrate</th><th>Fat</th></tr></thead>
<tbody>
<tr><td>Children 1&ndash;3</td><td>5&ndash;20%</td><td>45&ndash;65%</td><td>30&ndash;40%</td></tr>
<tr><td>Children 4&ndash;18</td><td>10&ndash;30%</td><td>45&ndash;65%</td><td>25&ndash;35%</td></tr>
<tr><td>Adults 19+</td><td>10&ndash;35%</td><td>45&ndash;65%</td><td>20&ndash;35%</td></tr>
<tr><td>Pregnancy / Lactation</td><td>10&ndash;35%</td><td>45&ndash;65%</td><td>20&ndash;35%</td></tr>
</tbody>
</table>

<h2>Daily Energy Requirements</h2>
<p>Values below are in kilocalories (kcal) based on activity level. &ldquo;Sedentary&rdquo; means less than 30 min light activity per day. &ldquo;Moderate&rdquo; is 30&ndash;60 min daily. &ldquo;Active&rdquo; is 60+ min daily.</p>
<table class="data-table">
<thead><tr><th>Age/Sex Group</th><th>Sedentary</th><th>Moderate</th><th>Active</th></tr></thead>
<tbody>
<tr><td>Children 2&ndash;3</td><td>1,000</td><td>1,000&ndash;1,400</td><td>1,000&ndash;1,400</td></tr>
<tr><td>Girls 4&ndash;8</td><td>1,200</td><td>1,400&ndash;1,600</td><td>1,400&ndash;1,800</td></tr>
<tr><td>Boys 4&ndash;8</td><td>1,400</td><td>1,400&ndash;1,600</td><td>1,600&ndash;2,000</td></tr>
<tr><td>Girls 9&ndash;13</td><td>1,600</td><td>1,600&ndash;2,000</td><td>1,800&ndash;2,200</td></tr>
<tr><td>Boys 9&ndash;13</td><td>1,800</td><td>1,800&ndash;2,200</td><td>2,000&ndash;2,600</td></tr>
<tr><td>Females 14&ndash;18</td><td>1,800</td><td>2,000</td><td>2,400</td></tr>
<tr><td>Males 14&ndash;18</td><td>2,200</td><td>2,400&ndash;2,800</td><td>2,800&ndash;3,200</td></tr>
<tr><td>Females 19&ndash;30</td><td>2,000</td><td>2,000&ndash;2,200</td><td>2,400</td></tr>
<tr><td>Males 19&ndash;30</td><td>2,400</td><td>2,600&ndash;2,800</td><td>3,000</td></tr>
<tr><td>Females 31&ndash;50</td><td>1,800</td><td>2,000</td><td>2,200</td></tr>
<tr><td>Males 31&ndash;50</td><td>2,200</td><td>2,400&ndash;2,600</td><td>2,800&ndash;3,000</td></tr>
<tr><td>Females 51&ndash;70</td><td>1,600</td><td>1,800</td><td>2,000&ndash;2,200</td></tr>
<tr><td>Males 51&ndash;70</td><td>2,000</td><td>2,200&ndash;2,400</td><td>2,400&ndash;2,800</td></tr>
<tr><td>Females 71+</td><td>1,600</td><td>1,800</td><td>2,000</td></tr>
<tr><td>Males 71+</td><td>2,000</td><td>2,200</td><td>2,400</td></tr>
<tr><td>Pregnant (2nd tri)</td><td colspan="3" style="text-align:center">+340 kcal/day above baseline</td></tr>
<tr><td>Pregnant (3rd tri)</td><td colspan="3" style="text-align:center">+452 kcal/day above baseline</td></tr>
<tr><td>Lactating (0&ndash;6 mo)</td><td colspan="3" style="text-align:center">+330 kcal/day above baseline</td></tr>
<tr><td>Lactating (6&ndash;12 mo)</td><td colspan="3" style="text-align:center">+400 kcal/day above baseline</td></tr>
</tbody>
</table>

<h2>Protein RDA (grams per day)</h2>
<table class="data-table">
<thead><tr><th>Age/Sex Group</th><th>RDA (g/day)</th><th>Per kg body weight</th></tr></thead>
<tbody>
<tr><td>Children 1&ndash;3</td><td>13 g</td><td>1.05 g/kg</td></tr>
<tr><td>Children 4&ndash;8</td><td>19 g</td><td>0.95 g/kg</td></tr>
<tr><td>Girls 9&ndash;13</td><td>34 g</td><td>0.87 g/kg</td></tr>
<tr><td>Boys 9&ndash;13</td><td>34 g</td><td>0.87 g/kg</td></tr>
<tr><td>Females 14&ndash;18</td><td>46 g</td><td>0.77 g/kg</td></tr>
<tr><td>Males 14&ndash;18</td><td>52 g</td><td>0.77 g/kg</td></tr>
<tr><td>Females 19&ndash;70+</td><td>46 g</td><td>0.75 g/kg</td></tr>
<tr><td>Males 19&ndash;70+</td><td>64 g</td><td>0.84 g/kg</td></tr>
<tr><td>Pregnant</td><td>60 g</td><td>+10 g above baseline</td></tr>
<tr><td>Lactating</td><td>67 g</td><td>+16 g above baseline</td></tr>
</tbody>
</table>

<div class="callout-amber">
  <strong>Older adults:</strong> Many experts recommend 1.0&ndash;1.2 g/kg/day for adults over 65 to prevent sarcopenia (age-related muscle loss) &mdash; significantly higher than the standard RDA of 0.75&ndash;0.84 g/kg.
</div>

<h2>Understanding Net Protein &mdash; food weight vs actual protein</h2>
<div class="nutrient-section">
  <p>When a food is listed as containing protein, that&rsquo;s the protein content by weight &mdash; not the weight of the food itself. This is one of the most common sources of confusion when meal planning.</p>
  <p><strong>Example:</strong> 150g of raw chicken breast contains approximately 33g of protein (about 22% by weight after cooking). Not 150g of protein.</p>
  <h3>Common foods &mdash; protein per 100g (cooked / as eaten)</h3>
  <table class="data-table">
  <thead><tr><th>Food</th><th>Protein per 100g</th></tr></thead>
  <tbody>
  <tr><td>Chicken breast</td><td>~31g</td></tr>
  <tr><td>Beef mince (lean)</td><td>~26g</td></tr>
  <tr><td>Canned tuna</td><td>~25g</td></tr>
  <tr><td>Canned sardines</td><td>~22g</td></tr>
  <tr><td>Cheddar cheese</td><td>~25g</td></tr>
  <tr><td>Eggs (whole)</td><td>~13g</td></tr>
  <tr><td>Greek yoghurt</td><td>~10g</td></tr>
  <tr><td>Oats (dry)</td><td>~17g</td></tr>
  <tr><td>Firm tofu</td><td>~8g</td></tr>
  <tr><td>Cooked lentils</td><td>~9g</td></tr>
  <tr><td>Cooked chickpeas</td><td>~8.9g</td></tr>
  <tr><td>Cow&rsquo;s milk</td><td>~3.4g</td></tr>
  </tbody>
  </table>
  <div class="callout">
    <strong>Bioavailability:</strong> Animal proteins are 90&ndash;99% digestible. Plant proteins are typically 50&ndash;80% digestible, and most are low in at least one essential amino acid &mdash; so vegans and vegetarians need roughly 10&ndash;20% more total protein to absorb the same amount.
  </div>
  <div class="callout-blue">
    <strong>Leucine threshold:</strong> Muscle protein synthesis requires approximately 2.5&ndash;3g of leucine per meal. Three meals of 30g protein stimulates muscle growth more effectively than one meal of 90g. Distribution across the day matters &mdash; especially for older adults.
  </div>
</div>

<h2>Fibre (Adequate Intake)</h2>
<p>Most Australians get approximately 20g/day &mdash; well below target for most demographics. Fibre is the most commonly underconsumed macronutrient.</p>
<table class="data-table">
<thead><tr><th>Age/Sex Group</th><th>AI (g/day)</th></tr></thead>
<tbody>
<tr><td>Children 1&ndash;3</td><td>14 g</td></tr>
<tr><td>Children 4&ndash;8</td><td>18 g</td></tr>
<tr><td>Girls 9&ndash;13</td><td>20 g</td></tr>
<tr><td>Boys 9&ndash;13</td><td>24 g</td></tr>
<tr><td>Females 14&ndash;18</td><td>22 g</td></tr>
<tr><td>Males 14&ndash;18</td><td>28 g</td></tr>
<tr><td>Females 19&ndash;50</td><td>25 g</td></tr>
<tr><td>Males 19&ndash;50</td><td>30 g</td></tr>
<tr><td>Females 51+</td><td>22 g</td></tr>
<tr><td>Males 51+</td><td>25 g</td></tr>
<tr><td>Pregnant</td><td>25&ndash;28 g</td></tr>
</tbody>
</table>
<div class="callout">
  <strong>Best budget fibre sources:</strong> Lentils (8g/100g cooked), oats (10g/100g dry), canned beans (6&ndash;8g/100g), brown rice (1.8g/100g cooked), potatoes with skin (2.2g/100g). A bowl of oats + a tin of lentils in a meal = roughly 18&ndash;22g fibre alone.
</div>

<h2>Water (Adequate Intake)</h2>
<table class="data-table">
<thead><tr><th>Age/Sex Group</th><th>AI (L/day &mdash; all sources)</th></tr></thead>
<tbody>
<tr><td>Children 1&ndash;3</td><td>1.3 L</td></tr>
<tr><td>Children 4&ndash;8</td><td>1.7 L</td></tr>
<tr><td>Girls 9&ndash;13</td><td>2.1 L</td></tr>
<tr><td>Boys 9&ndash;13</td><td>2.4 L</td></tr>
<tr><td>Females 14&ndash;18</td><td>2.3 L</td></tr>
<tr><td>Males 14&ndash;18</td><td>3.3 L</td></tr>
<tr><td>Females 19+</td><td>2.7 L</td></tr>
<tr><td>Males 19+</td><td>3.7 L</td></tr>
<tr><td>Pregnant</td><td>3.0 L</td></tr>
<tr><td>Lactating</td><td>3.8 L</td></tr>
</tbody>
</table>

<div class="callout-blue">
  <strong>All sources count:</strong> The daily target includes all fluid &mdash; not just plain water. Approximately 20&ndash;30% comes from food alone. Cucumber (96% water), tomatoes (94%), oranges (87%), milk (87%), oats with milk &mdash; all contribute. A typical vegetable-rich day provides 700&ndash;900 mL from food before drinking anything. Tea and coffee count too (contrary to myth, moderate caffeine does not cause net fluid loss).
</div>
<div class="callout-amber">
  <strong>Signs you&rsquo;re under-hydrated:</strong> urine darker than pale yellow, afternoon headaches, constipation, fatigue, difficulty concentrating. These often appear before thirst does.
</div>

<p>See the <a href="/guide/nrv/">full NRV Reference Tables</a> for detailed micronutrient targets by age and sex. For foods that cover these nutrients on a budget, see the <a href="/guide/foods-for-gaps/">Which Foods Fill Which Gaps</a> guide.</p>

<p style="font-size:12px;color:#94a3b8;margin-top:24px">Sources: NHMRC Australian Nutrient Reference Values (2006, updated 2017) &middot; Dietary Guidelines for Americans 2020&ndash;2025 (USDA/HHS) &middot; Institute of Medicine Dietary Reference Intakes for Energy, Carbohydrate, Fiber, Fat, Fatty Acids, Cholesterol, Protein, and Amino Acids (2005)</p>"""

p = BASE / "macronutrients"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "Macronutrient Requirements by Age &amp; Sex &mdash; OptimisedEats",
    "Complete tables for protein, carbohydrate, fat, fibre and water targets for every life stage. Based on Australian NHMRC and US NASEM reference values.",
    "macronutrient requirements Australia, protein RDA Australia, daily fibre intake, water intake Australia, AMDR Australia, protein per kg age",
    "Macronutrients", "/guide/macronutrients/", macro_body, related_for("/guide/macronutrients/")
), encoding="utf-8")
print("DONE guide/macronutrients/index.html")


# ── PAGE 3: 5 DAILY HABITS ────────────────────────────────────────────────────
habits_body = """<h1>5 Daily Habits That Cover Most Nutrient Gaps</h1>
<p class="lead">Meeting Australian NRV targets and physical activity guidelines simultaneously &mdash; at minimal cost &mdash; is entirely achievable. Five daily habits cover the vast majority of common deficiencies.</p>

<div class="callout">
  <strong>The principle:</strong> Rather than tracking 17 nutrients individually, these habits act as a system. Do all five daily, add the weekly habits below, and you&rsquo;ll cover the nutritional gaps that affect the majority of Australians.
</div>

<h2>The five daily habits</h2>
<div class="nutrient-section">
  <div class="habit-item">
    <div class="habit-num">1</div>
    <div class="habit-body">
      <div class="habit-title">2 eggs</div>
      <div class="habit-detail">Covers: B12, choline, selenium, Vitamin D, and protein. Two eggs provides 12g complete protein, 1.2&micro;g B12 (half the daily RDI), 150mg choline, and 80&ndash;100 IU Vitamin D. But the most important reason to make this your <em>first</em> meal component: after an overnight fast, your body is in a catabolic state &mdash; breaking down muscle protein for fuel. The leucine threshold to flip this to anabolic is ~3g, requiring 30&ndash;40g of quality protein. Two eggs alone (~12g) don&rsquo;t get you there &mdash; pair them with Greek yoghurt or a glass of milk to hit the threshold and stop the overnight breakdown. See the <a href="/guide/exercise-nutrition/">full catabolic cycle explainer</a>.</div>
      <span class="habit-cost">~$0.60 (pair with yoghurt to hit the threshold)</span>
    </div>
  </div>
  <div class="habit-item">
    <div class="habit-num">2</div>
    <div class="habit-body">
      <div class="habit-title">Dairy &mdash; yoghurt or 250 mL milk</div>
      <div class="habit-detail">Covers: calcium and iodine. A 200g serve of yoghurt provides approximately 300mg calcium (30% of adult RDI). Iodine in Australian dairy averages 50&ndash;70&micro;g per 250mL &mdash; a meaningful contribution to the 150&micro;g daily target. Choose plain, unsweetened yoghurt for the best nutritional value per dollar.</div>
      <span class="habit-cost">~$0.40&ndash;0.70</span>
    </div>
  </div>
  <div class="habit-item">
    <div class="habit-num">3</div>
    <div class="habit-body">
      <div class="habit-title">Citrus or capsicum &mdash; any Vitamin C source</div>
      <div class="habit-detail">Covers: Vitamin C (the iron absorption multiplier). Adding Vitamin C to any plant-iron meal can triple iron absorption. Half a capsicum, a squeeze of lemon juice, a small orange, or a handful of frozen broccoli all deliver 40&ndash;80mg &mdash; well above the 75&ndash;90mg RDI. The cheapest option is often a squeeze of lemon on lentils.</div>
      <span class="habit-cost">~$0.20&ndash;0.40</span>
    </div>
  </div>
  <div class="habit-item">
    <div class="habit-num">4</div>
    <div class="habit-body">
      <div class="habit-title">30 min brisk walk</div>
      <div class="habit-detail">Covers: Australian physical activity guidelines, bone loading (weight-bearing exercise), and Vitamin D synthesis. A 30-minute walk with arms and legs exposed in reasonable UV conditions generates 400&ndash;1,000 IU of Vitamin D. This is your free Vitamin D supplement. It also meets the minimum daily moderate activity target for adults.</div>
      <span class="habit-cost">Free</span>
    </div>
  </div>
  <div class="habit-item">
    <div class="habit-num">5</div>
    <div class="habit-body">
      <div class="habit-title">A handful of leafy greens</div>
      <div class="habit-detail">Covers: folate, Vitamin K, magnesium, Vitamin A. A 60g handful of spinach, silverbeet, or kale delivers roughly 130&micro;g folate (30% of the 400&micro;g RDI), 300&micro;g Vitamin K, 50mg magnesium, and significant Vitamin A as beta-carotene. Cook in olive oil to improve absorption of the fat-soluble vitamins.</div>
      <span class="habit-cost">~$0.20</span>
    </div>
  </div>
</div>

<h2>Weekly habits that cover the rest</h2>
<div class="nutrient-section">
  <div class="habit-item">
    <div class="habit-num">&#127371;</div>
    <div class="habit-body">
      <div class="habit-title">Organ meat once a week &mdash; chicken liver works best</div>
      <div class="habit-detail">One 100g serve of chicken liver covers: B12 for the entire week, your daily Vitamin A target, half your weekly iron target, and significant folate and zinc. Hidden in bolognese or a stir-fry with strong spices, most families don&rsquo;t detect it. This is the single highest return-on-investment food in Australian supermarkets.</div>
      <span class="habit-cost">~$1.00&ndash;1.50 per serve</span>
    </div>
  </div>
  <div class="habit-item">
    <div class="habit-num">&#129419;</div>
    <div class="habit-body">
      <div class="habit-title">Sardines once a week</div>
      <div class="habit-detail">Covers: Vitamin D, omega-3 (DHA/EPA), calcium (the bones), and B12. One tin provides approximately 400&ndash;500 IU Vitamin D, 1,500mg omega-3, and 350mg calcium &mdash; equivalent to a glass of milk. Two tins a week covers most adults&rsquo; weekly omega-3 target.</div>
      <span class="habit-cost">~$1.80 per tin</span>
    </div>
  </div>
  <div class="habit-item">
    <div class="habit-num">&#128170;</div>
    <div class="habit-body">
      <div class="habit-title">2 &times; strength training sessions</div>
      <div class="habit-detail">Preserves muscle mass, bone density, and insulin sensitivity &mdash; the three things that decline fastest with age and inactivity. No gym required: resistance bands, bodyweight exercises, or heavy household tasks all count. Australian guidelines recommend muscle-strengthening activities at least 2 days per week for adults.</div>
      <span class="habit-cost">Free</span>
    </div>
  </div>
  <div class="habit-item">
    <div class="habit-num">&#127811;</div>
    <div class="habit-body">
      <div class="habit-title">Legumes 3&ndash;4 times a week</div>
      <div class="habit-detail">Lentils, chickpeas, kidney beans, and cannellini beans: plant protein, fibre, magnesium, zinc, folate, and iron. At $1.40&ndash;1.80 per 400g tin (roughly 3&ndash;4 serves), they&rsquo;re the cheapest protein source available. Always pair with Vitamin C to maximise iron absorption.</div>
      <span class="habit-cost">~$0.25&ndash;0.50 per serve</span>
    </div>
  </div>
</div>

<h2>What this costs</h2>
<div class="highlight-box">
  <h3>&#128176; Weekly budget summary</h3>
  <p><strong>Single adult</strong> meeting all NRV targets and PA guidelines: <strong>~$47&ndash;55/week</strong> on food.</p>
  <p><strong>Family of 4</strong> following this framework: <strong>~$107&ndash;125/week</strong>.</p>
  <p>Gym membership or supplements: not required. Sun, eggs, sardines, liver, lentils, and a park cover the vast majority of needs for most demographics.</p>
</div>

<p>For food cost comparisons and the full <strong>tier 1/2/3 ranked food list</strong>, see the <a href="/guide/arsenal/">Budget Nutrition Arsenal</a>. For the weekly shopping list with prices, see <a href="/guide/shopping/">Smart Shopping</a>.</p>

<p style="font-size:12px;color:#94a3b8;margin-top:24px">Sources: NHMRC Australian Nutrient Reference Values (2006, updated 2017) &middot; Department of Health Australian Physical Activity &amp; Sedentary Behaviour Guidelines (2021) &middot; ABS National Nutrition &amp; Physical Activity Survey 2023 &middot; USDA FoodData Central nutrient database</p>"""

p = BASE / "daily-habits"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "5 Daily Habits That Cover Most Nutrient Gaps &mdash; OptimisedEats",
    "Five daily habits that cover the most common Australian nutrient deficiencies. Calcium, iron, B12, Vitamin D, folate and omega-3 &mdash; all on a $47/week food budget.",
    "daily nutrition habits Australia, how to eat healthy on a budget, nutrient gap fix Australia, cheap healthy eating habits, 5 foods daily nutrition",
    "5 Daily Habits", "/guide/daily-habits/", habits_body, related_for("/guide/daily-habits/")
), encoding="utf-8")
print("DONE guide/daily-habits/index.html")


# ── PAGE 4: ABSORPTION TIPS ───────────────────────────────────────────────────
absorption_body = """<h1>Nutrient Absorption Tips</h1>
<p class="lead">Eating the right foods is only half the equation &mdash; absorption determines how much you actually get. These rules can double or triple the effectiveness of what you already eat.</p>

<h2>Absorption enhancers</h2>
<div class="nutrient-section">
  <div class="absorption-row">
    <div class="absorption-icon">&#9889;</div>
    <div>
      <strong>Iron + Vitamin C (the most important pairing)</strong><br>
      <span style="font-size:13px;color:#475569">Eating Vitamin C-rich foods (tomato, capsicum, lemon, broccoli, potato) alongside plant-iron foods (lentils, beans, spinach, fortified cereal) increases non-heme iron absorption by 2&ndash;4&times;. This single habit can be the difference between borderline and adequate iron status for vegetarians and women of reproductive age. Always add a squeeze of lemon or some capsicum to legume-based meals.</span>
    </div>
  </div>
  <div class="absorption-row">
    <div class="absorption-icon">&#129697;</div>
    <div>
      <strong>Fat-soluble vitamins (A, D, E, K) + dietary fat</strong><br>
      <span style="font-size:13px;color:#475569">Vitamins A, D, E, and K require dietary fat to be absorbed from the gut. Cooking orange and green vegetables in olive oil, serving them with eggs, or adding a small amount of butter significantly improves absorption of beta-carotene and Vitamin K. Without fat, most of the beta-carotene from a raw carrot is lost.</span>
    </div>
  </div>
  <div class="absorption-row">
    <div class="absorption-icon">&#9728;&#65039;</div>
    <div>
      <strong>Calcium + Vitamin D (synergistic pair)</strong><br>
      <span style="font-size:13px;color:#475569">Vitamin D is essential for intestinal calcium absorption &mdash; without adequate Vitamin D, the body can only absorb 10&ndash;15% of dietary calcium. With sufficient Vitamin D, absorption rises to 30&ndash;40%. Sardines uniquely provide both calcium (from the bones) and Vitamin D in the same tin. Sun exposure remains the most effective Vitamin D strategy for most Australians.</span>
    </div>
  </div>
  <div class="absorption-row">
    <div class="absorption-icon">&#128029;</div>
    <div>
      <strong>Zinc + soaking (legumes and grains)</strong><br>
      <span style="font-size:13px;color:#475569">Soaking dried legumes overnight and discarding the water reduces phytate content by 30&ndash;60%, significantly improving zinc and iron absorption. Sprouting goes further still. For canned legumes (already cooked), rinsing removes some phytates. This matters most for vegetarians who rely on legumes as their primary zinc source.</span>
    </div>
  </div>
  <div class="absorption-row">
    <div class="absorption-icon">&#128336;</div>
    <div>
      <strong>Calcium &mdash; spread across the day</strong><br>
      <span style="font-size:13px;color:#475569">The gut has a limited calcium transport capacity. Above approximately 500mg in a single serving, absorption efficiency drops significantly. Spreading calcium across 2&ndash;3 dairy serves throughout the day (breakfast, lunch, dinner) absorbs substantially more than one large serve. This is particularly important for women over 50 who need 1,300mg/day.</span>
    </div>
  </div>
</div>

<h2>Tea and coffee &mdash; the mineral blocker most Australians don&rsquo;t know about</h2>
<div class="callout-red">
  <strong>Tannins in tea and chlorogenic acid in coffee</strong> bind to non-heme iron and zinc in the gut, reducing iron absorption by 60&ndash;90% and zinc absorption by 15&ndash;30% when consumed with a meal or within 1 hour either side.
</div>

<div class="nutrient-section">
  <h3>Which is worse?</h3>
  <p>Tea is generally more potent than coffee for iron inhibition. Black tea with a meal can reduce iron absorption by up to 90%. Coffee reduces it by approximately 40&ndash;60%.</p>
  <p>Heme iron (from meat) is much less affected &mdash; about 10&ndash;15% reduction. Plant-based iron (lentils, spinach, fortified cereals) bears the full brunt.</p>

  <h3>Does milk in coffee help?</h3>
  <p>No &mdash; the calcium in milk adds a competing inhibitor. One issue compounds the other.</p>

  <h3>The fix</h3>
  <p>Wait 1 hour before or after meals before having tea or coffee. Have your morning coffee before breakfast, or wait until it&rsquo;s been at least an hour since eating. This alone can meaningfully improve iron and zinc status, particularly for women of reproductive age and vegetarians.</p>

  <h3>The Vitamin C counterbalance</h3>
  <p>A glass of orange juice, half a capsicum, or any high-Vitamin C food with a plant-iron meal can increase absorption by 2&ndash;4&times;, largely offsetting tannin inhibition. The pairing matters more than avoiding tea &mdash; but ideally do both.</p>
</div>

<h2>Absorption inhibitors</h2>
<div class="nutrient-section">
  <div class="absorption-row">
    <div class="absorption-icon">&#9749;</div>
    <div>
      <strong>Tea/coffee + iron:</strong> Tannins reduce iron absorption by 60&ndash;90%. Wait at least 1 hour after meals before drinking tea or coffee.
    </div>
  </div>
  <div class="absorption-row">
    <div class="absorption-icon">&#129370;</div>
    <div>
      <strong>Calcium + iron (timing matters):</strong> High-calcium foods and calcium supplements compete with iron for the same transporter. Don&rsquo;t take calcium supplements with iron-rich meals. Avoid a large glass of milk alongside your iron-rich legume dinner.
    </div>
  </div>
  <div class="absorption-row">
    <div class="absorption-icon">&#127807;</div>
    <div>
      <strong>Phytates (beans, grains, nuts, seeds):</strong> Phytic acid binds zinc, iron, and calcium, reducing mineral absorption. Soaking, sprouting, fermentation, and cooking all significantly reduce phytate content. This is why sourdough bread has better mineral bioavailability than regular bread.
    </div>
  </div>
  <div class="absorption-row">
    <div class="absorption-icon">&#129367;</div>
    <div>
      <strong>Oxalates (spinach, silverbeet, beet greens, rhubarb):</strong> Oxalates bind calcium in the gut, making it unavailable for absorption. Spinach is excellent for folate and Vitamin K but is a poor calcium source &mdash; the calcium is largely blocked by oxalates. Dairy, sardines, and fortified foods are far more reliable calcium sources.
    </div>
  </div>
</div>

<h2>Special considerations by group</h2>
<div class="nutrient-section">
  <div class="absorption-row">
    <div class="absorption-icon">&#127807;</div>
    <div>
      <strong>Vegetarians and vegans:</strong> B12 supplementation is essential (no reliable plant source). Consider supplementing iron, zinc, iodine, and omega-3 (algae-based DHA) if not eating fortified foods regularly. Pair every plant-iron meal with Vitamin C. Soak or sprout legumes before cooking.
    </div>
  </div>
  <div class="absorption-row">
    <div class="absorption-icon">&#128116;</div>
    <div>
      <strong>Older adults (50+):</strong> B12 absorption from food declines due to reduced gastric acid production &mdash; consider a 100&ndash;400 &micro;g/day supplement. Vitamin D supplementation is recommended especially in winter for those over 70. Increase protein to 1.0&ndash;1.2 g/kg to counteract anabolic resistance.
    </div>
  </div>
  <div class="absorption-row">
    <div class="absorption-icon">&#128684;</div>
    <div>
      <strong>Smokers:</strong> Require an additional 35 mg/day of Vitamin C above the standard RDA, as smoking significantly increases oxidative destruction of Vitamin C. Smoking also impairs calcium absorption and accelerates bone loss.
    </div>
  </div>
  <div class="absorption-row">
    <div class="absorption-icon">&#129387;</div>
    <div>
      <strong>Pregnancy:</strong> Iron absorption naturally increases in the second and third trimester as the body upregulates absorption efficiency. However, the increased requirement (27mg/day) is so large that most women still need supplementation. Take iron supplements away from calcium-rich foods and tea/coffee. See the <a href="/guide/pregnancy/">Pregnancy Nutrition guide</a> for full details.
    </div>
  </div>
</div>

<p>For the full list of nutrient targets, see <a href="/guide/nrv/">NRV Reference Tables</a>. For the practical weekly framework, see <a href="/guide/daily-habits/">5 Daily Habits</a>.</p>

<p style="font-size:12px;color:#94a3b8;margin-top:24px">Sources: NHMRC Australian Nutrient Reference Values (2006, updated 2017) &middot; Hallberg L, Hulthen L. &ldquo;Prediction of dietary iron absorption.&rdquo; Am J Clin Nutr. 2000 &middot; Morck TA, Lynch SR, Cook JD. &ldquo;Inhibition of food iron absorption by coffee.&rdquo; Am J Clin Nutr. 1983 &middot; Hurrell R, Egli I. &ldquo;Iron bioavailability and dietary reference values.&rdquo; Am J Clin Nutr. 2010</p>"""

p = BASE / "absorption"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "Nutrient Absorption Tips &mdash; How to Get More From Food &mdash; OptimisedEats",
    "Practical nutrient absorption rules for Australians. Iron and Vitamin C, fat-soluble vitamins and fat, calcium timing, tea and coffee blocking, phytates and oxalates explained.",
    "iron absorption Australia, vitamin C iron, calcium absorption, nutrient absorption tips, phytates foods, tea coffee iron block, zinc absorption",
    "Absorption Tips", "/guide/absorption/", absorption_body, related_for("/guide/absorption/")
), encoding="utf-8")
print("DONE guide/absorption/index.html")


# ── PAGE 5: SLEEP & NUTRITION ─────────────────────────────────────────────────
sleep_body = """<h1>Sleep &amp; Nutrition &mdash; The Bidirectional Relationship</h1>
<p class="lead">Specific nutrient deficiencies impair sleep quality. And poor sleep drives the appetite patterns that lead to further deficiency. Breaking this cycle through nutrition is one of the most underutilised interventions for sleep improvement.</p>

<div class="callout">
  <strong>Why this matters:</strong> Most sleep advice focuses on screens and schedules. But the nutritional foundation of sleep is rarely discussed &mdash; despite strong evidence that magnesium, iron, Vitamin D, tryptophan, and B vitamins all directly affect sleep architecture.
</div>

<h2>How nutrient deficiencies impair sleep</h2>

<div class="nutrient-section">
  <div class="impact-box" style="display:flex;gap:12px;padding:14px 0;border-bottom:1px solid #f1f5f9;align-items:flex-start">
    <div style="font-size:22px;flex-shrink:0">&#129430;</div>
    <div>
      <strong>Magnesium &mdash; the most clinically significant sleep-nutrition link</strong>
      <p style="font-size:13px;color:#475569;margin:6px 0 0">Magnesium activates GABA receptors (the brain&rsquo;s primary inhibitory neurotransmitter), regulates the hypothalamic-pituitary axis, and modulates melatonin synthesis. Deficiency increases cortisol at night, reduces sleep efficiency, increases arousal frequency, and worsens restless leg syndrome.</p>
      <p style="font-size:13px;color:#475569;margin:6px 0 0">Studies in deficient individuals show magnesium supplementation (300&ndash;400mg glycinate or malate before bed) significantly improves sleep onset, duration, and quality within 4&ndash;6 weeks. Magnesium is deficient in approximately 31% of Australian adults.</p>
      <p style="font-size:13px;color:#475569;margin:6px 0 0"><strong>Budget sources:</strong> pumpkin seeds (156mg per 30g), spinach (78mg per 100g cooked), lentils (71mg per 100g cooked), dark chocolate, almonds.</p>
    </div>
  </div>

  <div class="impact-box" style="display:flex;gap:12px;padding:14px 0;border-bottom:1px solid #f1f5f9;align-items:flex-start">
    <div style="font-size:22px;flex-shrink:0">&#127969;</div>
    <div>
      <strong>Tryptophan and protein &mdash; the melatonin precursor</strong>
      <p style="font-size:13px;color:#475569;margin:6px 0 0">Tryptophan is the dietary precursor to serotonin, which is then converted to melatonin in the pineal gland. Inadequate protein intake &mdash; particularly in the evening &mdash; reduces tryptophan availability and impairs melatonin synthesis. Low-protein diets are associated with lighter, less restorative sleep.</p>
      <p style="font-size:13px;color:#475569;margin:6px 0 0"><strong>Tryptophan-rich foods:</strong> turkey, chicken, eggs, milk (the traditional warm milk before bed delivers both tryptophan and calcium), cheese, pumpkin seeds, oats.</p>
    </div>
  </div>

  <div class="impact-box" style="display:flex;gap:12px;padding:14px 0;border-bottom:1px solid #f1f5f9;align-items:flex-start">
    <div style="font-size:22px;flex-shrink:0">&#9728;&#65039;</div>
    <div>
      <strong>Vitamin D &mdash; sleep duration and architecture</strong>
      <p style="font-size:13px;color:#475569;margin:6px 0 0">Vitamin D receptors exist throughout the brainstem sleep centres. Deficiency is associated with shorter sleep duration, higher rates of sleep disorders, and increased daytime sleepiness. Blood Vitamin D levels below 20 nmol/L are strongly correlated with poor sleep architecture.</p>
      <p style="font-size:13px;color:#475569;margin:6px 0 0">21% of Australian adults are deficient. The fix is largely free: 15&ndash;30 min daily sun exposure on arms and legs in reasonable UV conditions. In winter in southern Australia, a supplement of 1,000&ndash;2,000 IU/day is reasonable. See the <a href="/guide/nutrient-gaps/">Nutrient Gaps guide</a> for the UV mushroom hack.</p>
    </div>
  </div>

  <div class="impact-box" style="display:flex;gap:12px;padding:14px 0;border-bottom:1px solid #f1f5f9;align-items:flex-start">
    <div style="font-size:22px;flex-shrink:0">&#129370;</div>
    <div>
      <strong>Calcium &mdash; melatonin production partner</strong>
      <p style="font-size:13px;color:#475569;margin:6px 0 0">Calcium works synergistically with tryptophan for melatonin production. Calcium deficiency is associated with difficulty falling asleep and fragmented sleep. The traditional warm milk before bed is not a myth &mdash; it delivers both tryptophan and calcium simultaneously, supporting melatonin synthesis.</p>
    </div>
  </div>

  <div class="impact-box" style="display:flex;gap:12px;padding:14px 0;border-bottom:1px solid #f1f5f9;align-items:flex-start">
    <div style="font-size:22px;flex-shrink:0">&#129354;</div>
    <div>
      <strong>Iron &mdash; the primary cause of restless leg syndrome</strong>
      <p style="font-size:13px;color:#475569;margin:6px 0 0">Iron deficiency is the primary nutritional cause of restless leg syndrome (RLS), affecting an estimated 15% of the population. RLS causes irresistible urges to move the legs at night, dramatically fragmenting sleep. Crucially, standard blood tests may show normal haemoglobin while ferritin is low.</p>
      <p style="font-size:13px;color:#475569;margin:6px 0 0"><strong>Key insight:</strong> Ferritin above 75 &micro;g/L significantly reduces RLS symptoms in most sufferers. Standard GP testing often only checks haemoglobin &mdash; ask specifically for serum ferritin if you experience 2&ndash;4am wake-ups with leg discomfort.</p>
    </div>
  </div>

  <div class="impact-box" style="display:flex;gap:12px;padding:14px 0;align-items:flex-start">
    <div style="font-size:22px;flex-shrink:0">&#127801;</div>
    <div>
      <strong>B vitamins (B6, B12, folate) &mdash; the conversion pathway</strong>
      <p style="font-size:13px;color:#475569;margin:6px 0 0">B vitamins are required for the conversion of tryptophan to serotonin and then melatonin. B12 deficiency is associated with disrupted circadian rhythms and vivid, disturbing dreams. B6 deficiency impairs serotonin synthesis directly. Folate deficiency affects overall methylation, including neurotransmitter production.</p>
    </div>
  </div>
</div>

<h2>How poor sleep drives poor nutrition</h2>
<div class="nutrient-section">
  <p>The relationship is strongly bidirectional. After just one night of poor sleep (under 6 hours):</p>
  <ul style="font-size:14px;color:#374151;line-height:1.7;padding-left:20px">
    <li><strong>Ghrelin (hunger hormone) increases by 24%.</strong> Leptin (satiety hormone) decreases by 18%. Result: an additional 300&ndash;500 extra calories consumed the following day on average, predominantly from high-carbohydrate, high-fat, ultra-processed foods.</li>
    <li><strong>Prefrontal cortex activity decreases</strong> (impulse control, executive function), while the amygdala&rsquo;s food-reward response increases. Sleep-deprived individuals show significantly greater activation to images of junk food than well-rested controls.</li>
    <li><strong>Insulin sensitivity decreases by 20&ndash;30%</strong> after 4&ndash;6 nights of restricted sleep &mdash; driving blood sugar dysregulation that further disrupts sleep architecture. A self-reinforcing cycle.</li>
  </ul>
</div>

<h2>Blood sugar and sleep architecture</h2>
<p>Blood sugar instability is one of the least-discussed causes of poor sleep. When blood glucose drops significantly during the night (reactive hypoglycaemia), the adrenal glands release cortisol and adrenaline to raise it &mdash; waking you at 2&ndash;4am with a racing heart and mind.</p>

<div class="callout-red">
  <strong>Dietary drivers of nocturnal blood sugar instability:</strong> high-glycaemic dinners, alcohol (disrupts glucose regulation for 4&ndash;6 hours after drinking), excess refined sugar and processed carbohydrates, and inadequate protein and fat at the evening meal.
</div>

<div class="callout">
  <strong>Fix:</strong> Ensure the evening meal includes adequate protein (25&ndash;35g), moderate healthy fat, and a significant vegetable component. Reduce refined carbohydrate load at dinner. A small protein-rich snack (Greek yoghurt, cheese, or a boiled egg) an hour before bed can prevent nocturnal hypoglycaemia in susceptible individuals.
</div>

<h2>Practical nutritional sleep protocol</h2>
<div class="nutrient-section">
  <div class="habit-item">
    <div class="habit-num">&#127761;</div>
    <div class="habit-body">
      <div class="habit-title">Evening meal</div>
      <div class="habit-detail">Include 30g+ protein, significant vegetables, moderate complex carbohydrates. Avoid high-sugar desserts. Finish eating 2&ndash;3 hours before bed. A dinner of chicken or fish with roasted vegetables and brown rice or lentils is close to ideal.</div>
    </div>
  </div>
  <div class="habit-item">
    <div class="habit-num">&#9728;&#65039;</div>
    <div class="habit-body">
      <div class="habit-title">Daily magnesium, calcium and Vitamin D</div>
      <div class="habit-detail">Pumpkin seeds, dark leafy greens, dark chocolate and legumes for magnesium. Dairy or sardines for calcium. Sun exposure daily for Vitamin D &mdash; or supplement in winter at 1,000&ndash;2,000 IU/day. These three nutrients work together on sleep architecture.</div>
    </div>
  </div>
  <div class="habit-item">
    <div class="habit-num">&#129354;</div>
    <div class="habit-body">
      <div class="habit-title">Address iron deficiency if you wake at 2&ndash;4am</div>
      <div class="habit-detail">Ask your GP to test serum ferritin (not just haemoglobin). Target ferritin above 75 &micro;g/L. Iron-rich foods: liver, red meat, lentils, beans, spinach &mdash; always with Vitamin C. See the <a href="/guide/nutrient-gaps/">Nutrient Gaps guide</a> for the full iron strategy.</div>
    </div>
  </div>
  <div class="habit-item">
    <div class="habit-num">&#129430;</div>
    <div class="habit-body">
      <div class="habit-title">Consider magnesium glycinate before bed</div>
      <div class="habit-detail">300&ndash;400mg magnesium glycinate or malate 1 hour before bed is one of the safest and most evidence-backed sleep supplements available. This is one of very few supplements with robust trial data for sleep improvement. Glycinate form is gentler on the gut than magnesium oxide.</div>
    </div>
  </div>
  <div class="habit-item">
    <div class="habit-num">&#9749;</div>
    <div class="habit-body">
      <div class="habit-title">Caffeine cutoff</div>
      <div class="habit-detail">Caffeine has a half-life of 5&ndash;7 hours. Coffee at 2pm means half the caffeine is still circulating at 9pm. Cut off at noon for most people, 10am for caffeine-sensitive individuals. Decaf after midday is not a myth &mdash; it genuinely improves sleep onset latency.</div>
    </div>
  </div>
</div>

<p>For the full nutrition framework, see <a href="/guide/daily-habits/">5 Daily Habits</a> and <a href="/guide/deficiency-symptoms/">Deficiency Symptoms</a>. For magnesium-rich meal ideas, see <a href="/guide/nutrient-gaps/">Nutrient Gaps</a>.</p>

<p style="font-size:12px;color:#94a3b8;margin-top:24px">Sources: Abbasi B, et al. &ldquo;The effect of magnesium supplementation on primary insomnia.&rdquo; J Res Med Sci. 2012 &middot; Spiegel K, et al. &ldquo;Sleep curtailment in healthy young men is associated with decreased leptin levels.&rdquo; Ann Intern Med. 2004 &middot; Van Cauter E, et al. &ldquo;Impact of sleep and sleep loss on neuroendocrine and metabolic function.&rdquo; Horm Res. 2007 &middot; Earley CJ, et al. &ldquo;Abnormalities in CSF concentrations of ferritin and transferrin in restless legs syndrome.&rdquo; Neurology. 2000 &middot; Gominak SC. &ldquo;Vitamin D deficiency changes the intestinal microbiome reducing B vitamin production.&rdquo; Med Hypotheses. 2016</p>"""

p = BASE / "sleep-nutrition"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "Sleep &amp; Nutrition &mdash; How Deficiencies Wreck Your Sleep &mdash; OptimisedEats",
    "Magnesium, iron, Vitamin D and B vitamins all directly affect sleep quality. A practical guide to the nutritional causes of poor sleep and what to do about them.",
    "sleep and nutrition Australia, magnesium sleep, restless leg syndrome iron, vitamin D sleep, melatonin food sources, insomnia nutrition, blood sugar sleep",
    "Sleep &amp; Nutrition", "/guide/sleep-nutrition/", sleep_body, related_for("/guide/sleep-nutrition/")
), encoding="utf-8")
print("DONE guide/sleep-nutrition/index.html")


# ── PAGE 6: WESTON A. PRICE ───────────────────────────────────────────────────
wap_body = """<h1>The Weston A. Price Legacy &mdash; What Traditional Diets Knew</h1>
<p class="lead">In the 1930s, a Canadian dentist travelled the world documenting what happened to isolated communities the moment they adopted processed food. What he found remains one of the most compelling nutritional datasets ever assembled.</p>

<div class="callout-blue">
  <strong>Why this matters today:</strong> Price&rsquo;s empirical observations &mdash; made decades before modern nutritional science existed &mdash; align remarkably well with what epigenetics, developmental biology, and nutritional research now confirm. His work is experiencing significant rehabilitation in academic circles.
</div>

<h2>Who was Weston A. Price?</h2>
<p>Dr Weston A. Price (1870&ndash;1948) was a Canadian-American dentist who, disturbed by the deteriorating dental and physical health he was seeing in his Cleveland practice, undertook one of the most remarkable self-funded research expeditions in nutritional history. Between the late 1920s and late 1930s, he travelled to isolated communities around the world to study people still eating traditional diets &mdash; before the influence of industrialised food had reached them.</p>
<p>His findings were documented in his 1939 masterwork, <em>Nutrition and Physical Degeneration</em> &mdash; with thousands of photographs comparing traditional and modernised populations within the same ethnic group, often within the same family.</p>

<h2>What Price documented</h2>
<div class="nutrient-section">
  <h3>Dental arch width and cavity rates</h3>
  <p style="font-size:14px;color:#374151">Traditional populations consistently showed broad dental arches, full sets of straight teeth with no crowding, and cavity rates of 0&ndash;2%. The moment these same populations adopted refined flour, sugar, and vegetable oils &mdash; sometimes within a single generation &mdash; cavity rates climbed to 20&ndash;40%.</p>
  <p style="font-size:14px;color:#374151">Children born <em>after</em> the dietary switch showed narrow dental arches, crowded and crooked teeth, reduced jaw width, and pinched nasal passages &mdash; despite having the same genetic heritage as their parents.</p>

  <h3>Facial bone structure</h3>
  <p style="font-size:14px;color:#374151">Traditional-diet children showed full cheekbone development, wide nostrils, broad palates, and prominent jaw lines. Their first-generation modernised peers &mdash; same parents, same genetics &mdash; showed narrow faces, recessed jaws, crowded teeth, and an epidemic of mouth-breathing.</p>
  <div class="wap-quote">Price argued, and modern research has confirmed, that these are nutritional developmental issues, not genetic ones. The genes were the same; the nutritional environment had changed.
  </div>

  <h3>Physical health and fertility</h3>
  <p style="font-size:14px;color:#374151">Traditional populations had exceptional physical endurance, fertility, ease of childbirth, resistance to tuberculosis (then epidemic), and low rates of chronic disease. These advantages eroded within one to two generations of adopting what Price called &ldquo;the displacing foods of modern commerce.&rdquo;</p>
</div>

<h2>The traditional diets he studied</h2>
<p>Price studied over a dozen distinct traditional dietary cultures. Despite extraordinary variation in what these populations ate, they shared common features: virtually no refined flour, no refined sugar, no vegetable oils, and high consumption of animal organ meats, fermented foods, and mineral-rich bone broths.</p>

<div class="nutrient-section">
  <div class="absorption-row">
    <div class="absorption-icon">&#127988;</div>
    <div><strong>Swiss mountain villages (Loetschental Valley):</strong> Rye bread, raw dairy, organ meats, bone broth. Virtually zero dental caries. Robust skeletal development.</div>
  </div>
  <div class="absorption-row">
    <div class="absorption-icon">&#127988;</div>
    <div><strong>Outer Hebrides, Scotland:</strong> Oats, cod and other seafood, cod liver oil, shellfish. Cavity rate under 1%.</div>
  </div>
  <div class="absorption-row">
    <div class="absorption-icon">&#127756;</div>
    <div><strong>Indigenous Peoples of North America:</strong> Organ meats (especially liver), bone marrow, dried fish roe, berries, fermented foods. Superb physical development and fertility.</div>
  </div>
  <div class="absorption-row">
    <div class="absorption-icon">&#127798;</div>
    <div><strong>Polynesian islanders:</strong> Seafood, coconut in many forms, taro, fermented products. Outstanding dental and skeletal development.</div>
  </div>
  <div class="absorption-row">
    <div class="absorption-icon">&#127981;</div>
    <div><strong>Maasai, Dinkas, and other African pastoralists:</strong> Raw milk, blood, meat, organ meats. Among the tallest and most physically robust populations Price encountered.</div>
  </div>
  <div class="absorption-row">
    <div class="absorption-icon">&#127793;</div>
    <div><strong>Japanese coastal communities:</strong> Seafood including shellfish, fish roe, seaweed, fermented soy. Among the lowest caries rates of any group studied.</div>
  </div>
</div>

<h2>Activator X &mdash; now proposed to be Vitamin K2</h2>
<p>Price identified a fat-soluble compound he called &ldquo;Activator X&rdquo; that appeared to be the key driver of skeletal and dental development in traditional diets. It was present in high concentrations in: grass-fed dairy fat (butter, cream), certain organ meats, and fish roe.</p>
<p>By the 2000s, researchers &mdash; most notably Dr Kate Rheaume-Bleue &mdash; proposed that Activator X is most likely <strong>Vitamin K2</strong> (specifically the MK-4 form). This identification remains a well-supported hypothesis rather than formally confirmed science, but the mechanistic fit is compelling.</p>
<p>Vitamin K2 directs calcium to bones and teeth (via osteocalcin activation) and simultaneously removes calcium from soft tissues &mdash; arteries, kidneys, joints. It works in concert with Vitamins A and D, which Price also identified as synergistic &ldquo;fat-soluble activators.&rdquo;</p>
<div class="callout">
  This explains why traditional cultures consuming significant grass-fed dairy fat, organ meats, and fermented foods had superior bone and dental development compared to populations eating the same amount of calcium from lower-K2 sources.
</div>
<p><strong>Best budget K2 sources:</strong> Natto (fermented soy, available from Asian supermarkets &mdash; extremely high in MK-7 form), hard cheeses, butter from grass-fed cows, egg yolks, chicken liver.</p>

<h2>Price, pre-conception, and epigenetics</h2>
<p>One of Price&rsquo;s most significant findings &mdash; and the one most relevant to modern epigenetics research &mdash; was his documentation of deliberate pre-conception nutritional preparation in traditional cultures.</p>
<p>Across cultures as different as the Maasai, the Pacific Islanders, and Indigenous Canadian communities, Price found that traditional societies had specific foods <strong>reserved for pregnant and soon-to-be-pregnant women</strong>. These were without exception the most nutrient-dense foods available:</p>
<ul style="font-size:14px;color:#374151;line-height:1.8;padding-left:20px">
  <li><strong>Fish roe</strong> &mdash; extremely high in DHA, fat-soluble vitamins A, D, E, K2, zinc, and iodine</li>
  <li><strong>Liver and organ meats</strong> &mdash; the most nutrient-dense foods on earth by virtually any measure</li>
  <li><strong>Bone marrow</strong> &mdash; fat-soluble vitamins, essential fatty acids, collagen precursors</li>
  <li><strong>Raw or fermented dairy from grass-fed animals</strong> &mdash; K2, fat-soluble vitamins, calcium, B12</li>
  <li><strong>Shellfish and seafood</strong> &mdash; iodine, zinc, omega-3, B12</li>
</ul>
<div class="wap-quote">Price&rsquo;s observation was that these cultural practices &mdash; developed over millennia of observed outcomes, not laboratory science &mdash; systematically loaded mothers with exactly the fat-soluble vitamins (A, D, K2) and essential fatty acids (DHA) that modern nutritional science now recognises as critical for foetal skeletal development, brain formation, and epigenetic programming.
</div>
<p>Modern prenatal vitamins provide folate, iron, and some B vitamins &mdash; important, but a fraction of what Price&rsquo;s traditional diets delivered. Choline, DHA, Vitamin K2, and preformed Vitamin A (retinol) are almost entirely absent from standard prenatal supplements. These were the very nutrients traditional cultures prioritised.</p>

<h2>Price&rsquo;s legacy in modern research</h2>
<p>Price&rsquo;s work was largely dismissed for decades. It is now experiencing significant rehabilitation as modern developmental biology, epigenetics, and nutritional science converge on the same conclusions he reached empirically:</p>
<ul style="font-size:14px;color:#374151;line-height:1.8;padding-left:20px">
  <li><strong>Fat-soluble vitamins (A, D, K2) are essential for skeletal and facial development</strong> &mdash; confirmed by multiple modern trials and observational studies.</li>
  <li><strong>Pre-conception nutrition matters as much as gestational nutrition</strong> &mdash; confirmed by epigenetics research showing paternal and maternal nutritional epigenetic marks are both transmitted to offspring. See the <a href="/guide/pre-conception/">Pre-Conception guide</a>.</li>
  <li><strong>Industrialised food displaces nutrient-dense whole foods and generates deficiency patterns</strong> that drive degenerative disease &mdash; a core thesis now supported by decades of epidemiology. See the <a href="/guide/hidden-hunger/">Hidden Hunger guide</a>.</li>
</ul>

<div class="callout-amber">
  <strong>A note on critical evaluation:</strong> The Weston A. Price Foundation (westonaprice.org) promotes Price&rsquo;s work but has expanded into positions that go beyond his original research &mdash; including some that are not well-supported by modern evidence. The original research is valuable; the Foundation&rsquo;s current recommendations should be evaluated critically alongside mainstream nutritional science.
</div>

<p><strong>For further reading:</strong> <em>Nutrition and Physical Degeneration</em> by Weston A. Price (1939, available free online). <em>Vitamin K2 and the Calcium Paradox</em> by Kate Rheaume-Bleue (2012).</p>

<p style="font-size:12px;color:#94a3b8;margin-top:24px">Sources: Price WA. <em>Nutrition and Physical Degeneration</em> (1939) &middot; Rheaume-Bleue K. <em>Vitamin K2 and the Calcium Paradox</em> (2012) &middot; Geleijnse JM, et al. &ldquo;Dietary intake of menaquinone is associated with a reduced risk of coronary heart disease.&rdquo; J Nutr. 2004 &middot; Knapen MH, et al. &ldquo;Three-year low-dose menaquinone-7 supplementation helps decrease bone loss in healthy postmenopausal women.&rdquo; Osteoporos Int. 2013</p>"""

p = BASE / "weston-price"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "Weston A. Price &mdash; What Traditional Diets Knew &mdash; OptimisedEats",
    "Dr Weston A. Price documented the health of traditional diet communities in the 1930s. A guide to his findings, Vitamin K2, Activator X, and the modern science that confirms his work.",
    "Weston A Price diet, traditional diets nutrition, vitamin K2 activator X, pre-conception nutrition traditional, ancestral diet health, grass fed dairy nutrition",
    "Weston A. Price", "/guide/weston-price/", wap_body, related_for("/guide/weston-price/")
), encoding="utf-8")
print("DONE guide/weston-price/index.html")
