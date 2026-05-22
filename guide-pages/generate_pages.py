"""Generate all static HTML pages for the OptimisedEats guide hub."""
import os, pathlib

BASE = pathlib.Path(__file__).parent
CSS = (BASE / "_shared.css").read_text(encoding="utf-8")

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
<style>{CSS}</style>
</head>
<body>
<header class="site-header">
  <div class="site-header-inner">
    <a class="logo" href="/"><span>Optimised</span>Eats</a>
    <a class="header-cta" href="/">Open Free App →</a>
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
  <p style="margin-top:6px;font-size:11px;color:#cbd5e1">This information is for general educational purposes only and does not constitute medical or dietary advice. Please consult a qualified health professional for personal guidance.</p>
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

# Hub index is written by generate_all.py — not here.

# ── BUDGET BASICS ─────────────────────────────────────────────────────────────
budget_body = """
<h1>Budget Nutrition Basics</h1>
<p class="lead">Eating well doesn't require an expensive diet. These are the cheapest, most nutrient-dense foods available at Australian and New Zealand supermarkets right now.</p>

<h2>The cheapest nutrient-dense foods</h2>
<p>Price per kilogram matters less than <strong>cost per unit of nutrition</strong>. The foods below consistently deliver the most protein, vitamins and minerals per dollar.</p>

<table class="data-table">
  <thead><tr><th>Food</th><th>Cost (approx.)</th><th>Why it's a powerhouse</th></tr></thead>
  <tbody>
    <tr><td>Rolled oats</td><td>~$2/kg</td><td>Fibre, B vitamins, manganese, slow-release energy</td></tr>
    <tr><td>Red lentils</td><td>~$3/kg</td><td>Plant protein, folate, iron, fibre</td></tr>
    <tr><td>Canned sardines</td><td>~$1.50/can</td><td>Omega-3, vitamin D, calcium (from bones), B12</td></tr>
    <tr><td>Eggs (12-pack)</td><td>~$5–7</td><td>Complete protein, choline, vitamins A, D, B12</td></tr>
    <tr><td>Frozen mixed veg</td><td>~$2–3/kg</td><td>Vitamins A, C, K; fibre; often more nutritious than fresh</td></tr>
    <tr><td>Canned chickpeas</td><td>~$1.20/can</td><td>Protein, fibre, folate, iron</td></tr>
    <tr><td>Whole chicken</td><td>~$4–7 each</td><td>Complete protein, zinc, selenium, B vitamins</td></tr>
    <tr><td>Sweet potato</td><td>~$2–3/kg</td><td>Beta-carotene (vitamin A), vitamin C, potassium, fibre</td></tr>
    <tr><td>Full-cream milk</td><td>~$1.50–2/L</td><td>Calcium, iodine, protein, vitamin D (if fortified)</td></tr>
    <tr><td>Frozen spinach</td><td>~$2–3/500g</td><td>Iron, folate, vitamin K, magnesium</td></tr>
  </tbody>
</table>

<div class="highlight-box">
  <h3>💡 The sardine secret</h3>
  <p>Canned sardines are one of the most underrated budget foods. A single 95g can delivers roughly 15g protein, 200mg calcium (from softened bones), vitamin D, and omega-3 fatty acids — all for around $1.50. They're one of the few affordable sources of vitamin D in Australia.</p>
</div>

<h2>How much does healthy eating really cost?</h2>
<p>A realistic daily food budget for a single adult eating nutritiously is <strong>$7–12 per day</strong>, or $50–85 per week. Families of 4 can often achieve $120–180 per week with smart planning.</p>
<p>Key strategies that lower the bill:</p>
<ul>
  <li><strong>Legumes as your protein base</strong> — lentils and chickpeas cost 60–80% less than meat per gram of protein</li>
  <li><strong>Eggs over packaged snacks</strong> — two eggs cost ~80c and are more filling and nutritious than most snack bars</li>
  <li><strong>Frozen over fresh</strong> for vegetables you'll cook — nutritionally equivalent and far cheaper when produce is out of season</li>
  <li><strong>Buy whole, not pre-cut</strong> — a whole chicken is often 40% cheaper per kg than chicken breast fillets</li>
</ul>

<h2>Nutrients Australians commonly fall short on</h2>
<p>Australian dietary surveys identify these as the most commonly inadequate nutrients:</p>
<ul>
  <li><strong>Vitamin D</strong> — despite our sunshine, office work and sunscreen use mean many Australians are deficient. Sardines, eggs and UV-exposed mushrooms help.</li>
  <li><strong>Magnesium</strong> — found in legumes, wholegrains, nuts and leafy greens</li>
  <li><strong>Iodine</strong> — use iodised salt and eat seafood or dairy regularly</li>
  <li><strong>Folate</strong> — critical in pregnancy; found in lentils, spinach, broccoli</li>
  <li><strong>Iron</strong> — especially in women of reproductive age; red meat, legumes with vitamin C foods</li>
</ul>

<div class="warning-box">
  <h3>⚠️ Don't stress every single day</h3>
  <p>Most vitamins and minerals balance out over the week, not day-by-day. Fat-soluble vitamins (A, D, E, K) and B12 are stored by the body for weeks or months. Focus on your weekly average rather than perfecting every meal.</p>
</div>

<div class="cta-box">
  <h2>Build your personalised meal plan</h2>
  <p>Our free app calculates exact nutrient targets for each person in your household based on their age, sex and life stage — then suggests meals to hit those targets on your budget.</p>
  <a class="cta-btn" href="/">Try it free →</a>
</div>
"""

p = BASE / "budget-basics"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "Budget Nutrition Basics — How to Eat Well for Less | OptimisedEats",
    "The cheapest nutrient-dense foods at Australian supermarkets. Learn how to eat healthily for $7–12 per day with practical strategies for families.",
    "budget nutrition Australia, cheap healthy food, nutrient dense cheap foods, affordable meal planning",
    "Budget Basics", "/guide/budget-basics/",
    budget_body,
    other_related("/guide/budget-basics/")
), encoding="utf-8")
print("DONE guide/budget-basics/index.html")

# ── PREGNANCY ─────────────────────────────────────────────────────────────────
pregnancy_body = """
<h1>Pregnancy Nutrition on a Budget</h1>
<p class="lead">Your nutrient needs increase significantly during pregnancy — but eating well for two doesn't mean spending double. Here's what matters most and the cheapest foods to get it.</p>

<h2>The most critical nutrients in pregnancy</h2>

<h3>Folate (Folic acid)</h3>
<p>Folate is essential in the first trimester to prevent neural tube defects. The recommended intake jumps to <strong>600 mcg/day</strong> during pregnancy (up from 400 mcg). Best budget sources:</p>
<ul>
  <li>Red lentils — 1 cup cooked delivers ~360 mcg folate (~60% of daily need)</li>
  <li>Frozen spinach — 1 cup cooked ~263 mcg</li>
  <li>Canned chickpeas — 1 cup ~282 mcg</li>
  <li>Broccoli — 1 cup cooked ~168 mcg</li>
</ul>
<p>Most midwives and GPs recommend a folate supplement (400–800 mcg/day) from at least one month before conception through the first trimester.</p>

<h3>Iron</h3>
<p>Iron needs nearly double in pregnancy to <strong>27 mg/day</strong> (up from 18 mg for women of reproductive age). Iron supports the expanding blood volume and foetal development.</p>
<ul>
  <li>Kangaroo mince — ~7 mg per 100g (one of the richest iron foods available)</li>
  <li>Beef mince (lean) — ~3 mg per 100g</li>
  <li>Canned lentils — ~3.3 mg per cup</li>
  <li>Pair plant iron sources with vitamin C (capsicum, citrus) to double absorption</li>
</ul>

<h3>Iodine</h3>
<p>Iodine is critical for foetal brain and thyroid development. Australian soils are iodine-poor, making dietary iodine harder to get. Target: <strong>220 mcg/day</strong>.</p>
<ul>
  <li>Use iodised salt (not sea salt or Himalayan salt, which are low in iodine)</li>
  <li>Dairy milk — ~50 mcg per cup</li>
  <li>Canned tuna or salmon — ~35 mcg per 100g</li>
  <li>Eggs — ~27 mcg each</li>
</ul>
<p>Many pregnancy multivitamins include 150 mcg iodine — check your supplement label.</p>

<h3>DHA (Omega-3)</h3>
<p>DHA supports foetal brain and eye development. Aim for at least <strong>200 mg/day</strong>.</p>
<ul>
  <li>Canned sardines — ~1000 mg omega-3 per can (excellent)</li>
  <li>Canned salmon — ~1500 mg per 100g</li>
  <li>Eggs (omega-3 enriched) — ~300 mg each</li>
</ul>

<h3>Calcium</h3>
<p>The growing baby draws calcium from your bones if your intake is low. Target: <strong>1000 mg/day</strong>.</p>
<ul>
  <li>Full-cream milk — ~300 mg per cup (cheapest source)</li>
  <li>Canned sardines with bones — ~200 mg per 95g can</li>
  <li>Hard cheese — ~200–300 mg per 30g serve</li>
  <li>Frozen broccoli — ~62 mg per cup</li>
</ul>

<div class="highlight-box">
  <h3>🐟 Sardines in pregnancy</h3>
  <p>Canned sardines are one of the best pregnancy foods available: they provide DHA omega-3, calcium (from bones), vitamin D, iodine, and B12 in a single affordable can (~$1.50). They're low in mercury unlike large predatory fish such as shark, swordfish and flake — which should be limited in pregnancy.</p>
</div>

<h2>Foods to limit or avoid in pregnancy</h2>
<ul>
  <li><strong>High-mercury fish</strong>: shark (flake), swordfish, marlin, orange roughy — limit to once a fortnight</li>
  <li><strong>Liver and pâté</strong>: very high in vitamin A (retinol) — can cause birth defects in excess</li>
  <li><strong>Unpasteurised dairy</strong>, soft cheeses (brie, camembert, feta unless cooked), deli meats — listeria risk</li>
  <li><strong>Raw or undercooked eggs, meat and seafood</strong></li>
  <li><strong>Alcohol</strong> — no safe amount has been established</li>
  <li><strong>Caffeine</strong> — limit to 200 mg/day (about 2 instant coffees)</li>
</ul>

<h2>Sample budget pregnancy meal day (~$8)</h2>
<table class="data-table">
  <thead><tr><th>Meal</th><th>Foods</th><th>Cost</th></tr></thead>
  <tbody>
    <tr><td>Breakfast</td><td>Oats with milk + banana + handful of almonds</td><td>~$1.50</td></tr>
    <tr><td>Lunch</td><td>Lentil soup with frozen spinach + wholegrain bread</td><td>~$2.50</td></tr>
    <tr><td>Snack</td><td>2 boiled eggs + piece of fruit</td><td>~$1.20</td></tr>
    <tr><td>Dinner</td><td>Sardine pasta with garlic and olive oil + side salad</td><td>~$2.80</td></tr>
  </tbody>
</table>

<div class="cta-box">
  <h2>Track pregnancy nutrition for free</h2>
  <p>Our app has a Pregnancy profile that sets the right nutrient targets automatically. See exactly how each meal contributes to your daily folate, iron, calcium and DHA goals.</p>
  <a class="cta-btn" href="/">Open the free app →</a>
</div>
"""

p = BASE / "pregnancy"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "Pregnancy Nutrition on a Budget | OptimisedEats",
    "Folate, iron, iodine and DHA needs during pregnancy — and the cheapest foods to meet them in Australia and New Zealand.",
    "pregnancy nutrition Australia, folate pregnancy, iron pregnancy, cheap pregnancy food, DHA pregnancy",
    "Pregnancy Nutrition", "/guide/pregnancy/",
    pregnancy_body,
    other_related("/guide/pregnancy/")
), encoding="utf-8")
print("DONE guide/pregnancy/index.html")

# ── KIDS ──────────────────────────────────────────────────────────────────────
kids_body = """
<h1>Kids &amp; Toddler Nutrition on a Budget</h1>
<p class="lead">Children's brains and bodies grow fast — but the cheapest foods often deliver the most critical nutrients for development. Here's what matters at each stage.</p>

<h2>Iron: the most important nutrient for toddlers</h2>
<p>Iron deficiency is the most common nutritional deficiency in Australian children. Low iron in the first two years of life can cause permanent cognitive impairment. The warning signs are often subtle — fatigue, pale skin, poor appetite, and slower development.</p>
<p><strong>Toddler iron target (1–3 years): 9 mg/day</strong></p>
<ul>
  <li>Beef mince — ~3 mg per 100g (the most bioavailable form, haem iron)</li>
  <li>Kangaroo mince — ~7 mg per 100g (exceptional)</li>
  <li>Chicken thigh — ~1.3 mg per 100g</li>
  <li>Lentils — ~3.3 mg per cup cooked (pair with tomato or capsicum for better absorption)</li>
  <li>Fortified breakfast cereals — check labels, some deliver 2–5 mg per serve</li>
</ul>

<div class="warning-box">
  <h3>⚠️ Cow's milk and iron absorption</h3>
  <p>Cow's milk given before 12 months can interfere with iron absorption and cause gut bleeding. After 12 months, limit to ~500 ml/day — too much milk fills small stomachs and crowds out iron-rich foods.</p>
</div>

<h2>Calcium for growing bones</h2>
<p>Calcium is critical for bone density, which builds throughout childhood and peaks around age 25. Dairy is the most concentrated affordable source.</p>
<table class="data-table">
  <thead><tr><th>Age</th><th>Calcium target</th><th>Cheap food sources</th></tr></thead>
  <tbody>
    <tr><td>1–3 years</td><td>500 mg/day</td><td>1–2 cups milk, yoghurt, cheese</td></tr>
    <tr><td>4–8 years</td><td>700 mg/day</td><td>2 cups milk or equivalent</td></tr>
    <tr><td>9–11 years</td><td>1000 mg/day</td><td>Milk + cheese + sardines</td></tr>
    <tr><td>12–18 years</td><td>1300 mg/day</td><td>3–4 dairy serves + sardines with bones</td></tr>
  </tbody>
</table>

<h2>Omega-3 for brain development</h2>
<p>DHA omega-3 is a structural fat in the brain. Children who eat fish regularly score consistently higher on reading and attention tests in clinical trials.</p>
<ul>
  <li>Canned sardines mashed into pasta sauce or toast — kids often don't notice</li>
  <li>Canned tuna — 2–3 times per week is safe (limit larger fish due to mercury)</li>
  <li>Omega-3 enriched eggs — easiest option for fish-refusing kids</li>
</ul>

<h2>Practical tips for fussy eaters</h2>
<ul>
  <li><strong>Serve iron-rich foods first</strong> when children are hungriest</li>
  <li><strong>Involve kids in cooking</strong> — children are more likely to eat what they helped prepare</li>
  <li><strong>Repeated exposure works</strong> — a child may need to see a new food 10–15 times before accepting it; don't give up</li>
  <li><strong>Don't use dessert as a reward</strong> — it trains kids to undervalue main meals</li>
  <li><strong>Mash or blend</strong> sardines, lentils and spinach into bolognese, rissoles or pasta sauce</li>
</ul>

<h2>Budget meals kids actually eat</h2>
<table class="data-table">
  <thead><tr><th>Meal</th><th>Key nutrients delivered</th><th>Cost per serve</th></tr></thead>
  <tbody>
    <tr><td>Bolognese with hidden lentils</td><td>Iron, protein, folate, fibre</td><td>~$1.50</td></tr>
    <tr><td>Egg and veggie fried rice</td><td>Protein, choline, vitamins A and C</td><td>~$1.20</td></tr>
    <tr><td>Sardine & avocado toast</td><td>Omega-3, calcium, healthy fats</td><td>~$1.80</td></tr>
    <tr><td>Chicken & sweet potato tray bake</td><td>Protein, zinc, beta-carotene, vitamin C</td><td>~$2.50</td></tr>
    <tr><td>Lentil and vegetable soup</td><td>Plant protein, folate, iron, fibre</td><td>~$1.00</td></tr>
  </tbody>
</table>

<div class="highlight-box">
  <h3>🎯 The Stealth Nutrition trick</h3>
  <p>Blend cooked red lentils into any tomato-based sauce — they dissolve completely and add protein, iron and folate without changing the taste or texture significantly. A 400g can of lentils costs ~$1.20 and feeds 4 kids.</p>
</div>

<div class="cta-box">
  <h2>Plan meals for every child in your household</h2>
  <p>Add each child's age to the app — it automatically adjusts nutrient targets for toddlers, school-age kids and teens and shows which meals meet their specific needs.</p>
  <a class="cta-btn" href="/">Open the free app →</a>
</div>
"""

p = BASE / "kids"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "Kids & Toddler Nutrition on a Budget | OptimisedEats",
    "Iron for brain development, calcium for bones, omega-3 for focus — the cheapest foods to hit these targets for children in Australia and New Zealand.",
    "kids nutrition Australia, toddler iron, children calcium, cheap kids meals, fussy eater nutrition",
    "Kids & Toddlers", "/guide/kids/",
    kids_body,
    other_related("/guide/kids/")
), encoding="utf-8")
print("DONE guide/kids/index.html")

# ── BATCH COOKING ─────────────────────────────────────────────────────────────
batch_body = """
<h1>Batch Cooking: Cook Once, Eat All Week</h1>
<p class="lead">Batch cooking is the single most effective strategy for cutting your food bill without sacrificing nutrition. Spend 2–3 hours on a Sunday and eat well for half the week with zero extra effort.</p>

<h2>Why batch cooking saves money</h2>
<ul>
  <li><strong>Reduces food waste</strong> — pre-planned meals mean ingredients get used before they spoil</li>
  <li><strong>Eliminates impulse buys and takeaway</strong> — if dinner is already in the fridge, you won't spend $20 on UberEats</li>
  <li><strong>Bulk buying</strong> — buying 2 kg of lentils or a whole bag of oats is dramatically cheaper per kilogram</li>
  <li><strong>Energy efficiency</strong> — one big pot of soup uses barely more gas/electricity than a small one</li>
</ul>

<h2>The core batch-cook formula</h2>
<p>Build each session around these three components:</p>

<h3>1. A protein base (cook in bulk, use 3 ways)</h3>
<ul>
  <li>Whole roast chicken (~$6) → dinner night 1, sandwiches day 2, soup day 3</li>
  <li>2 kg beef or kangaroo mince (~$15) → bolognese, tacos, rissoles or burger patties</li>
  <li>1 kg dried lentils (~$3) → soup, salad, dahl, mince extender</li>
</ul>

<h3>2. A grain or starchy base</h3>
<ul>
  <li>Big pot of brown rice or pasta — serve as sides, in salads, or fried rice</li>
  <li>Baked sweet potatoes — eat as sides or mash into breakfast bowls</li>
  <li>Oat-based muffins or energy balls for snacks</li>
</ul>

<h3>3. Roasted or blanched vegetables</h3>
<ul>
  <li>Two trays of mixed vegetables (frozen is fine) — use in wraps, pasta, rice dishes</li>
  <li>A bag of frozen spinach cooked down — stir into anything for added iron and folate</li>
</ul>

<h2>Freezer-friendly meals</h2>
<p>These freeze perfectly and last 2–3 months:</p>
<table class="data-table">
  <thead><tr><th>Meal</th><th>Portions per batch</th><th>Cost per serve</th></tr></thead>
  <tbody>
    <tr><td>Red lentil soup</td><td>8–10 serves</td><td>~$0.80</td></tr>
    <tr><td>Beef/kangaroo bolognese</td><td>8 serves</td><td>~$1.50</td></tr>
    <tr><td>Chicken and vegetable casserole</td><td>6 serves</td><td>~$2.00</td></tr>
    <tr><td>Dahl (lentil curry)</td><td>8 serves</td><td>~$0.90</td></tr>
    <tr><td>Bean and beef chilli</td><td>8 serves</td><td>~$1.40</td></tr>
    <tr><td>Egg muffins (baked)</td><td>12 pieces</td><td>~$0.40 each</td></tr>
  </tbody>
</table>

<h2>A realistic 2-hour Sunday session</h2>
<ol>
  <li><strong>0:00</strong> — Put whole chicken in oven (200°C, 1.5 hrs)</li>
  <li><strong>0:10</strong> — Start large pot of lentil soup on the stove</li>
  <li><strong>0:20</strong> — Cook a big pot of rice or pasta</li>
  <li><strong>0:30</strong> — Roast two trays of mixed vegetables (frozen is fine)</li>
  <li><strong>1:00</strong> — Brown 1 kg mince; portion half for bolognese, half for tacos</li>
  <li><strong>1:30</strong> — Chicken comes out; shred and portion into 3 containers</li>
  <li><strong>2:00</strong> — Package everything into labelled containers; freeze what won't be eaten by Wednesday</li>
</ol>

<div class="highlight-box">
  <h3>📦 Container tip</h3>
  <p>Label containers with the date and contents. Use a permanent marker on masking tape. Freeze meals flat in zip-lock bags to save space — they thaw faster too. A set of glass containers lasts years and avoids plastic leaching into food.</p>
</div>

<h2>What doesn't freeze well</h2>
<ul>
  <li>Salads and raw vegetables — make fresh</li>
  <li>Cooked potato (goes watery) — sweet potato is fine though</li>
  <li>Dairy-based sauces (cream, béchamel) — can separate; add dairy fresh when reheating</li>
  <li>Boiled eggs — the whites go rubbery</li>
</ul>

<div class="cta-box">
  <h2>Plan your batch cook session</h2>
  <p>Our app generates a shopping list for a full week of meals for your family — optimised to minimise waste and maximise batch-cooking opportunities.</p>
  <a class="cta-btn" href="/">Build your weekly plan →</a>
</div>
"""

p = BASE / "batch-cooking"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "Batch Cooking Guide — Cook Once, Eat All Week | OptimisedEats",
    "How to batch cook nutritious meals for your family in 2 hours. Freezer-friendly recipes and strategies that cut your food bill in half.",
    "batch cooking Australia, meal prep budget, freezer meals family, cheap meal prep",
    "Batch Cooking", "/guide/batch-cooking/",
    batch_body,
    other_related("/guide/batch-cooking/")
), encoding="utf-8")
print("DONE guide/batch-cooking/index.html")

# ── SHOPPING ──────────────────────────────────────────────────────────────────
shopping_body = """
<h1>Smart Grocery Shopping on a Budget</h1>
<p class="lead">The average Australian household wastes $2,500 worth of food per year. A few simple shopping habits can slash your bill without eating worse — often while eating better.</p>

<h2>Unit pricing: the most important skill</h2>
<p>The shelf price is nearly irrelevant. The <strong>unit price</strong> (price per 100g or per kg) is what you compare. Most Australian supermarkets are legally required to show it.</p>
<ul>
  <li>A 400g tin of chickpeas at $1.20 = $3/kg</li>
  <li>A 1 kg bag of dried chickpeas at $3.50 = $3.50/kg (sounds more expensive — but dried yield 2.5× volume when cooked, so effective cost is ~$1.40/kg)</li>
  <li>The "family size" pack is almost always cheaper per unit than the "regular" size</li>
</ul>

<h2>Frozen vs fresh vegetables</h2>
<p>Frozen vegetables are often <strong>more nutritious</strong> than fresh equivalents. They're picked at peak ripeness and flash-frozen within hours. Fresh produce can spend days in transit and display, losing water-soluble vitamins.</p>
<table class="data-table">
  <thead><tr><th>Situation</th><th>Choose</th></tr></thead>
  <tbody>
    <tr><td>Vegetables you'll cook (soups, stir-fries, curries)</td><td>Frozen — cheaper, consistent, no waste</td></tr>
    <tr><td>Salads and raw eating</td><td>Fresh — texture matters</td></tr>
    <tr><td>Produce in season locally</td><td>Fresh — cheaper and often tastier</td></tr>
    <tr><td>Produce out of season</td><td>Frozen — dramatically cheaper, better quality</td></tr>
    <tr><td>Herbs you use occasionally</td><td>Frozen (in ice cubes) or dried — fresh wilts fast</td></tr>
  </tbody>
</table>

<h2>When specials are actually worth it</h2>
<p>Buy extra and freeze when these are on special:</p>
<ul>
  <li>Meat (mince, chicken thighs, whole chickens) — freezes perfectly for months</li>
  <li>Canned goods (sardines, tuna, beans, tomatoes) — 2-year shelf life, stock up when 50% off</li>
  <li>Cheese — hard cheeses like cheddar freeze well (may crumble when thawed, but fine for cooking)</li>
</ul>
<p>Don't buy on special: fresh vegetables (unless you'll use them in 2 days), bread (goes stale), or products you've never tried and might not like.</p>

<h2>Coles vs Woolworths vs Aldi vs markets</h2>
<ul>
  <li><strong>Aldi</strong>: consistently cheapest for pantry staples — oats, pasta, canned goods, eggs, dairy. Often 20–40% cheaper than Coles/Woolworths for equivalent products.</li>
  <li><strong>Coles/Woolworths</strong>: competitive on marked-down meat (check the yellow sticker section near closing time), specials on branded goods</li>
  <li><strong>Farmers markets</strong>: can be good value for seasonal produce — but compare prices; some markets charge premium prices</li>
  <li><strong>Asian grocers</strong>: often the cheapest for fresh ginger, garlic, tofu, fish sauce, rice, noodles</li>
</ul>

<h2>A weekly shop structure that works</h2>
<ol>
  <li>Check what's already in the fridge/freezer/pantry first</li>
  <li>Plan 4–5 dinners (the others are leftovers or batch-cook meals)</li>
  <li>Write a list before you go — stick to it</li>
  <li>Never shop hungry</li>
  <li>Shop the perimeter first (produce, meat, dairy), then fill in pantry items</li>
  <li>Check the yellow sticker / reduced section when you arrive</li>
</ol>

<div class="highlight-box">
  <h3>🥚 Eggs: the ultimate budget hack</h3>
  <p>A 12-pack of eggs at $6 works out to 50c per egg — each one delivering 6g protein, choline, vitamins A, D, B12 and selenium. Two eggs cost $1 and are more satiating and nutritious than most packaged snacks. Buy the 12-pack or larger; the per-egg price drops significantly.</p>
</div>

<h2>Foods never worth buying on a budget</h2>
<ul>
  <li>Pre-cut and pre-washed vegetables — you pay a 50–100% premium for 5 minutes of prep work</li>
  <li>Single-serve yoghurt or snack packs — buy the 1 kg tub and portion yourself</li>
  <li>Flavoured oats (sachets) — buy plain oats and add your own banana and honey for a fraction of the cost</li>
  <li>Bottled salad dressing — olive oil + lemon juice + mustard costs cents and is healthier</li>
  <li>Protein bars — two boiled eggs deliver more protein and nutrition for less money</li>
</ul>

<div class="cta-box">
  <h2>Get a personalised shopping list</h2>
  <p>Our free app builds a complete shopping list for your household's weekly meal plan — sorted by category, with estimated costs at current supermarket prices.</p>
  <a class="cta-btn" href="/">Generate your shopping list →</a>
</div>
"""

p = BASE / "shopping"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "Smart Budget Grocery Shopping Guide | OptimisedEats",
    "How to cut your grocery bill without eating worse. Unit pricing, frozen vs fresh, Aldi vs Woolworths, and what's never worth buying.",
    "budget grocery shopping Australia, cheap supermarket tips, unit pricing food, Aldi vs Woolworths nutrition",
    "Smart Shopping", "/guide/shopping/",
    shopping_body,
    other_related("/guide/shopping/")
), encoding="utf-8")
print("DONE guide/shopping/index.html")

# ── CUISINES ──────────────────────────────────────────────────────────────────
cuisines_body = """
<h1>World Cuisines That Are Cheap and Nutritious</h1>
<p class="lead">Many of the world's most nutritious cuisines evolved from poverty — using legumes, whole grains, and small amounts of meat to feed families on very little. These traditions map perfectly onto a budget-conscious approach to healthy eating.</p>

<h2>Mediterranean diet: the gold standard of nutrition</h2>
<p>The Mediterranean diet consistently ranks as the most evidence-backed dietary pattern for long-term health. The core is cheap: legumes, olive oil, wholegrains, vegetables, fish and moderate dairy.</p>
<h3>Key meals to adopt:</h3>
<ul>
  <li><strong>Greek lentil soup (Fakes)</strong> — lentils, tinned tomatoes, olive oil, oregano: ~$1 per serve</li>
  <li><strong>Chickpea and spinach stew</strong> — canned chickpeas, frozen spinach, garlic, cumin: ~$1.20 per serve</li>
  <li><strong>Sardine pasta</strong> — canned sardines, olive oil, garlic, lemon, pasta: ~$1.80 per serve</li>
  <li><strong>Greek yoghurt with oats and honey</strong> — calcium, protein, probiotics: ~$1.00 per serve</li>
</ul>
<p>Olive oil is the most important ingredient. It's not cheap per bottle (~$8–12), but you use small amounts — a $10 bottle lasts a month of daily cooking and delivers heart-protective monounsaturated fats.</p>

<h2>South Asian and Indian cuisine</h2>
<p>Indian cooking is built around legumes (dahl), spices, and small amounts of meat — making it one of the most naturally budget-friendly nutritious cuisines globally.</p>
<ul>
  <li><strong>Red lentil dahl</strong> — red lentils, canned tomatoes, onion, garlic, cumin, turmeric, garam masala: ~$0.90 per serve, serves 6</li>
  <li><strong>Chana masala (chickpea curry)</strong> — canned chickpeas, tomatoes, spices: ~$1.00 per serve</li>
  <li><strong>Egg curry</strong> — hard boiled eggs in spiced tomato sauce: ~$1.20 per serve</li>
  <li><strong>Saag (spinach) with paneer or tofu</strong> — frozen spinach, garlic, ginger, spices: ~$1.50 per serve</li>
</ul>
<p>Invest in a basic spice collection (cumin, turmeric, garam masala, coriander) — roughly $15–20 upfront from an Asian grocer, but they last 12+ months and transform cheap legumes into deeply flavourful meals.</p>

<h2>East Asian cuisine</h2>
<p>Japanese, Chinese, Korean and Vietnamese cuisines all excel at extracting maximum flavour and nutrition from minimal ingredients.</p>
<ul>
  <li><strong>Japanese miso soup</strong> — miso paste, tofu, dried seaweed (wakame), spring onions: exceptional iodine and probiotics for ~$0.50 per serve</li>
  <li><strong>Egg fried rice</strong> — day-old rice, 2–3 eggs, frozen peas and corn, soy sauce: ~$1.00 per serve</li>
  <li><strong>Korean-inspired bibimbap bowl</strong> — rice, fried egg, sautéed spinach, carrot, sesame oil: ~$1.80 per serve</li>
  <li><strong>Vietnamese pho-style noodle soup</strong> — rice noodles, beef or chicken bones, star anise, cinnamon, ginger, fish sauce: ~$1.50 per serve (bones are cheap)</li>
</ul>

<h2>Middle Eastern cuisine</h2>
<p>Hummus, falafel, tabbouleh and shakshuka are all cheap, nutritious, and easy to make at home for a fraction of the café price.</p>
<ul>
  <li><strong>Shakshuka</strong> — eggs poached in spiced tomato sauce: ~$1.20 per serve</li>
  <li><strong>Homemade hummus</strong> — canned chickpeas, tahini, garlic, lemon, olive oil: ~$0.50 per serve (vs $5+ for store-bought)</li>
  <li><strong>Lentil and bulgur pilaf (Mujaddara)</strong> — one of the most nutritious cheap grain-legume combinations: ~$0.90 per serve</li>
  <li><strong>Baked falafel</strong> — canned chickpeas, herbs, spices: ~$1.20 for 12 pieces</li>
</ul>

<div class="highlight-box">
  <h3>🌶️ Spices are the best investment</h3>
  <p>Buying spices from an Asian or Indian grocer costs 50–80% less than supermarket branded spices. A $2 bag of cumin seeds from an Asian grocer is equivalent to 3–4 supermarket jars at $3–4 each. Whole spices also last longer and taste better when freshly ground.</p>
</div>

<div class="cta-box">
  <h2>Find budget meals that match your taste</h2>
  <p>Our app includes recipes inspired by Mediterranean, Asian and Middle Eastern cuisines — filtered by cuisine type, cost, and nutritional needs.</p>
  <a class="cta-btn" href="/">Explore recipes →</a>
</div>
"""

p = BASE / "cuisines"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "Budget World Cuisines: Cheap & Nutritious Meal Ideas | OptimisedEats",
    "Mediterranean, Indian, Asian and Middle Eastern meals that are naturally cheap and nutritious. Recipes under $2 per serve inspired by global food traditions.",
    "cheap world cuisine Australia, budget Mediterranean diet, Indian dahl recipe cheap, Asian budget meals",
    "World Cuisines", "/guide/cuisines/",
    cuisines_body,
    other_related("/guide/cuisines/")
), encoding="utf-8")
print("DONE guide/cuisines/index.html")

# ── RECIPES ───────────────────────────────────────────────────────────────────
recipes_body = """
<h1>Budget Recipe Ideas</h1>
<p class="lead">These are the meals that deliver the most nutrition per dollar. Each one is built around cheap powerhouse ingredients — sardines, eggs, lentils, oats, frozen vegetables — and takes under 30 minutes.</p>

<h2>🐟 Sardine recipes</h2>
<p>Sardines are one of the best-value foods in Australia: roughly $1.50 per can, they deliver omega-3, vitamin D, calcium, and B12. Here's how to make them delicious.</p>

<h3>Sardine pasta with lemon and capers</h3>
<ul>
  <li>Cook 100g pasta. Drain.</li>
  <li>In the same pan: 1 can sardines (drained, roughly broken up), 2 garlic cloves, zest and juice of half a lemon, 1 tbsp capers, chilli flakes.</li>
  <li>Toss with pasta, top with parsley.</li>
  <li><strong>Cost: ~$2.50 | Time: 15 min | Serves: 2</strong></li>
</ul>

<h3>Sardine toast with avocado</h3>
<ul>
  <li>Toast 2 slices sourdough. Spread half an avocado.</li>
  <li>Top with 1 can sardines, sliced cherry tomatoes, lemon juice, salt and pepper.</li>
  <li><strong>Cost: ~$2.50 | Time: 5 min | Serves: 1</strong></li>
</ul>

<h2>🥚 Egg recipes</h2>
<p>Eggs are the ultimate cheap protein. At ~50c each, two eggs give you 12g protein, choline, vitamin A, D, B12 and selenium.</p>

<h3>Shakshuka (baked eggs in tomato sauce)</h3>
<ul>
  <li>Fry 1 onion + 1 capsicum in oil. Add 2 garlic cloves, 1 tsp cumin, ½ tsp paprika. Cook 2 min.</li>
  <li>Add 1 can crushed tomatoes. Simmer 5 min. Make 4 wells; crack an egg into each.</li>
  <li>Cover and cook 8 min until whites are set. Serve with bread.</li>
  <li><strong>Cost: ~$3 | Time: 20 min | Serves: 2</strong></li>
</ul>

<h3>Egg fried rice</h3>
<ul>
  <li>Day-old rice works best. Heat oil in wok. Add 3 eggs — scramble quickly.</li>
  <li>Add 2 cups cold rice, 1 cup frozen peas/corn. Stir-fry 3 min.</li>
  <li>Add soy sauce, sesame oil, spring onions. Done.</li>
  <li><strong>Cost: ~$1.20 | Time: 10 min | Serves: 2</strong></li>
</ul>

<h2>🫘 Lentil recipes</h2>
<p>Red lentils dissolve into soups and sauces. Cooked lentils freeze perfectly. A 1 kg bag (~$3) cooks up to 8–10 serves.</p>

<h3>Red lentil soup</h3>
<ul>
  <li>Fry 1 onion + 3 garlic cloves in oil. Add 1 tsp cumin, 1 tsp turmeric, ½ tsp coriander.</li>
  <li>Add 1 cup red lentils (rinsed), 1 can crushed tomatoes, 800ml stock.</li>
  <li>Simmer 20 min until lentils dissolve. Squeeze in lemon juice. Serve with bread.</li>
  <li><strong>Cost: ~$0.80 per serve | Time: 25 min | Serves: 6</strong></li>
</ul>

<h3>Lentil bolognese</h3>
<ul>
  <li>Replace half the mince in any bolognese with cooked red lentils.</li>
  <li>They absorb the tomato flavours and are indistinguishable from mince in texture once cooked.</li>
  <li>Cuts the cost per serve by ~40% while adding fibre and folate.</li>
  <li><strong>Cost: ~$1.50 per serve | Time: 30 min | Serves: 6</strong></li>
</ul>

<h2>🌾 Oat recipes</h2>
<p>Rolled oats (~$2/kg) are one of the cheapest sources of fibre, B vitamins and slow-release energy. Far cheaper than packaged cereals.</p>

<h3>Overnight oats</h3>
<ul>
  <li>Mix ½ cup oats + ½ cup milk + 1 tbsp chia seeds in a jar. Refrigerate overnight.</li>
  <li>Top with banana, a spoon of peanut butter, or frozen berries.</li>
  <li><strong>Cost: ~$0.80 | Time: 2 min prep | Serves: 1</strong></li>
</ul>

<h3>Savoury oat porridge</h3>
<ul>
  <li>Cook oats in stock (not water). Stir in a fried egg on top, spinach, soy sauce.</li>
  <li>Better protein balance and more filling than sweet oats.</li>
  <li><strong>Cost: ~$1.00 | Time: 10 min | Serves: 1</strong></li>
</ul>

<h2>🦘 Kangaroo recipes</h2>
<p>Kangaroo is the leanest red meat in Australia with exceptional iron and zinc. Available as mince (~$8–10/kg) at most supermarkets.</p>

<h3>Kangaroo bolognese</h3>
<ul>
  <li>Fry 500g kangaroo mince until browned. Add 1 onion, 2 garlic cloves, 1 carrot, 1 can crushed tomatoes, 1 tbsp tomato paste.</li>
  <li>Simmer 20 min. Serve on pasta. Add grated parmesan.</li>
  <li><strong>Cost: ~$2.80 per serve | Time: 25 min | Serves: 4</strong></li>
  <li>Iron: ~5.5 mg per serve — over 30% of adult daily target</li>
</ul>

<div class="highlight-box">
  <h3>❄️ Freezer staples to always have on hand</h3>
  <p>With these in your freezer and pantry, you can make a nutritious meal in under 20 minutes any night: frozen mixed vegetables, frozen spinach, frozen chicken thighs or mince (defrost in fridge overnight), canned sardines and tomatoes, eggs, red lentils, rolled oats, garlic, onion, rice or pasta.</p>
</div>

<div class="cta-box">
  <h2>Find recipes matched to your nutritional gaps</h2>
  <p>The app tracks which nutrients you're low on each day and highlights recipes that fill those gaps — filtered by cost, prep time, and the dietary preferences of your household.</p>
  <a class="cta-btn" href="/">Try the recipe planner →</a>
</div>
"""

p = BASE / "recipes"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "Budget Nutrition Recipes — Sardines, Eggs, Lentils & More | OptimisedEats",
    "Quick cheap recipes built around the most nutritious affordable foods: sardines, eggs, lentils, oats and kangaroo. Under $2.50 per serve.",
    "cheap healthy recipes Australia, budget sardine recipe, lentil soup recipe, egg recipe cheap, kangaroo recipe",
    "Budget Recipes", "/guide/recipes/",
    recipes_body,
    other_related("/guide/recipes/")
), encoding="utf-8")
print("DONE guide/recipes/index.html")

print("\nAll guide pages generated successfully!")
