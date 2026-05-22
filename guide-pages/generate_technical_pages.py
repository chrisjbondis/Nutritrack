"""Generate detailed/technical HTML pages for the OptimisedEats guide hub.
These pages are booklet-style with full tables, NRV data, and absorption rules.
Run this after generate_pages.py (shares the same _shared.css).
"""
import pathlib

BASE = pathlib.Path(__file__).parent
CSS = (BASE / "_shared.css").read_text(encoding="utf-8")

EXTRA_CSS = """
.nutrient-section{margin:32px 0;padding:24px;background:#fff;border:1px solid #e2e8f0;border-radius:12px}
.nutrient-section h2{border-top:none;margin-top:0;padding-top:0}
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
.nrv-note{font-size:12px;color:#94a3b8;font-style:italic;margin-top:4px}
.demo-tabs{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0}
.data-table th{font-size:12px}
.data-table td{font-size:13px}
.data-table td:not(:first-child){text-align:center}
.data-table th:not(:first-child){text-align:center}
"""

def page(title, desc, keywords, breadcrumb_label, canonical, body_html, related_links):
    related = "".join(f'<a class="related-link" href="{h}">{l}</a>' for l,h in related_links)
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
  <a href="/">Home</a><span>›</span><a href="/guide/">Nutrition Guide</a><span>›</span>{breadcrumb_label}
</div>
<main>
{body_html}
<div class="related">
  <h2>More guides</h2>
  <div class="related-grid">{related}</div>
</div>
</main>
<footer class="site-footer">
  <p>© 2025 OptimisedEats · Free nutrition planning for Australians &amp; New Zealanders · <a href="/">Open App</a></p>
  <p style="margin-top:6px;font-size:11px;color:#cbd5e1">Information is based on NHMRC Australian Nutrient Reference Values (2006, updated 2017) and ABS National Nutrition and Physical Activity Survey data. For general educational purposes only — not a substitute for personalised medical or dietary advice.</p>
</footer>
</body>
</html>"""

ALL_RELATED = [
    ("Budget Basics",         "/guide/budget-basics/"),
    ("Nutrient Gaps",         "/guide/nutrient-gaps/"),
    ("Deficiency Symptoms",   "/guide/deficiency-symptoms/"),
    ("Pre-Conception",        "/guide/pre-conception/"),
    ("Pregnancy Nutrition",   "/guide/pregnancy/"),
    ("Hidden Hunger",         "/guide/hidden-hunger/"),
    ("Kids & Toddlers",       "/guide/kids/"),
    ("NRV Reference Tables",  "/guide/nrv/"),
    ("Budget Arsenal",        "/guide/arsenal/"),
    ("Batch Cooking",         "/guide/batch-cooking/"),
    ("Smart Shopping",        "/guide/shopping/"),
    ("World Cuisines",        "/guide/cuisines/"),
    ("106 Recipes",           "/guide/recipes/"),
    ("Disclaimer",            "/guide/disclaimer/"),
]

def other_related(current_path):
    return [(l,h) for l,h in ALL_RELATED if h != current_path]


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1: NUTRIENT GAPS
# ═══════════════════════════════════════════════════════════════════════════════

gaps_body = """
<h1>The 6 Nutrient Gaps Most Australians Have</h1>
<p class="lead">Australian Bureau of Statistics survey data shows most Australians consistently fall short on the same six nutrients. Here's the data, the cheapest foods to fix each gap, and the absorption rules that make the difference.</p>

<div class="highlight-box">
  <h3>Why these 6?</h3>
  <p>These are ranked by the proportion of the Australian population failing to meet the Estimated Average Requirement (EAR) — the intake needed to meet the needs of half the population. They're also the gaps most linked to fatigue, poor immunity, weak bones, and developmental problems in children.</p>
</div>

<div class="nutrient-section">
<h2>1. Calcium <span class="gap-stat">60%+ fall short</span></h2>
<p><strong>Why it matters:</strong> Calcium builds and maintains bone density throughout life. Children and teenagers build peak bone mass — shortfalls now mean fracture risk decades later. Adults who don't meet calcium targets lose bone density from their 30s onward. Calcium also drives muscle contraction, nerve transmission, and blood clotting.</p>
<p><strong>RDI:</strong> 1,000 mg/day (adults) · 1,300 mg/day (teens 12–18 &amp; adults 70+) · 1,000 mg/day (pregnancy &amp; lactation)</p>

<table class="data-table">
  <thead><tr><th>Food</th><th>Serve</th><th>Calcium</th><th>% of adult RDI</th><th>Approx. cost</th></tr></thead>
  <tbody>
    <tr><td>Canned sardines (with bones)</td><td>1 tin (95g)</td><td>~350 mg</td><td>35%</td><td>~$1.50</td></tr>
    <tr><td>Calcium-set tofu</td><td>100g</td><td>~350 mg</td><td>35%</td><td>~$0.60</td></tr>
    <tr><td>Full-cream milk</td><td>250 mL</td><td>~300 mg</td><td>30%</td><td>~$0.40</td></tr>
    <tr><td>Greek yoghurt</td><td>200g</td><td>~250 mg</td><td>25%</td><td>~$0.60</td></tr>
    <tr><td>Cheddar cheese</td><td>30g</td><td>~200 mg</td><td>20%</td><td>~$0.40</td></tr>
    <tr><td>Kale (cooked)</td><td>1 cup</td><td>~180 mg</td><td>18%</td><td>~$0.40</td></tr>
    <tr><td>Bok choy (cooked)</td><td>1 cup</td><td>~160 mg</td><td>16%</td><td>~$0.30</td></tr>
    <tr><td>Almonds</td><td>30g</td><td>~75 mg</td><td>7.5%</td><td>~$0.50</td></tr>
  </tbody>
</table>
<div class="absorption-rule">
  <div class="absorption-icon">💡</div>
  <div><strong>Absorption rule:</strong> Calcium absorbs best in doses under 500 mg. Spread intake across 2–3 meals rather than taking it all at once. Vitamin D is essential for calcium absorption — without adequate vitamin D, even high calcium intake is poorly utilised.</div>
</div>
</div>

<div class="nutrient-section">
<h2>2. Zinc (in males) <span class="gap-stat">48% fall short</span></h2>
<p><strong>Why it matters:</strong> Zinc drives immune function, wound healing, testosterone production, taste/smell, and protein synthesis. Male RDI is nearly double the female RDI due to higher physiological demand and losses. Zinc deficiency is strongly linked to reduced immunity and poor wound healing.</p>
<p><strong>RDI:</strong> 14 mg/day (men) · 8 mg/day (women) · 10–11 mg/day (pregnancy)</p>

<table class="data-table">
  <thead><tr><th>Food</th><th>Serve</th><th>Zinc</th><th>% of male RDI</th><th>Approx. cost</th></tr></thead>
  <tbody>
    <tr><td>Beef mince (lean)</td><td>100g</td><td>~8 mg</td><td>57%</td><td>~$1.00</td></tr>
    <tr><td>Kangaroo mince</td><td>100g</td><td>~6.5 mg</td><td>46%</td><td>~$1.00</td></tr>
    <tr><td>Lentils (cooked)</td><td>200g</td><td>~2.5 mg</td><td>18%</td><td>~$0.20</td></tr>
    <tr><td>Chickpeas (cooked)</td><td>160g</td><td>~2.5 mg</td><td>18%</td><td>~$0.20</td></tr>
    <tr><td>Pumpkin seeds</td><td>30g</td><td>~2.2 mg</td><td>16%</td><td>~$0.30</td></tr>
    <tr><td>Rolled oats</td><td>80g dry</td><td>~2.3 mg</td><td>16%</td><td>~$0.10</td></tr>
    <tr><td>Eggs</td><td>2 large</td><td>~1.3 mg</td><td>9%</td><td>~$0.60</td></tr>
    <tr><td>Cheddar cheese</td><td>30g</td><td>~1.0 mg</td><td>7%</td><td>~$0.40</td></tr>
  </tbody>
</table>
<div class="absorption-rule">
  <div class="absorption-icon">💡</div>
  <div><strong>Absorption rule:</strong> Zinc from meat (haem) is far more bioavailable than from plant sources. If you rely on legumes and grains for zinc, soak them overnight before cooking — this reduces phytates by 30–60% and roughly doubles zinc absorption. Avoid taking zinc supplements with iron supplements (they compete for absorption).</div>
</div>
</div>

<div class="nutrient-section">
<h2>3. Iron (in women 18–29) <span class="gap-stat">47% fall short</span></h2>
<p><strong>Why it matters:</strong> Iron carries oxygen in red blood cells (haemoglobin) and stores oxygen in muscles (myoglobin). It's critical for energy, cognition, and immune function. Women of reproductive age have dramatically higher requirements due to menstrual losses. Iron deficiency is the world's most common nutritional deficiency and the leading cause of anaemia.</p>
<p><strong>RDI:</strong> 18 mg/day (women 19–50) · 8 mg/day (men) · 27 mg/day (pregnancy) · 9 mg/day (lactation)</p>

<table class="data-table">
  <thead><tr><th>Food</th><th>Serve</th><th>Iron</th><th>% of women's RDI</th><th>Type</th><th>Cost</th></tr></thead>
  <tbody>
    <tr><td>Lentils (cooked)</td><td>1 cup</td><td>6.6 mg</td><td>37%</td><td>Non-haem</td><td>~$0.20</td></tr>
    <tr><td>Kangaroo mince</td><td>100g</td><td>~5.5–7 mg</td><td>31–39%</td><td>Haem</td><td>~$1.00</td></tr>
    <tr><td>Spinach (cooked)</td><td>1 cup</td><td>3.6 mg</td><td>20%</td><td>Non-haem</td><td>~$0.30</td></tr>
    <tr><td>Kidney beans (cooked)</td><td>1 cup</td><td>3.9 mg</td><td>22%</td><td>Non-haem</td><td>~$0.20</td></tr>
    <tr><td>Beef mince (lean)</td><td>100g</td><td>3.2 mg</td><td>18%</td><td>Haem</td><td>~$1.00</td></tr>
    <tr><td>Dark chocolate (70%+)</td><td>30g</td><td>3.4 mg</td><td>19%</td><td>Non-haem</td><td>~$0.50</td></tr>
    <tr><td>Tofu (firm)</td><td>100g</td><td>3.0 mg</td><td>17%</td><td>Non-haem</td><td>~$0.60</td></tr>
    <tr><td>Weet-Bix (fortified)</td><td>2 biscuits</td><td>2.6 mg</td><td>14%</td><td>Non-haem</td><td>~$0.20</td></tr>
  </tbody>
</table>
<div class="absorption-rule">
  <div class="absorption-icon">🔴</div>
  <div><strong>Critical absorption rule:</strong> Iron is the one nutrient that <em>cannot</em> be caught up on over the week — the body needs a steady supply. Non-haem iron (from plants) is poorly absorbed unless paired with vitamin C, which can triple absorption. Always eat iron-rich plant foods with: capsicum, tomato, citrus, or broccoli. Avoid tea or coffee within 1 hour of an iron-rich meal (tannins block absorption by up to 60%).</div>
</div>
</div>

<div class="nutrient-section">
<h2>4. Magnesium <span class="gap-stat">31% fall short</span></h2>
<p><strong>Why it matters:</strong> Magnesium is involved in over 300 enzymatic reactions. It regulates blood sugar, blood pressure, muscle and nerve function, protein synthesis, and bone development. Low magnesium is strongly associated with poor sleep quality, muscle cramps, anxiety, and fatigue — symptoms often attributed to other causes.</p>
<p><strong>RDI:</strong> 420 mg/day (men) · 320 mg/day (women) · 350–360 mg/day (pregnancy)</p>

<table class="data-table">
  <thead><tr><th>Food</th><th>Serve</th><th>Magnesium</th><th>% of men's RDI</th><th>Approx. cost</th></tr></thead>
  <tbody>
    <tr><td>Pumpkin seeds</td><td>30g</td><td>~160 mg</td><td>38%</td><td>~$0.30</td></tr>
    <tr><td>Spinach (cooked)</td><td>1 cup</td><td>~157 mg</td><td>37%</td><td>~$0.30</td></tr>
    <tr><td>Black beans (cooked)</td><td>1 cup</td><td>~120 mg</td><td>29%</td><td>~$0.20</td></tr>
    <tr><td>Almonds</td><td>30g</td><td>~75 mg</td><td>18%</td><td>~$0.50</td></tr>
    <tr><td>Brown rice (cooked)</td><td>1 cup</td><td>~84 mg</td><td>20%</td><td>~$0.15</td></tr>
    <tr><td>Rolled oats</td><td>80g dry</td><td>~55 mg</td><td>13%</td><td>~$0.10</td></tr>
    <tr><td>Lentils (cooked)</td><td>1 cup</td><td>~71 mg</td><td>17%</td><td>~$0.20</td></tr>
    <tr><td>Banana</td><td>1 medium</td><td>~32 mg</td><td>8%</td><td>~$0.30</td></tr>
  </tbody>
</table>
<div class="absorption-rule">
  <div class="absorption-icon">💡</div>
  <div><strong>Absorption note:</strong> Magnesium absorption is reduced by high calcium intake (they compete). If supplementing calcium, space magnesium-rich foods away from it. Alcohol and high-sugar diets increase magnesium excretion. Pumpkin seeds are the most cost-effective single source — 30g/day covers ~38% of male needs for around 30 cents.</div>
</div>
</div>

<div class="nutrient-section">
<h2>5. Vitamin D <span class="gap-stat">21% deficient</span></h2>
<p><strong>Why it matters:</strong> Vitamin D is actually a hormone that regulates calcium absorption, immune function, cell growth, and inflammation. Despite Australia's sunshine, deficiency is widespread due to indoor work, sunscreen use, darker skin tones (which require longer sun exposure), and obesity (Vit D is fat-soluble and sequesters in adipose tissue). Vitamin D deficiency is linked to osteoporosis, depression, increased infection risk, and multiple sclerosis risk.</p>
<p><strong>RDI:</strong> 600 IU/day (15 mcg) adults 19–70 · 800 IU/day (20 mcg) adults 70+</p>

<table class="data-table">
  <thead><tr><th>Source</th><th>Amount</th><th>Vitamin D</th><th>% of adult RDI</th><th>Cost</th></tr></thead>
  <tbody>
    <tr><td>Sun exposure (UV index 3+, arms/legs)</td><td>15–30 min</td><td>600–1,000 IU</td><td>100–167%</td><td>Free</td></tr>
    <tr><td>UV-exposed mushrooms (gill-side up)</td><td>100g</td><td>~400+ IU</td><td>67%</td><td>~$0.50</td></tr>
    <tr><td>Canned salmon</td><td>100g</td><td>~350 IU</td><td>58%</td><td>~$2.00</td></tr>
    <tr><td>Canned sardines</td><td>1 tin (95g)</td><td>~250 IU</td><td>42%</td><td>~$1.50</td></tr>
    <tr><td>Eggs (omega-3 enriched)</td><td>2 large</td><td>~80–100 IU</td><td>13–17%</td><td>~$0.80</td></tr>
    <tr><td>Fortified milk</td><td>250 mL</td><td>~40 IU</td><td>7%</td><td>~$0.40</td></tr>
  </tbody>
</table>
<div class="absorption-rule">
  <div class="absorption-icon">☀️</div>
  <div><strong>Sun rule:</strong> The UV index must be 3 or above for skin to synthesise vitamin D. In southern Australia (Melbourne, Adelaide, Hobart) this doesn't happen in winter months (May–August) — supplementation is strongly recommended for those latitudes. Check the Australian Bureau of Meteorology UV index before relying on sun exposure.</div>
</div>
<div class="absorption-rule">
  <div class="absorption-icon">💡</div>
  <div><strong>Mushroom hack:</strong> Place mushrooms gill-side up in direct sunlight for 30–60 minutes — they synthesise vitamin D just like human skin does, and the vitamin D persists even after cooking. This can boost a 100g serve from nearly zero to 400+ IU for essentially no cost.</div>
</div>
</div>

<div class="nutrient-section">
<h2>6. Vitamin A <span class="gap-stat">23% fall short</span></h2>
<p><strong>Why it matters:</strong> Vitamin A supports vision (especially night vision), immune defence, skin health, and cell growth. It comes in two forms: preformed retinol (from animal foods — immediately usable) and beta-carotene (from plant foods — converted to retinol, but conversion is inefficient). Vitamin A deficiency is the leading cause of preventable blindness in children worldwide; even mild deficiency impairs immune response.</p>
<p><strong>RDI:</strong> 900 mcg RAE/day (men) · 700 mcg RAE/day (women) · 800 mcg RAE/day (pregnancy)</p>
<p><em>RAE = Retinol Activity Equivalents. 1 mcg retinol = 12 mcg beta-carotene from food.</em></p>

<table class="data-table">
  <thead><tr><th>Food</th><th>Serve</th><th>Vitamin A (RAE)</th><th>% of men's RDI</th><th>Cost</th></tr></thead>
  <tbody>
    <tr><td>Sweet potato (baked)</td><td>1 medium (130g)</td><td>~960 mcg</td><td>107%</td><td>~$0.40</td></tr>
    <tr><td>Kale (cooked)</td><td>1/2 cup</td><td>~885 mcg</td><td>98%</td><td>~$0.30</td></tr>
    <tr><td>Carrots (cooked)</td><td>1/2 cup</td><td>~665 mcg</td><td>74%</td><td>~$0.20</td></tr>
    <tr><td>Pumpkin (cooked)</td><td>1/2 cup</td><td>~730 mcg</td><td>81%</td><td>~$0.20</td></tr>
    <tr><td>Spinach (cooked)</td><td>1/2 cup</td><td>~472 mcg</td><td>52%</td><td>~$0.20</td></tr>
    <tr><td>Red capsicum (raw)</td><td>1/2 cup</td><td>~117 mcg</td><td>13%</td><td>~$0.40</td></tr>
    <tr><td>Eggs</td><td>2 large</td><td>~90 mcg</td><td>10%</td><td>~$0.60</td></tr>
  </tbody>
</table>
<div class="absorption-rule">
  <div class="absorption-icon">🥕</div>
  <div><strong>Critical absorption rule:</strong> Beta-carotene from plant foods <em>requires dietary fat</em> to be absorbed. Always eat orange/yellow/green vegetables with a fat source — olive oil, avocado, eggs, or meat. Cooking also significantly increases beta-carotene bioavailability versus raw (cooked carrots have roughly 3× the absorbable beta-carotene of raw carrots).</div>
</div>
<div class="warning-box">
  <h3>Vitamin A toxicity — preformed retinol only</h3>
  <p>Beta-carotene from vegetables cannot cause toxicity (excess just turns skin slightly orange). But preformed retinol (from liver, supplements) can accumulate to toxic levels. <strong>Do not supplement preformed vitamin A</strong> beyond 3,000 mcg/day. Liver is safe 1–2 times per week for most adults but should be limited in pregnancy (risk of foetal abnormality at very high doses).</p>
</div>
</div>

<h2>The Daily Stack to Cover All 6 Gaps</h2>
<p>These foods together, eaten regularly, address all six gaps without supplements for most healthy adults. Total daily food cost: approximately <strong>$2.00–2.50</strong>.</p>

<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:20px;margin:16px 0">
  <div class="stack-item">
    <div><div class="stack-food">2 eggs daily</div><div class="stack-detail">Covers: Vitamin D (partial), B12, zinc, choline, vitamin A (partial)</div></div>
    <div class="stack-cost">~$0.60–1.00</div>
  </div>
  <div class="stack-item">
    <div><div class="stack-food">250 mL milk or 200g yoghurt</div><div class="stack-detail">Covers: Calcium (25–30%), iodine, B12, protein</div></div>
    <div class="stack-cost">~$0.40–0.60</div>
  </div>
  <div class="stack-item">
    <div><div class="stack-food">30g pumpkin seeds daily</div><div class="stack-detail">Covers: Magnesium (38% men), zinc (16%), iron, omega-3</div></div>
    <div class="stack-cost">~$0.30</div>
  </div>
  <div class="stack-item">
    <div><div class="stack-food">Sweet potato or 2 large carrots (with fat)</div><div class="stack-detail">Covers: Vitamin A (74–107%), fibre, potassium</div></div>
    <div class="stack-cost">~$0.20–0.40</div>
  </div>
  <div class="stack-item">
    <div><div class="stack-food">1 cup lentils or beans (3–4× per week)</div><div class="stack-detail">Covers: Iron (37%), zinc, magnesium, folate, fibre, protein</div></div>
    <div class="stack-cost">~$0.20/serve</div>
  </div>
  <div class="stack-item">
    <div><div class="stack-food">1 tin sardines (1–2× per week)</div><div class="stack-detail">Covers: Vitamin D (42%), calcium (35%), omega-3, B12, protein</div></div>
    <div class="stack-cost">~$1.50/tin</div>
  </div>
  <div class="stack-item">
    <div><div class="stack-food">100g beef or kangaroo mince (1–2× per week)</div><div class="stack-detail">Covers: Zinc (46–57%), haem iron (18–39%), B12, selenium</div></div>
    <div class="stack-cost">~$1.00/serve</div>
  </div>
  <div class="stack-item">
    <div><div class="stack-food">1/2 cup red capsicum with iron-rich meals</div><div class="stack-detail">Vitamin C to triple non-haem iron absorption</div></div>
    <div class="stack-cost">~$0.40</div>
  </div>
</div>

<h2>Absorption Rules Summary</h2>
<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:20px;margin:16px 0">
  <div class="absorption-rule">
    <div class="absorption-icon">🥩</div>
    <div><strong>Iron + Vitamin C (always)</strong> — Pair plant-based iron foods with capsicum, tomato, citrus or broccoli. Can triple non-haem iron absorption.</div>
  </div>
  <div class="absorption-rule">
    <div class="absorption-icon">🥕</div>
    <div><strong>Vitamin A + dietary fat (always)</strong> — Beta-carotene needs fat to absorb. Roast carrots in olive oil; eat sweet potato with eggs or meat.</div>
  </div>
  <div class="absorption-rule">
    <div class="absorption-icon">🫘</div>
    <div><strong>Zinc + soaking legumes</strong> — Soak lentils, chickpeas, beans overnight before cooking. Reduces phytates by 30–60%, nearly doubling zinc absorption.</div>
  </div>
  <div class="absorption-rule">
    <div class="absorption-icon">🥛</div>
    <div><strong>Calcium — spread across the day</strong> — The body absorbs calcium best in doses under 500 mg. Two to three dairy serves across the day is better than one large dose.</div>
  </div>
  <div class="absorption-rule">
    <div class="absorption-icon">☕</div>
    <div><strong>Iron — avoid tea/coffee within 1 hour</strong> — Tannins in tea and coffee bind to iron and reduce absorption by up to 60%. Drink water or orange juice with iron-rich meals instead.</div>
  </div>
  <div class="absorption-rule">
    <div class="absorption-icon">☀️</div>
    <div><strong>Vitamin D — sun exposure requires UV index 3+</strong> — Check the UV forecast. In winter in southern Australia, sun exposure won't synthesise vitamin D — food sources and supplementation become essential.</div>
  </div>
</div>

<div class="cta-box">
  <h2>See exactly where your gaps are</h2>
  <p>Enter your household members' ages and the app tracks which of these six nutrients you're getting enough of — and which meals will fill the gaps today.</p>
  <a class="cta-btn" href="/">Open the free app</a>
</div>
"""

p = BASE / "nutrient-gaps"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "The 6 Nutrient Gaps Most Australians Have | OptimisedEats",
    "ABS survey data shows 21–60% of Australians fall short on calcium, zinc, iron, magnesium, vitamin D and vitamin A. Full food tables with costs and absorption rules.",
    "nutrient deficiency Australia, calcium deficiency Australia, iron deficiency women, magnesium shortfall, vitamin D deficiency, zinc deficiency men",
    "Nutrient Gaps", "/guide/nutrient-gaps/",
    gaps_body,
    other_related("/guide/nutrient-gaps/")
), encoding="utf-8")
print("DONE guide/nutrient-gaps/index.html")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2: NRV REFERENCE TABLES
# ═══════════════════════════════════════════════════════════════════════════════

nrv_body = """
<h1>Australian Nutrient Reference Values — Complete Reference Tables</h1>
<p class="lead">These are the official NHMRC Nutrient Reference Values (NRVs) for Australia and New Zealand, published 2006 and updated 2017. Use these to understand how your nutrient requirements change across life stages.</p>

<div class="highlight-box">
  <h3>Understanding the terms</h3>
  <ul>
    <li><strong>RDI (Recommended Dietary Intake)</strong> — the daily intake sufficient to meet the needs of nearly all healthy people in a demographic group (97–98%). This is the target to aim for.</li>
    <li><strong>EAR (Estimated Average Requirement)</strong> — meets the needs of 50% of people. If you're below the EAR, you're very likely deficient.</li>
    <li><strong>AI (Adequate Intake)</strong> — used when an RDI can't be established; based on observed intakes of healthy populations.</li>
    <li><strong>UL (Upper Level of Intake)</strong> — the highest daily intake unlikely to cause harm. Toxicity is possible above this level.</li>
  </ul>
</div>

<h2>Daily Energy Requirements</h2>
<p>Energy requirements depend on age, sex, and physical activity level (PAL). Values below assume a sedentary to lightly active lifestyle.</p>
<table class="data-table">
  <thead><tr><th>Age / sex</th><th>Energy (kJ/day)</th><th>Energy (kcal/day)</th></tr></thead>
  <tbody>
    <tr><td>Children 4–8</td><td>6,500–7,100</td><td>1,554–1,697</td></tr>
    <tr><td>Children 9–11 (boys)</td><td>8,200</td><td>1,960</td></tr>
    <tr><td>Children 9–11 (girls)</td><td>7,400</td><td>1,768</td></tr>
    <tr><td>Teens 14–18 (boys)</td><td>11,700</td><td>2,795</td></tr>
    <tr><td>Teens 14–18 (girls)</td><td>9,000</td><td>2,150</td></tr>
    <tr><td>Adult men 19–30</td><td>10,900</td><td>2,604</td></tr>
    <tr><td>Adult women 19–30</td><td>8,700</td><td>2,079</td></tr>
    <tr><td>Adult men 51–70</td><td>9,600</td><td>2,293</td></tr>
    <tr><td>Adult women 51–70</td><td>7,900</td><td>1,887</td></tr>
    <tr><td>Pregnancy (2nd trimester)</td><td>+1,400</td><td>+335</td></tr>
    <tr><td>Lactation (first 6 months)</td><td>+2,100</td><td>+502</td></tr>
  </tbody>
</table>
<p class="nrv-note">Source: NHMRC Nutrient Reference Values for Australia and New Zealand, 2006 (updated 2017). Active individuals may require 20–80% more energy than values shown.</p>

<h2>Macronutrients</h2>
<table class="data-table">
  <thead><tr><th>Nutrient</th><th>Children 4–8</th><th>Teens 14–18 (M/F)</th><th>Adults 19–50 (M/F)</th><th>Pregnancy</th><th>Elderly 70+ (M/F)</th></tr></thead>
  <tbody>
    <tr><td><strong>Protein RDI (g/day)</strong></td><td>20g</td><td>65 / 45g</td><td>64 / 46g</td><td>58–60g</td><td>81 / 57g</td></tr>
    <tr><td><strong>Fibre AI (g/day)</strong></td><td>18g</td><td>28 / 22g</td><td>30 / 25g</td><td>28g</td><td>30 / 25g</td></tr>
    <tr><td><strong>Water AI (L/day)</strong></td><td>1.2–1.6L</td><td>2.7 / 2.2L</td><td>3.4 / 2.8L</td><td>3.1L</td><td>3.4 / 2.8L</td></tr>
  </tbody>
</table>
<p class="nrv-note">AMDR (Acceptable Macronutrient Distribution Ranges): Carbohydrates 45–65% of energy · Fat 20–35% · Protein 10–35%. Saturated fat: &lt;10% of energy. Added sugars: &lt;10% of energy.</p>

<h2>Fat-Soluble Vitamins</h2>
<table class="data-table">
  <thead><tr><th>Nutrient</th><th>Children 4–8</th><th>Teens 14–18 (M/F)</th><th>Adults 19–50 (M/F)</th><th>Pregnancy</th><th>Lactation</th><th>UL (adults)</th></tr></thead>
  <tbody>
    <tr><td><strong>Vitamin A (mcg RAE)</strong></td><td>400</td><td>900 / 700</td><td>900 / 700</td><td>800</td><td>1,100</td><td>3,000</td></tr>
    <tr><td><strong>Vitamin D (mcg / IU)</strong></td><td>5 / 200</td><td>5 / 200</td><td>5 / 200 (≤50) · 10–15 / 400–600 (51+)</td><td>5 / 200</td><td>5 / 200</td><td>80 / 3,200</td></tr>
    <tr><td><strong>Vitamin E (mg)</strong></td><td>6</td><td>10 / 8</td><td>10 / 7</td><td>7</td><td>11</td><td>300</td></tr>
    <tr><td><strong>Vitamin K (mcg) AI</strong></td><td>55</td><td>65 / 60</td><td>70 / 60</td><td>60</td><td>60</td><td>—</td></tr>
  </tbody>
</table>
<p class="nrv-note">Vitamin D values shown are RDIs. Many experts recommend higher vitamin D targets (600–2,000 IU/day) for adults, especially in winter or at southern latitudes. Consult your GP for testing and personalised advice.</p>

<h2>Water-Soluble Vitamins</h2>
<table class="data-table">
  <thead><tr><th>Nutrient</th><th>Children 4–8</th><th>Teens 14–18 (M/F)</th><th>Adults 19–50 (M/F)</th><th>Pregnancy</th><th>Lactation</th></tr></thead>
  <tbody>
    <tr><td><strong>Vitamin C (mg)</strong></td><td>35</td><td>40 / 40</td><td>45 / 45</td><td>60</td><td>85</td></tr>
    <tr><td><strong>Vitamin B1 — Thiamin (mg)</strong></td><td>0.6</td><td>1.1 / 0.9</td><td>1.2 / 1.1</td><td>1.4</td><td>1.4</td></tr>
    <tr><td><strong>Vitamin B2 — Riboflavin (mg)</strong></td><td>0.6</td><td>1.3 / 1.1</td><td>1.3 / 1.1</td><td>1.4</td><td>1.6</td></tr>
    <tr><td><strong>Vitamin B3 — Niacin (mg NE)</strong></td><td>8</td><td>16 / 14</td><td>16 / 14</td><td>18</td><td>17</td></tr>
    <tr><td><strong>Vitamin B6 (mg)</strong></td><td>0.6</td><td>1.3 / 1.2</td><td>1.3 / 1.3</td><td>1.9</td><td>2.0</td></tr>
    <tr><td><strong>Folate (mcg DFE)</strong></td><td>200</td><td>400 / 400</td><td>400 / 400</td><td>600</td><td>500</td></tr>
    <tr><td><strong>Vitamin B12 (mcg)</strong></td><td>1.5</td><td>2.4 / 2.4</td><td>2.4 / 2.4</td><td>2.6</td><td>2.8</td></tr>
    <tr><td><strong>Choline (mg) AI</strong></td><td>250</td><td>375 / 375</td><td>550 / 425</td><td>450</td><td>550</td></tr>
  </tbody>
</table>
<p class="nrv-note">Folate in pregnancy: Women planning a pregnancy should start supplementing 400–800 mcg/day of folic acid one month before conception and through the first trimester. DFE = Dietary Folate Equivalents (food folate + 1.7× supplemental folic acid).</p>

<h2>Major Minerals</h2>
<table class="data-table">
  <thead><tr><th>Nutrient</th><th>Children 4–8</th><th>Teens 14–18 (M/F)</th><th>Adults 19–50 (M/F)</th><th>Pregnancy</th><th>Elderly 70+ (M/F)</th></tr></thead>
  <tbody>
    <tr><td><strong>Calcium (mg)</strong></td><td>700</td><td>1,300 / 1,300</td><td>1,000 / 1,000</td><td>1,000</td><td>1,300 / 1,300</td></tr>
    <tr><td><strong>Magnesium (mg)</strong></td><td>130</td><td>410 / 360</td><td>420 / 320</td><td>350–360</td><td>420 / 320</td></tr>
    <tr><td><strong>Potassium (mg) AI</strong></td><td>2,300</td><td>3,600 / 2,600</td><td>3,800 / 2,800</td><td>2,800</td><td>3,800 / 2,800</td></tr>
    <tr><td><strong>Phosphorus (mg)</strong></td><td>500</td><td>1,250 / 1,250</td><td>1,000 / 1,000</td><td>1,000</td><td>1,000 / 1,000</td></tr>
  </tbody>
</table>

<h2>Trace Minerals</h2>
<table class="data-table">
  <thead><tr><th>Nutrient</th><th>Children 4–8</th><th>Teens 14–18 (M/F)</th><th>Adults 19–50 (M/F)</th><th>Pregnancy</th><th>Lactation</th></tr></thead>
  <tbody>
    <tr><td><strong>Iron (mg)</strong></td><td>10</td><td>11 / 15</td><td>8 / 18</td><td>27</td><td>9</td></tr>
    <tr><td><strong>Zinc (mg)</strong></td><td>5</td><td>13 / 7</td><td>14 / 8</td><td>10–11</td><td>11–12</td></tr>
    <tr><td><strong>Iodine (mcg)</strong></td><td>90</td><td>150 / 150</td><td>150 / 150</td><td>220</td><td>270</td></tr>
    <tr><td><strong>Selenium (mcg)</strong></td><td>25</td><td>70 / 60</td><td>70 / 60</td><td>65</td><td>75</td></tr>
    <tr><td><strong>Copper (mg)</strong></td><td>0.6</td><td>1.3 / 1.2</td><td>1.7 / 1.2</td><td>1.3</td><td>1.5</td></tr>
  </tbody>
</table>

<h2>Special Population Notes</h2>

<h3>Pregnancy</h3>
<ul>
  <li><strong>Folate:</strong> +50% increase to 600 mcg/day. Supplementation strongly recommended from pre-conception through first trimester.</li>
  <li><strong>Iron:</strong> Increases to 27 mg/day — the highest of any demographic. Haem sources (meat) are strongly advised alongside plant sources with vitamin C.</li>
  <li><strong>Iodine:</strong> Increases to 220 mcg/day (up 47%). Australian soils are iodine-poor — use iodised salt; consider a prenatal supplement with 150 mcg iodine.</li>
  <li><strong>Choline:</strong> 450 mg/day — supports foetal brain development. Eggs are the richest affordable source (2 eggs ≈ 280 mg).</li>
  <li><strong>DHA:</strong> Not in NHMRC tables, but WHO recommends 200+ mg/day for pregnancy. Canned sardines and salmon are the most affordable sources.</li>
</ul>

<h3>Elderly (70+)</h3>
<ul>
  <li><strong>Calcium:</strong> Rises to 1,300 mg/day (same as teenagers) — bone loss accelerates in post-menopausal women.</li>
  <li><strong>Vitamin D:</strong> Increases to 15–20 mcg (600–800 IU/day). Elderly skin is less efficient at synthesising vitamin D from sun exposure.</li>
  <li><strong>Protein:</strong> Recommended at 1.0–1.2 g/kg body weight (higher than the 0.75 g/kg for younger adults) to prevent sarcopenia (muscle loss).</li>
  <li><strong>B12:</strong> Absorption from food declines with age due to reduced stomach acid. B12 from supplements or fortified foods (not requiring stomach acid) is preferred.</li>
</ul>

<h3>Vegan / Plant-Based</h3>
<ul>
  <li><strong>B12:</strong> <em>Cannot</em> be reliably obtained from plant foods. Supplementation is essential — 500–2,000 mcg cyanocobalamin per week.</li>
  <li><strong>Iron:</strong> Only non-haem iron available — always pair with vitamin C, and increase intake by ~80% over RDI to compensate for lower bioavailability.</li>
  <li><strong>Zinc:</strong> Plant zinc is poorly absorbed. Soak all legumes; increase intake by ~50% over RDI.</li>
  <li><strong>Iodine:</strong> Seaweed is highly variable. Use iodised salt or supplement.</li>
  <li><strong>Omega-3 DHA:</strong> ALA from flaxseed/chia converts poorly to DHA. Algae-based DHA supplements are the only reliable vegan source.</li>
  <li><strong>Calcium:</strong> Use calcium-set tofu, fortified plant milks, and green vegetables. Avoid high-oxalate greens (spinach, chard) as the sole calcium source — oxalates block absorption.</li>
</ul>

<div class="cta-box">
  <h2>Your personalised NRV targets in the app</h2>
  <p>Enter each family member's age, sex and life stage — the app calculates their exact NRV targets and tracks how each day's meals measure up.</p>
  <a class="cta-btn" href="/">Calculate your targets</a>
</div>
"""

p = BASE / "nrv"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "Australian Nutrient Reference Values — Complete NRV Tables | OptimisedEats",
    "Complete NHMRC Nutrient Reference Values (RDI, AI, EAR, UL) for all demographics — children, teens, adults, pregnancy, lactation and elderly. Updated 2017.",
    "Australian nutrient reference values, NHMRC NRV tables, RDI Australia, nutrient requirements by age, vitamin mineral requirements Australia",
    "NRV Reference Tables", "/guide/nrv/",
    nrv_body,
    other_related("/guide/nrv/")
), encoding="utf-8")
print("DONE guide/nrv/index.html")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3: BUDGET NUTRITION ARSENAL
# ═══════════════════════════════════════════════════════════════════════════════

arsenal_body = """
<h1>The Budget Nutrition Arsenal</h1>
<p class="lead">Not all cheap foods are equal. This is a ranked system for building a nutritious diet at minimum cost — organised into three tiers based on nutrient density per dollar, versatility, and shelf life.</p>

<div class="highlight-box">
  <h3>How to use this list</h3>
  <p>Build your diet around Tier 1 foods as your daily base. Add Tier 2 foods for variety and completeness. Use Tier 3 strategically to fill specific gaps. Most families can meet 90%+ of their nutrient targets with the first two tiers alone.</p>
</div>

<h2><span class="tier-badge tier1">TIER 1</span> Nutritional Pillars — Build your diet around these</h2>
<p>These are the highest nutrient density per dollar foods available in Australian supermarkets. Each one is cheap, versatile, shelf-stable or freezable, and covers multiple nutrients.</p>

<div class="nutrient-section">
<h3>Eggs (~$0.50–0.60 each)</h3>
<p>The most complete whole food at any price point. Two eggs deliver approximately:</p>
<ul>
  <li>12g complete protein (all essential amino acids)</li>
  <li>Vitamin B12 (46% RDI), Vitamin A (16%), Vitamin D (12%), Choline (280 mg — 50–65% RDI)</li>
  <li>Selenium (54% RDI), Zinc (9%), Iron (9%)</li>
</ul>
<p>Buy the 12-pack or larger — the per-egg price drops 20–30% vs smaller packs. Free-range and omega-3 enriched eggs deliver meaningfully more vitamin D and omega-3 for a small price premium.</p>
</div>

<div class="nutrient-section">
<h3>Red Lentils (~$3–5/kg dry)</h3>
<p>The best-value plant protein in Australia. Per 200g cooked serve:</p>
<ul>
  <li>18g protein, 16g fibre</li>
  <li>Folate (72% RDI), Iron (37% women's RDI), Zinc (18%)</li>
  <li>Magnesium (17%), Potassium (21%), B1 Thiamin (22%)</li>
</ul>
<p>Red lentils cook in 15–20 minutes without soaking. They dissolve completely into soups and sauces, making them ideal for hidden nutrition in family cooking. Buy 1–2 kg bags for maximum savings.</p>
</div>

<div class="nutrient-section">
<h3>Canned Sardines (~$1.50–2.50/tin)</h3>
<p>One of the most underrated foods in Australia. A single 95g tin delivers:</p>
<ul>
  <li>23g protein</li>
  <li>Omega-3 (DHA + EPA): ~1,000–1,500 mg</li>
  <li>Vitamin D: ~250 IU (42% RDI) — one of the few affordable food sources</li>
  <li>Calcium: ~350 mg (35% RDI) from softened bones</li>
  <li>Vitamin B12: ~150% RDI</li>
  <li>Selenium: ~70% RDI</li>
</ul>
<p>Buy in bulk when on special — shelf life of 2–3 years. Sardines in olive oil offer better omega-3 preservation than brine or tomato sauce.</p>
</div>

<div class="nutrient-section">
<h3>Rolled Oats (~$2–4/kg)</h3>
<p>The cheapest complete breakfast and the most versatile grain. Per 80g dry serve:</p>
<ul>
  <li>11g protein, 8g fibre (including beta-glucan — clinically proven to lower LDL cholesterol)</li>
  <li>Manganese (191% RDI), Phosphorus (41%), Magnesium (13%), Zinc (16%)</li>
  <li>B1 Thiamin (51%), Iron (22%), Selenium (22%)</li>
</ul>
<p>Much cheaper than any packaged cereal with a fraction of the added sugar. Buy the 1–2 kg bags. Traditional rolled oats have a lower glycaemic index than quick oats.</p>
</div>

<div class="nutrient-section">
<h3>Frozen Spinach / Kale (~$2–3/500g)</h3>
<p>Nutritionally superior to fresh for cooking purposes and far cheaper. Per 1 cup cooked (180g):</p>
<ul>
  <li>Vitamin K: 250%+ RDI (vital for blood clotting and bone health)</li>
  <li>Vitamin A: 47% RDI (as beta-carotene)</li>
  <li>Folate: 33% RDI, Iron: 36% women's RDI, Magnesium: 37%</li>
  <li>Vitamin C: 29% RDI, Calcium: 24%</li>
</ul>
<p>A 500g bag costs ~$2–3 and contains the equivalent of 3–4 fresh bunches. Add to anything — soups, pasta sauce, curries, eggs. Almost impossible to detect when blended into sauces.</p>
</div>

<div class="nutrient-section">
<h3>Chicken (whole or thighs) (~$4–7 whole / ~$6–8/kg thighs)</h3>
<p>The most affordable complete animal protein. A whole chicken typically yields 4–5 meals and the carcass makes 2–3 litres of bone broth.</p>
<ul>
  <li>Per 100g cooked thigh: 26g protein, Zinc (20%), Selenium (35%), B3 Niacin (50%), B6 (30%), B12 (10%)</li>
  <li>Thighs are 40–50% cheaper per kg than breast fillets with superior fat content (monosaturated)</li>
</ul>
</div>

<h2><span class="tier-badge tier2">TIER 2</span> Essential Supporting Foods</h2>
<p>These foods provide variety, specific nutrients, and build complete meals around your Tier 1 base.</p>

<table class="data-table">
  <thead><tr><th>Food</th><th>Approx. cost</th><th>Primary nutritional value</th></tr></thead>
  <tbody>
    <tr><td>Sweet potato</td><td>~$2–3/kg</td><td>Vitamin A (107% RDI per medium), fibre, potassium, vitamin C</td></tr>
    <tr><td>Canned tomatoes</td><td>~$0.80–1.20/tin</td><td>Lycopene (antioxidant, bioavailable when cooked), vitamin C, folate</td></tr>
    <tr><td>Carrots</td><td>~$1.50/kg</td><td>Beta-carotene (vitamin A — 74% RDI per ½ cup cooked), fibre, potassium</td></tr>
    <tr><td>Full-cream milk</td><td>~$1.50–2/L</td><td>Calcium (300mg/cup), iodine, protein, B12, B2</td></tr>
    <tr><td>Brown rice</td><td>~$2–3/kg</td><td>Fibre, manganese, B vitamins, magnesium — more nutritious than white</td></tr>
    <tr><td>Canned chickpeas</td><td>~$1.20/400g tin</td><td>Plant protein, folate, iron, zinc, fibre</td></tr>
    <tr><td>Pumpkin seeds</td><td>~$8–12/kg</td><td>Magnesium (38% RDI/30g), zinc (16%), omega-3 ALA, iron</td></tr>
    <tr><td>Frozen mixed vegetables</td><td>~$2–3/kg</td><td>Vitamins A, C, K; fibre; B vitamins — nutritionally equivalent to fresh</td></tr>
    <tr><td>Bananas</td><td>~$2–3/kg</td><td>Potassium, B6, magnesium, quick energy, prebiotic fibre</td></tr>
    <tr><td>Cabbage</td><td>~$1–2/head</td><td>Vitamin C (54% RDI/cup), vitamin K, folate — one of the cheapest vegetables</td></tr>
    <tr><td>Beef mince (lean)</td><td>~$8–12/kg</td><td>Complete protein, zinc (57% RDI/100g), haem iron (18%), B12, selenium</td></tr>
    <tr><td>Kangaroo mince</td><td>~$9–12/kg</td><td>Leanest red meat in AU — iron (31–39% RDI/100g), zinc (46%), protein, B12</td></tr>
  </tbody>
</table>

<h2><span class="tier-badge tier3">TIER 3</span> Strategic Gap-Fillers</h2>
<p>These foods fill specific nutritional holes cost-effectively. Use them targeted rather than as daily staples.</p>

<table class="data-table">
  <thead><tr><th>Food</th><th>Gap it fills</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>Canned salmon (~$2–3/tin)</td><td>Vitamin D, omega-3, calcium</td><td>Higher vitamin D than sardines; useful variety</td></tr>
    <tr><td>Peanut butter (~$4–5/kg)</td><td>Healthy fats, protein, niacin, magnesium</td><td>Check for no-added-sugar varieties; very satiating</td></tr>
    <tr><td>Fortified breakfast cereal</td><td>Iron, B vitamins, folate</td><td>Check label — choose low sugar, high iron (>25% RDI/serve)</td></tr>
    <tr><td>Iodised salt</td><td>Iodine</td><td>Critical — regular salt and sea salt are NOT iodised. Switch to iodised.</td></tr>
    <tr><td>Frozen berries (~$4–6/kg)</td><td>Antioxidants, vitamin C, fibre</td><td>Significantly cheaper than fresh; nutritionally equivalent</td></tr>
    <tr><td>Dark chocolate 70%+ (~$3–4/100g)</td><td>Iron (19% RDI/30g), magnesium, antioxidants</td><td>Small amounts go a long way; avoid milk chocolate</td></tr>
    <tr><td>Canned tuna (~$1.50–2/tin)</td><td>Protein, omega-3, selenium, B12</td><td>Good variety to sardines; lower vitamin D but more popular with kids</td></tr>
    <tr><td>Greek yoghurt (~$5–7/kg)</td><td>Calcium, probiotics, protein, B12</td><td>Probiotics support gut microbiome; full-fat is more satiating</td></tr>
    <tr><td>Walnuts (~$15–20/kg)</td><td>Omega-3 ALA, brain-protective polyphenols</td><td>Most expensive item here but a small daily serve (30g) is effective</td></tr>
    <tr><td>Beef/chicken liver (~$3–6/kg)</td><td>B12 (2,917% RDI/100g), vitamin A, folate, iron, riboflavin</td><td>Limit to 1–2×/week. Exceptional nutrition but very high vitamin A — avoid in pregnancy first trimester.</td></tr>
  </tbody>
</table>

<h2>Weekly Shopping Budget Targets</h2>
<table class="data-table">
  <thead><tr><th>Household</th><th>Tight budget</th><th>Comfortable budget</th><th>Includes</th></tr></thead>
  <tbody>
    <tr><td>Single adult</td><td>$47/week</td><td>$65/week</td><td>All Tier 1 + most Tier 2 foods</td></tr>
    <tr><td>Couple</td><td>$85/week</td><td>$110/week</td><td>Full nutrient coverage for two adults</td></tr>
    <tr><td>Family of 4 (2 adults, 2 kids)</td><td>$107/week</td><td>$145/week</td><td>Age-appropriate quantities for children</td></tr>
  </tbody>
</table>

<div class="cta-box">
  <h2>Build your personalised shopping list</h2>
  <p>The app uses this exact tiered approach to generate shopping lists for your household — based on each person's nutrient targets and your weekly budget.</p>
  <a class="cta-btn" href="/">Generate your shopping list</a>
</div>
"""

p = BASE / "arsenal"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "The Budget Nutrition Arsenal — Best Value Foods in Australia | OptimisedEats",
    "A 3-tier ranked system of the most nutrient-dense affordable foods in Australian supermarkets. Eggs, sardines, lentils, oats — with full nutrient data per serve.",
    "best value healthy foods Australia, nutrient dense cheap foods, budget nutrition arsenal, cheap superfoods Australia",
    "Budget Arsenal", "/guide/arsenal/",
    arsenal_body,
    other_related("/guide/arsenal/")
), encoding="utf-8")
print("DONE guide/arsenal/index.html")

print("\nAll technical pages generated!")
