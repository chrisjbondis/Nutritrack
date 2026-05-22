"""Generate Life Stages, Vegan Nutrition, and Exercise pages."""
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
.callout-purple{background:#faf5ff;border-left:4px solid #7c3aed;padding:14px 18px;border-radius:0 8px 8px 0;margin:16px 0}
.life-stage{margin:0 0 32px;border-radius:14px;overflow:hidden;border:1px solid #e2e8f0}
.life-stage-header{padding:16px 20px;display:flex;align-items:center;gap:14px}
.life-stage-icon{font-size:28px;flex-shrink:0}
.life-stage-title{font-size:18px;font-weight:800;color:#fff;margin:0}
.life-stage-sub{font-size:13px;color:rgba(255,255,255,0.85);margin:2px 0 0}
.life-stage-body{padding:18px 20px;background:#fff}
.gap-row{display:flex;gap:12px;align-items:flex-start;padding:10px 0;border-bottom:1px solid #f1f5f9}
.gap-row:last-child{border-bottom:none}
.gap-icon{font-size:18px;flex-shrink:0;margin-top:2px}
.gap-stat{display:inline-block;background:#fef2f2;color:#dc2626;font-weight:800;font-size:12px;padding:1px 9px;border-radius:20px;margin-left:6px}
.myth-box{background:#fef2f2;border:2px solid #fca5a5;border-radius:12px;padding:18px 20px;margin:20px 0}
.myth-label{font-size:11px;font-weight:900;color:#dc2626;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px}
.myth-text{font-size:15px;font-weight:700;color:#7f1d1d;margin:0 0 10px}
.reality-label{font-size:11px;font-weight:900;color:#16a34a;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px}
.reality-text{font-size:14px;color:#14532d;margin:0}
.protein-bar{background:linear-gradient(90deg,#16a34a,#15803d);border-radius:8px;padding:16px 20px;color:#fff;margin:16px 0}
.protein-bar h3{color:#fff;margin:0 0 8px;font-size:16px;border:none}
.protein-bar p{margin:4px 0;font-size:13px;color:rgba(255,255,255,0.9)}
.data-table{width:100%;border-collapse:collapse;font-size:13px;margin:12px 0}
.data-table th{background:#f1f5f9;color:#374151;padding:8px 10px;text-align:left;font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.3px}
.data-table td{padding:8px 10px;border-bottom:1px solid #f1f5f9;vertical-align:top}
.data-table th:not(:first-child),.data-table td:not(:first-child){text-align:center}
.vegan-card{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:18px;margin:0 0 14px}
.vegan-card h3{margin:0 0 8px;font-size:16px;border:none;padding:0}
.must-badge{display:inline-block;background:#dc2626;color:#fff;font-size:10px;font-weight:900;padding:2px 8px;border-radius:20px;margin-left:8px;letter-spacing:.5px;vertical-align:middle}
.important-badge{display:inline-block;background:#f59e0b;color:#fff;font-size:10px;font-weight:900;padding:2px 8px;border-radius:20px;margin-left:8px;letter-spacing:.5px;vertical-align:middle}
.ex-table{width:100%;border-collapse:collapse;font-size:12px;margin:14px 0}
.ex-table th{background:#1e3a5f;color:#fff;padding:9px 10px;text-align:left;font-size:11px;font-weight:700}
.ex-table td{padding:8px 10px;border-bottom:1px solid #f1f5f9;vertical-align:top;font-size:12px}
.ex-table tr:nth-child(even) td{background:#f8fafc}
.habit-item{display:flex;gap:14px;align-items:flex-start;padding:12px 0;border-bottom:1px solid #f1f5f9}
.habit-item:last-child{border-bottom:none}
.habit-num{font-size:20px;flex-shrink:0;min-width:30px}
.habit-body{flex:1}
.habit-title{font-weight:700;color:#0f172a;font-size:14px;margin-bottom:3px}
.habit-detail{font-size:13px;color:#475569;line-height:1.5}
.app-link-box{background:linear-gradient(135deg,#f0fdf4,#dcfce7);border:1px solid #86efac;border-radius:12px;padding:16px 20px;margin:24px 0;display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}
.app-link-box p{margin:0;font-size:14px;color:#166534}
.app-link-btn{background:#16a34a;color:#fff;padding:8px 18px;border-radius:8px;font-weight:700;font-size:13px;white-space:nowrap;text-decoration:none}
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
    ("Which Foods Fill Gaps",   "/guide/foods-for-gaps/"),
    ("Macronutrients",          "/guide/macronutrients/"),
    ("5 Daily Habits",          "/guide/daily-habits/"),
    ("Absorption Tips",         "/guide/absorption/"),
    ("Sleep &amp; Nutrition",   "/guide/sleep-nutrition/"),
    ("Weston A. Price",         "/guide/weston-price/"),
    ("Nutrient Gaps by Life Stage", "/guide/life-stages/"),
    ("Vegan &amp; Plant-Based", "/guide/vegan-nutrition/"),
    ("Exercise &amp; Nutrition","/guide/exercise-nutrition/"),
    ("Disclaimer",              "/guide/disclaimer/"),
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

def app_link(text="Track your household in the free app"):
    return f"""<div class="app-link-box">
  <p>&#128247; <strong>{text}</strong> &mdash; enter each person&rsquo;s age and sex to see their exact targets and how your meals measure up.</p>
  <a class="app-link-btn" href="/">Open free app</a>
</div>"""


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1: NUTRIENT GAPS BY LIFE STAGE
# ═══════════════════════════════════════════════════════════════════════════════

life_body = f"""<h1>Nutrient Gaps by Life Stage</h1>
<p class="lead">The nutrients most commonly missed change significantly at each life stage. This guide covers the most clinically important gaps for every age group &mdash; and the cheapest foods to close them.</p>

<div class="callout-blue">
  <strong>How this differs from the NRV tables:</strong> The <a href="/guide/nrv/">NRV reference tables</a> show what the targets are. This page explains <em>why</em> each life stage misses specific nutrients, what the consequences are, and what to prioritise on a budget.
</div>

<!-- CHILDREN -->
<div class="life-stage">
  <div class="life-stage-header" style="background:linear-gradient(135deg,#f59e0b,#d97706)">
    <div class="life-stage-icon">&#129378;</div>
    <div>
      <div class="life-stage-title">Children &mdash; Ages 4 to 13</div>
      <div class="life-stage-sub">Foundation years for bone density, brain development, and immune function</div>
    </div>
  </div>
  <div class="life-stage-body">
    <div class="gap-row">
      <div class="gap-icon">&#129370;</div>
      <div><strong>Calcium <span class="gap-stat">most common gap</span></strong><br>
      <span style="font-size:13px;color:#475569">Peak bone mass is set before age 25 &mdash; shortfalls in childhood permanently reduce the ceiling. Children 4&ndash;8 need 700mg/day; ages 9&ndash;13 need 1,000mg. Budget fix: 250mL milk + 200g yoghurt covers ~550mg. Add 30g cheese to a meal and you&rsquo;re at 750mg.</span></div>
    </div>
    <div class="gap-row">
      <div class="gap-icon">&#9728;&#65039;</div>
      <div><strong>Vitamin D</strong><br>
      <span style="font-size:13px;color:#475569">Essential for calcium absorption and immune development. Children in childcare and school spend increasing time indoors. 15&ndash;20 min midday sun on arms and legs in reasonable UV conditions covers requirements for most children. In winter in southern states, a 400&ndash;600 IU supplement is reasonable.</span></div>
    </div>
    <div class="gap-row">
      <div class="gap-icon">&#129354;</div>
      <div><strong>Iron &mdash; for brain development</strong><br>
      <span style="font-size:13px;color:#475569">Iron deficiency in children causes measurable cognitive deficits and behavioural problems &mdash; even before anaemia develops. Children 4&ndash;8 need 10mg/day; ages 9&ndash;13 need 8mg. Practical: minced beef hidden in bolognese, lentil-based meals 3&times;/week, always with a tomato-based sauce (Vitamin C triples absorption).</span></div>
    </div>
    <div class="gap-row">
      <div class="gap-icon">&#127807;</div>
      <div><strong>Fibre and potassium</strong><br>
      <span style="font-size:13px;color:#475569">Children who eat ultra-processed foods consistently undershoot fibre (14&ndash;24g/day target) and potassium. Both drive gut microbiome diversity and cardiovascular health foundations. Oats, lentils, bananas, and sweet potato are the cheapest fixes. See the <a href="/guide/hidden-hunger/">Hidden Hunger guide</a> for the UPF connection.</span></div>
    </div>
    <div class="callout" style="margin-top:12px">
      <strong>Budget priority:</strong> Full-fat dairy (yoghurt, milk, cheese) + a weekly liver meal hidden in mince + lentils 3&times;/week covers the major gaps for under $2/day extra.
    </div>
  </div>
</div>

<!-- ADOLESCENTS -->
<div class="life-stage">
  <div class="life-stage-header" style="background:linear-gradient(135deg,#8b5cf6,#7c3aed)">
    <div class="life-stage-icon">&#129489;</div>
    <div>
      <div class="life-stage-title">Adolescents &mdash; Ages 14 to 18</div>
      <div class="life-stage-sub">Highest nutrient requirements of any life stage relative to body size</div>
    </div>
  </div>
  <div class="life-stage-body">
    <div class="gap-row">
      <div class="gap-icon">&#129370;</div>
      <div><strong>Calcium <span class="gap-stat">critical window</span></strong><br>
      <span style="font-size:13px;color:#475569">Requirements are highest of any life stage: 1,300mg/day for both boys and girls. Over 90% of teenage girls fall short. This is the most important calcium window &mdash; the skeleton is actively laying down density that will determine lifelong fracture risk. Three dairy serves a day (milk, yoghurt, cheese) is the target.</span></div>
    </div>
    <div class="gap-row">
      <div class="gap-icon">&#129354;</div>
      <div><strong>Iron &mdash; especially girls after menarche <span class="gap-stat">47% fall short</span></strong><br>
      <span style="font-size:13px;color:#475569">Girls&rsquo; iron requirement jumps to 15mg/day after their first period. This is the single most common nutrient deficiency in Australian teenage girls. Symptoms (fatigue, poor concentration, irritability) are frequently attributed to stress or poor sleep rather than iron. Weekly red meat or liver + lentils 3&times;/week + always pairing with Vitamin C is the strategy. Teenage boys need 11mg/day &mdash; more manageable but worth monitoring.</span></div>
    </div>
    <div class="gap-row">
      <div class="gap-icon">&#129428;</div>
      <div><strong>Zinc &mdash; boys especially</strong><br>
      <span style="font-size:13px;color:#475569">Boys 14&ndash;18 need 13mg/day &mdash; the highest zinc requirement of any demographic. Zinc drives testosterone production, growth, and immune function during the most rapid growth period. Typical teenage diets (processed foods, low red meat) commonly fall short. Eggs, pumpkin seeds, and lean red meat are the budget fix.</span></div>
    </div>
    <div class="gap-row">
      <div class="gap-icon">&#129302;</div>
      <div><strong>Magnesium, Vitamin D, potassium</strong><br>
      <span style="font-size:13px;color:#475569">All three are commonly low in teenagers who eat high-UPF diets. Magnesium (360&ndash;410mg/day) affects sleep quality, anxiety, and muscle function &mdash; all issues that affect many teenagers. 30g pumpkin seeds on morning oats covers ~150mg magnesium.</span></div>
    </div>
  </div>
</div>

<!-- ADULT WOMEN -->
<div class="life-stage">
  <div class="life-stage-header" style="background:linear-gradient(135deg,#ec4899,#db2777)">
    <div class="life-stage-icon">&#128105;</div>
    <div>
      <div class="life-stage-title">Adult Women &mdash; Ages 19 to 50</div>
      <div class="life-stage-sub">Highest iron requirement of any non-pregnant group</div>
    </div>
  </div>
  <div class="life-stage-body">
    <div class="gap-row">
      <div class="gap-icon">&#129354;</div>
      <div><strong>Iron &mdash; 18mg/day <span class="gap-stat">47% of women 18&ndash;29 fall short</span></strong><br>
      <span style="font-size:13px;color:#475569">The highest iron RDA of any non-pregnant group. Monthly blood loss combined with low dietary iron intake makes deficiency extremely common. Symptoms progress from subtle (fatigue, cold hands) to significant (breathlessness, heart palpitations) before most women seek help. Weekly red meat + lentils + always with Vitamin C + avoid tea/coffee within 1 hour of iron-rich meals. See <a href="/guide/deficiency-symptoms/">Deficiency Symptoms</a> for the full three-stage progression.</span></div>
    </div>
    <div class="gap-row">
      <div class="gap-icon">&#127811;</div>
      <div><strong>Folate &mdash; especially pre-conception</strong><br>
      <span style="font-size:13px;color:#475569">400&micro;g/day RDI for non-pregnant women; increases to 600&micro;g during pregnancy. Neural tube closure happens in the first 28 days of pregnancy &mdash; often before a woman knows she&rsquo;s pregnant. Folate should be optimised before conception. Liver, lentils, spinach, and canned beans are the budget sources. See <a href="/guide/pre-conception/">Pre-Conception guide</a>.</span></div>
    </div>
    <div class="gap-row">
      <div class="gap-icon">&#129370;</div>
      <div><strong>Calcium and Vitamin D</strong><br>
      <span style="font-size:13px;color:#475569">1,000mg/day calcium through to age 50, then jumping to 1,300mg after menopause. Building and maintaining bone density in the 30s and 40s is the most effective prevention for post-menopausal osteoporosis.</span></div>
    </div>
  </div>
</div>

<!-- ADULT MEN -->
<div class="life-stage">
  <div class="life-stage-header" style="background:linear-gradient(135deg,#3b82f6,#2563eb)">
    <div class="life-stage-icon">&#128104;</div>
    <div>
      <div class="life-stage-title">Adult Men &mdash; Ages 19 to 50</div>
      <div class="life-stage-sub">Tend to over-consume sodium and protein while missing potassium, magnesium, fibre and zinc</div>
    </div>
  </div>
  <div class="life-stage-body">
    <div class="gap-row">
      <div class="gap-icon">&#129428;</div>
      <div><strong>Zinc <span class="gap-stat">48% of men fall short</span></strong><br>
      <span style="font-size:13px;color:#475569">Men need 14mg/day &mdash; nearly double the female RDI. Zinc drives testosterone production, immune function, wound healing, and taste and smell. The typical Australian male diet (high processed food, moderate-to-low red meat) commonly misses this. Zinc from plant sources is 25&ndash;50% less bioavailable than from red meat. Eggs, pumpkin seeds, and a weekly liver or beef meal cover the gap affordably.</span></div>
    </div>
    <div class="gap-row">
      <div class="gap-icon">&#127807;</div>
      <div><strong>Potassium, magnesium and fibre</strong><br>
      <span style="font-size:13px;color:#475569">Men over-consume sodium (averaging 3,200mg vs the 2,300mg maximum) while consistently under-consuming potassium (target 3,800mg), which blunts the cardiovascular impact. Magnesium (420mg/day for adult men) is deficient in 31% of Australian adults. Lentils, bananas, potatoes, oats, and spinach address all three affordably.</span></div>
    </div>
    <div class="gap-row">
      <div class="gap-icon">&#127803;</div>
      <div><strong>Vitamin E and selenium</strong><br>
      <span style="font-size:13px;color:#475569">Both are antioxidant nutrients commonly low in men eating low-variety diets. Vitamin E is found in nuts, seeds, and olive oil. A single Brazil nut provides a full day&rsquo;s selenium (60&micro;g target). One nut a day, every day, is the entire selenium strategy.</span></div>
    </div>
  </div>
</div>

<!-- OLDER ADULTS -->
<div class="life-stage">
  <div class="life-stage-header" style="background:linear-gradient(135deg,#0f766e,#0d9488)">
    <div class="life-stage-icon">&#129491;</div>
    <div>
      <div class="life-stage-title">Older Adults &mdash; Ages 65 and over</div>
      <div class="life-stage-sub">The most nutritionally complex life stage &mdash; and the most under-supported</div>
    </div>
  </div>
  <div class="life-stage-body">

    <div class="myth-box">
      <div class="myth-label">&#10060; Common myth</div>
      <div class="myth-text">&ldquo;I&rsquo;m less active now, so I need less food.&rdquo;</div>
      <div class="reality-label">&#9989; The reality</div>
      <div class="reality-text">Older adults need <strong>more protein per kilogram</strong>, not less &mdash; despite lower activity levels. The muscle-building machinery becomes less responsive with age (anabolic resistance), so a higher stimulus is required to achieve the same result. Eating less compounds the problem dramatically, accelerating muscle loss, falls risk, and loss of independence.</div>
    </div>

    <h3 style="margin-top:20px">Anabolic resistance &mdash; why less protein means disaster</h3>
    <p style="font-size:14px;color:#374151">After approximately age 65, the muscle protein synthesis response to protein becomes significantly blunted. In young adults, approximately 20g of high-quality protein per meal maximally stimulates muscle building. In older adults, that threshold rises to <strong>35&ndash;40g per meal</strong> &mdash; nearly double. Below this threshold, muscle breakdown continues to outpace rebuilding regardless of overall protein intake.</p>

    <div class="protein-bar">
      <h3>Evidence-based protein targets for older adults</h3>
      <p><strong>Healthy older adults (65+):</strong> 1.2&ndash;1.6 g/kg/day &mdash; vs the standard RDI of 0.84 g/kg which is set to prevent deficiency, not preserve muscle</p>
      <p><strong>Active older adults doing resistance exercise:</strong> 1.6&ndash;2.0 g/kg/day</p>
      <p><strong>Recovering from illness, surgery, or sarcopenia:</strong> 2.0&ndash;2.5 g/kg/day</p>
      <p style="margin-top:8px;font-size:12px;color:rgba(255,255,255,0.75)">Example: A 70kg woman at age 70 should target 84&ndash;112g protein/day minimum &mdash; compared to the RDI of ~59g. Most older Australians consume far less than this.</p>
    </div>

    <div class="callout-purple">
      <strong>The leucine connection:</strong> Leucine is the amino acid that directly triggers muscle protein synthesis via the mTOR pathway. The leucine threshold per meal rises from ~3g in young adults to 3.5&ndash;4g in older adults. This means the <em>quality</em> of protein matters as much as quantity. <strong>High-leucine budget sources:</strong> Greek yoghurt (2g leucine per 200g serve), eggs (1.1g per egg), canned tuna/salmon (~2g per 100g), chicken breast, beef mince. Three serves of Greek yoghurt a day is a practical, affordable high-leucine strategy.
    </div>

    <div class="myth-box" style="margin-top:20px">
      <div class="myth-label">&#10060; The breakfast trap</div>
      <div class="myth-text">&ldquo;I&rsquo;m not that hungry in the morning, so I just have toast and a coffee.&rdquo;</div>
      <div class="reality-label">&#9989; What this means physiologically</div>
      <div class="reality-text">After an overnight fast, the body is in a catabolic state &mdash; breaking down muscle protein to fuel the brain. The cortisol awakening response (peaking ~30&ndash;45 min after waking) amplifies this. Toast and coffee does not provide enough protein to cross the leucine threshold. In an older adult with anabolic resistance, this means 14&ndash;16 hours of net muscle breakdown every single day &mdash; compounded over years, this is sarcopenia in slow motion. Fix: 3 eggs + 200g Greek yoghurt = ~38g protein, ~$1.60. See the <a href="/guide/exercise-nutrition/">Exercise &amp; Nutrition guide</a> for the full catabolic cycle explainer.</div>
    </div>

    <h3 style="margin-top:20px">The taste and smell problem &mdash; why older adults eat less without realising it</h3>
    <p style="font-size:14px;color:#374151">Taste bud sensitivity declines significantly with age &mdash; typically beginning in the 60s and accelerating through the 70s and 80s. Smell (which accounts for ~80% of what we perceive as taste) declines similarly. The result: food becomes less appealing, appetite decreases, and portion sizes shrink &mdash; often without the person recognising what&rsquo;s happening.</p>
    <div class="callout-amber">
      <strong>Practical strategies to maintain appetite:</strong>
      <ul style="margin:8px 0 0;padding-left:20px;font-size:13px">
        <li>Use stronger flavours: garlic, lemon, vinegar, fresh herbs, spices &mdash; all cheap and all stimulate appetite</li>
        <li>Eat with others when possible &mdash; social eating consistently increases intake by 20&ndash;30%</li>
        <li>Prioritise nutrient density over volume &mdash; Greek yoghurt, eggs, sardines, and cheese deliver more per bite than low-density options</li>
        <li>Smoothies and soups: liquid meals maintain nutrition when solid food appetite falls</li>
        <li>Smaller, more frequent meals: 4&ndash;5 smaller meals rather than 3 large ones maintains total daily intake better when appetite is reduced</li>
      </ul>
    </div>

    <h3 style="margin-top:20px">Other critical gaps in older adults</h3>
    <div class="gap-row">
      <div class="gap-icon">&#129479;</div>
      <div><strong>Vitamin B12 &mdash; absorption declines with age</strong><br>
      <span style="font-size:13px;color:#475569">Gastric acid production decreases with age, impairing B12 absorption from food. By age 70, a meaningful proportion of older adults have sub-optimal B12 status despite adequate dietary intake. Regular testing recommended. Fortified foods and supplements (cyanocobalamin or methylcobalamin, 100&ndash;400&micro;g/day) bypass the absorption problem. Liver, sardines, eggs, and milk are dietary sources.</span></div>
    </div>
    <div class="gap-row">
      <div class="gap-icon">&#9728;&#65039;</div>
      <div><strong>Vitamin D &mdash; RDI increases to 800 IU after age 70</strong><br>
      <span style="font-size:13px;color:#475569">Skin becomes less efficient at synthesising Vitamin D from UV exposure with age. Older adults who spend limited time outdoors (especially in aged care) are at high risk. Supplementation of 800&ndash;1,000 IU/day is widely recommended for those over 70 who don&rsquo;t get regular sun exposure.</span></div>
    </div>
    <div class="gap-row">
      <div class="gap-icon">&#129370;</div>
      <div><strong>Calcium &mdash; 1,300mg/day for women over 50</strong><br>
      <span style="font-size:13px;color:#475569">Post-menopausal bone loss accelerates dramatically without adequate calcium. Women over 50 need 1,300mg/day (up from 1,000mg), and men over 70 need 1,200mg. Spread across 2&ndash;3 dairy serves throughout the day for best absorption &mdash; the gut can only absorb ~500mg efficiently per serving.</span></div>
    </div>
    <div class="gap-row">
      <div class="gap-icon">&#129428;</div>
      <div><strong>Zinc &mdash; immune function, wound healing, and appetite</strong><br>
      <span style="font-size:13px;color:#475569">Commonly low in elderly Australians. Zinc affects immune function, wound healing &mdash; and critically &mdash; taste and smell. Low zinc exacerbates the taste bud decline problem, further reducing appetite. Eggs, meat, and lentils cover requirements inexpensively.</span></div>
    </div>

    <div class="callout" style="margin-top:16px">
      <strong>The compounding problem:</strong> Reduced appetite (taste decline) &rarr; less protein intake &rarr; muscle loss (sarcopenia) &rarr; reduced strength &rarr; less activity &rarr; further muscle loss &rarr; falls and fractures. Breaking this cycle with adequate protein, resistance exercise, and appetite strategies is the single most effective intervention for healthy ageing. See the <a href="/guide/exercise-nutrition/">Exercise &amp; Nutrition guide</a> for the resistance training component.
    </div>
  </div>
</div>

{app_link()}

<p>For the full nutrient targets by age and sex, see the <a href="/guide/nrv/">NRV Reference Tables</a>. For which foods cover each gap, see <a href="/guide/foods-for-gaps/">Which Foods Fill Which Gaps</a>.</p>

<p style="font-size:12px;color:#94a3b8;margin-top:24px">Sources: NHMRC Australian Nutrient Reference Values (2006, updated 2017) &middot; ABS National Nutrition &amp; Physical Activity Survey 2023 &middot; Bauer J, et al. &ldquo;Evidence-based recommendations for optimal dietary protein intake in older people.&rdquo; J Am Med Dir Assoc. 2013 &middot; Cruz-Jentoft AJ, et al. &ldquo;Sarcopenia: revised European consensus on definition and diagnosis.&rdquo; Age Ageing. 2019 &middot; Moore DR, et al. &ldquo;Ingested protein dose response of muscle and albumin protein synthesis after resistance exercise in young men.&rdquo; Am J Clin Nutr. 2009</p>"""

p = BASE / "life-stages"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "Nutrient Gaps by Life Stage &mdash; OptimisedEats",
    "The most important nutrient gaps for every Australian life stage: children, teenagers, adult women, adult men, and older adults. Includes the protein synthesis problem in ageing.",
    "nutrient gaps by age Australia, elderly nutrition protein, teenage girl iron deficiency Australia, older adult protein requirements, sarcopenia nutrition Australia, anabolic resistance diet",
    "Nutrient Gaps by Life Stage", "/guide/life-stages/", life_body, related_for("/guide/life-stages/")
), encoding="utf-8")
print("DONE guide/life-stages/index.html")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2: VEGAN & PLANT-BASED NUTRITION
# ═══════════════════════════════════════════════════════════════════════════════

vegan_body = f"""<h1>Vegan &amp; Plant-Based Nutrition in Australia</h1>
<p class="lead">A well-planned plant-based diet can meet almost all nutritional needs &mdash; but several nutrients require specific attention or supplementation. This guide covers the non-negotiables, in priority order.</p>

<div class="callout-red">
  <strong>The honest summary:</strong> One nutrient (B12) requires mandatory supplementation regardless of how well-planned your diet is. Three others (iron, zinc, omega-3) need active dietary strategies. Two more (iodine, calcium) need specific food choices. Get these right and plant-based eating is nutritionally viable for all life stages.
</div>

<div class="vegan-card">
  <h3>&#9889; Vitamin B12 <span class="must-badge">SUPPLEMENT REQUIRED</span></h3>
  <p style="font-size:14px;color:#374151">There is no reliable plant-based source of Vitamin B12. Algae, fermented foods, and nutritional yeast contain B12 analogues that are not biologically active in humans. B12 deficiency develops slowly (the liver stores 2&ndash;3 years&rsquo; worth) but is devastating when it arrives: irreversible nerve damage, megaloblastic anaemia, cognitive impairment, and neurological symptoms that may be mistaken for dementia in older vegans.</p>
  <div class="callout-red" style="margin-top:12px">
    <strong>Minimum:</strong> 50 &micro;g/day (cyanocobalamin or methylcobalamin) daily, OR 2,000 &micro;g once per week &mdash; the high dose compensates for the passive absorption pathway when active absorption is saturated. Choose supplements over fortified foods for reliability.
  </div>
  <p style="font-size:13px;color:#475569;margin-top:10px">Cost: a 90-day supply of 1,000&micro;g B12 tablets costs approximately $8&ndash;12 at Australian pharmacies. It is the single most important purchase a vegan can make.</p>
</div>

<div class="vegan-card">
  <h3>&#129354; Iron <span class="important-badge">ACTIVE STRATEGY REQUIRED</span></h3>
  <p style="font-size:14px;color:#374151">Plant-based (non-heme) iron is 2&ndash;3&times; less absorbable than heme iron from meat. This is not a reason to avoid plant iron &mdash; it is a reason to be strategic about it.</p>
  <ul style="font-size:13px;color:#475569;line-height:1.8;padding-left:20px;margin-top:8px">
    <li><strong>Always pair with Vitamin C:</strong> A squeeze of lemon, tomato, capsicum, or broccoli alongside lentils, beans, or spinach can increase iron absorption 2&ndash;4&times;. This is the single most effective iron strategy for vegans.</li>
    <li><strong>Avoid tea and coffee within 1 hour of iron-rich meals.</strong> Tannins reduce non-heme iron absorption by 60&ndash;90%.</li>
    <li><strong>Soak and rinse legumes</strong> before cooking to reduce phytates by 30&ndash;60%, improving iron (and zinc) bioavailability.</li>
    <li><strong>Eat more total iron:</strong> Aim for 1.8&times; the standard RDI to compensate for lower bioavailability. Women 19&ndash;50: ~32mg/day from plant sources (vs 18mg standard RDI).</li>
  </ul>
  <p style="font-size:13px;color:#475569;margin-top:8px"><strong>Best budget plant iron sources:</strong> Lentils (3.3mg/100g cooked), canned kidney beans (2.9mg/100g), firm tofu (3mg/100g), fortified breakfast cereal, oats, spinach, pumpkin seeds.</p>
  <div class="callout-amber" style="margin-top:12px">
    <strong>Testing:</strong> Ask your GP for a serum ferritin test (not just haemoglobin). Ferritin below 30 &micro;g/L indicates depleted iron stores even before anaemia develops. Female vegans and those who menstruate should test annually.
  </div>
</div>

<div class="vegan-card">
  <h3>&#129428; Zinc <span class="important-badge">ACTIVE STRATEGY REQUIRED</span></h3>
  <p style="font-size:14px;color:#374151">Phytates in grains, legumes, nuts, and seeds bind zinc in the gut, reducing absorption by 25&ndash;50% compared to animal-source zinc. This means vegans need roughly 50% more total dietary zinc to achieve the same absorbed amount.</p>
  <p style="font-size:13px;color:#475569;margin-top:8px"><strong>Strategies to improve zinc absorption:</strong></p>
  <ul style="font-size:13px;color:#475569;line-height:1.7;padding-left:20px;margin-top:4px">
    <li>Soak dried legumes overnight and discard water before cooking &mdash; reduces phytate content 30&ndash;60%</li>
    <li>Sprouting further reduces phytates and increases zinc bioavailability</li>
    <li>Sourdough fermentation reduces phytates in bread &mdash; a meaningful advantage over regular bread</li>
    <li>Include pumpkin seeds (8mg/100g) regularly &mdash; the highest plant zinc source</li>
  </ul>
  <p style="font-size:13px;color:#475569;margin-top:8px"><strong>Vegan zinc targets:</strong> Men 14mg/day &times; 1.5 = aim for ~21mg from plant sources. Women 8mg/day &times; 1.5 = aim for ~12mg.</p>
</div>

<div class="vegan-card">
  <h3>&#129490; Omega-3 (DHA and EPA) <span class="important-badge">SUPPLEMENT RECOMMENDED</span></h3>
  <p style="font-size:14px;color:#374151">ALA (alpha-linolenic acid) from flaxseed, chia seeds, walnuts, and hemp seeds is the plant form of omega-3. The problem: conversion to the biologically active DHA and EPA forms is inefficient &mdash; approximately 5&ndash;15% conversion for DHA, less for EPA. For most healthy adults, adequate ALA intake is sufficient. But for pregnancy, breastfeeding, infants, and those with cardiovascular or cognitive concerns, the conversion may be insufficient.</p>
  <div class="callout" style="margin-top:12px">
    <strong>Recommended:</strong> Algae-based DHA/EPA supplement (200&ndash;300mg DHA/day). Algae is where fish get their DHA &mdash; going directly to the source bypasses the inefficient conversion. Available at Australian health food stores and chemists for ~$20&ndash;30/month.
  </div>
  <p style="font-size:13px;color:#475569;margin-top:10px"><strong>Best budget ALA sources:</strong> Ground flaxseed (2.4g ALA per tbsp, ~$0.10/serve), chia seeds (5g per 30g serve), walnuts (2.6g per 30g serve).</p>
</div>

<div class="vegan-card">
  <h3>&#127985; Calcium</h3>
  <p style="font-size:14px;color:#374151">Without dairy, calcium requires deliberate food choices. The challenge is that many plant calcium sources contain oxalates (spinach, silverbeet) or phytates (legumes) that significantly reduce calcium absorption.</p>
  <table class="data-table" style="margin-top:12px">
  <thead><tr><th>Food</th><th>Calcium per serve</th><th>Absorption rate</th><th>Notes</th></tr></thead>
  <tbody>
  <tr><td>Fortified plant milk (250mL)</td><td>300mg</td><td>~30%</td><td>Look for calcium carbonate fortification</td></tr>
  <tr><td>Calcium-set tofu (100g)</td><td>200&ndash;350mg</td><td>~31%</td><td>Check label &mdash; must say &ldquo;calcium sulfate&rdquo;</td></tr>
  <tr><td>Tahini (2 tbsp)</td><td>130mg</td><td>~20%</td><td>Sesame oxalate reduces absorption</td></tr>
  <tr><td>Kale, bok choy (100g cooked)</td><td>100&ndash;150mg</td><td>~50%</td><td>Lower oxalate &mdash; best plant calcium source</td></tr>
  <tr><td>Spinach (100g cooked)</td><td>136mg</td><td>~5%</td><td>High oxalate &mdash; poor calcium source</td></tr>
  <tr><td>Canned white beans (100g)</td><td>90mg</td><td>~17%</td><td>Phytates reduce absorption</td></tr>
  </tbody>
  </table>
  <div class="callout-amber" style="margin-top:12px">
    <strong>Strategy:</strong> 2&times; fortified plant milk + calcium-set tofu + kale or bok choy 3&times;/week covers calcium requirements for most adults. Avoid relying on spinach or silverbeet as a calcium source despite their high listed calcium content &mdash; the oxalate binding makes it largely unavailable.
  </div>
</div>

<div class="vegan-card">
  <h3>&#127758; Iodine <span class="important-badge">SUPPLEMENT USUALLY NEEDED</span></h3>
  <p style="font-size:14px;color:#374151">Seaweed is widely promoted as a vegan iodine source but is actually the worst option &mdash; iodine content varies 100-fold between species and even between batches of the same species. Nori can range from 16&micro;g to over 1,000&micro;g per sheet. This variability makes it impossible to reliably dose from seaweed.</p>
  <div class="callout-red" style="margin-top:12px">
    <strong>Reliable options:</strong> Use iodised salt (use modestly &mdash; only 1/4 tsp covers the 150&micro;g target but sodium intake must be managed), OR take a kelp supplement standardised to ~150&micro;g iodine per day. Vegans who avoid dairy and fish are at particular risk of deficiency.
  </div>
</div>

<div class="vegan-card">
  <h3>&#9728;&#65039; Vitamin D</h3>
  <p style="font-size:14px;color:#374151">Same requirements as omnivores. Sun exposure covers requirements for most Australians most of the year (15&ndash;30 min daily on arms and legs). In winter in southern states, or for those with limited sun exposure, a supplement of 1,000&ndash;2,000 IU/day is appropriate. Ensure any supplement is labelled D3 (cholecalciferol) from lichen &mdash; not D2 &mdash; for best bioavailability.</p>
</div>

<h2>Protein on a vegan diet</h2>
<p>Vegan protein sources are nutritionally adequate but two adjustments are needed:</p>
<div class="callout">
  <strong>1. Eat 10&ndash;20% more total protein</strong> than the standard RDI to compensate for lower digestibility of plant proteins (DIAAS scores typically 0.5&ndash;0.8 vs 1.0&ndash;1.2 for animal proteins).
</div>
<div class="callout">
  <strong>2. Combine protein sources across the day</strong> to cover all essential amino acids. Legumes (high in lysine, low in methionine) + grains (high in methionine, low in lysine) complement each other. Rice and lentils, beans on toast, hummus with bread &mdash; these traditional pairings are nutritionally sound.
</div>
<p style="font-size:14px;color:#374151"><strong>Best budget vegan protein sources:</strong> Cooked lentils (9g/100g), firm tofu (8g/100g), cooked chickpeas (8.9g/100g), oats dry (17g/100g), peanut butter (25g/100g), tempeh (19g/100g).</p>

<h2>Life stages requiring extra attention</h2>
<div class="callout-purple">
  <strong>Pregnancy and breastfeeding:</strong> Mandatory B12 supplement + algae DHA (300mg/day) + iron monitoring (serum ferritin testing recommended each trimester) + iodine supplement (150&micro;g/day in addition to diet). Inform your GP or midwife. See the <a href="/guide/pregnancy/">Pregnancy Nutrition guide</a>.
</div>
<div class="callout-amber">
  <strong>Children and teenagers:</strong> B12 mandatory. Iron and zinc monitoring strongly recommended. Calcium from fortified plant milk (3 serves/day) is critical during growth. See <a href="/guide/kids/">Kids &amp; Toddlers</a> and the <a href="/guide/life-stages/">Life Stages guide</a>.
</div>
<div class="callout-blue">
  <strong>Older adults:</strong> B12 supplement (gastric acid decline makes food-based B12 unreliable regardless of source). Increase protein to 1.2&ndash;1.6 g/kg/day. Algae DHA for cognitive and cardiovascular protection. See the <a href="/guide/life-stages/">Life Stages guide</a> for the full older adult protein story.
</div>

{app_link("Track your plant-based diet in the free app")}

<p style="font-size:12px;color:#94a3b8;margin-top:24px">Sources: NHMRC Australian Nutrient Reference Values (2006, updated 2017) &middot; Melina V, Craig W, Levin S. &ldquo;Position of the Academy of Nutrition and Dietetics: Vegetarian Diets.&rdquo; J Acad Nutr Diet. 2016 &middot; Saunders AV, et al. &ldquo;Zinc and vegetarian diets.&rdquo; Med J Aust. 2013 &middot; Pawlak R, et al. &ldquo;How prevalent is vitamin B12 deficiency among vegetarians?&rdquo; Nutr Rev. 2013 &middot; Hurrell R, Egli I. &ldquo;Iron bioavailability and dietary reference values.&rdquo; Am J Clin Nutr. 2010</p>"""

p = BASE / "vegan-nutrition"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "Vegan &amp; Plant-Based Nutrition Australia &mdash; OptimisedEats",
    "The essential nutrient guide for Australian vegans. B12, iron, zinc, omega-3, calcium, iodine and protein strategies for plant-based diets at every life stage.",
    "vegan nutrition Australia, plant based diet nutrients, B12 vegan supplement, vegan iron absorption, vegan calcium sources, algae DHA Australia, vegan pregnancy nutrition",
    "Vegan &amp; Plant-Based", "/guide/vegan-nutrition/", vegan_body, related_for("/guide/vegan-nutrition/")
), encoding="utf-8")
print("DONE guide/vegan-nutrition/index.html")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3: EXERCISE & NUTRITION
# ═══════════════════════════════════════════════════════════════════════════════

exercise_body = f"""<h1>Exercise, Movement &amp; Nutrition</h1>
<p class="lead">Exercise and nutrition are inseparable &mdash; each amplifies the benefits of the other. Being active changes what you need to eat. This guide covers the Australian guidelines, how exercise shifts your nutrient requirements, and how to fuel activity on a real budget.</p>

<h2>Australian Physical Activity Guidelines summary</h2>
<table class="ex-table">
<thead><tr><th>Age Group</th><th>Weekly Cardio Target</th><th>Strength Training</th><th>Sedentary Behaviour</th></tr></thead>
<tbody>
<tr><td><strong>Children 5&ndash;12</strong></td><td>60 min/day moderate-to-vigorous</td><td>3&times;/week muscle &amp; bone strengthening</td><td>Max 2hrs recreational screen time/day</td></tr>
<tr><td><strong>Teens 13&ndash;17</strong></td><td>60 min/day; some vigorous</td><td>3&times;/week resistance &amp; bone-loading</td><td>Break up sitting; limit leisure screens</td></tr>
<tr><td><strong>Adults 18&ndash;64</strong></td><td>150&ndash;300 min moderate OR 75&ndash;150 min vigorous/week</td><td>2&times;/week muscle-strengthening</td><td>Break up long sitting regularly</td></tr>
<tr><td><strong>Older Adults 65+</strong></td><td>150&ndash;300 min moderate/week</td><td>2&times;/week strength + balance</td><td>Move more, sit less; any activity counts</td></tr>
</tbody>
</table>
<div class="callout-blue">
  <strong>A 30-minute brisk walk daily</strong> meets the minimum adult cardio target (150 min/week), generates Vitamin D, costs nothing, and is sustainable for almost every fitness level. It is the single highest-return physical activity investment for sedentary adults.
</div>

<h2>Why strength training is non-negotiable</h2>
<div class="nutrient-section">
  <div class="gap-row">
    <div class="gap-icon">&#129351;</div>
    <div><strong>Muscle mass is the strongest predictor of healthy ageing</strong><br>
    <span style="font-size:13px;color:#475569">More muscle means better glucose regulation, better bone density, lower fall risk, and longer independent living. Sarcopenia (age-related muscle loss) begins in your 30s at approximately 1% per year if not actively counteracted. Weight training directly reverses this.</span></div>
  </div>
  <div class="gap-row">
    <div class="gap-icon">&#129504;</div>
    <div><strong>Insulin sensitivity improves independently of weight loss</strong><br>
    <span style="font-size:13px;color:#475569">Just 2 sessions per week of resistance exercise reduces type 2 diabetes risk by 30&ndash;35%. The mechanism is separate from and additive to aerobic exercise benefits.</span></div>
  </div>
  <div class="gap-row">
    <div class="gap-icon">&#129459;</div>
    <div><strong>Bone density responds to mechanical loading</strong><br>
    <span style="font-size:13px;color:#475569">Weight-bearing resistance exercise is the most effective non-pharmacological strategy for reducing osteoporosis risk &mdash; more effective than calcium supplementation alone.</span></div>
  </div>
  <div class="gap-row">
    <div class="gap-icon">&#128176;</div>
    <div><strong>You don&rsquo;t need a gym</strong><br>
    <span style="font-size:13px;color:#475569">Push-ups, squats, lunges, planks, and bodyweight rows are free and fully effective for most people. A set of resistance bands (~$15 once) and a backpack filled with books covers progressive loading. No ongoing costs required.</span></div>
  </div>
</div>

<h2>How exercise changes your nutrient requirements</h2>
<table class="ex-table">
<thead><tr><th>Nutrient</th><th>Target for Active Adults</th><th>Why It Changes</th><th>Budget Strategy</th></tr></thead>
<tbody>
<tr><td><strong>Protein</strong></td><td>1.2&ndash;1.7 g/kg/day (active)<br><small style="color:#94a3b8">vs 0.75 g/kg sedentary</small></td><td>Muscle repair and synthesis after resistance exercise. Upper end (1.5&ndash;1.7) for weight training; lower-mid (1.2&ndash;1.4) for endurance</td><td>Eggs + lentils + sardines covers most needs at ~$1.50/day extra</td></tr>
<tr><td><strong>Carbohydrates</strong></td><td>4&ndash;7 g/kg/day for performance</td><td>Primary fuel for moderate-to-high intensity exercise. 1&ndash;1.5 g/kg post-exercise for glycogen recovery</td><td>Oats, banana, rice, bread &mdash; the cheapest energy sources</td></tr>
<tr><td><strong>Iron</strong></td><td>Female athletes: up to 30% higher need</td><td>Foot-strike haemolysis (red cell destruction from impact), sweat losses, and increased turnover</td><td>Weekly red meat or liver; combine with Vitamin C foods always</td></tr>
<tr><td><strong>Magnesium</strong></td><td>10&ndash;20% above sedentary RDI</td><td>Muscle contraction, energy production, lost in sweat. Hot Australian summers increase losses significantly</td><td>Pumpkin seeds (534mg per 100g), spinach, lentils</td></tr>
<tr><td><strong>Electrolytes</strong></td><td>Increases with sweat volume</td><td>Sodium, potassium and magnesium lost in sweat. Critical in hot, humid conditions</td><td>Banana + pinch of salt + water beats sports drinks at 1/20th the cost</td></tr>
<tr><td><strong>Omega-3</strong></td><td>1.6g ALA/day + EPA/DHA beneficial</td><td>Anti-inflammatory; supports muscle repair, may reduce DOMS and improve recovery time</td><td>Sardines 2&times;/week, ground flaxseed on oats daily</td></tr>
<tr><td><strong>Vitamin D</strong></td><td>Same RDI but more consequential</td><td>Supports muscle fibre development; deficiency measurably impairs strength gains and recovery</td><td>15&ndash;30 min sun on arms/legs most days; supplement in winter</td></tr>
</tbody>
</table>

<h2>Protein timing &mdash; when you eat matters as much as how much</h2>
<div class="callout">
  <strong>Post-workout window:</strong> 20&ndash;40g of protein within 2 hours of resistance exercise maximises muscle protein synthesis. The anabolic window is real, though more generous than the &ldquo;30 seconds or it doesn&rsquo;t count&rdquo; myth suggests. Budget post-workout meal: 2 boiled eggs + 250mL milk = ~25g protein, complete amino acid profile, ~$0.90. Beats any protein bar.
</div>
<div class="callout-blue">
  <strong>Distribution across the day:</strong> Three meals of 30&ndash;40g protein stimulates more total muscle synthesis than one meal of 90g and two small ones. Getting protein at every meal matters as much as hitting the daily total.
</div>

<h2>Breaking the overnight catabolic cycle &mdash; why your first meal matters most</h2>
<div class="myth-box">
  <div class="myth-label">&#10060; What most people do</div>
  <div class="myth-text">Toast, cereal, a piece of fruit, or skip breakfast entirely &mdash; then wonder why building muscle is so hard.</div>
  <div class="reality-label">&#9989; What&rsquo;s actually happening</div>
  <div class="reality-text">You&rsquo;ve been in a catabolic state since roughly 10pm last night. Your first meal is the switch that flips you back to anabolic &mdash; but only if it hits the protein threshold. A small or low-protein breakfast doesn&rsquo;t flip the switch. It just reduces the rate of breakdown slightly while you stay in net negative protein balance until lunch &mdash; a 14&ndash;16 hour catabolic window.</div>
</div>

<div class="nutrient-section">
  <h3>The overnight fast &mdash; what&rsquo;s happening in your body</h3>
  <p style="font-size:14px;color:#374151">During an 8&ndash;12 hour overnight fast, the body enters a catabolic state by necessity. The brain needs glucose continuously. With no incoming food, the body runs gluconeogenesis &mdash; manufacturing glucose from amino acids stripped from muscle tissue. This is normal and unavoidable. What matters is how long it continues after you wake up.</p>
  <p style="font-size:14px;color:#374151">The <strong>cortisol awakening response</strong> peaks approximately 30&ndash;45 minutes after waking. This morning cortisol spike is catabolic by design &mdash; it mobilises energy for the day ahead by breaking down protein stores. It&rsquo;s a feature, not a bug. But combined with an already-fasted state, it means you&rsquo;re in maximum catabolism at 7am.</p>

  <h3>The leucine threshold &mdash; what it takes to flip the switch</h3>
  <p style="font-size:14px;color:#374151">Muscle protein synthesis is triggered by the mTOR pathway, and leucine is the essential amino acid that directly activates it. The threshold for switching from net breakdown to net building is approximately <strong>3g of leucine per meal</strong> &mdash; equivalent to roughly 30&ndash;40g of complete protein.</p>
  <div class="callout-red">
    <strong>Below the leucine threshold, muscle protein synthesis barely activates.</strong> This means 15g of protein at breakfast (one egg, or a small bowl of yoghurt, or a piece of toast) provides amino acids but doesn&rsquo;t flip the anabolic switch. You remain in net catabolic state until your next meal &mdash; if that meal is lunch, you&rsquo;ve been breaking down muscle for 14&ndash;16 hours.
  </div>

  <h3>Common breakfasts &mdash; do they hit the threshold?</h3>
  <table class="data-table">
  <thead><tr><th>Breakfast</th><th>Protein</th><th>Leucine (approx)</th><th>Flips anabolic switch?</th></tr></thead>
  <tbody>
  <tr><td>2 slices toast + vegemite</td><td>~8g</td><td>~0.5g</td><td style="color:#dc2626;font-weight:700">No</td></tr>
  <tr><td>Bowl of corn flakes + milk</td><td>~9g</td><td>~0.6g</td><td style="color:#dc2626;font-weight:700">No</td></tr>
  <tr><td>Banana + coffee</td><td>~1g</td><td>~0.1g</td><td style="color:#dc2626;font-weight:700">No</td></tr>
  <tr><td>2 eggs on toast</td><td>~18g</td><td>~1.4g</td><td style="color:#f59e0b;font-weight:700">Borderline</td></tr>
  <tr><td>3 eggs scrambled</td><td>~21g</td><td>~1.7g</td><td style="color:#f59e0b;font-weight:700">Borderline</td></tr>
  <tr><td>2 eggs + 200g Greek yoghurt</td><td>~32g</td><td>~2.7g</td><td style="color:#16a34a;font-weight:700">Yes &#10003;</td></tr>
  <tr><td>3 eggs + 250mL milk</td><td>~30g</td><td>~2.5g</td><td style="color:#16a34a;font-weight:700">Yes &#10003;</td></tr>
  <tr><td>2 eggs + 100g cottage cheese + toast</td><td>~33g</td><td>~2.8g</td><td style="color:#16a34a;font-weight:700">Yes &#10003;</td></tr>
  <tr><td>Greek yoghurt (200g) + pumpkin seeds + oats</td><td>~28g</td><td>~2.2g</td><td style="color:#16a34a;font-weight:700">Yes &#10003;</td></tr>
  </tbody>
  </table>

  <h3>For older adults &mdash; the stakes are higher</h3>
  <p style="font-size:14px;color:#374151">Due to anabolic resistance, the leucine threshold rises to approximately <strong>3.5&ndash;4g per meal</strong> for adults over 65 &mdash; requiring 35&ndash;40g of high-quality protein to trigger the same muscle-building response. A typical low-protein breakfast in an older adult isn&rsquo;t just suboptimal &mdash; it&rsquo;s actively contributing to sarcopenia, one meal at a time, compounded every single morning for years.</p>
  <div class="callout-purple">
    <strong>Budget morning fix for older adults:</strong> 3 eggs + 200g Greek yoghurt = ~38g protein, ~3.3g leucine, ~$1.60. This single habit change &mdash; applied consistently &mdash; is one of the most meaningful interventions for preventing age-related muscle loss. See the <a href="/guide/life-stages/">Life Stages guide</a> for the full sarcopenia and anabolic resistance picture.
  </div>

  <h3>The compounding effect</h3>
  <p style="font-size:14px;color:#374151">One subthreshold breakfast doesn&rsquo;t cause noticeable muscle loss. But 365 of them per year, for 10 years, compounded by gradual activity decline, is one of the primary mechanisms behind why people lose significant muscle mass as they age &mdash; and why it happens gradually enough that most people don&rsquo;t notice until function is already compromised.</p>
</div>

<h2>Budget active person &mdash; weekly blueprint</h2>
<div class="nutrient-section">
  <h3>Movement (free or near-free)</h3>
  <div class="habit-item">
    <div class="habit-num">&#128170;</div>
    <div class="habit-body">
      <div class="habit-title">Mon / Thu &mdash; bodyweight strength circuit (30&ndash;40 min)</div>
      <div class="habit-detail">Push-ups, squats, lunges, rows (using a table edge or resistance band), planks, hip hinges. Progressive &mdash; add reps each week. No gym needed.</div>
    </div>
  </div>
  <div class="habit-item">
    <div class="habit-num">&#127939;</div>
    <div class="habit-body">
      <div class="habit-title">Daily &mdash; 30 min brisk walk</div>
      <div class="habit-detail">Meets the 150 min/week moderate cardio target. Generates Vitamin D. Costs nothing. Do it after lunch for maximum UV exposure in southern states.</div>
    </div>
  </div>
  <div class="habit-item">
    <div class="habit-num">&#127944;</div>
    <div class="habit-body">
      <div class="habit-title">Weekend &mdash; one longer enjoyable session</div>
      <div class="habit-detail">Bushwalk, swim, bike ride, social sport. Enjoyable activity is 3&times; more sustainable than joyless exercise. This is the session you&rsquo;ll keep doing in 5 years.</div>
    </div>
  </div>

  <h3 style="margin-top:16px">Nutrition adjustments (budget-aligned)</h3>
  <div class="habit-item">
    <div class="habit-num">&#129428;</div>
    <div class="habit-body">
      <div class="habit-title">Post-workout: 2 boiled eggs + 250mL milk</div>
      <div class="habit-detail">~25g complete protein, ~$0.90. Covers the post-exercise protein window without supplements.</div>
    </div>
  </div>
  <div class="habit-item">
    <div class="habit-num">&#129419;</div>
    <div class="habit-body">
      <div class="habit-title">Weekly sardine meal</div>
      <div class="habit-detail">Omega-3, Vitamin D, protein, calcium in one ~$1.80 meal. Anti-inflammatory and supports exercise recovery.</div>
    </div>
  </div>
  <div class="habit-item">
    <div class="habit-num">&#127820;</div>
    <div class="habit-body">
      <div class="habit-title">Daily banana post-exercise or any time</div>
      <div class="habit-detail">Potassium replacement, quick carbohydrate for glycogen recovery, ~$0.30. Better than a sports drink for most workouts under 90 minutes.</div>
    </div>
  </div>
  <div class="habit-item">
    <div class="habit-num">&#129302;</div>
    <div class="habit-body">
      <div class="habit-title">Pumpkin seeds on oats or yoghurt daily</div>
      <div class="habit-detail">Addresses the magnesium gap that exercise opens up, especially in summer. ~$0.25/serve for 150&ndash;160mg magnesium.</div>
    </div>
  </div>
</div>

<h2>Sedentary behaviour &mdash; the hidden risk</h2>
<p>Physical inactivity is the fourth largest risk factor for global mortality. But separate from exercise, <strong>prolonged sitting is an independent risk factor</strong> &mdash; even in people who exercise regularly. An hour of gym does not undo eight hours of sitting.</p>
<div class="callout-amber">
  <strong>Break up sitting every 30&ndash;60 minutes.</strong> Even a 2-minute walk to the kitchen substantially improves glucose regulation and circulation. Set an hourly reminder. Three 10-minute bouts of brisk walking produces similar cardiovascular benefit to one 30-minute bout &mdash; the &ldquo;exercise snack&rdquo; approach works.
</div>

<h2>Sarcopenia &mdash; the muscle loss crisis in ageing</h2>
<p>Sarcopenia affects an estimated 10&ndash;20% of Australians over 65, rising to 30&ndash;50% over 80. It is the leading cause of falls, fractures, disability, and loss of independence in older adults, with an annual economic cost exceeding $2.5 billion in Australia.</p>
<div class="callout-red">
  <strong>Protein alone cannot prevent sarcopenia.</strong> Resistance exercise is the essential co-factor. The anabolic signal from weight training sensitises muscle tissue to protein for 24&ndash;48 hours post-exercise. Without this signal, even high protein intake produces minimal muscle protein synthesis in older adults. Both are required.
</div>
<div class="callout">
  <strong>Older adults: 3&ndash;4 strength sessions per week</strong> with 25&ndash;40g protein within 2 hours produces the best outcomes for muscle preservation &mdash; compared to the guideline minimum of 2 sessions. The Australian guidelines represent the floor, not the optimal target. See the <a href="/guide/life-stages/">Life Stages guide</a> for the full protein and anabolic resistance story.
</div>

<h2>Exercise for special populations</h2>
<div class="nutrient-section">
  <div class="gap-row">
    <div class="gap-icon">&#129491;</div>
    <div><strong>Older adults (65+):</strong> Balance training is mandatory &mdash; it is the single most effective intervention to prevent falls, the leading cause of injury-related death in Australians over 65. Tai chi meets both balance and moderate activity requirements. Chair-based exercises are appropriate for those with mobility limitations.</div>
  </div>
  <div class="gap-row">
    <div class="gap-icon">&#127981;</div>
    <div><strong>Children and teenagers:</strong> Organised sport covers activity guidelines and social development. Unstructured active play, walking/cycling to school also count. Screen time displacement is the primary driver of inactivity in Australian children &mdash; active transport to school adds 20&ndash;30 min/day automatically.</div>
  </div>
  <div class="gap-row">
    <div class="gap-icon">&#129387;</div>
    <div><strong>Pregnancy:</strong> Exercise is strongly encouraged throughout low-risk pregnancy (150&ndash;300 min/week moderate). Swimming and walking are ideal. Strength training is safe with appropriate modifications. Exercise during pregnancy reduces gestational diabetes risk by 38%, reduces caesarean rate, and improves infant outcomes. See the <a href="/guide/pregnancy/">Pregnancy Nutrition guide</a>.</div>
  </div>
</div>

{app_link("See your household's exact nutrient targets in the free app")}

<p style="font-size:12px;color:#94a3b8;margin-top:24px">Sources: Department of Health Australia. <em>Physical Activity and Sedentary Behaviour Guidelines</em> (2021) &middot; Cruz-Jentoft AJ, et al. &ldquo;Sarcopenia: revised European consensus.&rdquo; Age Ageing. 2019 &middot; ACSM Position Stand on Nutrition and Athletic Performance &middot; Colberg SR, et al. &ldquo;Physical Activity/Exercise and Diabetes.&rdquo; Diabetes Care. 2016 &middot; Bauer J, et al. &ldquo;Evidence-based recommendations for optimal dietary protein intake in older people.&rdquo; J Am Med Dir Assoc. 2013</p>"""

p = BASE / "exercise-nutrition"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "Exercise, Movement &amp; Nutrition &mdash; OptimisedEats",
    "How exercise changes your nutrient requirements. Australian physical activity guidelines, protein timing, sarcopenia, and fuelling activity on a budget.",
    "exercise nutrition Australia, how much protein active adults, sarcopenia diet exercise, physical activity guidelines Australia, strength training diet, fuelling exercise budget",
    "Exercise &amp; Nutrition", "/guide/exercise-nutrition/", exercise_body, related_for("/guide/exercise-nutrition/")
), encoding="utf-8")
print("DONE guide/exercise-nutrition/index.html")
print("\nAll life/exercise pages generated!")
