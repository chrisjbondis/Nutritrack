"""Generate pre-conception and deficiency-symptoms guide pages."""
import pathlib

BASE = pathlib.Path(__file__).parent
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
.tea-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px;margin:12px 0}
.tea-card{padding:10px 12px;border-radius:8px;font-size:13px}
.tea-safe{background:#f0fdf4;border:1px solid #bbf7d0}
.tea-caution{background:#fffbeb;border:1px solid #fde68a}
.tea-avoid{background:#fef2f2;border:1px solid #fecaca}
.tea-label{font-weight:700;margin-bottom:2px}
.tea-detail{font-size:11px;color:#64748b}
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
  <p>&#169; 2025 OptimisedEats &middot; Free nutrition planning for Australians &amp; New Zealanders &middot; <a href="/">Open App</a></p>
  <p style="margin-top:6px;font-size:11px;color:#cbd5e1">Information is based on NHMRC Australian Nutrient Reference Values and peer-reviewed research. For general educational purposes only &mdash; not a substitute for personalised medical advice. Consult your GP or midwife before making significant dietary changes during pre-conception or pregnancy.</p>
</footer>
</body>
</html>"""

ALL_RELATED = [
    ("Budget Basics",         "/guide/budget-basics/"),
    ("Nutrient Gaps",         "/guide/nutrient-gaps/"),
    ("Deficiency Symptoms",   "/guide/deficiency-symptoms/"),
    ("Hidden Hunger",         "/guide/hidden-hunger/"),
    ("Pre-Conception",        "/guide/pre-conception/"),
    ("Pregnancy Nutrition",   "/guide/pregnancy/"),
    ("Kids &amp; Toddlers",   "/guide/kids/"),
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


# =============================================================================
# PAGE 1: PRE-CONCEPTION NUTRITION — BOTH PARTNERS
# =============================================================================

precon_body = """
<h1>Pre-Conception Nutrition — For Both Partners</h1>
<p class="lead">The nutritional status of <em>both</em> partners in the months before conception profoundly shapes the health of a child. This is one of the most important and least-discussed areas of nutrition science.</p>

<div class="callout">
  <strong>Start 6 months before you plan to conceive &mdash; both partners.</strong><br>
  Many critical developmental processes occur in the first 3&ndash;4 weeks of pregnancy &mdash; often before a woman even knows she is pregnant. Nutritional deficiencies that exist at the moment of conception cannot be fully corrected after the fact.
</div>

<h2>Why both partners? The epigenetics evidence</h2>
<p>Your DNA is the instruction manual. Epigenetic marks are sticky notes on that manual &mdash; they tell cells which pages to read and which to ignore. These marks are profoundly influenced by diet, particularly during critical windows: the months before conception, foetal development, and early childhood.</p>
<p>Key nutrients that control epigenetic marks include:</p>
<ul>
  <li><strong>Folate, B12, and choline</strong> &mdash; supply methyl groups for DNA methylation (critical for gene regulation)</li>
  <li><strong>Zinc</strong> &mdash; acts as a cofactor for enzymes that modify histones (how tightly DNA is wound)</li>
  <li><strong>Vitamin D</strong> &mdash; directly regulates expression of over 1,000 genes via receptors on chromatin</li>
  <li><strong>Iron</strong> &mdash; affects histone demethylase activity</li>
  <li><strong>Omega-3 (DHA)</strong> &mdash; alters gene expression in the brain, immune cells, and adipose tissue</li>
</ul>

<div class="highlight-box">
  <h3>The Dutch Hunger Winter</h3>
  <p>Children born to mothers pregnant during the 1944&ndash;45 Dutch famine have been studied for 80+ years. Exposed during the <em>first trimester</em>, they showed significantly higher adult rates of schizophrenia, bipolar disorder, obesity, type 2 diabetes, and cardiovascular disease &mdash; compared to siblings born just months earlier or later. These effects were passed to their children too.</p>
  <p>The lesson: nutritional conditions at the moment cells are dividing fastest &mdash; conception and the first trimester &mdash; leave marks that last a lifetime.</p>
</div>

<h2>Nutrition for both partners</h2>
<div class="partner-grid">
  <div class="partner-card partner-female">
    <h3>&#9792; Female partner</h3>
    <p style="font-size:13px;color:#64748b;margin-bottom:14px">Building reserves and optimal hormonal environment</p>
    <ul>
      <li><strong>Folate &mdash; 400&ndash;800 mcg/day supplement</strong><br>Neural tube closure happens days 21&ndash;28 of gestation &mdash; before most women know they are pregnant. Every woman who could conceive should be supplementing. Diet alone is not reliable enough.</li>
      <li style="margin-top:10px"><strong>Iron &mdash; build stores now</strong><br>Iron requirements nearly double in pregnancy (to 27 mg/day). Women who enter pregnancy with low ferritin have little buffer. If you&rsquo;re frequently tired, ask your GP to check ferritin (not just haemoglobin).</li>
      <li style="margin-top:10px"><strong>Iodine &mdash; 150 mcg supplement</strong><br>NHMRC recommends 150 mcg iodine daily from pre-conception through lactation. Australian soils are iodine-poor. Use iodised salt and consider a prenatal multivitamin with iodine.</li>
      <li style="margin-top:10px"><strong>DHA omega-3 &mdash; 200+ mg/day</strong><br>The foetal brain accumulates DHA rapidly in the third trimester. Maternal DHA depletion is strongly linked to postpartum depression. Sardines 2&times;/week or an algae-based supplement.</li>
      <li style="margin-top:10px"><strong>Choline &mdash; 425 mg/day (rises to 450 in pregnancy)</strong><br>Choline supports foetal brain development and is needed for DNA methylation. 2 eggs daily covers ~280 mg &mdash; the most affordable source.</li>
    </ul>
  </div>
  <div class="partner-card partner-male">
    <h3>&#9794; Male partner</h3>
    <p style="font-size:13px;color:#64748b;margin-bottom:14px">Sperm quality, DNA integrity, and epigenetic contribution</p>
    <ul>
      <li><strong>Zinc &mdash; 14 mg/day (RDI)</strong><br>Zinc is essential for testosterone production and sperm development. Zinc deficiency directly impairs sperm count, motility, and morphology. 48% of Australian men fall short of the RDI. Beef mince (8 mg/100g), pumpkin seeds (2.2 mg/30g), and oats (2.3 mg/80g dry) are the cheapest sources.</li>
      <li style="margin-top:10px"><strong>Folate &mdash; 400 mcg/day</strong><br>Folate is required for DNA synthesis in sperm production. Low paternal folate is associated with chromosomal abnormalities in sperm. This is rarely mentioned but well-evidenced.</li>
      <li style="margin-top:10px"><strong>DHA omega-3</strong><br>DHA is concentrated in the sperm midpiece &mdash; the engine that drives motility. Low DHA is associated with poor sperm motility. Sardines, salmon, or an omega-3 supplement.</li>
      <li style="margin-top:10px"><strong>Vitamin C &mdash; 90 mg/day</strong><br>Sperm DNA is vulnerable to oxidative damage. Vitamin C is a key antioxidant that protects sperm DNA integrity. Half a capsicum (~150 mg) or a glass of orange juice daily is sufficient.</li>
      <li style="margin-top:10px"><strong>Selenium &mdash; 70 mcg/day</strong><br>Selenium is essential for sperm motility and structural integrity of the sperm flagellum. Two Brazil nuts provide the full daily requirement &mdash; or 95g of sardines (70% RDI).</li>
    </ul>
  </div>
</div>

<h2>The key foods for pre-conception (both partners)</h2>
<table class="data-table">
  <thead><tr><th>Food</th><th>Key pre-conception nutrients</th><th>Cost</th><th>How often</th></tr></thead>
  <tbody>
    <tr><td>Eggs</td><td>Choline, folate, DHA, selenium, vitamin D, B12</td><td>~$0.60/2 eggs</td><td>Daily</td></tr>
    <tr><td>Sardines or salmon (canned)</td><td>DHA omega-3, selenium, vitamin D, B12, calcium</td><td>~$1.50/tin</td><td>2&ndash;3&times;/week</td></tr>
    <tr><td>Lentils and chickpeas</td><td>Folate, iron, zinc, fibre</td><td>~$0.20/cup</td><td>3&ndash;4&times;/week</td></tr>
    <tr><td>Beef or kangaroo mince</td><td>Zinc, haem iron, B12, selenium</td><td>~$1.00/100g</td><td>2&times;/week</td></tr>
    <tr><td>Leafy greens (spinach, kale)</td><td>Folate, iron, vitamin K, magnesium</td><td>~$0.30/cup</td><td>Daily</td></tr>
    <tr><td>Full-cream milk or yoghurt</td><td>Iodine, calcium, B12, protein</td><td>~$0.50/serve</td><td>Daily</td></tr>
    <tr><td>Pumpkin seeds</td><td>Zinc, magnesium, selenium, omega-3 ALA</td><td>~$0.30/30g</td><td>Daily</td></tr>
    <tr><td>Colourful vegetables</td><td>Folate, antioxidants, beta-carotene, vitamin C</td><td>~$0.30/serve</td><td>Daily</td></tr>
  </tbody>
</table>

<h2>What traditional cultures knew</h2>
<p>Researcher Weston A. Price studied traditional communities worldwide in the 1930s &mdash; Swiss mountain villages, Pacific islanders, Indigenous North Americans, Maasai pastoralists, and Japanese coastal communities. Despite their vast differences, every one of these cultures had <strong>specific foods reserved for couples planning to conceive and pregnant women</strong>. Without exception these were the most nutrient-dense foods available:</p>
<ul>
  <li>Fish roe (eggs) &mdash; extraordinarily rich in DHA, zinc, B12, vitamin D and choline</li>
  <li>Liver and organ meats &mdash; the richest source of folate, B12, iron, zinc, and vitamin A</li>
  <li>Bone marrow &mdash; fat-soluble vitamins, collagen precursors</li>
  <li>Shellfish &mdash; zinc (oysters are the richest food source), iodine, selenium, omega-3</li>
  <li>Grass-fed dairy &mdash; vitamin K2 (Activator X), fat-soluble vitamins</li>
</ul>
<p>Price found that couples fed these foods for 6+ months before conception had children with exceptional bone structure, dental arch width, and resistance to tuberculosis. He was observing epigenetics decades before the science existed to explain it.</p>

<h2>What to avoid in the pre-conception period</h2>
<div class="warning-box">
  <h3>Both partners &mdash; 3+ months before conception</h3>
  <ul>
    <li><strong>Alcohol</strong> &mdash; damages sperm DNA and disrupts female hormone balance. Even moderate intake affects conception rates and early foetal development.</li>
    <li><strong>Smoking</strong> &mdash; reduces sperm quality and female ovarian reserve significantly.</li>
    <li><strong>Ultra-processed foods high in trans fats</strong> &mdash; trans fats reduce sperm quality and are associated with ovulatory infertility.</li>
    <li><strong>Extreme caloric restriction or overweight</strong> &mdash; both impair fertility. Gradual movement toward a healthy weight before conception is beneficial.</li>
  </ul>
</div>
<div class="warning-box">
  <h3>Female partner &mdash; once trying to conceive</h3>
  <ul>
    <li><strong>Liver (first trimester)</strong> &mdash; very high preformed vitamin A can be teratogenic at high doses. Limit liver to 1&times;/week during pre-conception and avoid in the first trimester.</li>
    <li><strong>High-mercury fish</strong> &mdash; shark (flake), swordfish, marlin, orange roughy. Limit to once a fortnight. Safe: sardines, salmon, tuna (2&ndash;3&times;/week).</li>
  </ul>
</div>

<h2>Folate: the non-negotiable for every reproductive-age woman</h2>
<p>Neural tube closure &mdash; the formation of the brain and spinal cord &mdash; occurs between <strong>days 21&ndash;28 of gestation</strong>. At this point, most women do not yet know they are pregnant. Folate deficiency during this window causes spina bifida and anencephaly, which are among the most preventable birth defects.</p>
<p><strong>The recommendation is clear and universal:</strong> every woman of reproductive age who could conceive should take 400&ndash;800 mcg of folic acid daily. Not after a positive pregnancy test &mdash; <em>all the time, continuously</em>. No exceptions.</p>
<p>Food folate sources (to supplement, not replace, a folic acid tablet):</p>
<ul>
  <li>1 cup cooked lentils &mdash; ~360 mcg (60% of non-pregnant RDI)</li>
  <li>1 cup frozen spinach &mdash; ~263 mcg</li>
  <li>1 cup cooked chickpeas &mdash; ~282 mcg</li>
  <li>2 eggs &mdash; ~47 mcg</li>
</ul>

<div class="cta-box">
  <h2>Track pre-conception nutrition for free</h2>
  <p>Set up a profile for each partner in the app &mdash; it calculates exact targets for folate, zinc, DHA, iron and all other key pre-conception nutrients and shows how your daily meals measure up.</p>
  <a class="cta-btn" href="/">Open the free app</a>
</div>
"""

p = BASE / "pre-conception"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "Pre-Conception Nutrition for Both Partners | OptimisedEats",
    "Nutrition for both partners before conception matters enormously. Zinc for sperm, folate for neural tubes, DHA for brain development — the evidence and the cheapest foods to act on it.",
    "pre-conception nutrition Australia, fertility nutrition both partners, male fertility nutrition, folate pre-conception, zinc fertility, DHA sperm",
    "Pre-Conception", "/guide/pre-conception/",
    precon_body,
    other_related("/guide/pre-conception/")
), encoding="utf-8")
print("DONE guide/pre-conception/index.html")


# =============================================================================
# PAGE 2: WHAT DEFICIENCIES ACTUALLY DO TO YOU
# =============================================================================

deficiency_body = """
<h1>What Nutrient Deficiencies Actually Do to You</h1>
<p class="lead">Numbers on a nutrition label don't feel urgent. These do. Here's what falling short on the most common Australian nutritional gaps actually looks like &mdash; from the first subtle signs to the full clinical picture.</p>

<div class="callout">
  <strong>Most deficiencies develop silently.</strong> By the time obvious symptoms appear, you&rsquo;ve typically been deficient for months. The early stages &mdash; where damage is already occurring &mdash; often feel like ordinary tiredness, stress, or aging.
</div>

<div class="nutrient-section">
<h2>Iron deficiency &mdash; affects 47% of Australian women aged 18&ndash;29</h2>
<p>Iron deficiency is the world's most common nutritional deficiency. It progresses in stages, and most women are told their blood test is &ldquo;normal&rdquo; even at Stage 1.</p>

<div class="stage-bar">
  <div class="stage stage-1">
    <strong>Stage 1 &mdash; Depleted stores</strong>
    Ferritin below 30 mcg/L. Haemoglobin still normal &mdash; often dismissed as &ldquo;fine.&rdquo; Brain function measurably impaired. Persistent fatigue. Reduced exercise tolerance. Poor temperature regulation. Difficulty concentrating.
  </div>
  <div class="stage stage-2">
    <strong>Stage 2 &mdash; Iron-deficient erythropoiesis</strong>
    Worsening fatigue and pallor. Headaches. Irritability. Restless legs at night. Reduced immunity (frequent colds). Hair begins thinning noticeably. Difficulty concentrating worsens.
  </div>
  <div class="stage stage-3">
    <strong>Stage 3 &mdash; Iron deficiency anaemia</strong>
    Breathlessness on exertion. Heart palpitations. Cold intolerance. Brittle, spoon-shaped nails. Cracking at corners of the mouth. Smooth, painful tongue. Significant cognitive impairment: processing speed, verbal memory, attention all affected.
  </div>
</div>

<div class="callout-red">
  <strong>The ferritin gap:</strong> Standard blood tests check haemoglobin. Ferritin (your iron stores) can be critically low while haemoglobin remains normal. Ask specifically for a <em>ferritin</em> test. Levels below 30 mcg/L are associated with measurable cognitive impairment even when haemoglobin is normal. Many GPs use a lower threshold of 12&ndash;15 mcg/L as their &ldquo;deficient&rdquo; cutoff &mdash; which misses many women who are functionally iron-depleted.
</div>

<h3>Iron deficiency in pregnancy &mdash; the stakes are highest here</h3>
<p>The foetal brain is iron-avid in the third trimester &mdash; this is the developmental window that cannot be recovered. Iron deficiency during pregnancy is linked to:</p>
<ul>
  <li>Premature birth and low birth weight</li>
  <li>Impaired foetal hippocampus development (the brain's memory centre)</li>
  <li>Lasting cognitive deficits in the child that persist into adolescence <em>even after iron is repleted</em></li>
  <li>Postpartum depression in the mother</li>
</ul>
<p>Iron requirements nearly double in pregnancy to 27 mg/day. Women who enter pregnancy already iron-depleted have almost no buffer.</p>
<p><strong>Cheapest iron-rich foods:</strong> Lentils (6.6 mg/cup, ~$0.20) &bull; Kangaroo mince (3.5&ndash;7 mg/100g, ~$1.00) &bull; Spinach cooked (3.6 mg/cup, ~$0.30) &bull; Always pair plant iron with vitamin C to triple absorption. Avoid tea/coffee within 1 hour of iron-rich meals.</p>
</div>

<div class="nutrient-section">
<h2>Vitamin D deficiency &mdash; 21% of Australian adults deficient</h2>
<p>Despite living in one of the sunniest countries on earth, vitamin D deficiency is widespread in Australia due to indoor work, sunscreen use, and southern latitude winters. Vitamin D is actually a hormone &mdash; it regulates over 1,000 genes directly.</p>

<div class="impact-box">
  <div class="impact-icon">🧠</div>
  <div><strong>Mental health:</strong> Vitamin D deficiency is one of the most consistent nutritional correlates of depression and seasonal affective disorder. Vitamin D directly modulates serotonin synthesis and brain-derived neurotrophic factor (BDNF) &mdash; a protein essential for forming new brain connections. Supplementation in deficient individuals shows measurable improvement in depressive symptoms.</div>
</div>
<div class="impact-box">
  <div class="impact-icon">🛡️</div>
  <div><strong>Immune system:</strong> Vitamin D receptors are present on virtually every immune cell. Deficiency increases susceptibility to respiratory infections, is strongly associated with autoimmune conditions (multiple sclerosis, type 1 diabetes, rheumatoid arthritis, inflammatory bowel disease), and correlates with increased all-cause cancer mortality.</div>
</div>
<div class="impact-box">
  <div class="impact-icon">🤰</div>
  <div><strong>Pregnancy:</strong> Deficiency is linked to pre-eclampsia, gestational diabetes, increased C-section rate, impaired foetal skeletal development, and low birth weight. Children born to vitamin D-deficient mothers have higher rates of asthma, schizophrenia, and type 1 diabetes.</div>
</div>
<div class="impact-box">
  <div class="impact-icon">🦴</div>
  <div><strong>Bones:</strong> Severe deficiency causes rickets in children (bowed legs, soft skull, delayed tooth eruption) and osteomalacia in adults (bone pain, muscle weakness). Subclinical deficiency accelerates osteoporosis silently over decades.</div>
</div>

<div class="highlight-box">
  <h3>&#9728;&#65039; The mushroom hack</h3>
  <p>Place button mushrooms <strong>gill-side up</strong> in direct sunlight for 30&ndash;60 minutes before use. Mushrooms synthesise vitamin D just like human skin does &mdash; and the vitamin D persists even after cooking. A 100g serve can deliver 400+ IU (67% of the adult RDI) for around 50 cents. Leave a punnet out every time you buy them.</p>
  <p><strong>UV index must be 3+</strong> for synthesis to occur &mdash; in mushrooms or humans. In Victoria and NZ between May and August, the UV index rarely reaches 3 even at midday. During these months, food sources and supplementation (1,000&ndash;2,000 IU vitamin D3/day) become essential.</p>
  <p><strong>Sunscreen note:</strong> SPF 30+ sunscreen reduces vitamin D synthesis by ~95&ndash;99%. This is the right trade-off for skin cancer prevention &mdash; but it means many Australians who apply sunscreen daily need dietary or supplemental vitamin D year-round, not just in winter.</p>
</div>
</div>

<div class="nutrient-section">
<h2>Folate deficiency &mdash; every reproductive-age woman is at risk</h2>
<p>Folate is required for DNA synthesis, cell division, and the methylation reactions that control gene expression. The most catastrophic consequence is neural tube defects, but folate deficiency has wider effects at all ages.</p>

<div class="impact-box">
  <div class="impact-icon">🧬</div>
  <div><strong>Neural tube defects (pregnancy):</strong> Neural tube closure occurs days 21&ndash;28 of gestation &mdash; before most women know they are pregnant. Folate deficiency at this moment causes spina bifida and anencephaly. Adequate folate prevents up to 70% of neural tube defects. <em>Every woman of reproductive age who could conceive should supplement 400&ndash;800 mcg/day, all the time.</em></div>
</div>
<div class="impact-box">
  <div class="impact-icon">🩸</div>
  <div><strong>Megaloblastic anaemia:</strong> Without folate, red blood cells can't divide properly. They become abnormally large and few &mdash; megaloblastic anaemia. Symptoms: fatigue, weakness, shortness of breath, pale skin, mouth sores, and a smooth painful tongue (identical presentation to B12 deficiency &mdash; always test both).</div>
</div>
<div class="impact-box">
  <div class="impact-icon">❤️</div>
  <div><strong>Cardiovascular disease:</strong> Folate (along with B6 and B12) regulates homocysteine, an amino acid that damages blood vessel walls at elevated levels. Low folate &rarr; high homocysteine &rarr; increased risk of heart attack and stroke.</div>
</div>

<p><strong>Cheapest folate sources:</strong> 1 cup cooked lentils (~360 mcg, $0.20) &bull; 1 cup chickpeas (~282 mcg, $0.20) &bull; 1 cup frozen spinach (~263 mcg, $0.30) &bull; 1 cup broccoli (~168 mcg, $0.40)</p>
</div>

<div class="nutrient-section">
<h2>DHA (Omega-3) deficiency</h2>
<p>DHA makes up 40% of the polyunsaturated fat in the human brain. It is the primary structural fat of the foetal brain and retina. Most Australians eat far less than recommended.</p>

<div class="impact-box">
  <div class="impact-icon">🧠</div>
  <div><strong>Brain structure and cognition:</strong> Inadequate DHA impairs neuronal membrane fluidity, reduces synapse formation, and is associated with cognitive decline and increased risk of Alzheimer's disease. Long-term low omega-3 intake is a meaningful, modifiable dementia risk factor.</div>
</div>
<div class="impact-box">
  <div class="impact-icon">😔</div>
  <div><strong>Mental health:</strong> Low omega-3 intake is associated with depression, anxiety, bipolar disorder, and ADHD. Multiple clinical trials show EPA (a related omega-3) has antidepressant effects comparable to medication in mild-to-moderate depression. Postpartum depression rates are significantly higher in countries with low seafood consumption.</div>
</div>
<div class="impact-box">
  <div class="impact-icon">🤰</div>
  <div><strong>Pregnancy and infant development:</strong> The third trimester is the period of most rapid foetal brain growth &mdash; DHA demand peaks exactly then. Maternal DHA deficiency is associated with lower infant IQ, poorer visual acuity, and higher rates of postpartum depression in the mother (whose stores are depleted to provision the baby).</div>
</div>

<p><strong>Cheapest DHA sources:</strong> Sardines (~1,000&ndash;1,500 mg omega-3/tin, $1.50) &bull; Canned salmon (~1,500 mg/100g, $2.00) &bull; Omega-3 enriched eggs (~300 mg each, ~$0.80) &bull; The target for pregnant and breastfeeding women is 200+ mg DHA/day &mdash; one tin of sardines per week exceeds this easily.</p>
</div>

<div class="nutrient-section">
<h2>Zinc deficiency (especially in men)</h2>
<p>Zinc is involved in over 300 enzymatic reactions. It is essential for immune function, wound healing, testosterone production, taste and smell, protein synthesis, and DNA repair.</p>

<div class="impact-box">
  <div class="impact-icon">&#9794;&#65039;</div>
  <div><strong>Male fertility:</strong> Zinc is essential for testosterone production and sperm development. Zinc deficiency directly reduces sperm count, motility, and morphology. In women, zinc deficiency disrupts ovulation and is associated with PCOS. 48% of Australian men fail to meet the zinc RDI (14 mg/day) &mdash; one of the highest shortfall rates of any nutrient.</div>
</div>
<div class="impact-box">
  <div class="impact-icon">🤒</div>
  <div><strong>Immune function:</strong> Zinc deficiency impairs development and function of immune cells. People with low zinc have impaired wound healing, increased susceptibility to infections, and longer illness duration. Even mild deficiency reduces the body's ability to fight infections.</div>
</div>
<div class="impact-box">
  <div class="impact-icon">👃</div>
  <div><strong>Taste and smell:</strong> Zinc is directly required for taste bud and olfactory receptor function. Mild zinc deficiency causes hypogeusia (reduced taste acuity) and hyposmia (reduced smell) &mdash; often attributed to aging but frequently nutritional. This can lead to poorer food choices as food becomes less pleasurable.</div>
</div>
<div class="impact-box">
  <div class="impact-icon">🤰</div>
  <div><strong>Pregnancy:</strong> Zinc deficiency in the first trimester is associated with neural tube defects, cleft palate, foetal growth restriction, and premature birth.</div>
</div>

<p><strong>Cheapest zinc sources:</strong> Beef mince (8 mg/100g, $1.00) &bull; Kangaroo mince (6.5 mg/100g, $1.00) &bull; Pumpkin seeds (2.2 mg/30g, $0.30) &bull; Lentils (2.5 mg/cup, $0.20) &bull; Soak legumes overnight to reduce phytates and roughly double zinc absorption.</p>
</div>

<div class="nutrient-section">
<h2>Magnesium deficiency &mdash; 31% of adults fall short</h2>
<p>Magnesium is involved in over 300 enzymatic processes. Its deficiency is largely invisible on standard tests because blood magnesium is tightly maintained even when tissue magnesium is low.</p>

<div class="impact-box">
  <div class="impact-icon">😴</div>
  <div><strong>Sleep:</strong> Magnesium activates the parasympathetic nervous system (rest-and-digest) and regulates melatonin. Low magnesium is strongly associated with insomnia, poor sleep quality, and frequent night waking. Supplementation improves sleep onset and quality in deficient individuals, particularly older adults.</div>
</div>
<div class="impact-box">
  <div class="impact-icon">😰</div>
  <div><strong>Anxiety and stress response:</strong> Magnesium modulates the hypothalamic-pituitary-adrenal (HPA) axis &mdash; the stress response system. Chronic stress depletes magnesium, and low magnesium amplifies the stress response, creating a vicious cycle. Low magnesium is consistently found in people with anxiety disorders.</div>
</div>
<div class="impact-box">
  <div class="impact-icon">💪</div>
  <div><strong>Muscle cramps and weakness:</strong> Magnesium is required for muscle relaxation (calcium causes contraction, magnesium causes relaxation). Deficiency causes muscle cramps, spasms, tremors, and general muscle weakness. Night cramps are frequently a magnesium deficiency symptom.</div>
</div>
<div class="impact-box">
  <div class="impact-icon">🩺</div>
  <div><strong>Blood sugar and metabolic health:</strong> Magnesium is a cofactor for insulin receptor signalling. Low magnesium is associated with insulin resistance, metabolic syndrome, and type 2 diabetes. Even modest increases in magnesium intake are associated with reduced diabetes risk in population studies.</div>
</div>

<p><strong>Cheapest magnesium sources:</strong> Pumpkin seeds (160 mg/30g, $0.30) &bull; Spinach cooked (157 mg/cup, $0.30) &bull; Black beans (120 mg/cup, $0.20) &bull; Brown rice (84 mg/cup, $0.15) &bull; The simplest daily fix: 30g pumpkin seeds on morning oats + 1 cup spinach at dinner = ~317 mg.</p>
</div>

<div class="nutrient-section">
<h2>Iodine deficiency</h2>
<p>Australia's soils are among the most iodine-poor in the world. Iodine is essential for thyroid hormone production, which regulates metabolism, energy, temperature, and &mdash; critically &mdash; foetal brain development.</p>

<div class="impact-box">
  <div class="impact-icon">🧠</div>
  <div><strong>Brain development (pregnancy):</strong> Iodine deficiency is the world's leading preventable cause of intellectual disability. Even mild deficiency during pregnancy reduces child IQ by 8&ndash;16 points on average. The effect is irreversible. Requirement increases from 150 to 220 mcg/day during pregnancy.</div>
</div>
<div class="impact-box">
  <div class="impact-icon">⚡</div>
  <div><strong>Thyroid and metabolism:</strong> Low iodine &rarr; low thyroid hormone &rarr; fatigue, weight gain, cold intolerance, hair loss, dry skin, constipation, brain fog. These symptoms often mimic depression and are frequently misattributed. A swollen thyroid (goitre) is the visible sign of prolonged iodine deficiency.</div>
</div>

<p><strong>Simple fix:</strong> Switch to iodised salt (not sea salt, not Himalayan &mdash; these are not iodised). Add seafood and dairy. During pregnancy, supplement 150 mcg/day iodine (check your prenatal multivitamin contains it).</p>
</div>

<div class="cta-box">
  <h2>Find out where your gaps are</h2>
  <p>The app tracks your daily intake of all these nutrients across your household &mdash; and highlights when you&rsquo;re consistently falling short, with meal suggestions to fill the gap.</p>
  <a class="cta-btn" href="/">Open the free app</a>
</div>
"""

p = BASE / "deficiency-symptoms"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "What Nutrient Deficiencies Actually Do to You | OptimisedEats",
    "Iron deficiency stages, vitamin D and depression, DHA and postpartum depression, zinc and male fertility — what falling short on Australia's most common nutrient gaps actually looks like.",
    "nutrient deficiency symptoms Australia, iron deficiency stages, vitamin D deficiency effects, zinc deficiency men, folate deficiency pregnancy, magnesium deficiency symptoms",
    "Deficiency Symptoms", "/guide/deficiency-symptoms/",
    deficiency_body,
    other_related("/guide/deficiency-symptoms/")
), encoding="utf-8")
print("DONE guide/deficiency-symptoms/index.html")


# =============================================================================
# PAGE 3: DISCLAIMER — NOTE FROM THE AUTHOR
# =============================================================================

disclaimer_body = """
<h1>Disclaimer &mdash; Note from the Author</h1>
<p class="lead">OptimisedEats was built by a researcher, not a dietitian. Here&rsquo;s what that means for how you should use this information.</p>

<div class="nutrient-section">
<h2>About this project</h2>
<p>My name is Chris. I&rsquo;m not a dietitian, doctor, or registered health professional. I&rsquo;m a researcher who spent hundreds of hours working through the peer-reviewed literature on nutrition science, Australian dietary surveys, and the economics of food.</p>
<p>OptimisedEats grew out of a personal project to understand how to feed a household well &mdash; particularly families with children, pregnant women, and people on limited budgets &mdash; without overspending or relying on expensive supplements or proprietary diet programs.</p>
<p>The result is what you see here: a free app, a set of evidence-based guides, and a recipe index &mdash; all grounded in publicly available research and Australian supermarket pricing.</p>
</div>

<div class="nutrient-section">
<h2>What this is &mdash; and what it isn&rsquo;t</h2>
<div class="callout-red">
  <strong>Not medical advice.</strong> Nothing on this website or in the app is a substitute for personalised advice from a qualified health professional. If you have a medical condition, are pregnant, or are considering significant dietary changes, consult your GP, midwife, dietitian, or specialist.
</div>
<p>This site provides <strong>general nutrition education</strong> based on publicly available Australian and international dietary guidelines. It is intended to:</p>
<ul>
  <li>Help people understand nutrient reference values and where common gaps occur in Australian diets</li>
  <li>Suggest affordable, nutrient-dense foods and recipes</li>
  <li>Provide context around life-stage nutrition (pregnancy, infancy, ageing)</li>
  <li>Make evidence-based nutrition information accessible to people without a health science background</li>
</ul>
<p>It is <strong>not</strong> intended to diagnose deficiencies, treat any medical condition, or replace individualised dietary assessment. Nutrient needs vary significantly between individuals based on genetics, health history, medications, absorption capacity, and many other factors that a general tool cannot account for.</p>
</div>

<div class="nutrient-section">
<h2>Sources and methodology</h2>
<p>All nutrient targets in the app and guides are drawn from authoritative public sources:</p>
<ul>
  <li><strong>NHMRC Nutrient Reference Values (NRVs)</strong> &mdash; Australian and New Zealand reference intakes for all nutrients, published by the National Health and Medical Research Council. The primary source for all RDI, AI, UL, and EAR values used in this tool.</li>
  <li><strong>Australian Bureau of Statistics (ABS)</strong> &mdash; National Nutrition and Physical Activity Survey data on actual dietary intake across Australian demographics.</li>
  <li><strong>USDA FoodData Central</strong> &mdash; Nutrient composition data for individual foods, used where Australian databases have gaps.</li>
  <li><strong>IOM / NASEM (Institute of Medicine / National Academies)</strong> &mdash; Dietary Reference Intakes used for cross-referencing, particularly for nutrients where Australian and US guidance aligns.</li>
  <li><strong>Peer-reviewed literature</strong> &mdash; Studies on absorption rates, nutrient interactions (e.g. tannins and iron, Vit C and iron absorption), and specific life-stage requirements cited throughout the guides.</li>
</ul>
<p>Food costs are based on current pricing at Coles, Woolworths, and Aldi in Australia. Prices are approximate and vary by store, region, and season. All costs are per-serve unless stated.</p>
</div>

<div class="nutrient-section">
<h2>Accuracy and updates</h2>
<p>I&rsquo;ve made every effort to ensure the information is accurate and aligned with current Australian dietary guidelines. Nutrition science does evolve, and recommendations are updated periodically &mdash; if you notice something that appears outdated or incorrect, please get in touch.</p>
<p>The app&rsquo;s nutrient tracking is a <strong>guide</strong>, not a precise measurement. Nutrient content in food varies with preparation method, ripeness, storage, and individual variation. The figures should be treated as useful approximations, not clinical measurements.</p>
</div>

<div class="nutrient-section">
<h2>Intellectual property</h2>
<p>All written content, code, recipe development, and nutritional analysis presented on OptimisedEats is original work. It has been developed independently through personal research and is protected by Australian copyright law.</p>
<p>You are welcome to share links to these guides. You may quote short passages for educational or journalistic purposes with attribution. Please do not republish substantial portions of this content without permission.</p>
<p>The OptimisedEats app code is proprietary. The nutritional guides are free for personal and educational use.</p>
</div>

<div class="callout">
  <strong>In summary:</strong> Use this as a starting point, not an endpoint. This tool is designed to help you ask better questions and make more informed choices &mdash; not to replace the professional relationships that matter for your health.
</div>

<div class="cta-box">
  <h2>Back to the nutrition guides</h2>
  <p>Explore evidence-based guides on every life stage, common nutrient gaps, and budget meal planning.</p>
  <a class="cta-btn" href="/guide/">All guides</a>
</div>
"""

p = BASE / "disclaimer"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "Disclaimer &mdash; Note from the Author | OptimisedEats",
    "OptimisedEats is built by a researcher, not a dietitian. Read about the sources, methodology, limitations, and intellectual property terms for this free nutrition tool.",
    "OptimisedEats disclaimer, nutrition information sources, NHMRC dietary guidelines, not medical advice, budget nutrition research",
    "Disclaimer", "/guide/disclaimer/",
    disclaimer_body,
    other_related("/guide/disclaimer/")
), encoding="utf-8")
print("DONE guide/disclaimer/index.html")


# =============================================================================
# PAGE 4: HIDDEN HUNGER — ULTRA-PROCESSED FOODS AND CHILDREN
# =============================================================================

hidden_hunger_body = """
<h1>Hidden Hunger: How Ultra-Processed Foods Are Starving Children of Nutrients</h1>
<p class="lead">Australia&rsquo;s children are not starving for calories. They are starving for everything else. This is the defining nutrition crisis of the modern era &mdash; and the science is now clear on exactly what it does to developing brains and bodies.</p>

<div class="callout-red">
  <strong>Hidden Hunger defined:</strong> A state where children are overfed on energy (calories) but severely deficient in the vitamins and minerals their brains and bodies require. Processed food fills the stomach while emptying the nutrient profile.
</div>

<div class="nutrient-section">
<h2>What the research actually shows</h2>
<p>Three landmark studies have now quantified exactly what ultra-processed food (UPF) does to children&rsquo;s nutrient status. The numbers are striking.</p>

<div class="impact-box">
  <div class="impact-icon">&#x26A0;&#xFE0F;</div>
  <div>
    <strong>2.57&times; higher risk of multiple deficiencies (The SENDO Project, 2023)</strong><br>
    A large pediatric cohort study (mean age 5 years) found that children with the highest UPF consumption had <strong>2.57 times higher odds of being inadequate in 3 or more essential micronutrients simultaneously</strong> compared to children eating minimally processed diets. The proportion of children suffering multiple nutrient inadequacies jumped from 23% on whole-food diets to 35% on high-processed diets &mdash; a 52% relative increase. This is not a marginal effect.
    <div class="nrv-note">Garc&iacute;a-Blanco et al. (2023). European Journal of Pediatrics, 182(8), 3537&ndash;3547.</div>
  </div>
</div>

<div class="impact-box">
  <div class="impact-icon">&#x1F4CA;</div>
  <div>
    <strong>16 out of 17 key micronutrients lower in processed foods</strong><br>
    A comprehensive nutritional evaluation tracking dietary fractions found that 16 of 17 key micronutrients evaluated were significantly lower in ultra-processed formulations compared to natural alternatives. More alarming: the content of 10 of those micronutrients in processed foods <strong>failed to reach even half the level found in whole foods</strong>. The depleted nutrients include Vitamin B12, Vitamin D, Vitamin E, niacin, pyridoxine, copper, iron, phosphorus, magnesium, selenium, and zinc.
    <div class="nrv-note">Louzada et al. (2015). Revista de Sa&uacute;de P&uacute;blica, 49, 1&ndash;8. Cited 411 times.</div>
  </div>
</div>

<div class="impact-box">
  <div class="impact-icon">&#x1F9EA;</div>
  <div>
    <strong>Zinc, B12 and fibre: the consistent casualties</strong><br>
    Global evaluations of children&rsquo;s diets confirm that a higher reliance on modern convenience foods consistently drives severe drops in zinc, vitamin B12, and dietary fibre across all demographics studied &mdash; regardless of income level or country.
    <div class="nrv-note">Morais et al. (2024). Children, 11(9), 1089.</div>
  </div>
</div>
</div>

<div class="nutrient-section">
<h2>Why parents can&rsquo;t just &ldquo;make better choices&rdquo;</h2>
<p>Modern processed foods are engineered to override normal appetite regulation. Understanding this is essential before judging any parent struggling with a child who will only eat beige food.</p>

<div class="impact-box">
  <div class="impact-icon">&#x1F9E0;</div>
  <div>
    <strong>Dopaminergic hijacking</strong><br>
    The precise combinations of high fat and refined sugar in commercial children&rsquo;s snacks trigger &ldquo;supra-additive&rdquo; mid-brain dopamine firing. This overstimulates reward pathways and rapidly shifts a child&rsquo;s eating behaviour from goal-directed (eating when hungry) to habitual and cue-triggered &mdash; the same neurological mechanism underlying addiction. The child isn&rsquo;t being difficult. Their reward system has been captured.
    <div class="nrv-note">The consequences of ultra-processed foods on brain development during prenatal, adolescent and adult stages. (2025). Frontiers in Public Health, 13, Article 1590083.</div>
  </div>
</div>

<div class="impact-box">
  <div class="impact-icon">&#x1F4C9;</div>
  <div>
    <strong>Measurable cognitive decline</strong><br>
    In pediatric cohorts, every <strong>10% increase in daily energy from ultra-processed foods predicted a significant decline in composite executive function scores</strong> &mdash; independently of the child&rsquo;s socioeconomic status or BMI. This includes working memory, impulse control, and attention. These are the skills required for learning. The diet is directly shaping the capacity to learn.
    <div class="nrv-note">Frontiers in Public Health, 2025.</div>
  </div>
</div>

<div class="impact-box">
  <div class="impact-icon">&#x1F372;</div>
  <div>
    <strong>Sensory homogeneity and ARFID</strong><br>
    Processed foods are manufactured to possess perfect sensory consistency &mdash; the same uniform texture, crunch, flavour, and colour every single time. Real foods (fruit, vegetables, meat) vary naturally. This industrial uniformity trains children to expect and demand predictability, and can trigger or worsen <strong>Avoidant/Restrictive Food Intake Disorder (ARFID)</strong>: a genuine clinical feeding disorder where children become so sensitised to sensory variation that whole-food textures trigger distress responses. Children become locked into nutrient-barren foods &mdash; not because parents failed, but because neurological sensitisation was allowed to develop unchallenged.
    <div class="nrv-note">Frontiers in Public Health, 2025.</div>
  </div>
</div>
</div>

<div class="nutrient-section">
<h2>The four nutrients most depleted &mdash; and what that looks like in a child</h2>

<div class="partner-grid">
  <div class="partner-card partner-female">
    <h3>&#x1F9B7; Zinc</h3>
    <p><strong>Why it&rsquo;s stripped:</strong> Refining removes zinc from grains; phytates in processed foods bind what little remains, blocking absorption.</p>
    <p><strong>What it looks like:</strong> Slowed growth, frequent infections that take too long to clear, poor wound healing, short attention spans, and irritability. Zinc deficiency is functionally invisible on a blood panel until it&rsquo;s severe &mdash; subclinical depletion affects cognition first.</p>
  </div>
  <div class="partner-card partner-male">
    <h3>&#x1F4A1; Vitamin B12</h3>
    <p><strong>Why it&rsquo;s stripped:</strong> Processed diets replace bioavailable animal proteins with refined carbohydrates and plant oils that contain no B12 whatsoever.</p>
    <p><strong>What it looks like:</strong> Developmental delays, macrocytic anaemia, unexplained fatigue, neurological irritability or apathy in toddlers. B12 is essential for myelin sheath formation &mdash; the insulation around nerve fibres. Deficiency in early childhood can cause permanent neurological damage.</p>
  </div>
  <div class="partner-card" style="border-top:3px solid #f59e0b">
    <h3>&#x26A1; Magnesium &amp; B-Vitamins</h3>
    <p><strong>Why it&rsquo;s stripped:</strong> Processing removes B vitamins from grains. Worse: high refined sugar intake forces the body to burn through internal magnesium and B-vitamin stores just to metabolise the glucose load.</p>
    <p><strong>What it looks like:</strong> Neurotransmitter dysregulation &mdash; emotional instability, severe mood swings, heightened anxiety, and disrupted sleep. The same child whose diet is causing deficiencies is often the child described as &ldquo;difficult&rdquo; or &ldquo;emotional&rdquo;.
    <div class="nrv-note" style="margin-top:8px">Ultra-Processed Foods and Mental Health in Children and Adolescents. (2024). Nutrients, 16(6), 899.</div></p>
  </div>
  <div class="partner-card" style="border-top:3px solid #3b82f6">
    <h3>&#x2600;&#xFE0F; Vitamin D &amp; Calcium</h3>
    <p><strong>Why it&rsquo;s stripped:</strong> Sugary juices, flavoured drinks, and snack foods displace fortified dairy and whole-food calcium sources entirely.</p>
    <p><strong>What it looks like:</strong> Weakened dental enamel, delayed teething, poor bone density maturation during the critical window of skeletal development. The consequences are structural and lifelong &mdash; peak bone mass is set in childhood and adolescence.</p>
  </div>
</div>
</div>

<div class="nutrient-section">
<h2>This starts before birth &mdash; and before conception</h2>
<p>The Hidden Hunger problem does not begin when a child starts eating solids. It begins in the womb &mdash; and arguably before conception.</p>
<div class="callout">
  <strong>Epigenetic programming:</strong> The Dutch Hunger Winter studies and subsequent research demonstrate that a mother&rsquo;s nutritional status during pregnancy epigenetically programs a child&rsquo;s metabolic and appetite-regulating systems. A child born to a micronutrient-depleted mother faces a higher baseline risk of metabolic dysfunction and altered food preferences &mdash; before they ever taste a processed food.
</div>
<p>Flavour preferences are also established in utero through amniotic fluid. Mothers who eat a varied, whole-food diet during pregnancy expose their babies to a broader flavour profile &mdash; making them statistically more accepting of vegetables and varied textures after weaning. Mothers eating a processed-food-dominant diet do the opposite.</p>
<p>This is why the pre-conception and pregnancy nutrition period is not separate from the Hidden Hunger question &mdash; it is the first chapter of it.</p>
<p><a href="/guide/pre-conception/" style="color:#16a34a;font-weight:700">Read: Pre-Conception Nutrition &mdash; Both Partners &rarr;</a></p>
</div>

<div class="nutrient-section">
<h2>What actually works &mdash; practical steps</h2>
<p>Understanding the neuroscience points to specific, evidence-informed strategies rather than generic &ldquo;eat less junk food&rdquo; advice:</p>
<ul>
  <li><strong>Repeated exposure without pressure:</strong> Research consistently shows 10&ndash;15 non-coercive exposures are needed before a child accepts a novel food. One refusal is not rejection &mdash; it is the normal starting point.</li>
  <li><strong>Variety from the start:</strong> Introduce textural variety from the beginning of solids (around 6 months). The sensory homogeneity window that enables ARFID is narrowest in infancy.</li>
  <li><strong>Replace, don&rsquo;t just remove:</strong> Removing processed food without replacing its palatability creates conflict. Whole-food versions of the same flavour profiles (e.g., fruit-based sweetness, umami from cheese or meat, crunch from nuts/seeds) ease the neurological transition.</li>
  <li><strong>Prioritise the depleted four:</strong> Zinc-rich foods (meat, legumes, pumpkin seeds), B12 sources (eggs, dairy, meat), magnesium-dense foods (dark leafy greens, nuts), and daily Vitamin D exposure or supplementation through winter.</li>
  <li><strong>The UPF budget reality:</strong> Gram for gram, whole foods are almost always cheaper per nutrient than processed alternatives. A tin of sardines provides more zinc, B12, calcium, and omega-3 than a week of crackers and flavoured cheese for a fraction of the cost. The &ldquo;healthy food is expensive&rdquo; narrative is a marketing construct, not a nutritional reality.</li>
</ul>
<p><a href="/guide/kids/" style="color:#16a34a;font-weight:700">Read: Kids &amp; Toddlers Nutrition Guide &rarr;</a><br>
<a href="/guide/budget-basics/" style="color:#16a34a;font-weight:700">Read: Budget Nutrition Basics &rarr;</a></p>
</div>

<div class="nutrient-section">
<h2>References</h2>
<p style="font-size:13px;line-height:1.8;color:#475569">
Garc&iacute;a-Blanco, L., de la O, V., Santiago, S., Pouso, A., Mart&iacute;nez-Gonz&aacute;lez, M. &Aacute;., &amp; Mart&iacute;n-Calvo, N. (2023). High consumption of ultra-processed foods is associated with increased risk of micronutrient inadequacy in children: The SENDO project. <em>European Journal of Pediatrics</em>, 182(8), 3537&ndash;3547. <a href="https://doi.org/10.1007/s00431-023-05026-9" target="_blank" rel="noopener noreferrer" style="color:#16a34a">doi:10.1007/s00431-023-05026-9</a> (Cited 40&times;)<br><br>
Louzada, M. L. da C., et al. (2015). Impact of ultra-processed foods on micronutrient content in the Brazilian diet. <em>Revista de Sa&uacute;de P&uacute;blica</em>, 49, 1&ndash;8. <a href="https://doi.org/10.1590/s0034-8910.2015049006211" target="_blank" rel="noopener noreferrer" style="color:#16a34a">doi:10.1590/s0034-8910.2015049006211</a> (Cited 411&times;)<br><br>
Morais, R., et al. (2024). Ultra-processed foods and nutritional intake of children and adolescents. <em>Children</em>, 11(9), 1089. <a href="https://doi.org/10.3390/children11091089" target="_blank" rel="noopener noreferrer" style="color:#16a34a">doi:10.3390/children11091089</a><br><br>
The consequences of ultra-processed foods on brain development during prenatal, adolescent and adult stages. (2025). <em>Frontiers in Public Health</em>, 13, Article 1590083. <a href="https://doi.org/10.3389/fpubh.2025.1590083" target="_blank" rel="noopener noreferrer" style="color:#16a34a">doi:10.3389/fpubh.2025.1590083</a><br><br>
Ultra-processed foods and mental health in children and adolescents: Evidence from a systematic review. (2024). <em>Nutrients</em>, 16(6), 899. <a href="https://doi.org/10.3390/nu16060899" target="_blank" rel="noopener noreferrer" style="color:#16a34a">doi:10.3390/nu16060899</a>
</p>
</div>

<div class="cta-box">
  <h2>Track what your kids are actually getting</h2>
  <p>Add your children to the free app and see their daily nutrient coverage against age-specific Australian targets &mdash; including zinc, B12, magnesium, calcium and Vitamin D.</p>
  <a class="cta-btn" href="/">Open the free app</a>
</div>
"""

p = BASE / "hidden-hunger"
p.mkdir(exist_ok=True)
(p / "index.html").write_text(page(
    "Hidden Hunger: Ultra-Processed Foods and Children | OptimisedEats",
    "How ultra-processed foods cause hidden micronutrient deficiency in children — the SENDO 2.57x risk study, dopamine hijacking, ARFID, and what to do about it. Evidence-based guide for Australian parents.",
    "ultra-processed food children Australia, hidden hunger kids, UPF micronutrient deficiency, ARFID children diet, processed food brain development, zinc deficiency children, children nutrition Australia",
    "Hidden Hunger", "/guide/hidden-hunger/",
    hidden_hunger_body,
    other_related("/guide/hidden-hunger/")
), encoding="utf-8")
print("DONE guide/hidden-hunger/index.html")

print("\nAll new pages generated!")
