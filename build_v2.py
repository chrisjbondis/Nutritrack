"""
build_v2.py — Optimised Eats build pipeline
Source: budget-nutrition-app-LATEST.jsx (complete, not truncated)
Output: /tmp/oe-v2/src/App.jsx ready for `npm run build`
"""
import re, os

BASE = r"C:\Users\user\Documents\Claude\Projects\How best to feed people at different ages and sexs for the least amount of money based on what their requirements are"
SRC  = BASE + r"\budget-nutrition-app-LATEST.jsx"
HERO = BASE + r"\budget-nutrition-au-dist-full.zip"
OUT  = BASE + r"\budget-nutrition-au-project\src\App.jsx"

with open(SRC, "r", encoding="utf-8") as f:
    src = f.read()
print(f"Loaded {len(src)} bytes from LATEST")

# =============================================================================
# 1. Add useLocalStorage hook before export default function App()
# =============================================================================
ULS = '''
function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try { const item = window.localStorage.getItem(key); return item ? JSON.parse(item) : initialValue; }
    catch { return initialValue; }
  });
  const setValue = (value) => {
    try {
      const v = value instanceof Function ? value(storedValue) : value;
      setStoredValue(v);
      window.localStorage.setItem(key, JSON.stringify(v));
    } catch {}
  };
  return [storedValue, setValue];
}

'''
anchor = 'export default function App() {'
if anchor in src:
    src = src.replace(anchor, ULS + anchor, 1)
    print("1. useLocalStorage hook added OK")
else:
    print("ERROR 1: App anchor not found")

# =============================================================================
# 2. Replace useState → useLocalStorage for persistent state
# =============================================================================
replacements = [
    ('const [tab, setTab] = useState("profile");',
     'const [tab, setTab] = useLocalStorage("oe_tab", "profile");'),
    ('const [household, setHousehold] = useState([]);',
     'const [household, setHousehold] = useLocalStorage("oe_household", []);'),
    ('const [activeId, setActiveId] = useState(null);',
     'const [activeId, setActiveId] = useLocalStorage("oe_activeId", null);'),
    ('const [plan, setPlan] = useState({ breakfast: [], lunch: [], dinner: [], snack: [] });',
     'const [plan, setPlan] = useLocalStorage("oe_plan", { breakfast: [], lunch: [], dinner: [], snack: [] });'),
    ('const [checked, setChecked] = useState({});',
     'const [checked, setChecked] = useLocalStorage("oe_checked", {});'),
]
for old, new in replacements:
    if old in src:
        src = src.replace(old, new, 1)
        print(f"2. Replaced: {old[:50]}...")
    else:
        print(f"WARNING 2: not found: {old[:50]}...")

# weekPlan has multi-line value — handle separately
old_wp = '''const [weekPlan, setWeekPlan] = useState({
    mon: { breakfast: [], lunch: [], dinner: [], snack: [] },
    tue: { breakfast: [], lunch: [], dinner: [], snack: [] },
    wed: { breakfast: [], lunch: [], dinner: [], snack: [] },
    thu: { breakfast: [], lunch: [], dinner: [], snack: [] },
    fri: { breakfast: [], lunch: [], dinner: [], snack: [] },
    sat: { breakfast: [], lunch: [], dinner: [], snack: [] },
    sun: { breakfast: [], lunch: [], dinner: [], snack: [] },
  });'''
new_wp = '''const [weekPlan, setWeekPlan] = useLocalStorage("oe_weekPlan", {
    mon: { breakfast: [], lunch: [], dinner: [], snack: [] },
    tue: { breakfast: [], lunch: [], dinner: [], snack: [] },
    wed: { breakfast: [], lunch: [], dinner: [], snack: [] },
    thu: { breakfast: [], lunch: [], dinner: [], snack: [] },
    fri: { breakfast: [], lunch: [], dinner: [], snack: [] },
    sat: { breakfast: [], lunch: [], dinner: [], snack: [] },
    sun: { breakfast: [], lunch: [], dinner: [], snack: [] },
  });'''
if old_wp in src:
    src = src.replace(old_wp, new_wp, 1)
    print("2. weekPlan useLocalStorage OK")
else:
    print("WARNING 2: weekPlan anchor not found")

# =============================================================================
# 3. Add country state (after showLog)
# =============================================================================
old_log = '  const [showLog, setShowLog] = useState(false);'
new_log = old_log + '\n  const [country, setCountry] = useLocalStorage("oe_country", null);'
if old_log in src:
    src = src.replace(old_log, new_log, 1)
    print("3. country state added OK")
else:
    print("ERROR 3: showLog anchor not found")

# =============================================================================
# 4. COUNTRY_CONFIG — insert after COMMON_FOODS, before NutrientBar
# =============================================================================
CC = r"""
const COUNTRY_CONFIG = {
  AU: {
    name: "Australia", flag: "\u{1F1E6}\u{1F1FA}", currency: "AUD", symbol: "$",
    priceMultiplier: 1,
    stores: "Coles & Woolworths",
    statsTitle: "Australian Nutrition Reality",
    statsPct: "4.2%",
    statsWake: "of adults meet BOTH fruit AND veg recommendations",
    statsSource: "ABS National Nutrition Survey 2023",
    statsSubtitle: "⚠️ Australians NOT Meeting Requirements:",
    statItems: [
      { n: "Calcium", p: 60, d: "90% of teen girls & women 50+ fall short", c: "#ef4444" },
      { n: "Zinc (males)", p: 48, d: "Nearly half of all males", c: "#ef4444" },
      { n: "Iron (women 18–29)", p: 47, d: "Nearly half of young women", c: "#ef4444" },
      { n: "Magnesium", p: 31, d: "1 in 3 people", c: "#f59e0b" },
      { n: "Vitamin A", p: 23, d: "Almost 1 in 4", c: "#f59e0b" },
      { n: "Vitamin D", p: 21, d: "1 in 5 adults deficient", c: "#f59e0b" },
      { n: "Riboflavin B2", p: 20, d: "4.9 million Australians", c: "#f59e0b" },
      { n: "Thiamin B1", p: 16, d: "Getting worse since 2011", c: "#22c55e" },
    ],
    statsFooter: "ABS 2023 · NHMRC NRVs · USDA FoodData · Dept Health PA Guidelines",
  },
  NZ: {
    name: "New Zealand", flag: "\u{1F1F3}\u{1F1FF}", currency: "NZD", symbol: "$",
    priceMultiplier: 1.50,
    stores: "Pak'nSave & Woolworths NZ",
    statsTitle: "NZ Nutrition Reality",
    statsPct: "∼5%",
    statsWake: "of adults meet BOTH fruit AND veg recommendations",
    statsSource: "NZ Health Survey 2023/24",
    statsSubtitle: "⚠️ New Zealanders NOT Meeting Requirements:",
    statItems: [
      { n: "Calcium", p: 55, d: "Over 2 million New Zealanders", c: "#ef4444" },
      { n: "Zinc (males)", p: 45, d: "Nearly half of all men", c: "#ef4444" },
      { n: "Iron (women)", p: 43, d: "Women of childbearing age", c: "#ef4444" },
      { n: "Vitamin D", p: 32, d: "Especially South Island winters", c: "#f59e0b" },
      { n: "Magnesium", p: 28, d: "Over 1 million New Zealanders", c: "#f59e0b" },
      { n: "Folate (women)", p: 22, d: "Women aged 15–44", c: "#f59e0b" },
      { n: "Iodine", p: 19, d: "Linked to low seafood intake", c: "#22c55e" },
    ],
    statsFooter: "NZ Health Survey 2023/24 · NZ/AU NRVs · USDA FoodData",
  },
};
function getCC() {
  try { const c = JSON.parse(localStorage.getItem('oe_country')); return COUNTRY_CONFIG[c] || COUNTRY_CONFIG.AU; } catch(e) { return COUNTRY_CONFIG.AU; }
}
function fmt(n) { const cc = getCC(); return cc.symbol + (n * cc.priceMultiplier).toFixed(2); }
"""
anchor_cc = '  ]},\n];\n\nfunction FoodLogger'
if anchor_cc in src:
    src = src.replace(anchor_cc, '  ]},\n];' + CC + '\nfunction FoodLogger', 1)
    print("4. COUNTRY_CONFIG inserted OK")
else:
    print("ERROR 4: FoodLogger anchor not found")

# =============================================================================
# 5. Add cc helper after ready
# =============================================================================
old_ready = '  const ready = household.length > 0;\n'
new_ready  = '  const ready = household.length > 0;\n  const cc = COUNTRY_CONFIG[country] || COUNTRY_CONFIG.AU;\n'
if old_ready in src:
    src = src.replace(old_ready, new_ready, 1)
    print("5. cc helper added OK")
else:
    print("ERROR 5: ready anchor not found")

# =============================================================================
# 6. Country picker — early return before main App return
# =============================================================================
main_return = (
    '  return (\n'
    '    <div style={{ minHeight: "100vh", background: "linear-gradient(135deg,#0f172a,#1e293b,#0f172a)"'
)
picker = (
    '  if (!country) {\n'
    '    return (\n'
    '      <div style={{ minHeight: "100dvh", background: "#0f172a", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: 24, fontFamily: "system-ui,sans-serif" }}>\n'
    '        <div style={{ fontSize: 56, marginBottom: 12 }}>🥦</div>\n'
    '        <h1 style={{ color: "#f1f5f9", fontSize: 24, fontWeight: 800, margin: "0 0 8px", textAlign: "center" }}>Where are you cooking?</h1>\n'
    '        <p style={{ color: "#94a3b8", fontSize: 14, textAlign: "center", margin: "0 0 32px", lineHeight: 1.6 }}>We\'ll show prices in your local currency and<br/>reference your nearest supermarkets.</p>\n'
    '        <div style={{ display: "flex", gap: 16, flexWrap: "wrap", justifyContent: "center" }}>\n'
    '          {[["AU", "🇦🇺", "Australia", "Coles & Woolworths · AUD"], ["NZ", "🇳🇿", "New Zealand", "Pak\'nSave & Woolworths NZ · NZD"]].map(([code, flag, name, sub]) => (\n'
    '            <button key={code} onClick={() => setCountry(code)}\n'
    '              style={{ background: "rgba(255,255,255,0.05)", border: "2px solid rgba(255,255,255,0.1)", borderRadius: 20, padding: "28px 36px", cursor: "pointer", textAlign: "center", minWidth: 160, color: "inherit" }}\n'
    '              onMouseOver={e => e.currentTarget.style.borderColor = "#22c55e"}\n'
    '              onMouseOut={e => e.currentTarget.style.borderColor = "rgba(255,255,255,0.1)"}>\n'
    '              <div style={{ fontSize: 52, marginBottom: 10 }}>{flag}</div>\n'
    '              <div style={{ color: "#f1f5f9", fontSize: 19, fontWeight: 800, marginBottom: 4 }}>{name}</div>\n'
    '              <div style={{ color: "#64748b", fontSize: 12 }}>{sub}</div>\n'
    '            </button>\n'
    '          ))}\n'
    '        </div>\n'
    '      </div>\n'
    '    );\n'
    '  }\n\n'
)
if main_return in src:
    src = src.replace(main_return, picker + main_return, 1)
    print("6. Country picker added OK")
else:
    print("ERROR 6: main return anchor not found")

# =============================================================================
# 7. Price display replacements
# =============================================================================
count = len(re.findall(r'\$\{(\w+)\.toFixed\(2\)\}', src))
src = re.sub(r'\$\{(\w+)\.toFixed\(2\)\}', lambda m: '{fmt(' + m.group(1) + ')}', src)
src = src.replace('${totalCost.toFixed(0)}', '{cc.symbol}{Math.round(totalCost * cc.priceMultiplier)}')
src = src.replace(
    "${totalMeals > 0 ? (totalCost / 7).toFixed(2) : '0.00'}",
    "{totalMeals > 0 ? fmt(totalCost / 7) : cc.symbol + '0.00'}"
)
src = src.replace('"Save $" + saved.toFixed(2)', '"Save " + fmt(saved)')
print(f"7. Price replacements: {count} simple + 3 special")

# =============================================================================
# 8. Learn tab — dynamic stats from cc
# =============================================================================
old_title = (
    '              <h2 style={{ margin: "6px 0", fontSize: 17, fontWeight: 700 }}>Australian Nutrition Reality</h2>\n'
    '              <p style={{ margin: 0, fontSize: 12, color: "#94a3b8" }}>ABS National Nutrition Survey 2023</p>'
)
new_title = (
    '              <h2 style={{ margin: "6px 0", fontSize: 17, fontWeight: 700 }}>{cc.statsTitle}</h2>\n'
    '              <p style={{ margin: 0, fontSize: 12, color: "#94a3b8" }}>{cc.statsSource}</p>'
)
if old_title in src:
    src = src.replace(old_title, new_title, 1)
    print("8a. Stats title OK")
else:
    print("WARNING 8a: stats title not found")

old_stat = (
    '            <div style={{ background: "rgba(239,68,68,0.12)", border: "1px solid rgba(239,68,68,0.3)", borderRadius: 16, padding: 20, marginBottom: 16, textAlign: "center" }}>\n'
    '              <div style={{ fontSize: 44, fontWeight: 800, color: "#ef4444" }}>4.2%</div>\n'
    '              <div style={{ fontSize: 13, color: "#fca5a5", fontWeight: 600 }}>of adults meet BOTH fruit AND veg recommendations</div>\n'
    '            </div>\n'
    '            <div style={{ fontSize: 13, fontWeight: 700, color: "#f59e0b", marginBottom: 10 }}>⚠️ Australians NOT Meeting Requirements:</div>\n'
    '            {[\n'
    '              { n: "Calcium", p: 60, d: "90% of teen girls & women 50+ fall short", c: "#ef4444" },\n'
    '              { n: "Zinc (males)", p: 48, d: "Nearly half of all males", c: "#ef4444" },\n'
    '              { n: "Iron (women 18-29)", p: 47, d: "Nearly half of young women", c: "#ef4444" },\n'
    '              { n: "Magnesium", p: 31, d: "1 in 3 people", c: "#f59e0b" },\n'
    '              { n: "Vitamin A", p: 23, d: "Almost 1 in 4", c: "#f59e0b" },\n'
    '              { n: "Vitamin D", p: 21, d: "1 in 5 adults deficient", c: "#f59e0b" },\n'
    '              { n: "Riboflavin B2", p: 20, d: "4.9 million Australians", c: "#f59e0b" },\n'
    '              { n: "Thiamin B1", p: 16, d: "Getting worse since 2011", c: "#22c55e" },\n'
    '            ].map(d => ('
)
new_stat = (
    '            <div style={{ background: "rgba(239,68,68,0.12)", border: "1px solid rgba(239,68,68,0.3)", borderRadius: 16, padding: 20, marginBottom: 16, textAlign: "center" }}>\n'
    '              <div style={{ fontSize: 44, fontWeight: 800, color: "#ef4444" }}>{cc.statsPct}</div>\n'
    '              <div style={{ fontSize: 13, color: "#fca5a5", fontWeight: 600 }}>{cc.statsWake}</div>\n'
    '            </div>\n'
    '            <div style={{ fontSize: 13, fontWeight: 700, color: "#f59e0b", marginBottom: 10 }}>{cc.statsSubtitle}</div>\n'
    '            {cc.statItems.map(d => ('
)
if old_stat in src:
    src = src.replace(old_stat, new_stat, 1)
    print("8b. Stat items OK")
else:
    print("WARNING 8b: stat block not found")

src = src.replace(
    'ABS 2023 · NHMRC NRVs · USDA FoodData · Dept Health PA Guidelines</div>',
    '{cc.statsFooter}</div>'
)
print("8c. Stats footer replaced")

# =============================================================================
# 9. Profile tab — country changer button
# =============================================================================
change_btn = (
    '\n            <div style={{ textAlign: "center", marginTop: 20, paddingTop: 16, borderTop: "1px solid rgba(255,255,255,0.06)" }}>\n'
    '              <div style={{ fontSize: 12, color: "#475569", marginBottom: 8 }}>{cc.flag} {cc.name} · {cc.currency}</div>\n'
    '              <button onClick={() => setCountry(null)} style={{ background: "none", border: "1px solid rgba(255,255,255,0.12)", borderRadius: 8, padding: "6px 16px", color: "#64748b", cursor: "pointer", fontSize: 12 }}>🌏 Change Country</button>\n'
    '            </div>'
)
profile_close = '          </div>\n        )}\n\n        {/* DASHBOARD */'
if profile_close in src:
    src = src.replace(profile_close, change_btn + '\n          </div>\n        )}\n\n        {/* DASHBOARD */', 1)
    print("9. Country changer added to profile OK")
else:
    print("WARNING 9: profile close anchor not found")

# =============================================================================
# 10. Age input fix
# =============================================================================
old_age = 'onChange={e => setEditing({ ...editing, age: parseInt(e.target.value) || 1 })}'
new_age = 'onChange={e => setEditing({ ...editing, age: e.target.value === "" ? "" : (parseInt(e.target.value) || 1) })}'
if old_age in src:
    src = src.replace(old_age, new_age, 1)
    print("10a. Age input fix OK")
else:
    print("WARNING 10a: age input not found (may already be fixed)")

old_save = ('if (!editing.name.trim()) return; '
            'if (household.find(m => m.id === editing.id)) { setHousehold(h => h.map(m => m.id === editing.id ? editing : m)); } '
            'else { const nm = { ...editing, id: Date.now() }; setHousehold(h => [...h, nm]); setActiveId(nm.id); } setEditing(null);')
new_save = ('if (!editing.name.trim()) return; '
            'const saved = { ...editing, age: parseInt(editing.age) || 1 }; '
            'if (household.find(m => m.id === saved.id)) { setHousehold(h => h.map(m => m.id === saved.id ? saved : m)); } '
            'else { const nm = { ...saved, id: Date.now() }; setHousehold(h => [...h, nm]); setActiveId(nm.id); } setEditing(null);')
if old_save in src:
    src = src.replace(old_save, new_save, 1)
    print("10b. Save normalize OK")
else:
    print("WARNING 10b: save anchor not found")

# =============================================================================
# 11. RECIPE_BOOSTS — insert after BOOSTS array, patch render sites
# =============================================================================
RB = r"""

const RECIPE_BOOSTS = {
  // BREAKFASTS
  b1:  ["milk","banana","seeds","flax","yoghurt"],   // Overnight Oats
  b2:  ["cheese","spinach","seeds"],                  // Egg & Spinach Scramble
  b3:  ["egg","spinach"],                             // Sardine Toast
  b5:  ["milk","banana","seeds","flax","yoghurt"],   // Power Weet-Bix
  b8:  ["egg","cheese","spinach"],                    // Big Breakfast
  b9:  ["egg","spinach"],                             // Liver on Toast
  b10: ["egg","cheese","spinach"],                    // Egg Bean Burrito
  // LUNCHES
  l1:  ["spinach","yoghurt","seeds"],                 // Red Lentil Soup
  l2:  ["egg","spinach","seeds"],                     // Egg Fried Rice
  l3:  ["egg","seeds","flax"],                        // Chickpea Cabbage Slaw
  l4:  ["banana","milk","flax","yoghurt"],            // PB Spinach Smoothie
  l5:  ["egg","cheese","spinach"],                    // Bean & Cheese Quesadilla
  l6:  ["egg","cheese","spinach"],                    // Bean & Veg Wrap
  l7:  ["egg","spinach","seeds"],                     // 3-Bean Salad
  l8:  ["egg","cheese","spinach"],                    // Baked Beans on Toast
  l9:  ["egg","spinach","seeds","flax"],              // Tuna & Bean Salad
  l10: ["yoghurt","cheese","spinach"],                // Black Bean & Corn Soup
  l11: ["egg","spinach","seeds"],                     // Hummus & Veg Plate
  c2:  ["spinach","seeds"],                           // Chicken & Lentil Soup
  hl3: ["cheese","spinach"],                          // Liver Sausage Rolls
  // DINNERS
  d1:  ["spinach","yoghurt","seeds"],                 // Lentil Potato Curry
  d2:  ["cheese","spinach","seeds"],                  // Sardine Pasta
  d3:  ["egg","spinach","seeds"],                     // Liver Stir-Fry
  d4:  ["cheese","yoghurt","spinach","seeds"],        // Bean & Veg Stew
  d6:  ["cheese","spinach"],                          // Hidden Liver Bolognese
  d7:  ["cheese","spinach","yoghurt"],                // Bean Tacos
  d8:  ["cheese","spinach","yoghurt"],                // Chickpea & Potato Bake
  d9:  ["cheese","spinach","seeds"],                  // Sausage & Bean Casserole
  c1:  ["cheese","spinach","seeds"],                  // Chicken Tray Bake
  c3:  ["spinach","yoghurt","seeds"],                 // Chicken Curry
  hl1: ["cheese","spinach"],                          // Hidden Liver Meatballs
  hl2: ["cheese","spinach","seeds"],                  // Liver Cottage Pie
  bh1: ["egg","spinach","seeds"],                     // Heart Stir-Fry
  bh2: ["yoghurt","cheese","spinach"],                // Heart Bean Chilli
  bh3: ["cheese","egg","spinach"],                    // Heart+Liver Burger
  m1:  ["cheese","spinach"],                          // Shakshuka
  a4:  ["egg","spinach","seeds"],                     // Peanut Noodles
  i1:  ["spinach","yoghurt","seeds"],                 // Classic Dal
  // NEW BUDGET BREAKFASTS
  nb1: ["egg","spinach","seeds"],                     // Tuna & Egg Rice Bowl
  nb2: ["banana","milk","flax","seeds","yoghurt"],   // PB Banana Oats
  nb3: ["egg","spinach","seeds"],                     // Ricotta & Tomato Toast
  nb4: ["cheese","spinach"],                          // Microwave Egg Mug
  nb5: ["spinach","cheese","seeds"],                  // Canned Salmon Omelette
  // NEW BUDGET LUNCHES
  nl1: ["egg","spinach","seeds","flax"],              // White Bean & Tuna Salad
  nl2: ["spinach","yoghurt","seeds"],                 // Lentil & Veg Soup
  nl3: ["egg","spinach","seeds"],                     // Sardine & Avo Rice Cakes
  nl4: ["yoghurt","spinach"],                         // Spiced Chickpea Wrap
  nl5: ["egg","cheese","spinach"],                    // Egg & Sweet Potato Hash
  // NEW BUDGET DINNERS
  nd1: ["egg","spinach","seeds"],                     // Chicken & Veg Congee
  nd2: ["cheese","spinach","yoghurt"],                // Black Bean Quesadillas
  nd3: ["cheese","spinach"],                          // Baked Eggs in Tomato
  nd4: ["egg","spinach","seeds"],                     // Tuna Fried Rice
  nd5: ["spinach","seeds"],                           // Split Pea & Ham Soup
  nd6: ["cheese","spinach","seeds"],                  // Hidden Liver Shepherd's Pie
  nd7: ["yoghurt","spinach","seeds"],                 // Chickpea & Spinach Curry
  // NEW BUDGET SNACKS
  ns1: ["cheese","seeds"],                            // Boiled Eggs & Veggies
  ns2: ["milk","yoghurt","banana"],                   // Pumpkin Seeds & Fruit
  ns3: ["seeds","flax","banana"],                     // Cottage Cheese & Pineapple
  // SNACKS
  s1:  ["seeds","flax","banana"],                     // Yoghurt Berry Bowl
  s2:  ["milk","seeds"],                              // Banana PB Bites
  s4:  ["yoghurt","milk","banana"],                   // Orange & Seeds
  s7:  ["banana","seeds","yoghurt"],                  // Milk + Fruit
  s8:  ["seeds","flax","banana"],                     // Loaded Yoghurt Bowl
  // B-SERIES EXTRAS
  b59: ["egg","cheese","spinach"],                    // Baked Beans on Toast
  b60: ["spinach","seeds"],                           // Cheese & Egg Toastie
  b61: ["spinach","seeds"],                           // Cheesy Baked Beans & Egg
  b62: ["spinach","seeds"],                           // Cheese & Tomato Omelette
  b63: ["spinach","seeds"],                           // Mega Breakfast Burrito
  // L-SERIES EXTRAS
  l64: ["egg","seeds","spinach","yoghurt"],           // Greek-Style Chickpea Salad
  l65: ["egg","cheese","spinach"],                    // Chicken Caesar-ish Salad
  l66: ["egg","seeds"],                               // Cheese & Apple Salad
  l67: ["egg","seeds","flax"],                        // Chicken & Cabbage Slaw
  l68: ["spinach","seeds","egg"],                     // Cheesy Pasta Salad
  l69: ["spinach","seeds","egg"],                     // Chicken & Bean Salad
  l70: ["spinach","egg"],                             // Grilled Cheese & Tomato
  l71: ["spinach","egg","yoghurt"],                   // Chicken & Cheese Quesadilla
  // D-SERIES EXTRAS
  d72: ["cheese","yoghurt","spinach"],                // Beef Mince Tacos
  d73: ["cheese","spinach","seeds"],                  // Beef Mince & Potato Bake
  d74: ["egg","spinach","seeds"],                     // Beef & Cabbage Stir-Fry
  d75: ["spinach","seeds"],                           // Whole Baked Fish
  d76: ["yoghurt","cheese","spinach"],                // Fish Tacos
  d77: ["cheese","egg","spinach","yoghurt"],          // Refried Beans (Dry)
  d78: ["cheese","yoghurt","spinach"],                // Bean Burrito Bowls
  d79: ["spinach","seeds","cheese"],                  // Chicken & Rice One-Pot
  d80: ["spinach","seeds"],                           // Honey Garlic Chicken
  // SN-SERIES
  sn81: ["egg","seeds"],                              // Cheese & Crackers
  sn82: ["egg","spinach","seeds"],                    // Cheese & Veggie Sticks
  sn83: ["egg","spinach","seeds"],                    // Cheese & Tomato Rice Cakes
};
"""
boosts_end = '];\n\nconst COMMON_FOODS'
if boosts_end in src:
    src = src.replace(boosts_end, '];' + RB + '\nconst COMMON_FOODS', 1)
    print("11a. RECIPE_BOOSTS inserted OK")
else:
    print("ERROR 11a: BOOSTS end anchor not found")

old_map = '{BOOSTS.map(b => {'
new_map = '{(RECIPE_BOOSTS[r.id] ? BOOSTS.filter(b => RECIPE_BOOSTS[r.id].includes(b.id)) : BOOSTS).map(b => {'
count_map = src.count(old_map)
src = src.replace(old_map, new_map)
print(f"11b. BOOSTS.map patched at {count_map} locations")

# =============================================================================
# Write
# =============================================================================
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(src)

print(f"\n✅ Done. {len(src)} bytes → {OUT}")
print(f"   useLocalStorage : {'useLocalStorage' in src}")
print(f"   COUNTRY_CONFIG  : {'COUNTRY_CONFIG' in src}")
print(f"   FeedbackForm    : {'FeedbackForm' in src}")
print(f"   setCountry      : {'setCountry' in src}")
print(f"   RECIPE_BOOSTS   : {'RECIPE_BOOSTS' in src}")
