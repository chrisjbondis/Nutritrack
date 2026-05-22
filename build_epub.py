"""
build_epub.py  --  Rebuild budget-nutrition-ebook.epub with:
  - Brand green styling (#16a34a)
  - Proper cover page with OptimisedEats branding
  - 3 new chapters: Life Stages, Vegan Nutrition, Catabolic Cycle
Reads all existing chapters from the epub, updates CSS and cover,
appends 3 new chapters, then writes a new epub in-place.

Requirements: Python standard library only (zipfile, re, pathlib).
Usage: python build_epub.py
"""

import zipfile, re
from pathlib import Path

EPUB_PATH = Path(__file__).parent / "budget-nutrition-ebook.epub"

# ── Brand CSS ──────────────────────────────────────────────────────────────────
NEW_CSS = """\
/* OptimisedEats - Budget Nutrition Guide */
body {
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 1em;
  line-height: 1.7;
  color: #1a1a1a;
  margin: 0 auto;
  max-width: 680px;
  padding: 1.2em 1.4em;
}
h1 { font-size: 1.9em; color: #16a34a; margin: 0.6em 0 0.4em; line-height: 1.2; }
h2 { font-size: 1.4em; color: #16a34a; margin: 1.2em 0 0.4em;
     border-bottom: 2px solid #bbf7d0; padding-bottom: 0.2em; }
h3 { font-size: 1.15em; color: #15803d; margin: 1em 0 0.3em; }
h4 { font-size: 1em; color: #166534; margin: 0.8em 0 0.2em; font-style: italic; }
p  { margin: 0.5em 0 0.8em; }
ul, ol { margin: 0.4em 0 0.8em 1.4em; }
li { margin-bottom: 0.35em; }
strong { color: #15803d; }
a  { color: #16a34a; }

/* Tables */
table { width: 100%; border-collapse: collapse; margin: 1em 0 1.4em; font-size: 0.92em; }
th { background-color: #16a34a; color: #fff; padding: 0.5em 0.7em; text-align: left; }
td { padding: 0.45em 0.7em; border-bottom: 1px solid #d1fae5; vertical-align: top; }
tr:nth-child(even) td { background-color: #f0fdf4; }

/* Callout boxes */
.callout, .tip, .warning, .info, .myth {
  border-radius: 6px;
  padding: 0.8em 1em;
  margin: 1em 0;
  font-size: 0.93em;
}
.callout { background: #f0fdf4; border-left: 4px solid #16a34a; }
.tip     { background: #ecfdf5; border-left: 4px solid #10b981; }
.warning { background: #fffbeb; border-left: 4px solid #f59e0b; }
.info    { background: #eff6ff; border-left: 4px solid #3b82f6; }
.myth    { background: #fdf4ff; border-left: 4px solid #a855f7; }
.callout-title { font-weight: bold; margin-bottom: 0.3em; display: block; }

/* Cover page */
.cover-page { text-align: center; padding: 3em 1em; }
.cover-title { font-size: 2.2em; color: #16a34a; font-weight: bold;
               line-height: 1.2; margin-bottom: 0.3em; }
.cover-subtitle { font-size: 1.2em; color: #166534; margin-bottom: 1em; }
.cover-rule { border: none; border-top: 4px solid #16a34a; width: 60%; margin: 1.2em auto; }
.cover-site { font-size: 1em; color: #15803d; font-weight: bold; }
.cover-tagline { font-size: 0.9em; color: #555; margin-top: 0.4em; }
"""

# ── XHTML wrapper ──────────────────────────────────────────────────────────────
def xhtml(title, body):
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE html>\n'
        '<html xmlns="http://www.w3.org/1999/xhtml" '
        'xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">\n'
        '<head>\n'
        '  <meta charset="UTF-8"/>\n'
        f'  <title>{title}</title>\n'
        '  <link rel="stylesheet" type="text/css" href="../style/main.css"/>\n'
        '</head>\n'
        '<body>\n'
        f'{body}\n'
        '</body>\n'
        '</html>\n'
    )

# ── Cover page ─────────────────────────────────────────────────────────────────
COVER_BODY = """\
<div class="cover-page">
  <p class="cover-title">The Budget Nutrition Guide</p>
  <p class="cover-subtitle">Feed Your Family Well &#8212; Without Breaking the Budget</p>
  <hr class="cover-rule"/>
  <p class="cover-site">OptimisedEats.com</p>
  <p class="cover-tagline">Evidence-based nutrition for every age, every budget</p>
  <br/><br/>
  <p style="font-size:0.85em;color:#888;">&#169; OptimisedEats &#8212; Free to share with attribution</p>
</div>"""

# ── Life Stages chapter ────────────────────────────────────────────────────────
LIFE_STAGES_BODY = """\
<h1>Nutrient Gaps by Life Stage</h1>
<p>Nutritional needs change dramatically across the lifespan. Understanding where each age group is
most at risk lets you target limited budget where it matters most.</p>

<h2>Infants and Toddlers (0&#8211;3 years)</h2>
<p>The fastest period of brain and body development. Deficiencies here can have lifelong consequences.</p>
<ul>
  <li><strong>Iron</strong> &#8212; breast milk is low in iron after 6 months; introduce iron-rich solids promptly</li>
  <li><strong>Zinc</strong> &#8212; critical for immune development and growth</li>
  <li><strong>Iodine</strong> &#8212; essential for thyroid and brain development</li>
  <li><strong>Vitamin D</strong> &#8212; especially in exclusively breastfed infants; supplement may be needed</li>
</ul>

<h2>Children and Adolescents (4&#8211;17 years)</h2>
<p>Rapid growth demands high intakes of several key nutrients &#8212; yet this is also the age of
ultra-processed food habits forming.</p>
<ul>
  <li><strong>Calcium</strong> &#8212; peak bone mass is built now; aim for 3 serves dairy or equivalent daily</li>
  <li><strong>Iron</strong> &#8212; teen girls are at high risk once menstruation starts</li>
  <li><strong>Zinc</strong> &#8212; growth spurts and acne both respond to adequate zinc</li>
  <li><strong>Magnesium</strong> &#8212; sleep quality, anxiety, and muscle function all improve with adequate intake</li>
</ul>

<h2>Adult Women (18&#8211;50 years)</h2>
<p>Reproductive years create unique demands, particularly around iron and folate.</p>
<ul>
  <li><strong>Iron</strong> &#8212; menstrual losses mean women need nearly double the iron of men</li>
  <li><strong>Folate</strong> &#8212; critical before and during pregnancy; build up stores before conception</li>
  <li><strong>Calcium + Vitamin D</strong> &#8212; laying down bone mass for later decades</li>
  <li><strong>Iodine</strong> &#8212; especially important for thyroid function and during pregnancy</li>
</ul>

<h2>Adult Men (18&#8211;50 years)</h2>
<ul>
  <li><strong>Zinc</strong> &#8212; testosterone, immunity, and sperm quality all depend on adequate zinc</li>
  <li><strong>Magnesium</strong> &#8212; chronically low in men eating Western diets; linked to poor sleep and mood</li>
  <li><strong>Fibre</strong> &#8212; men have higher colon cancer risk; 38g/day target is rarely met</li>
  <li><strong>Vitamin D</strong> &#8212; indoor workers at high risk; affects mood, immunity, and testosterone</li>
</ul>

<h2>Older Adults (65+ years)</h2>
<div class="myth">
  <span class="callout-title">&#128683; Myth: &#8220;I&#8217;m less active so I need less food&#8221;</span>
  <p>This is one of the most dangerous nutrition myths for older adults. While calorie needs may
  decrease slightly, <strong>protein requirements actually increase</strong> due to anabolic resistance
  &#8212; the age-related reduction in the body&#8217;s ability to use protein for muscle building.
  Eating less food means less protein, less calcium, less B12, less zinc. The result is accelerated
  muscle loss, falls, and cognitive decline.</p>
</div>

<h3>Anabolic Resistance and the Leucine Threshold</h3>
<p>From around age 30, we lose about 1% of muscle mass per year &#8212; a condition called sarcopenia.
By 65, this becomes clinically significant, affecting 10&#8211;20% of Australians. The cause is partly
<em>anabolic resistance</em>: the muscle&#8217;s reduced sensitivity to the amino acid signal for
protein synthesis.</p>
<p>The key driver is <strong>leucine</strong>, a branched-chain amino acid that acts as a trigger for
muscle building. In young adults, approximately 3g leucine per meal stimulates muscle synthesis. In
adults over 65, the threshold rises to <strong>3.5&#8211;4g leucine per meal</strong> &#8212;
equivalent to roughly 35&#8211;40g of high-quality protein.</p>

<div class="callout">
  <span class="callout-title">&#128161; What this means in practice</span>
  <p>Older adults need <strong>more protein per meal, not less</strong>. Spreading protein across
  3 meals (rather than one large serving) gives the body three chances to hit the leucine threshold
  and trigger muscle synthesis. A small serve of toast and tea for breakfast wastes that
  opportunity entirely.</p>
</div>

<h3>Key Gaps in Older Adults</h3>
<ul>
  <li><strong>Protein</strong> &#8212; aim for 1.2&#8211;1.6g per kg body weight (higher than younger adults)</li>
  <li><strong>Vitamin B12</strong> &#8212; stomach acid declines with age, reducing absorption; supplement often needed</li>
  <li><strong>Vitamin D</strong> &#8212; skin synthesis declines; risk of falls and fractures rises</li>
  <li><strong>Calcium</strong> &#8212; bone loss accelerates; post-menopausal women especially at risk</li>
  <li><strong>Zinc</strong> &#8212; immune function and wound healing; appetite loss worsens zinc status</li>
</ul>

<div class="warning">
  <span class="callout-title">&#9888; Taste changes are a hidden risk</span>
  <p>Taste buds decline in sensitivity with age. Older adults often find food less enjoyable and eat
  less as a result. This creates a vicious cycle: less food means fewer nutrients, which accelerates
  decline, which further reduces appetite. Seasoning food well (herbs, spices, lemon juice &#8212;
  not just salt) and eating socially can help maintain intake.</p>
</div>"""

# ── Vegan chapter ──────────────────────────────────────────────────────────────
VEGAN_BODY = """\
<h1>Vegan and Plant-Based Nutrition</h1>
<p>A well-planned plant-based diet can be extremely healthy and budget-friendly. The key word is
<em>planned</em> &#8212; a few nutrients require deliberate attention.</p>

<h2>The Non-Negotiables</h2>

<h3>Vitamin B12 &#8212; Mandatory Supplementation</h3>
<p>B12 does not occur in plant foods in usable amounts. This is not optional &#8212; B12 deficiency
causes irreversible neurological damage. Every vegan must supplement.</p>
<div class="warning">
  <span class="callout-title">&#9888; B12 is the one non-negotiable</span>
  <p>Symptoms of deficiency can take years to appear and may include fatigue, tingling extremities,
  memory problems, and irreversible nerve damage. A cheap cyanocobalamin supplement (1000mcg,
  2&#8211;3x per week) provides reliable protection. Cost: approximately $5&#8211;10 per year.</p>
</div>

<h3>Iron &#8212; More Needed, Less Absorbed</h3>
<p>Plants contain non-haem iron, absorbed at 2&#8211;20% efficiency vs. 15&#8211;35% for haem iron
from meat. Vegans need approximately 1.8x the RDI of iron.</p>
<ul>
  <li>Best sources: lentils, kidney beans, tofu, pumpkin seeds, fortified cereals, dark leafy greens</li>
  <li>Always eat iron-rich foods with vitamin C (lemon juice, tomato, capsicum)</li>
  <li>Avoid coffee/tea within 1 hour of iron-rich meals</li>
  <li>Soak and cook legumes &#8212; reduces phytates that block iron absorption</li>
</ul>

<h3>Zinc &#8212; Same Issue, Same Solution</h3>
<p>Plant zinc is also less bioavailable due to phytates in grains and legumes. Soaking, sprouting,
and fermenting dramatically improve zinc absorption.</p>
<p>Best budget sources: pepitas (pumpkin seeds), cashews, sunflower seeds, oats, legumes,
fortified cereals.</p>

<h3>Omega-3 Fatty Acids &#8212; The Right Type Matters</h3>
<p>ALA (from flax, chia, walnuts) is the plant form. The body converts only 5&#8211;10% to EPA and
DHA &#8212; the forms the brain actually needs. Algae-based omega-3 supplements provide EPA and DHA
directly (algae is where fish get theirs).</p>
<ul>
  <li>Eat 1 tbsp ground flaxseed or chia seeds daily for ALA</li>
  <li>Consider algae-based DHA supplement if not eating seaweed regularly</li>
</ul>

<h3>Calcium &#8212; Dairy-Free Sources</h3>
<table>
  <tr><th>Food</th><th>Serving</th><th>Calcium (mg)</th></tr>
  <tr><td>Fortified plant milk</td><td>250mL</td><td>300</td></tr>
  <tr><td>Firm tofu (calcium-set)</td><td>100g</td><td>350</td></tr>
  <tr><td>Bok choy, cooked</td><td>1 cup</td><td>160</td></tr>
  <tr><td>Almonds</td><td>30g</td><td>75</td></tr>
  <tr><td>Tahini</td><td>2 tbsp</td><td>130</td></tr>
  <tr><td>White beans</td><td>100g cooked</td><td>90</td></tr>
  <tr><td>Edamame</td><td>1 cup</td><td>98</td></tr>
  <tr><td>Fortified orange juice</td><td>250mL</td><td>300</td></tr>
</table>

<h3>Iodine</h3>
<p>Seaweed is the only reliable plant source, but iodine content varies wildly. Most vegans need
iodised salt or a supplement containing 150mcg iodine daily.</p>

<h2>Getting Enough Protein</h2>
<p>Complete proteins contain all 9 essential amino acids. Most plant proteins are incomplete, but
eating a varied diet throughout the day covers all amino acids. You don&#8217;t need to combine
proteins at every meal &#8212; just eat variety.</p>
<div class="callout">
  <span class="callout-title">&#128154; Budget protein powerhouses</span>
  <ul>
    <li>Red lentils &#8212; ~18g protein per 100g dry; cost ~50c per serve</li>
    <li>Chickpeas &#8212; ~15g per 100g dry; versatile in curries, salads, falafels</li>
    <li>Firm tofu &#8212; ~12g per 100g; complete protein</li>
    <li>Edamame &#8212; ~11g per 100g; complete protein</li>
    <li>Tempeh &#8212; ~19g per 100g; fermented = better absorption</li>
    <li>Oats &#8212; ~12g per 100g; good morning protein base</li>
  </ul>
</div>

<h2>The Low-Cost Vegan Week</h2>
<p>A nutritionally complete vegan diet can cost under $7 per day per adult. The pillars are: bulk
legumes (lentils, chickpeas, black beans), seasonal vegetables, oats, brown rice, frozen
spinach/peas, and fortified plant milk. Add flaxseed and a B12 supplement and you have all
bases covered.</p>"""

# ── Catabolic Cycle chapter ────────────────────────────────────────────────────
CATABOLIC_BODY = """\
<h1>The Overnight Catabolic Cycle</h1>
<h2>Why Your First Meal Protein Intake Matters More Than You Think</h2>

<p>Every night while you sleep, your body enters a catabolic (breakdown) state. Without incoming
nutrients, it must source fuel from somewhere &#8212; and muscle is on the menu.</p>

<h2>What Happens Overnight</h2>
<p>After your last meal, blood glucose falls and insulin drops. To maintain blood sugar and fuel the
brain, the body ramps up <strong>gluconeogenesis</strong> &#8212; manufacturing glucose from
non-carbohydrate sources. Amino acids from muscle protein are a prime feedstock.</p>
<p>By morning, you have been in a fasted, catabolic state for 8&#8211;12 hours. Cortisol peaks at
wake time (the <em>cortisol awakening response</em>), further promoting protein breakdown to prepare
the body for the day.</p>

<div class="warning">
  <span class="callout-title">&#9889; The cortisol awakening response</span>
  <p>Within 30&#8211;45 minutes of waking, cortisol spikes by 50&#8211;160% above baseline. This is
  normal and healthy &#8212; it mobilises energy for the day. But it also accelerates muscle protein
  breakdown. Without a high-protein first meal, this catabolic period extends well into the morning.</p>
</div>

<h2>The Leucine Threshold &#8212; The Trigger for Muscle Synthesis</h2>
<p>Muscle protein synthesis is not a gradual dial &#8212; it has a <strong>threshold effect</strong>.
The key signal is leucine, a branched-chain amino acid. When leucine in the blood reaches a
sufficient concentration, it triggers the mTOR pathway and muscle building begins.</p>
<ul>
  <li><strong>Under the threshold:</strong> minimal muscle synthesis regardless of other protein intake</li>
  <li><strong>At or above the threshold:</strong> mTOR activates, muscle synthesis switches on</li>
</ul>
<p>The threshold for a typical adult is approximately <strong>3g of leucine per meal</strong> &#8212;
roughly equivalent to 25&#8211;30g of high-quality protein. For adults over 65, anabolic resistance
raises this to <strong>3.5&#8211;4g leucine (35&#8211;40g protein)</strong>.</p>

<h2>Common Breakfasts That Don&#8217;t Cut It</h2>
<p>Most Australians eat breakfast far below the leucine threshold. Here is how common breakfasts
stack up:</p>
<table>
  <tr><th>Breakfast</th><th>Approx. Protein</th><th>Hits Threshold?</th></tr>
  <tr><td>2 slices toast + Vegemite</td><td>~8g</td><td>No</td></tr>
  <tr><td>Bowl of corn flakes + milk</td><td>~9g</td><td>No</td></tr>
  <tr><td>Banana + coffee</td><td>~1g</td><td>No</td></tr>
  <tr><td>Muesli bar + juice</td><td>~3g</td><td>No</td></tr>
  <tr><td>2 eggs on toast</td><td>~18g</td><td>Borderline</td></tr>
  <tr><td>3 eggs scrambled</td><td>~21g</td><td>Borderline</td></tr>
  <tr><td>2 eggs + 200g Greek yoghurt</td><td>~32g</td><td>Yes</td></tr>
  <tr><td>3 eggs + 250mL full-cream milk</td><td>~30g</td><td>Yes</td></tr>
  <tr><td>2 eggs + 100g cottage cheese + toast</td><td>~33g</td><td>Yes</td></tr>
  <tr><td>Greek yoghurt + oats + pumpkin seeds</td><td>~28g</td><td>Yes</td></tr>
</table>

<h2>Budget Breakfasts That Break the Cycle (Under $2)</h2>
<div class="callout">
  <span class="callout-title">&#128154; Best value high-protein breakfasts</span>
  <ul>
    <li><strong>2 eggs + 200g home-brand Greek yoghurt:</strong> ~32g protein, ~$1.40</li>
    <li><strong>Oats + 250mL full-cream milk + 2 tbsp pumpkin seeds:</strong> ~28g protein, ~$0.90</li>
    <li><strong>2 eggs + 100g cottage cheese on 1 slice toast:</strong> ~33g protein, ~$1.20</li>
    <li><strong>Tin of sardines on 2 slices wholegrain toast:</strong> ~31g protein, ~$1.60</li>
  </ul>
</div>

<h2>The Compounding Effect</h2>
<p>One skipped threshold at breakfast doesn&#8217;t seem like much. But over weeks and months,
consistently failing to hit the leucine threshold at the first meal of the day means:</p>
<ul>
  <li>Net muscle catabolism every morning before the first anabolic meal</li>
  <li>Slower recovery from exercise</li>
  <li>Gradual reduction in basal metabolic rate as muscle mass falls</li>
  <li>For older adults: accelerated sarcopenia and increased fall risk</li>
</ul>

<h2>Especially Critical for Older Adults</h2>
<p>In adults over 65, anabolic resistance means the body is less sensitive to the leucine signal.
Not only is the threshold higher, but the window for muscle protein synthesis after a meal is
narrower. This makes the breakfast protein dose even more important &#8212; each meal is a precious
opportunity that cannot be recovered if missed.</p>

<div class="tip">
  <span class="callout-title">&#128161; The simple rule</span>
  <p>Aim for <strong>at least 25&#8211;30g of protein at your first meal</strong>. This single habit,
  done consistently, is one of the most impactful things you can do for long-term muscle health,
  metabolic rate, and healthy ageing &#8212; at minimal cost.</p>
</div>"""


def build():
    print(f"Reading {EPUB_PATH} ...")

    # Read all existing content
    existing = {}
    with zipfile.ZipFile(EPUB_PATH, "r") as z:
        for name in z.namelist():
            existing[name] = z.read(name)

    print(f"  {len(existing)} files found in existing epub")

    # Detect the path structure (some epubs use EPUB/ prefix, some don't)
    has_epub_prefix = any(n.startswith("EPUB/") for n in existing)
    prefix = "EPUB/" if has_epub_prefix else ""
    print(f"  path prefix: '{prefix}'")

    # Find CSS file
    css_key = None
    for k in existing:
        if k.endswith("main.css") or k.endswith(".css"):
            css_key = k
            break
    if css_key:
        existing[css_key] = NEW_CSS.encode("utf-8")
        print(f"  CSS updated: {css_key}")
    else:
        # Create it
        css_key = f"{prefix}style/main.css"
        existing[css_key] = NEW_CSS.encode("utf-8")
        print(f"  CSS created: {css_key}")

    # Find cover / chap_00 - look for it
    cover_key = None
    for k in existing:
        if "chap_00" in k or "cover" in k.lower():
            cover_key = k
            break
    if cover_key:
        existing[cover_key] = xhtml("Cover", COVER_BODY).encode("utf-8")
        print(f"  Cover replaced: {cover_key}")

    # Add 3 new chapters
    ch23_key = f"{prefix}chap_23.xhtml"
    ch24_key = f"{prefix}chap_24.xhtml"
    ch25_key = f"{prefix}chap_25.xhtml"
    existing[ch23_key] = xhtml("Nutrient Gaps by Life Stage", LIFE_STAGES_BODY).encode("utf-8")
    existing[ch24_key] = xhtml("Vegan and Plant-Based Nutrition", VEGAN_BODY).encode("utf-8")
    existing[ch25_key] = xhtml("The Overnight Catabolic Cycle", CATABOLIC_BODY).encode("utf-8")
    print("  3 new chapters added (chap_23, chap_24, chap_25)")

    # Rebuild content.opf
    opf_key = None
    for k in existing:
        if k.endswith("content.opf") or k.endswith(".opf"):
            opf_key = k
            break

    if opf_key:
        # Find all xhtml chapter files in sorted order
        chap_keys = sorted(
            [k for k in existing if re.search(r"chap_\d+", k) and k.endswith(".xhtml")],
            key=lambda x: int(re.search(r"chap_(\d+)", x).group(1))
        )

        manifest_items = [
            f'    <item id="css" href="{css_key.split(prefix, 1)[-1]}" media-type="text/css"/>'
        ]
        spine_items = []
        for ck in chap_keys:
            rel = ck[len(prefix):]  # relative path from EPUB/
            item_id = re.sub(r"[^\w]", "", rel.replace(".xhtml", ""))
            manifest_items.append(
                f'    <item id="{item_id}" href="{rel}" media-type="application/xhtml+xml"/>'
            )
            spine_items.append(f'    <itemref idref="{item_id}"/>')

        opf = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">\n'
            '  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
            '    <dc:identifier id="uid">optimisedeats-budget-nutrition-guide</dc:identifier>\n'
            '    <dc:title>The Budget Nutrition Guide</dc:title>\n'
            '    <dc:creator>OptimisedEats.com</dc:creator>\n'
            '    <dc:language>en-AU</dc:language>\n'
            '    <dc:description>Evidence-based nutrition for every age and budget</dc:description>\n'
            '    <meta property="dcterms:modified">2026-05-17T00:00:00Z</meta>\n'
            '  </metadata>\n'
            '  <manifest>\n'
            '    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>\n'
            '    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>\n'
            + "\n".join(manifest_items) + "\n"
            '  </manifest>\n'
            '  <spine toc="ncx">\n'
            + "\n".join(spine_items) + "\n"
            '  </spine>\n'
            '</package>\n'
        )
        existing[opf_key] = opf.encode("utf-8")
        print(f"  content.opf rebuilt: {len(chap_keys)} chapters")

    # Extract titles from nav for TOC rebuild
    nav_key = None
    for k in existing:
        if k.endswith("nav.xhtml"):
            nav_key = k
            break

    # Build title map from existing nav
    title_map = {}
    if nav_key:
        nav_content = existing[nav_key].decode("utf-8", errors="replace")
        for fn, title in re.findall(r'href="(chap_[^"]+\.xhtml)"[^>]*>([^<]+)<', nav_content):
            title_map[fn] = title.strip()

    # Override/add new entries
    title_map["chap_00.xhtml"] = "Cover"
    title_map["chap_23.xhtml"] = "Nutrient Gaps by Life Stage"
    title_map["chap_24.xhtml"] = "Vegan and Plant-Based Nutrition"
    title_map["chap_25.xhtml"] = "The Overnight Catabolic Cycle"

    if nav_key:
        chap_keys_for_toc = sorted(
            [k for k in existing if re.search(r"chap_\d+", k) and k.endswith(".xhtml")],
            key=lambda x: int(re.search(r"chap_(\d+)", x).group(1))
        )
        nav_links = []
        for ck in chap_keys_for_toc:
            basename = ck.split("/")[-1]
            title = title_map.get(basename, basename)
            nav_links.append(f"      <li><a href=\"{basename}\">{title}</a></li>")

        nav_xhtml = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<!DOCTYPE html>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">\n'
            '<head><meta charset="UTF-8"/><title>Table of Contents</title></head>\n'
            '<body>\n'
            '  <nav epub:type="toc">\n'
            '    <h1>Table of Contents</h1>\n'
            '    <ol>\n'
            + "\n".join(nav_links) + "\n"
            '    </ol>\n'
            '  </nav>\n'
            '</body>\n'
            '</html>\n'
        )
        existing[nav_key] = nav_xhtml.encode("utf-8")
        print(f"  nav.xhtml rebuilt ({len(nav_links)} entries)")

    # Rebuild toc.ncx
    ncx_key = None
    for k in existing:
        if k.endswith("toc.ncx"):
            ncx_key = k
            break

    if ncx_key and nav_key:
        nav_points = []
        for i, ck in enumerate(chap_keys_for_toc):
            basename = ck.split("/")[-1]
            title = title_map.get(basename, basename)
            nav_points.append(
                f'  <navPoint id="np{i}" playOrder="{i+1}">\n'
                f'    <navLabel><text>{title}</text></navLabel>\n'
                f'    <content src="{basename}"/>\n'
                f'  </navPoint>'
            )
        ncx = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" '
            '"http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">\n'
            '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n'
            '  <head>\n'
            '    <meta name="dtb:uid" content="optimisedeats-budget-nutrition-guide"/>\n'
            '    <meta name="dtb:depth" content="1"/>\n'
            '    <meta name="dtb:totalPageCount" content="0"/>\n'
            '    <meta name="dtb:maxPageNumber" content="0"/>\n'
            '  </head>\n'
            '  <docTitle><text>The Budget Nutrition Guide</text></docTitle>\n'
            '  <navMap>\n'
            + "\n".join(nav_points) + "\n"
            '  </navMap>\n'
            '</ncx>\n'
        )
        existing[ncx_key] = ncx.encode("utf-8")
        print(f"  toc.ncx rebuilt")

    # Write new epub
    print(f"\nWriting {EPUB_PATH} ...")
    with zipfile.ZipFile(EPUB_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        # mimetype MUST be first and uncompressed (epub spec requirement)
        zout.writestr(
            zipfile.ZipInfo("mimetype"),
            "application/epub+zip",
            compress_type=zipfile.ZIP_STORED
        )
        for name, data in existing.items():
            if name == "mimetype":
                continue
            zout.writestr(name, data)

    size_kb = EPUB_PATH.stat().st_size // 1024
    print(f"\nDone!  budget-nutrition-ebook.epub  ({size_kb} KB)")
    print("  Brand green CSS applied")
    print("  Cover page updated")
    print("  New chapters: Life Stages | Vegan Nutrition | Catabolic Cycle")


if __name__ == "__main__":
    build()
