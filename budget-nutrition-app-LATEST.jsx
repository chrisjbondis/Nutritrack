import { useState, useMemo, useCallback, useEffect } from "react";

const NK = {
  protein:{name:"Protein",unit:"g",cat:"macro"},
  fibre:{name:"Fibre",unit:"g",cat:"macro"},
  vitA:{name:"Vitamin A",unit:"μg",cat:"vit"},
  vitC:{name:"Vitamin C",unit:"mg",cat:"vit"},
  vitD:{name:"Vitamin D",unit:"IU",cat:"vit"},
  vitK:{name:"Vitamin K",unit:"μg",cat:"vit"},
  folate:{name:"Folate",unit:"μg",cat:"vit"},
  vitB12:{name:"Vitamin B12",unit:"μg",cat:"vit"},
  choline:{name:"Choline",unit:"mg",cat:"vit"},
  calcium:{name:"Calcium",unit:"mg",cat:"min"},
  iron:{name:"Iron",unit:"mg",cat:"min"},
  magnesium:{name:"Magnesium",unit:"mg",cat:"min"},
  zinc:{name:"Zinc",unit:"mg",cat:"min"},
  potassium:{name:"Potassium",unit:"mg",cat:"min"},
  selenium:{name:"Selenium",unit:"μg",cat:"min"},
  iodine:{name:"Iodine",unit:"μg",cat:"min"},
  omega3:{name:"Omega-3",unit:"g",cat:"fat"},
};
const NKS = Object.keys(NK);
const DEMOG_MAP = {
  f_9:{age:11,sex:"female"}, m_9:{age:11,sex:"male"},
  f_14:{age:16,sex:"female"}, m_14:{age:16,sex:"male"},
  f_19:{age:30,sex:"female"}, m_19:{age:30,sex:"male"},
  f_51:{age:60,sex:"female"}, m_51:{age:60,sex:"male"},
  f_71:{age:75,sex:"female"}, m_71:{age:75,sex:"male"},
  preg:{pregnant:true}, lact:{lactating:true}
};

function getRDA(p) {
  if (!p) return {protein:46,fibre:25,vitA:700,vitC:75,vitD:600,vitK:90,folate:400,vitB12:2.4,choline:425,calcium:1000,iron:18,magnesium:310,zinc:8,potassium:4700,selenium:55,iodine:150,omega3:1.1,cal:2000};
  if (p.pregnant) return {protein:60,fibre:28,vitA:770,vitC:85,vitD:600,vitK:90,folate:600,vitB12:2.6,choline:450,calcium:1000,iron:27,magnesium:350,zinc:11,potassium:4700,selenium:60,iodine:220,omega3:1.1,cal:2350};
  if (p.lactating) return {protein:67,fibre:25,vitA:1300,vitC:120,vitD:600,vitK:90,folate:500,vitB12:2.8,choline:550,calcium:1000,iron:9,magnesium:310,zinc:12,potassium:5100,selenium:70,iodine:290,omega3:1.1,cal:2400};
  const s = p.sex === "male" ? "m" : "f";
  const a = p.age < 4 ? 1 : p.age < 9 ? 4 : p.age < 14 ? 9 : p.age < 19 ? 14 : p.age < 51 ? 19 : p.age < 71 ? 51 : 71;
  const T = {
    f_1:{protein:13,fibre:14,vitA:300,vitC:15,vitD:600,vitK:30,folate:150,vitB12:0.9,choline:200,calcium:700,iron:7,magnesium:80,zinc:3,potassium:3000,selenium:20,iodine:90,omega3:0.7,cal:1100},
    m_1:{protein:13,fibre:14,vitA:300,vitC:15,vitD:600,vitK:30,folate:150,vitB12:0.9,choline:200,calcium:700,iron:7,magnesium:80,zinc:3,potassium:3000,selenium:20,iodine:90,omega3:0.7,cal:1100},
    f_4:{protein:19,fibre:18,vitA:400,vitC:25,vitD:600,vitK:55,folate:200,vitB12:1.2,choline:250,calcium:1000,iron:10,magnesium:130,zinc:5,potassium:3800,selenium:30,iodine:90,omega3:0.9,cal:1400},
    m_4:{protein:19,fibre:18,vitA:400,vitC:25,vitD:600,vitK:55,folate:200,vitB12:1.2,choline:250,calcium:1000,iron:10,magnesium:130,zinc:5,potassium:3800,selenium:30,iodine:90,omega3:0.9,cal:1500},
    f_9:{protein:34,fibre:20,vitA:600,vitC:45,vitD:600,vitK:60,folate:300,vitB12:1.8,choline:375,calcium:1300,iron:8,magnesium:240,zinc:8,potassium:4500,selenium:40,iodine:120,omega3:1.0,cal:1800},
    m_9:{protein:34,fibre:24,vitA:600,vitC:45,vitD:600,vitK:60,folate:300,vitB12:1.8,choline:375,calcium:1300,iron:8,magnesium:240,zinc:8,potassium:4500,selenium:40,iodine:120,omega3:1.2,cal:2000},
    f_14:{protein:46,fibre:22,vitA:700,vitC:65,vitD:600,vitK:75,folate:400,vitB12:2.4,choline:400,calcium:1300,iron:15,magnesium:360,zinc:9,potassium:4700,selenium:55,iodine:150,omega3:1.1,cal:2000},
    m_14:{protein:52,fibre:28,vitA:900,vitC:75,vitD:600,vitK:75,folate:400,vitB12:2.4,choline:550,calcium:1300,iron:11,magnesium:410,zinc:11,potassium:4700,selenium:55,iodine:150,omega3:1.6,cal:2600},
    f_19:{protein:46,fibre:25,vitA:700,vitC:75,vitD:600,vitK:90,folate:400,vitB12:2.4,choline:425,calcium:1000,iron:18,magnesium:310,zinc:8,potassium:4700,selenium:55,iodine:150,omega3:1.1,cal:2000},
    m_19:{protein:64,fibre:30,vitA:900,vitC:90,vitD:600,vitK:120,folate:400,vitB12:2.4,choline:550,calcium:1000,iron:8,magnesium:400,zinc:11,potassium:4700,selenium:55,iodine:150,omega3:1.6,cal:2400},
    f_51:{protein:68,fibre:22,vitA:700,vitC:75,vitD:600,vitK:90,folate:400,vitB12:2.4,choline:425,calcium:1200,iron:8,magnesium:320,zinc:8,potassium:4700,selenium:55,iodine:150,omega3:1.1,cal:1800},
    m_51:{protein:85,fibre:25,vitA:900,vitC:90,vitD:600,vitK:120,folate:400,vitB12:2.4,choline:550,calcium:1000,iron:8,magnesium:420,zinc:11,potassium:4700,selenium:55,iodine:150,omega3:1.6,cal:2200},
    f_71:{protein:75,fibre:22,vitA:700,vitC:75,vitD:800,vitK:90,folate:400,vitB12:2.4,choline:425,calcium:1200,iron:8,magnesium:320,zinc:8,potassium:4700,selenium:55,iodine:150,omega3:1.1,cal:1800},
    m_71:{protein:95,fibre:25,vitA:900,vitC:90,vitD:800,vitK:120,folate:400,vitB12:2.4,choline:550,calcium:1200,iron:8,magnesium:420,zinc:11,potassium:4700,selenium:55,iodine:150,omega3:1.6,cal:2000},
  };
  return T[s + "_" + a] || T["f_19"];
}

const RECIPES = [
  {id:"b1",name:"Overnight Oats",type:"breakfast",cost:1.04,time:5,emoji:"🥣",desc:"No-cook oats with banana, peanut butter, seeds.",ing:["50g oats","150mL milk","1 tbsp peanut butter","½ banana","1 tbsp seeds"],steps:["Combine oats+milk","Add peanut butter","Top with banana+seeds","Fridge overnight"],n:{cal:480,protein:18,fibre:8,vitA:15,vitC:5,vitD:20,vitK:5,folate:40,vitB12:0.5,choline:30,calcium:200,iron:2.7,magnesium:140,zinc:2,potassium:500,selenium:12,iodine:25,omega3:0.3},tags:["quick","kid-friendly"]},
  {id:"b2",name:"Egg & Spinach Scramble",type:"breakfast",cost:1.56,time:7,emoji:"🍳",desc:"Eggs with spinach on toast.",ing:["2 eggs","60g spinach","Toast","Butter"],steps:["Cook spinach","Add eggs, stir","Serve on toast"],n:{cal:380,protein:20,fibre:4,vitA:280,vitC:12,vitD:80,vitK:250,folate:140,vitB12:1.0,choline:250,calcium:120,iron:3.6,magnesium:60,zinc:1.8,potassium:350,selenium:16,iodine:30,omega3:0.1},tags:["quick","pregnancy-safe"]},
  {id:"b3",name:"Sardine Toast",type:"breakfast",cost:2.34,time:5,emoji:"🐟",desc:"Sardines on toast. Omega-3 + calcium + B12.",ing:["1 tin sardines","Tomato","Toast","Lemon"],steps:["Mash sardines with lemon","Spread on toast","Top with tomato"],n:{cal:350,protein:25,fibre:2,vitA:30,vitC:12,vitD:250,vitK:5,folate:15,vitB12:8.9,choline:75,calcium:350,iron:2.9,magnesium:40,zinc:1.5,potassium:400,selenium:45,iodine:35,omega3:1.4},tags:["omega-3","sardine"]},
  {id:"b5",name:"Power Weet-Bix",type:"breakfast",cost:1.17,time:3,emoji:"💪",desc:"Fortified Weet-Bix + milk + seeds + banana + flax.",ing:["3 Weet-Bix","200mL milk","½ banana","Seeds","Flaxseed"],steps:["Weet-Bix + milk","Top with everything"],n:{cal:400,protein:14,fibre:8,vitA:40,vitC:5,vitD:30,vitK:5,folate:150,vitB12:0.8,choline:30,calcium:250,iron:4.5,magnesium:80,zinc:2.5,potassium:500,selenium:10,iodine:35,omega3:1.8},tags:["quick","kid-friendly","fortified"]},
  {id:"b8",name:"Big Breakfast",type:"breakfast",cost:2.6,time:12,emoji:"🍳",desc:"Eggs, beans, spinach, tomato, toast.",ing:["2 eggs","½ tin beans","Spinach","Tomato","Toast"],steps:["Heat beans","Cook spinach+eggs","Plate with toast"],n:{cal:500,protein:24,fibre:10,vitA:280,vitC:25,vitD:50,vitK:200,folate:160,vitB12:1.0,choline:260,calcium:130,iron:5,magnesium:80,zinc:2.5,potassium:700,selenium:16,iodine:30,omega3:0.1},tags:["high-protein","pregnancy-safe"]},
  {id:"b9",name:"Liver on Toast",type:"breakfast",cost:1.69,time:10,emoji:"🫀",desc:"Chicken liver on toast. Week's B12 in one serve.",ing:["100g chicken liver","½ onion","Toast","Butter, lemon"],steps:["Cook onion","Add liver 2-3 min/side","Serve on toast"],n:{cal:300,protein:22,fibre:2,vitA:3500,vitC:15,vitD:5,vitK:5,folate:250,vitB12:30,choline:200,calcium:20,iron:5,magnesium:25,zinc:2.5,potassium:250,selenium:18,iodine:8,omega3:0.05},tags:["organ-meat"]},
  {id:"b10",name:"Egg Bean Burrito",type:"breakfast",cost:1.82,time:10,emoji:"🌯",desc:"Eggs, beans, spinach, cheese in wrap. Freezable.",ing:["Tortilla","2 eggs","Beans","Spinach","Cheese"],steps:["Cook spinach+eggs","Warm tortilla","Fill and roll"],n:{cal:420,protein:22,fibre:6,vitA:200,vitC:8,vitD:50,vitK:100,folate:100,vitB12:0.8,choline:200,calcium:200,iron:3.5,magnesium:55,zinc:2.5,potassium:400,selenium:14,iodine:25,omega3:0.05},tags:["kid-friendly","freezer"]},
  {id:"l1",name:"Red Lentil Soup",type:"lunch",cost:1.17,time:35,emoji:"🍲",desc:"Thick lentil+carrot soup. Makes 6.",ing:["300g lentils","3 carrots","Onion, garlic","Tin tomatoes","Cumin, turmeric"],steps:["Cook onion+spices","Add lentils, carrots, tomatoes","Simmer 25 min, blend"],n:{cal:310,protein:18,fibre:12,vitA:840,vitC:22,vitD:0,vitK:15,folate:180,vitB12:0,choline:40,calcium:50,iron:4,magnesium:60,zinc:2,potassium:650,selenium:6,iodine:5,omega3:0.1},tags:["freezer","vegan","kid-friendly"]},
  {id:"l2",name:"Egg Fried Rice",type:"lunch",cost:1.43,time:15,emoji:"🍚",desc:"Leftover rice + eggs + veg.",ing:["1 cup cold rice","2 eggs","Frozen veg","Soy sauce"],steps:["Fry veg","Scramble eggs","Add rice+soy sauce"],n:{cal:450,protein:18,fibre:6,vitA:200,vitC:8,vitD:40,vitK:20,folate:50,vitB12:0.5,choline:140,calcium:60,iron:2.5,magnesium:80,zinc:2,potassium:350,selenium:15,iodine:20,omega3:0.3},tags:["quick","kid-friendly"]},
  {id:"l4",name:"PB Spinach Smoothie",type:"lunch",cost:1.3,time:3,emoji:"🥤",desc:"Hidden spinach smoothie.",ing:["Banana","Milk","peanut butter","Spinach","Flaxseed"],steps:["Blend everything"],n:{cal:420,protein:17,fibre:7,vitA:150,vitC:15,vitD:40,vitK:120,folate:100,vitB12:0.5,choline:40,calcium:300,iron:2.5,magnesium:110,zinc:2,potassium:700,selenium:10,iodine:30,omega3:2.0},tags:["quick","kid-friendly"]},
  {id:"l3",name:"Chickpea Cabbage Slaw",type:"lunch",cost:1.69,time:10,emoji:"🥗",desc:"Cold crunchy no-cook bowl. Chickpeas + cabbage + seeds.",ing:["½ tin chickpeas","2 cups cabbage, shredded","1 carrot, grated","2 tbsp sunflower seeds","Lemon, olive oil, cumin"],steps:["Combine cabbage, carrot, chickpeas","Dress with oil, lemon, cumin","Top with seeds"],n:{cal:380,protein:15,fibre:13,vitA:400,vitC:40,vitD:0,vitK:80,folate:140,vitB12:0,choline:30,calcium:80,iron:3.2,magnesium:70,zinc:2,potassium:500,selenium:8,iodine:5,omega3:0.1},tags:["quick","no-cook","vegan"]},
  {id:"l5",name:"Bean & Cheese Quesadilla",type:"lunch",cost:1.3,time:8,emoji:"🫔",desc:"Mashed beans + cheese in a toasted tortilla. $1, 8 min, done.",ing:["1 tortilla","½ tin beans, mashed","¼ cup cheese, grated","Optional: corn, capsicum, spinach"],steps:["Spread beans on half the tortilla","Add cheese and extras","Fold in half","Cook in dry pan 2-3 min each side"],n:{cal:380,protein:18,fibre:9,vitA:40,vitC:5,vitD:3,vitK:8,folate:80,vitB12:0.4,choline:25,calcium:250,iron:3,magnesium:50,zinc:2,potassium:400,selenium:6,iodine:12,omega3:0.02},tags:["quick","kid-friendly","vegetarian"]},
  {id:"l6",name:"Bean & Veg Wrap",type:"lunch",cost:1.56,time:5,emoji:"🌯",desc:"Canned beans + whatever veg you have in a wrap. Zero cooking if using canned.",ing:["1 tortilla","½ tin beans (any type)","Handful spinach","Grated carrot","2 tbsp cheese or yoghurt","Hot sauce (optional)"],steps:["Drain beans, lightly mash","Layer beans, spinach, carrot, cheese on tortilla","Add hot sauce if wanted","Roll up"],n:{cal:350,protein:16,fibre:10,vitA:250,vitC:10,vitD:2,vitK:60,folate:100,vitB12:0.3,choline:25,calcium:180,iron:3,magnesium:55,zinc:1.8,potassium:450,selenium:5,iodine:10,omega3:0.05},tags:["quick","no-cook","kid-friendly","vegetarian"]},
  {id:"l7",name:"3-Bean Salad",type:"lunch",cost:1.17,time:10,emoji:"🫘",desc:"3 tins of beans, onion, vinaigrette. Makes 6 serves. Lasts all week in the fridge.",ing:["1 tin kidney beans","1 tin chickpeas","1 tin cannellini beans","½ red onion, diced","1 carrot, diced","Parsley or coriander","Dressing: olive oil, lemon, cumin, salt"],steps:["Drain and rinse all beans","Combine with onion, carrot, herbs","Dress with oil, lemon, cumin, salt","Keeps 5 days in fridge"],n:{cal:280,protein:14,fibre:14,vitA:200,vitC:12,vitD:0,vitK:15,folate:160,vitB12:0,choline:30,calcium:80,iron:4,magnesium:70,zinc:2,potassium:550,selenium:5,iodine:4,omega3:0.05},tags:["no-cook","batch-cook","vegan"]},
  {id:"l8",name:"Baked Beans on Toast",type:"lunch",cost:1.04,time:5,emoji:"🫘",desc:"The simplest hot lunch. Surprisingly decent nutrition for almost nothing.",ing:["1 tin baked beans (or plain beans)","2 slices wholegrain toast","Butter","Optional: grated cheese on top"],steps:["Heat beans in pot or microwave","Toast bread, butter it","Pour beans on toast","Add cheese if using"],n:{cal:350,protein:16,fibre:12,vitA:15,vitC:5,vitD:0,vitK:4,folate:80,vitB12:0,choline:20,calcium:80,iron:3.5,magnesium:55,zinc:2,potassium:500,selenium:5,iodine:5,omega3:0.05},tags:["quick","vegan","kid-friendly"]},
  {id:"l9",name:"Tuna & Bean Salad",type:"lunch",cost:1.95,time:5,emoji:"🐟",desc:"Tin of tuna + tin of beans + whatever veg. High protein, omega-3.",ing:["1 tin tuna, drained","½ tin cannellini or kidney beans","Handful spinach or lettuce","½ capsicum or tomato, diced","Lemon juice, olive oil, salt"],steps:["Combine tuna, beans, and veg","Dress with lemon and oil","Season and eat"],n:{cal:380,protein:30,fibre:7,vitA:100,vitC:25,vitD:15,vitK:40,folate:80,vitB12:2.5,choline:40,calcium:40,iron:3,magnesium:45,zinc:2,potassium:450,selenium:35,iodine:15,omega3:0.3},tags:["quick","no-cook","high-protein"]},
  {id:"l10",name:"Black Bean & Corn Soup",type:"lunch",cost:1.1,time:25,emoji:"🍲",desc:"Thick, smoky bean soup. Freezes brilliantly. Serves 6.",ing:["2 tins black beans","1 tin tomatoes","1 cup frozen corn","1 onion, diced","2 garlic cloves","2 tsp cumin, 1 tsp smoked paprika","Lime juice, salt"],steps:["Cook onion 4 min, add garlic+spices","Add beans, tomatoes, corn, 1 cup water","Simmer 15 min","Mash half roughly with spoon for thickness","Season with lime and salt"],n:{cal:300,protein:15,fibre:15,vitA:50,vitC:15,vitD:0,vitK:8,folate:180,vitB12:0,choline:30,calcium:70,iron:4,magnesium:75,zinc:2,potassium:600,selenium:4,iodine:4,omega3:0.05},tags:["freezer","vegan","batch-cook"]},
  {id:"l11",name:"Hummus & Veg Plate",type:"lunch",cost:1.56,time:5,emoji:"🧆",desc:"Homemade hummus (or bought) with raw veg and bread. Cheap and nutrient-dense.",ing:["½ tin chickpeas, blended with tahini/lemon/garlic","Carrot sticks","Cucumber sticks","Capsicum slices","Wholegrain bread or crackers"],steps:["Blend chickpeas with 1 tbsp tahini, lemon, garlic, salt, splash of water","Serve with veg and bread for dipping"],n:{cal:340,protein:12,fibre:10,vitA:350,vitC:30,vitD:0,vitK:15,folate:100,vitB12:0,choline:25,calcium:70,iron:3,magnesium:50,zinc:1.5,potassium:400,selenium:5,iodine:3,omega3:0.05},tags:["quick","no-cook","vegan","kid-friendly"]},
  {id:"c2",name:"Chicken & Lentil Soup",type:"lunch",cost:1.56,time:40,emoji:"🐔",desc:"Shredded chicken + lentil soup. Serves 6.",ing:["500g chicken thigh","200g lentils","2 carrots, 2 potatoes","Onion, garlic, stock","Spinach, turmeric, cumin"],steps:["Brown chicken, add veg+spices","Add lentils, stock, simmer 25 min","Shred chicken, add spinach"],n:{cal:420,protein:28,fibre:10,vitA:600,vitC:20,vitD:5,vitK:100,folate:150,vitB12:0.4,choline:80,calcium:60,iron:4.5,magnesium:70,zinc:3,potassium:700,selenium:20,iodine:8,omega3:0.1},tags:["batch-cook","freezer","kid-friendly","chicken"]},
  {id:"hl3",name:"Liver Sausage Rolls",type:"lunch",cost:1.95,time:40,emoji:"🥟",desc:"Hidden liver in pastry. Perfect lunchboxes. Makes 12.",ing:["300g mince","100g beef liver, minced","Onion, carrot, grated","Egg, breadcrumbs, herbs","2 sheets puff pastry"],steps:["Mix mince, liver, veg, egg, crumbs","Shape along pastry","Roll, seal, cut into 12","Egg wash, bake 200°C 25 min"],n:{cal:280,protein:14,fibre:1,vitA:800,vitC:5,vitD:5,vitK:5,folate:60,vitB12:8,choline:90,calcium:20,iron:2.5,magnesium:20,zinc:2.5,potassium:200,selenium:10,iodine:5,omega3:0.03},tags:["batch-cook","freezer","kid-friendly","hidden-nutrients","organ-meat"]},
  {id:"d1",name:"Lentil Potato Curry",type:"dinner",cost:1.82,time:40,emoji:"🍛",desc:"One-pot curry. Serves 6.",ing:["250g lentils","4 potatoes","Onion, garlic, ginger","Tin tomatoes, spinach","Curry spices"],steps:["Cook onion+spices","Add potatoes, lentils, tomatoes","Simmer 25 min","Add spinach"],n:{cal:380,protein:18,fibre:14,vitA:700,vitC:35,vitD:0,vitK:180,folate:200,vitB12:0,choline:45,calcium:80,iron:4.5,magnesium:90,zinc:2.5,potassium:900,selenium:8,iodine:5,omega3:0.1},tags:["freezer","vegan","pregnancy-safe"]},
  {id:"d2",name:"Sardine Pasta",type:"dinner",cost:2.08,time:20,emoji:"🍝",desc:"Sardines+tomato+cabbage pasta. Serves 2.",ing:["200g pasta","Tin sardines","Tin tomatoes","Cabbage, garlic"],steps:["Cook pasta+cabbage","Make sauce","Add sardines, toss"],n:{cal:550,protein:30,fibre:10,vitA:60,vitC:40,vitD:250,vitK:65,folate:60,vitB12:8.9,choline:80,calcium:280,iron:4,magnesium:80,zinc:2.5,potassium:600,selenium:35,iodine:30,omega3:1.2},tags:["quick","omega-3","sardine"]},
  {id:"d3",name:"Liver Stir-Fry",type:"dinner",cost:1.95,time:20,emoji:"🥩",desc:"Most nutrient-dense dinner. Serves 4.",ing:["400g chicken liver","2 onions","Soy sauce, cumin","Rice, broccoli"],steps:["Cook onions","Sear liver 2 min/side","Add soy sauce","Serve with rice+broccoli"],n:{cal:480,protein:35,fibre:6,vitA:5600,vitC:55,vitD:15,vitK:130,folate:400,vitB12:60,choline:340,calcium:60,iron:9,magnesium:50,zinc:4,potassium:500,selenium:25,iodine:15,omega3:0.1},tags:["organ-meat"]},
  {id:"d6",name:"Hidden Liver Bolognese",type:"dinner",cost:2.34,time:55,emoji:"🍝",desc:"Kids can't detect liver. Serves 6.",ing:["300g beef mince","150g liver, minced","Onion, carrots","2 tins tomatoes","Herbs"],steps:["Cook veg","Brown mince+liver","Add tomatoes, simmer 30 min"],n:{cal:520,protein:32,fibre:8,vitA:1050,vitC:30,vitD:10,vitK:20,folate:160,vitB12:15,choline:170,calcium:60,iron:5.5,magnesium:50,zinc:4.5,potassium:600,selenium:18,iodine:10,omega3:0.1},tags:["freezer","kid-friendly","hidden-nutrients"]},
  {id:"c1",name:"Chicken Tray Bake",type:"dinner",cost:2.86,time:45,emoji:"🍗",desc:"Roasted thighs with veg. Serves 4.",ing:["8 chicken thighs","Potatoes, carrots, onions","Paprika, cumin"],steps:["Toss veg with spices","Top with chicken","Roast 200°C 40 min"],n:{cal:480,protein:35,fibre:5,vitA:500,vitC:25,vitD:10,vitK:8,folate:30,vitB12:0.5,choline:100,calcium:30,iron:2,magnesium:55,zinc:3,potassium:700,selenium:22,iodine:10,omega3:0.1},tags:["kid-friendly","chicken"]},
  {id:"c3",name:"Chicken Curry",type:"dinner",cost:2.34,time:35,emoji:"🍛",desc:"Budget chicken curry. Serves 4.",ing:["600g chicken thigh","Tin tomatoes","Onion, garlic, ginger","Spinach, curry spices"],steps:["Cook onion+spices","Seal chicken","Simmer 20 min","Add spinach"],n:{cal:450,protein:32,fibre:4,vitA:400,vitC:20,vitD:5,vitK:90,folate:80,vitB12:0.4,choline:90,calcium:60,iron:3,magnesium:55,zinc:3,potassium:550,selenium:22,iodine:8,omega3:0.1},tags:["freezer","chicken"]},
  {id:"d4",name:"Bean & Veg Stew",type:"dinner",cost:1.56,time:40,emoji:"🫘",desc:"Plant-based stew. Serves 6.",ing:["2 tins beans","Tin tomatoes","Potatoes, carrots","Spinach, paprika"],steps:["Cook onion+spices","Add veg, beans, tomatoes","Simmer 25 min","Add spinach"],n:{cal:340,protein:16,fibre:14,vitA:700,vitC:40,vitD:0,vitK:150,folate:180,vitB12:0,choline:40,calcium:100,iron:4.5,magnesium:80,zinc:2,potassium:800,selenium:5,iodine:5,omega3:0.1},tags:["freezer","vegan"]},
  {id:"hl1",name:"Hidden Liver Meatballs",type:"dinner",cost:2.08,time:40,emoji:"🫕",desc:"20% liver in meatballs. Makes 20.",ing:["400g mince","100g liver","Egg, oats, onion","Tomato sauce"],steps:["Mix mince+liver+egg+oats","Roll 20 balls","Brown, simmer in sauce"],n:{cal:440,protein:30,fibre:4,vitA:1800,vitC:20,vitD:8,vitK:10,folate:130,vitB12:18,choline:180,calcium:30,iron:5,magnesium:35,zinc:5,potassium:500,selenium:18,iodine:8,omega3:0.05},tags:["freezer","kid-friendly","hidden-nutrients","organ-meat"]},
  {id:"hl2",name:"Liver Cottage Pie",type:"dinner",cost:2.21,time:60,emoji:"🥧",desc:"Liver hidden under mash. Serves 6.",ing:["400g mince","100g liver","Carrots, peas","Tin tomatoes","Mash topping"],steps:["Cook veg, brown meat+liver","Simmer with tomatoes","Top with mash, bake 25 min"],n:{cal:460,protein:28,fibre:6,vitA:1500,vitC:25,vitD:8,vitK:15,folate:120,vitB12:14,choline:160,calcium:50,iron:4.5,magnesium:55,zinc:4.5,potassium:800,selenium:16,iodine:8,omega3:0.05},tags:["freezer","kid-friendly","hidden-nutrients","organ-meat"]},
  {id:"bh1",name:"Heart Stir-Fry",type:"dinner",cost:2.08,time:20,emoji:"💪",desc:"Beef heart sliced thin. Tastes like steak.",ing:["400g heart","Onion, cabbage, capsicum","Soy, sesame oil, ginger"],steps:["Sear heart 1-2 min","Stir-fry veg","Return heart, add sauce"],n:{cal:420,protein:32,fibre:4,vitA:300,vitC:30,vitD:3,vitK:40,folate:15,vitB12:9,choline:140,calcium:15,iron:6,magnesium:30,zinc:3,potassium:350,selenium:28,iodine:8,omega3:0.05},tags:["quick","organ-meat"]},
  {id:"bh2",name:"Heart Bean Chilli",type:"dinner",cost:1.82,time:45,emoji:"🌶️",desc:"Heart minced into chilli. Serves 6.",ing:["500g heart, minced","2 tins beans","Tin tomatoes","Cumin, paprika, chilli"],steps:["Cook onion+spices","Brown heart","Add tomatoes+beans","Simmer 30 min"],n:{cal:400,protein:30,fibre:12,vitA:100,vitC:20,vitD:3,vitK:10,folate:100,vitB12:8,choline:130,calcium:70,iron:7,magnesium:80,zinc:4,potassium:800,selenium:25,iodine:8,omega3:0.05},tags:["freezer","organ-meat","hidden-nutrients"]},
  {id:"bh3",name:"Heart+Liver Burger",type:"dinner",cost:1.69,time:25,emoji:"🍔",desc:"50% heart, 30% mince, 20% liver. Makes 8.",ing:["250g heart","150g mince","100g liver","Onion, egg, crumbs"],steps:["Mix all meat+binders","Shape 8 patties","Cook 3-4 min/side"],n:{cal:380,protein:28,fibre:1,vitA:2000,vitC:5,vitD:5,vitK:5,folate:100,vitB12:20,choline:200,calcium:15,iron:7,magnesium:30,zinc:4.5,potassium:350,selenium:22,iodine:8,omega3:0.05},tags:["freezer","kid-friendly","organ-meat","hidden-nutrients"]},
  {id:"m1",name:"Shakshuka",type:"dinner",cost:1.69,time:20,emoji:"🇮🇱",desc:"Eggs in spiced tomato sauce. Serves 2.",ing:["4 eggs","Tin tomatoes","Onion, spinach","Paprika, cumin","Bread"],steps:["Cook onion+spices","Add tomatoes+spinach","Crack eggs in","Cover 5-7 min"],n:{cal:380,protein:18,fibre:5,vitA:280,vitC:30,vitD:80,vitK:130,folate:120,vitB12:0.8,choline:200,calcium:100,iron:3.5,magnesium:55,zinc:2,potassium:500,selenium:14,iodine:25,omega3:0.1},tags:["quick"]},
  {id:"a4",name:"Peanut Noodles",type:"dinner",cost:1.56,time:20,emoji:"🥜",desc:"peanut butter sauce noodles + veg. Serves 2.",ing:["200g noodles","Cabbage, carrots, spinach","peanut butter, soy, vinegar"],steps:["Cook noodles","Whisk peanut butter sauce","Toss with veg"],n:{cal:520,protein:20,fibre:8,vitA:700,vitC:28,vitD:0,vitK:120,folate:100,vitB12:0,choline:35,calcium:80,iron:3,magnesium:90,zinc:2,potassium:550,selenium:8,iodine:5,omega3:0.1},tags:["quick","kid-friendly","vegan"]},
  {id:"i1",name:"Classic Dal",type:"dinner",cost:1.04,time:30,emoji:"🇮🇳",desc:"Indian lentils. Serves 6.",ing:["300g lentils","Onion, garlic, ginger","Tomatoes, garam masala"],steps:["Boil lentils 20 min","Make tadka","Combine"],n:{cal:280,protein:17,fibre:11,vitA:50,vitC:15,vitD:0,vitK:10,folate:200,vitB12:0,choline:35,calcium:40,iron:4,magnesium:55,zinc:2,potassium:550,selenium:5,iodine:5,omega3:0.1},tags:["freezer","vegan"]},
  {id:"d7",name:"Bean Tacos",type:"dinner",cost:1.56,time:15,emoji:"🌮",desc:"Spiced beans in tortillas with cabbage, cheese, lime. Serves 4.",ing:["2 tins beans (kidney or black)","1 onion, diced","2 tsp cumin, 1 tsp paprika, chilli","8 small tortillas","Shredded cabbage, grated cheese","Lime, yoghurt or sour cream"],steps:["Cook onion 3 min, add spices","Add beans, mash roughly, cook 5 min","Warm tortillas","Load with beans, cabbage, cheese, lime"],n:{cal:360,protein:18,fibre:14,vitA:50,vitC:20,vitD:2,vitK:30,folate:160,vitB12:0.3,choline:30,calcium:200,iron:4,magnesium:65,zinc:2.5,potassium:550,selenium:5,iodine:10,omega3:0.03},tags:["quick","kid-friendly","vegetarian"]},
  {id:"d8",name:"Chickpea & Potato Bake",type:"dinner",cost:1.43,time:45,emoji:"🧆",desc:"Roasted chickpeas and potatoes with spices. One tray. Serves 4.",ing:["2 tins chickpeas, drained","4 potatoes, cubed","2 carrots, chunked","1 onion, quartered","2 tbsp oil","Cumin, paprika, turmeric, garlic powder","Frozen spinach to serve"],steps:["Preheat 200°C","Toss chickpeas, potatoes, carrots, onion with oil+spices","Spread on tray, roast 35-40 min","Serve with wilted spinach and yoghurt"],n:{cal:350,protein:14,fibre:13,vitA:400,vitC:25,vitD:0,vitK:10,folate:140,vitB12:0,choline:30,calcium:70,iron:4,magnesium:70,zinc:2,potassium:700,selenium:5,iodine:4,omega3:0.05},tags:["vegan","batch-cook"]},
  {id:"d9",name:"Sausage & Bean Casserole",type:"dinner",cost:2.34,time:35,emoji:"🫘",desc:"Cheap snags + 2 tins beans in tomato sauce. Hearty comfort food. Serves 6.",ing:["6 beef or pork sausages","2 tins beans (cannellini or mixed)","1 tin tomatoes","1 onion, diced","2 garlic cloves","1 tsp smoked paprika, 1 tsp oregano","Splash Worcestershire"],steps:["Brown sausages in pot, remove and slice","Cook onion 3 min, add garlic+spices","Add beans, tomatoes, Worcestershire","Return sliced sausages, simmer 20 min","Season and serve with bread or rice"],n:{cal:420,protein:24,fibre:10,vitA:30,vitC:12,vitD:3,vitK:8,folate:100,vitB12:0.8,choline:40,calcium:80,iron:4,magnesium:55,zinc:3,potassium:550,selenium:12,iodine:8,omega3:0.05},tags:["freezer","kid-friendly"]},
  {id:"s1",name:"Yoghurt Berry Bowl",type:"snack",cost:1.04,time:2,emoji:"🫐",desc:"Calcium + vitamin C gap-filler.",ing:["200g Greek yoghurt","Frozen berries","Seeds, honey"],steps:["Top yoghurt with berries+seeds"],n:{cal:220,protein:15,fibre:3,vitA:30,vitC:25,vitD:5,vitK:8,folate:15,vitB12:0.8,choline:20,calcium:250,iron:0.8,magnesium:40,zinc:1.5,potassium:350,selenium:8,iodine:35,omega3:0.05},tags:["quick","snack","kid-friendly"]},
  {id:"s4",name:"Orange & Seeds",type:"snack",cost:0.78,time:2,emoji:"🍊",desc:"100% vitamin C + vitamin E + zinc.",ing:["1 orange","30g mixed seeds"],steps:["Peel and eat"],n:{cal:180,protein:5,fibre:4,vitA:15,vitC:70,vitD:0,vitK:3,folate:40,vitB12:0,choline:10,calcium:55,iron:1.5,magnesium:70,zinc:2,potassium:300,selenium:10,iodine:2,omega3:0.05},tags:["quick","snack","vegan"]},
  {id:"s8",name:"Loaded Yoghurt Bowl",type:"snack",cost:1.56,time:3,emoji:"🥣",desc:"Ultimate gap-filler: calcium, omega-3, potassium.",ing:["200g yoghurt","Flaxseed","Seeds","½ banana","Honey"],steps:["Layer everything"],n:{cal:300,protein:16,fibre:5,vitA:30,vitC:12,vitD:5,vitK:5,folate:25,vitB12:0.8,choline:25,calcium:260,iron:1.2,magnesium:75,zinc:2,potassium:550,selenium:10,iodine:35,omega3:1.8},tags:["quick","snack"]},
  {id:"s7",name:"Milk + Fruit",type:"snack",cost:0.91,time:1,emoji:"🥛",desc:"Calcium + vitamin C + iodine.",ing:["250mL milk","1 piece fruit"],steps:["Pour milk, eat fruit"],n:{cal:200,protein:9,fibre:3,vitA:60,vitC:30,vitD:40,vitK:3,folate:15,vitB12:0.5,choline:20,calcium:300,iron:0.3,magnesium:30,zinc:1,potassium:500,selenium:4,iodine:35,omega3:0.05},tags:["quick","snack","kid-friendly"]},
  {id:"s2",name:"Banana PB Bites",type:"snack",cost:0.65,time:3,emoji:"🍌",desc:"Potassium + magnesium.",ing:["Banana","2 tbsp peanut butter"],steps:["Slice banana, add peanut butter"],n:{cal:250,protein:8,fibre:4,vitA:5,vitC:10,vitD:0,vitK:2,folate:25,vitB12:0,choline:15,calcium:15,iron:0.8,magnesium:65,zinc:1,potassium:550,selenium:2,iodine:2,omega3:0.05},tags:["quick","snack","kid-friendly","vegan"]},
,
  {id:"nb1",name:"Tuna & Egg Rice Bowl",type:"breakfast",cost:1.82,time:10,emoji:"🍚",desc:"Savoury breakfast bowl. High protein + omega-3.",ing:["1 cup cooked rice","Tin tuna","1 egg","Soy sauce, sesame oil","Frozen peas"],steps:["Cook rice","Drain tuna","Poach/fry egg","Microwave peas 60 sec","Layer rice, tuna, peas, egg","Drizzle soy + sesame oil"],n:{cal:460,protein:38,fibre:3,vitA:85,vitC:8,vitD:50,vitK:5,folate:55,vitB12:2.4,choline:180,calcium:55,iron:2.8,magnesium:52,zinc:1.9,potassium:480,selenium:40,iodine:20,omega3:0.9},tags:["quick","omega-3"]},
  {id:"nb6",name:"Vegan Overnight Oats",type:"breakfast",cost:1.17,time:5,emoji:"🥣",desc:"No-cook vegan oats. Prep the night before, grab in the morning.",ing:["50g rolled oats","200mL plant milk (oat/soy/almond)","1 tbsp chia seeds","½ banana, sliced","1 tbsp peanut butter or almond butter","Maple syrup or agave to taste","Optional: frozen berries"],steps:["Combine oats, plant milk and chia seeds in a jar","Stir well","Refrigerate overnight (or at least 4 hours)","Top with banana, nut butter and a drizzle of maple syrup"],n:{cal:420,protein:12,fibre:9,vitA:10,vitC:8,vitD:0,vitK:3,folate:35,vitB12:0,choline:25,calcium:180,iron:2.8,magnesium:95,zinc:1.8,potassium:580,selenium:5,iodine:2,omega3:1.8},tags:["quick","vegan","kid-friendly"]},
  {id:"vb1",name:"Tofu Scramble",type:"breakfast",cost:1.56,time:10,emoji:"🍳",desc:"Vegan scrambled eggs. Turmeric gives it that yellow colour and an iron boost.",ing:["200g firm tofu","½ tsp turmeric","¼ tsp cumin","Handful spinach","2 mushrooms, sliced","Soy sauce","Toast"],steps:["Crumble tofu into a hot pan with a little oil","Add turmeric, cumin, soy sauce — stir well","Add mushrooms, cook 3 min","Add spinach, cook 1 min","Serve on toast"],n:{cal:320,protein:20,fibre:4,vitA:120,vitC:8,vitD:0,vitK:130,folate:65,vitB12:0,choline:35,calcium:200,iron:3.8,magnesium:55,zinc:1.8,potassium:420,selenium:12,iodine:3,omega3:0.3},tags:["quick","vegan","high-protein"]},
  {id:"vb2",name:"Chia Pudding",type:"breakfast",cost:1.04,time:3,emoji:"🫙",desc:"Set-and-forget breakfast. Huge omega-3 hit. Make 3 days ahead.",ing:["3 tbsp chia seeds","250mL plant milk","1 tsp vanilla","1 tsp maple syrup","Frozen berries to top"],steps:["Mix chia seeds, plant milk, vanilla and maple syrup in a jar","Stir well, leave 5 min, stir again","Refrigerate overnight","Top with berries to serve"],n:{cal:280,protein:9,fibre:11,vitA:10,vitC:15,vitD:0,vitK:3,folate:25,vitB12:0,choline:20,calcium:250,iron:2.5,magnesium:90,zinc:1.5,potassium:380,selenium:4,iodine:2,omega3:4.2},tags:["quick","vegan","no-cook","kid-friendly"]},
  {id:"vb3",name:"Avocado & Seed Toast",type:"breakfast",cost:1.43,time:5,emoji:"🥑",desc:"Vegan calcium + iron + healthy fat. Better than cafe avo toast.",ing:["2 slices wholegrain toast","½ avocado","1 tbsp mixed seeds (sunflower, pumpkin, sesame)","Lemon juice","Chilli flakes, salt and pepper"],steps:["Toast bread","Mash avo with lemon, salt, chilli","Spread on toast","Top generously with seeds"],n:{cal:380,protein:10,fibre:9,vitA:15,vitC:12,vitD:0,vitK:20,folate:90,vitB12:0,choline:25,calcium:75,iron:2.8,magnesium:80,zinc:2.2,potassium:580,selenium:12,iodine:2,omega3:0.2},tags:["quick","vegan","no-cook"]},
  {id:"vb4",name:"Berry Smoothie Bowl",type:"breakfast",cost:1.3,time:5,emoji:"🫐",desc:"Thick blended smoothie you eat with a spoon. Toppings add crunch and nutrients.",ing:["1 frozen banana","1 cup frozen mixed berries","3 tbsp plant milk (just enough to blend)","Toppings: seeds, oats, coconut flakes, fresh fruit"],steps:["Blend banana and berries with a splash of plant milk until thick","Pour into a bowl — it should be thicker than a smoothie","Top with seeds, oats and fresh fruit"],n:{cal:310,protein:6,fibre:8,vitA:30,vitC:35,vitD:0,vitK:8,folate:45,vitB12:0,choline:15,calcium:80,iron:1.8,magnesium:60,zinc:1.2,potassium:650,selenium:4,iodine:2,omega3:0.5},tags:["quick","vegan","kid-friendly"]},
  {id:"nb2",name:"PB Banana Oats",type:"breakfast",cost:1.1,time:5,emoji:"🥜",desc:"Simple sweet oats. Vegan, high-fibre.",ing:["½ cup oats","1 cup water/milk","1 banana","1 tbsp peanut butter","Honey, cinnamon"],steps:["Cook oats in water/milk 3-4 min","Slice banana, stir half in","Top with peanut butter, honey, banana, cinnamon"],n:{cal:385,protein:11,fibre:7,vitA:12,vitC:10,vitD:0,vitK:2,folate:32,vitB12:0,choline:20,calcium:42,iron:2.2,magnesium:68,zinc:1.6,potassium:620,selenium:6,iodine:2,omega3:0.1},tags:["quick","vegan","kid-friendly"]},
  {id:"nb3",name:"Ricotta & Tomato Toast",type:"breakfast",cost:1.43,time:5,emoji:"🍅",desc:"High calcium, high protein. Light & fresh.",ing:["2 slices bread","4 tbsp ricotta","2 tomatoes, sliced","Oregano, olive oil, salt and pepper"],steps:["Toast bread","Spread ricotta","Top with tomato","Season, drizzle oil"],n:{cal:320,protein:16,fibre:5,vitA:155,vitC:25,vitD:8,vitK:12,folate:65,vitB12:0.5,choline:35,calcium:220,iron:2.1,magnesium:48,zinc:1.2,potassium:510,selenium:12,iodine:15,omega3:0.1},tags:["quick"]},
  {id:"nb4",name:"Microwave Egg Mug",type:"breakfast",cost:0.91,time:3,emoji:"☕",desc:"Fastest protein hit. Hidden spinach for kids.",ing:["2 eggs","2 tbsp milk","1 tbsp frozen spinach","2 tbsp cheese","salt and pepper"],steps:["Spray mug","Whisk eggs+milk in mug","Add spinach+half cheese","Micro 60 sec, stir, 30-45 sec","Top remaining cheese"],n:{cal:240,protein:19,fibre:0,vitA:280,vitC:3,vitD:100,vitK:25,folate:70,vitB12:1.8,choline:190,calcium:185,iron:2,magnesium:22,zinc:1.8,potassium:220,selenium:24,iodine:40,omega3:0.2},tags:["quick","hidden-nutrients","kid-friendly"]},
  {id:"nb5",name:"Canned Salmon Omelette",type:"breakfast",cost:2.02,time:8,emoji:"🐟",desc:"Highest vitamin D breakfast. Bones = calcium.",ing:["3 eggs","Tin pink salmon (with bones)","1 tbsp milk","Frozen corn","Butter"],steps:["Microwave corn 60 sec","Whisk eggs+milk","Melt butter in pan","Add egg mix","When set, add salmon+corn to half","Fold, cook 1 min"],n:{cal:390,protein:40,fibre:1,vitA:310,vitC:3,vitD:560,vitK:3,folate:85,vitB12:5.2,choline:270,calcium:260,iron:2.5,magnesium:48,zinc:2.2,potassium:580,selenium:45,iodine:35,omega3:1.8},tags:["omega-3","calcium"]},
  {id:"nl1",name:"White Bean & Tuna Salad",type:"lunch",cost:1.69,time:5,emoji:"🥗",desc:"No-cook protein lunch. High fibre.",ing:["½ tin white beans","Tin tuna","Celery, red onion","Olive oil, lemon","Parsley, salt and pepper"],steps:["Rinse beans","Mix beans, tuna, celery, onion","Dress with oil, lemon, parsley"],n:{cal:375,protein:35,fibre:9,vitA:8,vitC:6,vitD:20,vitK:10,folate:140,vitB12:2,choline:70,calcium:110,iron:4.2,magnesium:88,zinc:2.4,potassium:920,selenium:48,iodine:25,omega3:0.8},tags:["quick","omega-3"]},
  {id:"nl2",name:"Lentil & Veg Soup",type:"lunch",cost:1.17,time:30,emoji:"🥕",desc:"Budget vegan soup. Freezer-friendly. Serves 4.",ing:["1 cup red lentils","2 carrots, 2 celery","1 onion","Tin tomatoes","Stock, cumin, turmeric"],steps:["Sauté veg 5 min","Add lentils, tomatoes, stock","Simmer 20 min","Season"],n:{cal:245,protein:14,fibre:11,vitA:320,vitC:18,vitD:0,vitK:15,folate:175,vitB12:0,choline:30,calcium:72,iron:4.5,magnesium:62,zinc:1.8,potassium:740,selenium:6,iodine:4,omega3:0.1},tags:["vegan","batch-cook","freezer"]},
  {id:"nl3",name:"Sardine & Avo Rice Cakes",type:"lunch",cost:1.56,time:5,emoji:"🐟",desc:"Omega-3 + calcium snack lunch.",ing:["4 rice cakes","Tin sardines","¼ avocado","Lemon, salt and pepper, chilli","Cucumber slices"],steps:["Mash avo with lemon","Spread on cakes","Top with sardines","Add cucumber, chilli"],n:{cal:340,protein:28,fibre:4,vitA:42,vitC:5,vitD:260,vitK:12,folate:65,vitB12:7.8,choline:90,calcium:310,iron:3.1,magnesium:52,zinc:1.6,potassium:580,selenium:48,iodine:40,omega3:1.6},tags:["quick","omega-3","calcium","sardine"]},
  {id:"nl4",name:"Spiced Chickpea Wrap",type:"lunch",cost:1.43,time:10,emoji:"🌯",desc:"Vegan protein wrap. Kid-friendly spices.",ing:["1 wrap","½ tin chickpeas","Cumin, paprika","Olive oil","Lettuce, carrot, yoghurt"],steps:["Toss chickpeas with oil+spices","Cook 3-4 min until crispy","Mix yoghurt with cumin","Load wrap with lettuce, carrot, chickpeas, yoghurt"],n:{cal:385,protein:14,fibre:10,vitA:185,vitC:4,vitD:0,vitK:8,folate:145,vitB12:0.1,choline:25,calcium:125,iron:3.8,magnesium:72,zinc:2,potassium:520,selenium:8,iodine:8,omega3:0.2},tags:["quick","vegan","kid-friendly"]},
  {id:"nl5",name:"Egg & Sweet Potato Hash",type:"lunch",cost:1.76,time:20,emoji:"🍳",desc:"Vitamin A powerhouse. Serves 2.",ing:["2 sweet potatoes","4 eggs","Onion, capsicum","Olive oil","Paprika, salt and pepper"],steps:["Dice sweet potato, microwave 4-5 min","Heat oil, cook onion+capsicum 4 min","Add sweet potato+paprika, cook 3-4 min","Make 4 wells, crack eggs","Cover, cook 3-4 min"],n:{cal:320,protein:16,fibre:5,vitA:980,vitC:55,vitD:100,vitK:8,folate:90,vitB12:1.2,choline:185,calcium:90,iron:2.8,magnesium:52,zinc:1.5,potassium:820,selenium:22,iodine:35,omega3:0.2},tags:["kid-friendly"]},
  {id:"nd1",name:"Chicken & Veg Congee",type:"dinner",cost:1.56,time:40,emoji:"🍲",desc:"Asian comfort food. Batch-cook. Serves 4.",ing:["1 cup rice","6 cups chicken stock","300g chicken thigh","Carrots, peas","Garlic, ginger, soy, sesame","Spring onions"],steps:["Boil rice, stock, chicken, garlic, ginger 25-30 min","Remove chicken, shred","Add carrot, peas, cook 5 min","Return chicken, add soy","Serve with sesame oil, spring onion"],n:{cal:310,protein:24,fibre:4,vitA:280,vitC:14,vitD:12,vitK:10,folate:62,vitB12:0.5,choline:65,calcium:55,iron:2.2,magnesium:48,zinc:2,potassium:620,selenium:18,iodine:8,omega3:0.2},tags:["batch-cook","freezer","kid-friendly","chicken"]},
  {id:"nd2",name:"Black Bean Quesadillas",type:"dinner",cost:1.37,time:15,emoji:"🫘",desc:"Vegan calcium + fibre. Kid-friendly. Serves 2.",ing:["4 wraps","Tin black beans","½ cup cheese","Frozen corn","Cumin, paprika, salt and pepper"],steps:["Mash beans with spices","Spread on 2 wraps","Top with corn+cheese","Place 2nd wrap on top","Cook 2-3 min/side in dry pan","Cut into wedges"],n:{cal:510,protein:20,fibre:13,vitA:65,vitC:3,vitD:8,vitK:5,folate:190,vitB12:0.2,choline:28,calcium:280,iron:4.8,magnesium:88,zinc:2.4,potassium:740,selenium:10,iodine:12,omega3:0.2},tags:["quick","kid-friendly","vegetarian"]},
  {id:"nd3",name:"Baked Eggs in Tomato",type:"dinner",cost:1.49,time:20,emoji:"🍳",desc:"Shakshuka-style. Easy dinner for 2.",ing:["4 eggs","Tin crushed tomatoes","Onion, garlic","Cumin, paprika, chilli","Bread","Optional feta"],steps:["Sauté onion","Add garlic+spices","Add tomatoes, simmer 5 min","Make 4 wells, crack eggs","Cover, cook 4-5 min","Top with feta if using"],n:{cal:355,protein:20,fibre:5,vitA:380,vitC:22,vitD:100,vitK:15,folate:115,vitB12:1.2,choline:200,calcium:145,iron:3.8,magnesium:58,zinc:2,potassium:720,selenium:26,iodine:45,omega3:0.3},tags:["quick","kid-friendly"]},
  {id:"nd4",name:"Tuna Fried Rice",type:"dinner",cost:1.43,time:15,emoji:"🍚",desc:"Leftover rice + tuna. Quick dinner for 2.",ing:["2 cups cooked rice","Tin tuna","2 eggs","Peas+corn mix","Garlic, soy, sesame oil"],steps:["Heat oil in wok","Add garlic 30 sec","Add rice, stir-fry 2 min","Push aside, scramble eggs","Add tuna+veg, stir-fry 2 min","Add soy+sesame oil"],n:{cal:420,protein:34,fibre:4,vitA:95,vitC:8,vitD:40,vitK:8,folate:68,vitB12:2.8,choline:160,calcium:65,iron:2.6,magnesium:52,zinc:1.8,potassium:540,selenium:42,iodine:28,omega3:0.8},tags:["quick","omega-3","kid-friendly"]},
  {id:"nd5",name:"Split Pea & Ham Soup",type:"dinner",cost:1.23,time:60,emoji:"🍖",desc:"Budget classic. Batch-cook. Serves 6.",ing:["500g split peas","Ham hock or bacon","Carrots, celery, onion","Garlic, bay leaves","8 cups water"],steps:["Combine all in pot","Boil, then simmer 60-90 min","Remove hock, shred meat, return","Season","Thickens when cool"],n:{cal:310,protein:22,fibre:14,vitA:265,vitC:6,vitD:0,vitK:10,folate:155,vitB12:0.3,choline:40,calcium:58,iron:3.2,magnesium:72,zinc:2.2,potassium:780,selenium:12,iodine:8,omega3:0.1},tags:["batch-cook","freezer"]},
  {id:"nd6",name:"Hidden Liver Shepherd's Pie",type:"dinner",cost:1.89,time:50,emoji:"🥧",desc:"20% liver hidden in lamb. Serves 6.",ing:["500g lamb mince","150g chicken liver, minced","800g potatoes","Carrots, peas, onion, garlic","Tomato paste, stock","Butter+milk for mash"],steps:["Boil potatoes, mash with butter+milk","Brown lamb+liver together","Add veg, tomato paste, stock","Simmer 10 min, add peas","Transfer to dish, top with mash","Rough up surface, bake 200°C 20 min"],n:{cal:390,protein:30,fibre:5,vitA:4200,vitC:22,vitD:20,vitK:15,folate:185,vitB12:12.5,choline:180,calcium:68,iron:7.2,magnesium:62,zinc:5.8,potassium:880,selenium:22,iodine:12,omega3:0.3},tags:["freezer","batch-cook","hidden-nutrients","organ-meat"]},
  {id:"nd7",name:"Chickpea & Spinach Curry",type:"dinner",cost:1.37,time:25,emoji:"🍛",desc:"Vegan iron bomb. Serves 4.",ing:["2 tins chickpeas","Tin tomatoes","Coconut milk","Frozen spinach","Onion, garlic, ginger","Cumin, coriander, turmeric, garam masala, chilli"],steps:["Cook onion 5 min","Add garlic, ginger, spices 1 min","Add tomatoes, coconut milk","Add chickpeas, simmer 10 min","Add spinach, cook 2-3 min","Season"],n:{cal:420,protein:15,fibre:12,vitA:620,vitC:20,vitD:0,vitK:85,folate:185,vitB12:0,choline:35,calcium:145,iron:5.8,magnesium:85,zinc:2.2,potassium:860,selenium:8,iodine:5,omega3:0.3},tags:["vegan","batch-cook","freezer"]},
  {id:"ns1",name:"Boiled Eggs & Veggies",type:"snack",cost:0.98,time:10,emoji:"🥚",desc:"Simple protein snack with veggie sticks.",ing:["2 eggs","Carrot sticks","Celery sticks","Optional hummus"],steps:["Boil eggs 7-8 min","Transfer to cold water, peel","Serve with veg sticks"],n:{cal:195,protein:14,fibre:3,vitA:590,vitC:8,vitD:100,vitK:12,folate:75,vitB12:1.2,choline:190,calcium:85,iron:1.9,magnesium:28,zinc:1.4,potassium:390,selenium:24,iodine:40,omega3:0.2},tags:["quick","snack","kid-friendly"]},
  {id:"ns2",name:"Pumpkin Seeds & Fruit",type:"snack",cost:0.78,time:1,emoji:"🎃",desc:"Zinc + magnesium + iron powerhouse.",ing:["3 tbsp pumpkin seeds","2 tbsp raisins","Optional dark chocolate square"],steps:["Combine in container","Eat"],n:{cal:220,protein:8,fibre:2,vitA:5,vitC:1,vitD:0,vitK:2,folate:18,vitB12:0,choline:8,calcium:22,iron:3.2,magnesium:98,zinc:2.8,potassium:340,selenium:6,iodine:1,omega3:0.1},tags:["quick","snack","vegan"]},
  {id:"ns3",name:"Cottage Cheese & Pineapple",type:"snack",cost:0.91,time:2,emoji:"🍍",desc:"Retro classic. High protein + calcium.",ing:["½ cup cottage cheese","½ cup tinned pineapple","Cinnamon"],steps:["Spoon cottage cheese in bowl","Top with pineapple","Sprinkle cinnamon"],n:{cal:155,protein:14,fibre:1,vitA:25,vitC:10,vitD:4,vitK:1,folate:22,vitB12:0.6,choline:22,calcium:110,iron:0.5,magnesium:18,zinc:0.9,potassium:260,selenium:8,iodine:18,omega3:0.1},tags:["quick","snack","kid-friendly"]},,
  {id:"b59",name:"Baked Beans on Toast",type:"breakfast",cost:0.85,time:5,emoji:"🫘",desc:"Classic Aussie brekkie. Budget staple.",ing:["½ tin baked beans","2 slices bread","Butter","salt and pepper, hot sauce"],steps:["Toast bread, butter","Heat beans 90 sec microwave","Pile on toast","Season"],n:{cal:310,protein:14,fibre:12,vitA:12,vitC:2,vitD:0,vitK:3,folate:85,vitB12:0,choline:25,calcium:80,iron:3.2,magnesium:58,zinc:1.4,potassium:580,selenium:5,iodine:5,omega3:0.1},tags:["quick","kid-friendly","budget"]},
  {id:"b60",name:"Cheese & Egg Toastie",type:"breakfast",cost:1.23,time:8,emoji:"🧀",desc:"Melted cheese + scrambled eggs. Protein bomb.",ing:["2 slices bread","2 eggs","40g cheese","Butter, salt and pepper"],steps:["Scramble eggs","Toast bread","Pile eggs on toast, top cheese","Press in hot pan 30sec/side to melt"],n:{cal:450,protein:28,fibre:3,vitA:280,vitC:0,vitD:100,vitK:3,folate:68,vitB12:1.4,choline:205,calcium:340,iron:2.8,magnesium:32,zinc:2.4,potassium:240,selenium:26,iodine:45,omega3:0.2},tags:["quick","calcium","kid-friendly"]},
  {id:"b61",name:"Cheesy Baked Beans & Egg",type:"breakfast",cost:1.43,time:10,emoji:"🍳",desc:"Ultimate protein breakfast. Aussie classic.",ing:["½ tin beans","2 eggs","30g cheese","2 toast","Butter, salt and pepper"],steps:["Heat beans","Fry/poach eggs","Toast bread, butter","Pile beans, eggs, cheese on toast"],n:{cal:520,protein:32,fibre:12,vitA:240,vitC:2,vitD:100,vitK:5,folate:110,vitB12:1.4,choline:210,calcium:320,iron:4.5,magnesium:68,zinc:2.8,potassium:720,selenium:28,iodine:50,omega3:0.2},tags:["calcium","iron","kid-friendly"]},
  {id:"b62",name:"Cheese & Tomato Omelette",type:"breakfast",cost:1.37,time:8,emoji:"🍅",desc:"Quick protein breakfast.",ing:["3 eggs","1 tomato, diced","40g cheese","Milk, butter, herbs"],steps:["Whisk eggs+milk","Melt butter in pan","Pour eggs, add tomato+cheese when set","Fold, cook 1 min"],n:{cal:420,protein:30,fibre:1,vitA:380,vitC:12,vitD:120,vitK:8,folate:88,vitB12:2.2,choline:215,calcium:380,iron:2.5,magnesium:28,zinc:2.6,potassium:360,selenium:32,iodine:55,omega3:0.3},tags:["quick","calcium"]},
  {id:"b63",name:"Mega Breakfast Burrito",type:"breakfast",cost:1.56,time:10,emoji:"🌯",desc:"Freezer-friendly breakfast. Make 5, freeze 4.",ing:["1 wrap","2 eggs","¼ tin beans","30g cheese","Salsa"],steps:["Scramble eggs","Warm beans","Layer eggs, beans, cheese in wrap","Roll tight","Toast in pan for crispy exterior","Wrap in foil, freeze up to 2 months"],n:{cal:520,protein:30,fibre:10,vitA:240,vitC:3,vitD:100,vitK:5,folate:125,vitB12:1.4,choline:205,calcium:320,iron:4.2,magnesium:78,zinc:2.6,potassium:620,selenium:28,iodine:50,omega3:0.2},tags:["freezer","batch-cook"]},
  {id:"l64",name:"Greek-Style Chickpea Salad",type:"lunch",cost:1.23,time:10,emoji:"🥗",desc:"Vegan salad. Serves 2. Batch-friendly.",ing:["Tin chickpeas","Cucumber, tomato, onion","Olive oil, lemon, oregano","Optional feta"],steps:["Combine veg + chickpeas","Dress with oil, lemon, oregano","Season","Top with feta if using"],n:{cal:320,protein:12,fibre:10,vitA:85,vitC:22,vitD:0,vitK:15,folate:145,vitB12:0,choline:30,calcium:85,iron:3.5,magnesium:62,zinc:1.8,potassium:580,selenium:8,iodine:5,omega3:0.2},tags:["vegan","batch-cook","quick"]},
  {id:"l65",name:"Chicken Caesar-ish Salad",type:"lunch",cost:1.89,time:15,emoji:"🥬",desc:"High protein salad. Serves 2.",ing:["300g cooked chicken","Lettuce","40g parmesan","Bread cubes for croutons","Yoghurt, lemon, garlic dressing"],steps:["Mix yoghurt, lemon, garlic, half parmesan","Toss lettuce with dressing","Top chicken, croutons, parmesan"],n:{cal:380,protein:32,fibre:3,vitA:120,vitC:8,vitD:16,vitK:12,folate:65,vitB12:0.6,choline:80,calcium:320,iron:2,magnesium:48,zinc:2.4,potassium:520,selenium:22,iodine:25,omega3:0.2},tags:["chicken","calcium"]},
  {id:"l66",name:"Cheese & Apple Salad",type:"lunch",cost:1.1,time:5,emoji:"🍎",desc:"Sweet + savoury quick lunch.",ing:["60g cheese cubed","1 apple sliced","Lettuce","Walnuts","Oil+vinegar"],steps:["Arrange lettuce","Top apple, cheese, nuts","Drizzle dressing"],n:{cal:380,protein:16,fibre:4,vitA:180,vitC:8,vitD:8,vitK:8,folate:45,vitB12:0.6,choline:30,calcium:420,iron:1.2,magnesium:52,zinc:2.2,potassium:380,selenium:8,iodine:20,omega3:0.8},tags:["quick","calcium","kid-friendly"]},
  {id:"l67",name:"Chicken & Cabbage Slaw",type:"lunch",cost:1.69,time:12,emoji:"🥗",desc:"High protein slaw. Serves 2.",ing:["300g chicken, shredded","¼ cabbage, shredded","Carrot, grated","Yoghurt-lemon-honey dressing"],steps:["Mix dressing","Toss cabbage + carrot","Top with chicken"],n:{cal:280,protein:28,fibre:4,vitA:420,vitC:35,vitD:12,vitK:18,folate:68,vitB12:0.4,choline:75,calcium:95,iron:1.8,magnesium:42,zinc:2,potassium:560,selenium:20,iodine:15,omega3:0.2},tags:["chicken","batch-cook","quick"]},
  {id:"l68",name:"Cheesy Pasta Salad",type:"lunch",cost:1.43,time:20,emoji:"🍝",desc:"Kid-friendly pasta salad. Serves 4.",ing:["300g pasta","100g cheese cubed","Frozen peas","Tomatoes","Mayo-lemon dressing"],steps:["Cook pasta, cool","Mix mayo + lemon","Combine pasta, cheese, peas, tomato","Toss with dressing"],n:{cal:380,protein:16,fibre:5,vitA:95,vitC:12,vitD:4,vitK:8,folate:68,vitB12:0.4,choline:32,calcium:240,iron:2.2,magnesium:48,zinc:1.6,potassium:320,selenium:12,iodine:18,omega3:0.1},tags:["calcium","kid-friendly","batch-cook"]},
  {id:"l69",name:"Chicken & Bean Salad",type:"lunch",cost:1.62,time:10,emoji:"🍗",desc:"Protein + fibre salad. Serves 2.",ing:["200g chicken diced","Tin white beans","Cherry tomatoes","Red onion","Oil+vinegar, parsley"],steps:["Combine beans, chicken, tomato, onion","Dress with oil+vinegar","Season, garnish parsley"],n:{cal:420,protein:32,fibre:10,vitA:85,vitC:18,vitD:8,vitK:12,folate:125,vitB12:0.3,choline:70,calcium:95,iron:4.2,magnesium:78,zinc:2.4,potassium:820,selenium:22,iodine:12,omega3:0.3},tags:["chicken","batch-cook"]},
  {id:"l70",name:"Grilled Cheese & Tomato",type:"lunch",cost:0.98,time:8,emoji:"🧀",desc:"Classic grilled cheese with tomato.",ing:["2 slices bread","60g cheese","1 tomato sliced","Butter, salt and pepper"],steps:["Butter outside of bread","Layer cheese + tomato inside","Cook 3 min/side in pan until golden"],n:{cal:380,protein:18,fibre:4,vitA:220,vitC:14,vitD:8,vitK:8,folate:52,vitB12:0.6,choline:35,calcium:420,iron:1.8,magnesium:38,zinc:2,potassium:280,selenium:12,iodine:22,omega3:0.1},tags:["quick","calcium","kid-friendly"]},
  {id:"l71",name:"Chicken & Cheese Quesadilla",type:"lunch",cost:1.76,time:10,emoji:"🌮",desc:"Quick protein lunch.",ing:["2 wraps","150g chicken shredded","50g cheese","Salsa","Cumin, paprika"],steps:["Season chicken with spices","Layer chicken+cheese on wrap","Top with salsa, second wrap","Cook 2-3 min/side","Cut into wedges"],n:{cal:580,protein:42,fibre:4,vitA:120,vitC:4,vitD:12,vitK:5,folate:65,vitB12:0.5,choline:85,calcium:380,iron:2.8,magnesium:58,zinc:3.2,potassium:480,selenium:24,iodine:28,omega3:0.2},tags:["quick","chicken","calcium","kid-friendly"]},
  {id:"d72",name:"Beef Mince Tacos",type:"dinner",cost:1.89,time:20,emoji:"🌮",desc:"Classic tacos. Serves 4.",ing:["500g beef mince","Onion","Cumin, paprika, chilli","Tin tomatoes","Taco shells, toppings"],steps:["Brown mince","Add onion, cook 3 min","Add spices, cook 1 min","Add tomatoes, simmer 10 min","Serve in shells with toppings"],n:{cal:420,protein:28,fibre:5,vitA:65,vitC:12,vitD:8,vitK:5,folate:45,vitB12:2.2,choline:75,calcium:85,iron:4.2,magnesium:48,zinc:5.5,potassium:620,selenium:18,iodine:8,omega3:0.1},tags:["kid-friendly","quick","batch-cook"]},
  {id:"d73",name:"Beef Mince & Potato Bake",type:"dinner",cost:2.02,time:50,emoji:"🥔",desc:"Layered bake. Serves 6.",ing:["500g beef mince","800g potatoes sliced","Onion, garlic","Tin tomatoes","Stock","Cheese"],steps:["Brown mince + onion + garlic","Add tomatoes + stock, simmer 10 min","Layer potatoes, mince, potatoes in dish","Cover, bake 180°C 35 min","Top cheese, bake 10 min"],n:{cal:380,protein:24,fibre:4,vitA:48,vitC:22,vitD:4,vitK:5,folate:42,vitB12:1.8,choline:68,calcium:95,iron:3.8,magnesium:52,zinc:4.8,potassium:780,selenium:16,iodine:12,omega3:0.1},tags:["batch-cook","freezer","kid-friendly"]},
  {id:"d74",name:"Beef & Cabbage Stir-Fry",type:"dinner",cost:1.56,time:20,emoji:"🥬",desc:"Quick budget stir-fry. Serves 4.",ing:["500g beef mince","½ cabbage shredded","Carrots","Garlic, ginger","Soy, sesame oil"],steps:["Brown mince, remove","Stir-fry cabbage + carrot 4 min","Add garlic + ginger 1 min","Return mince, add soy + sesame","Toss well"],n:{cal:320,protein:26,fibre:4,vitA:380,vitC:42,vitD:4,vitK:18,folate:68,vitB12:2,choline:70,calcium:75,iron:3.5,magnesium:42,zinc:5.2,potassium:580,selenium:16,iodine:8,omega3:0.2},tags:["quick","budget"]},
  {id:"d75",name:"Whole Baked Fish",type:"dinner",cost:2.34,time:35,emoji:"🐟",desc:"Whole fish market bargain. Serves 4.",ing:["800g whole fish (snapper/bream)","Lemon sliced","Garlic","Herbs","Olive oil, salt and pepper"],steps:["Score fish 3 times each side","Stuff cavity with lemon, garlic, herbs","Rub with oil, salt and pepper","Bake 200°C 25-30 min"],n:{cal:280,protein:38,fibre:0,vitA:120,vitC:12,vitD:340,vitK:5,folate:22,vitB12:3.2,choline:85,calcium:85,iron:1.2,magnesium:48,zinc:1.4,potassium:680,selenium:42,iodine:35,omega3:1.4},tags:["omega-3","budget"]},
  {id:"d76",name:"Fish Tacos",type:"dinner",cost:2.54,time:25,emoji:"🌮",desc:"Whole fish fillets in tacos. Serves 4.",ing:["600g fish fillets","Tortillas","Cabbage","Lime","Yoghurt","Cumin, paprika"],steps:["Cut fish into strips, season","Pan-fry 2-3 min/side","Mix yoghurt + lime","Warm tortillas","Fill with cabbage, fish, sauce"],n:{cal:320,protein:28,fibre:3,vitA:32,vitC:18,vitD:240,vitK:12,folate:48,vitB12:2.4,choline:75,calcium:85,iron:1.8,magnesium:52,zinc:1.2,potassium:520,selenium:38,iodine:30,omega3:1},tags:["omega-3","quick","kid-friendly"]},
  {id:"d77",name:"Refried Beans (Dry)",type:"dinner",cost:0.78,time:150,emoji:"🫘",desc:"500g dry beans → 6 serves. Freezer gold.",ing:["500g dry pinto beans","Onion","Garlic","Cumin, paprika","Oil, salt"],steps:["Soak beans overnight","Drain, boil 60-90 min until soft","Sauté onion + garlic + spices","Add beans, mash roughly","Season","Freeze portions"],n:{cal:280,protein:16,fibre:14,vitA:8,vitC:4,vitD:0,vitK:5,folate:185,vitB12:0,choline:32,calcium:70,iron:4.5,magnesium:88,zinc:2,potassium:820,selenium:6,iodine:3,omega3:0.2},tags:["vegan","batch-cook","freezer","budget"]},
  {id:"d78",name:"Bean Burrito Bowls",type:"dinner",cost:1.49,time:35,emoji:"🥙",desc:"Vegan bowl with dry beans. Serves 4.",ing:["2 cups cooked beans (from dry)","Rice","Capsicum","Corn","Avocado","Salsa, lime"],steps:["Cook rice, cook beans","Season beans with cumin","Sauté capsicum + corn","Assemble bowls: rice, beans, veg, avo, salsa"],n:{cal:420,protein:14,fibre:14,vitA:185,vitC:55,vitD:0,vitK:12,folate:165,vitB12:0,choline:35,calcium:68,iron:4.2,magnesium:95,zinc:2,potassium:920,selenium:6,iodine:4,omega3:0.2},tags:["vegan","batch-cook"]},
  {id:"d79",name:"Chicken & Rice One-Pot",type:"dinner",cost:2.08,time:45,emoji:"🍚",desc:"Complete meal in one pot. Serves 6.",ing:["800g chicken thighs","2 cups rice","Onion, carrots, peas","Stock","Garlic, paprika, thyme"],steps:["Brown chicken, remove","Sauté onion, carrot, garlic","Add rice, stir","Add stock + spices","Return chicken, cover, simmer 25 min","Add peas, cook 5 min"],n:{cal:420,protein:32,fibre:4,vitA:320,vitC:14,vitD:16,vitK:10,folate:68,vitB12:0.5,choline:70,calcium:55,iron:2.5,magnesium:58,zinc:2.6,potassium:620,selenium:20,iodine:12,omega3:0.2},tags:["chicken","batch-cook","kid-friendly"]},
  {id:"d80",name:"Honey Garlic Chicken",type:"dinner",cost:2.34,time:35,emoji:"🍯",desc:"Sticky chicken thighs. Serves 4.",ing:["8 chicken thighs","Garlic","Honey","Soy sauce","Oil, ginger"],steps:["Mix garlic, honey, soy, ginger","Place chicken in dish, pour sauce","Bake 200°C 30-35 min, basting halfway"],n:{cal:380,protein:34,fibre:0,vitA:85,vitC:2,vitD:16,vitK:3,folate:18,vitB12:0.5,choline:75,calcium:28,iron:1.8,magnesium:42,zinc:2.8,potassium:480,selenium:22,iodine:12,omega3:0.2},tags:["chicken","kid-friendly","batch-cook"]},
  {id:"sn81",name:"Cheese & Crackers",type:"snack",cost:0.91,time:2,emoji:"🧀",desc:"Classic cheese snack.",ing:["50g cheese","6 crackers","Apple sliced","Grapes"],steps:["Arrange cheese, crackers, fruit on plate"],n:{cal:320,protein:14,fibre:3,vitA:140,vitC:5,vitD:8,vitK:3,folate:28,vitB12:0.5,choline:28,calcium:360,iron:1.2,magnesium:32,zinc:1.8,potassium:240,selenium:8,iodine:18,omega3:0.1},tags:["quick","calcium","kid-friendly"]},
  {id:"sn82",name:"Cheese & Veggie Sticks",type:"snack",cost:0.85,time:3,emoji:"🥕",desc:"Cheese cubes + veg sticks.",ing:["50g cheese cubed","Carrot sticks","Celery","Hummus"],steps:["Cut cheese into cubes","Cut veg into sticks","Serve with hummus"],n:{cal:220,protein:13,fibre:3,vitA:620,vitC:8,vitD:8,vitK:12,folate:42,vitB12:0.5,choline:30,calcium:360,iron:0.8,magnesium:28,zinc:1.8,potassium:380,selenium:8,iodine:18,omega3:0.1},tags:["quick","calcium","kid-friendly"]},
  {id:"sn83",name:"Cheese & Tomato Rice Cakes",type:"snack",cost:0.72,time:3,emoji:"🍅",desc:"Quick savoury snack.",ing:["3 rice cakes","40g cheese","Tomato sliced","Oregano, salt and pepper"],steps:["Top rice cakes with cheese","Add tomato","Season","Optional: microwave 20 sec to melt"],n:{cal:210,protein:12,fibre:2,vitA:120,vitC:8,vitD:8,vitK:5,folate:18,vitB12:0.4,choline:26,calcium:280,iron:0.8,magnesium:22,zinc:1.5,potassium:180,selenium:8,iodine:15,omega3:0.1},tags:["quick","calcium"]},
  {id:"sn84",name:"Sardine & Avocado Rice Cakes",type:"snack",cost:1.43,time:3,emoji:"🐟",desc:"Omega-3 + B12 + calcium in 3 minutes. Surprisingly good.",ing:["4 rice cakes","½ tin sardines (95g)","¼ avocado","Squeeze of lemon","Salt and pepper, chilli flakes"],steps:["Mash avo with lemon + salt","Spread on rice cakes","Top with sardine pieces","Add chilli flakes"],n:{cal:290,protein:22,fibre:4,vitA:38,vitC:5,vitD:220,vitK:10,folate:48,vitB12:7.5,choline:72,calcium:280,iron:2.4,magnesium:42,zinc:1.4,potassium:520,selenium:40,iodine:32,omega3:1.4},tags:["quick","snack","omega-3","sardine"]},
  {id:"sn85",name:"Brazil Nut Trail Mix",type:"snack",cost:0.91,time:1,emoji:"🌰",desc:"1 Brazil nut = your full day of selenium. Add seeds + dark choc.",ing:["2 Brazil nuts","2 tbsp pumpkin seeds","1 tbsp sunflower seeds","2 squares dark chocolate (70%+)","Small handful raisins"],steps:["Combine in a container or zip bag","Eat"],n:{cal:260,protein:7,fibre:4,vitA:5,vitC:0,vitD:0,vitK:4,folate:22,vitB12:0,choline:12,calcium:38,iron:3.5,magnesium:115,zinc:2.6,potassium:340,selenium:68,iodine:2,omega3:0.2},tags:["quick","snack","vegan"]},
  {id:"sn86",name:"Tuna Rice Cakes",type:"snack",cost:1.17,time:3,emoji:"🐟",desc:"High protein + selenium snack. Beats chips every time.",ing:["4 rice cakes","Tin tuna, drained","2 tbsp yoghurt or mayo","Lemon, celery, salt and pepper"],steps:["Mix tuna with yoghurt/mayo + lemon","Season with salt and pepper","Pile on rice cakes","Add diced celery for crunch"],n:{cal:240,protein:26,fibre:1,vitA:12,vitC:3,vitD:15,vitK:3,folate:12,vitB12:2.2,choline:48,calcium:55,iron:1.2,magnesium:38,zinc:1,potassium:360,selenium:38,iodine:22,omega3:0.4},tags:["quick","snack","high-protein"]},
  {id:"sn87",name:"Hummus & Veggie Dip Plate",type:"snack",cost:0.98,time:5,emoji:"🥕",desc:"Iron + folate + fibre. Vegan and kid-friendly.",ing:["4 tbsp hummus (bought or from tin chickpeas)","Carrot sticks","Celery sticks","Capsicum strips","Cucumber slices","Wholegrain crackers"],steps:["Cut veg into sticks","Serve with hummus and crackers","Optional: add za'atar or paprika on hummus"],n:{cal:220,protein:8,fibre:8,vitA:460,vitC:42,vitD:0,vitK:18,folate:95,vitB12:0,choline:22,calcium:62,iron:2.8,magnesium:48,zinc:1.2,potassium:520,selenium:5,iodine:3,omega3:0.1},tags:["quick","snack","vegan","kid-friendly"]},
  {id:"sn88",name:"Boiled Egg & Vegemite Toast",type:"snack",cost:0.85,time:8,emoji:"🥚",desc:"B12 from egg + folate from Vegemite. Classic Aussie combo.",ing:["1 egg","1 slice wholegrain toast","Vegemite","Butter"],steps:["Boil egg 7-8 min","Toast bread","Butter and spread Vegemite","Eat egg alongside or sliced on toast"],n:{cal:215,protein:11,fibre:3,vitA:65,vitC:0,vitD:50,vitK:3,folate:85,vitB12:0.8,choline:122,calcium:48,iron:2.5,magnesium:25,zinc:1.2,potassium:180,selenium:12,iodine:22,omega3:0.05},tags:["quick","snack","kid-friendly"]},
  {id:"sn89",name:"Frozen Banana Nice Cream",type:"snack",cost:0.52,time:5,emoji:"🍌",desc:"1-ingredient ice cream. Kids go wild for it. Add peanut butter for protein.",ing:["2 bananas, frozen in chunks","Optional: 1 tbsp peanut butter","Optional: splash of milk for creamier texture"],steps:["Freeze bananas in chunks (at least 2 hours)","Blend in food processor until smooth","Add peanut butter or milk if using","Eat immediately or refreeze 20 min for firmer texture"],n:{cal:200,protein:4,fibre:5,vitA:8,vitC:22,vitD:0,vitK:2,folate:28,vitB12:0,choline:18,calcium:14,iron:0.6,magnesium:60,zinc:0.5,potassium:880,selenium:2,iodine:2,omega3:0.05},tags:["quick","snack","vegan","kid-friendly"]},
  {id:"sn90",name:"Miso Soup with Egg",type:"snack",cost:0.91,time:5,emoji:"🍜",desc:"Iodine + umami hit. Warming snack for winter.",ing:["1 tbsp miso paste","1.5 cups hot water","1 egg (soft-boiled or poached)","Spring onion","Optional: silken tofu"],steps:["Dissolve miso in hot (not boiling) water","Soft-boil egg 6-7 min or poach 3 min","Slice spring onion","Serve egg in miso broth, top with onion"],n:{cal:120,protein:9,fibre:0,vitA:65,vitC:2,vitD:50,vitK:2,folate:28,vitB12:0.6,choline:125,calcium:32,iron:1.5,magnesium:15,zinc:0.8,potassium:180,selenium:10,iodine:52,omega3:0.05},tags:["quick","snack"]},
  {id:"sn91",name:"Apple, Cheese & Walnuts",type:"snack",cost:1.1,time:3,emoji:"🍎",desc:"Omega-3 + calcium + fibre. Satisfying afternoon snack.",ing:["1 apple, sliced","40g cheddar, sliced","30g walnuts"],steps:["Slice apple and cheese","Arrange on plate with walnuts"],n:{cal:330,protein:12,fibre:4,vitA:145,vitC:8,vitD:8,vitK:3,folate:28,vitB12:0.4,choline:32,calcium:310,iron:1,magnesium:42,zinc:1.6,potassium:320,selenium:6,iodine:16,omega3:1.4},tags:["quick","snack","kid-friendly","calcium","omega-3"]},
  {id:"sn92",name:"Dates & Almond Butter",type:"snack",cost:1.04,time:2,emoji:"🌴",desc:"Iron + fibre + energy. Better than a muesli bar.",ing:["4 Medjool dates (or 8 dried)","2 tbsp almond butter","Pinch of sea salt"],steps:["Remove date pits if needed","Fill each date with almond butter","Add a pinch of salt on top"],n:{cal:280,protein:5,fibre:5,vitA:2,vitC:0,vitD:0,vitK:2,folate:15,vitB12:0,choline:12,calcium:68,iron:2.2,magnesium:55,zinc:0.8,potassium:540,selenium:2,iodine:1,omega3:0.1},tags:["quick","snack","vegan"]},
  // KANGAROO
  {id:"kg1",name:"Kangaroo Mince Bolognese",type:"dinner",cost:3.64,time:25,emoji:"🦘",desc:"Leanest red meat in Australia. Extremely high iron & zinc. Serves 2.",ing:["250g kangaroo mince","200g pasta","1 tin crushed tomatoes","1 onion, diced","3 cloves garlic","Olive oil, salt, pepper, Italian herbs"],steps:["Cook pasta per packet","Fry onion in oil 4 min","Add garlic 1 min","Add kangaroo mince, brown 5 min breaking up lumps","Add tomatoes + herbs, simmer 10 min","Serve over pasta"],n:{cal:520,protein:38,fibre:5,vitA:62,vitC:15,vitD:0,vitK:10,folate:48,vitB12:2.5,choline:68,calcium:42,iron:5.5,magnesium:72,zinc:6.5,potassium:750,selenium:30,iodine:3,omega3:0.2},tags:["kangaroo","high-protein","freezer"]},
  {id:"kg2",name:"Kangaroo Steak & Roasted Sweet Potato",type:"dinner",cost:4.16,time:30,emoji:"🦘",desc:"Highest iron dinner in the app. Don't overcook — kangaroo is best medium-rare.",ing:["180g kangaroo steak","1 large sweet potato, diced","2 handfuls spinach","2 cloves garlic","Olive oil, salt, pepper, paprika"],steps:["Preheat oven 200°C","Toss sweet potato in oil + paprika, roast 20-25 min","Season steak well","Cook in hot pan 2-3 min each side (medium-rare)","Rest steak 5 min before slicing","Wilt spinach in same pan with garlic","Serve steak over sweet potato and spinach"],n:{cal:420,protein:43,fibre:6,vitA:950,vitC:32,vitD:0,vitK:125,folate:62,vitB12:3.6,choline:92,calcium:62,iron:7.0,magnesium:78,zinc:8.0,potassium:980,selenium:32,iodine:2,omega3:0.2},tags:["kangaroo","high-protein"]},
  {id:"kg3",name:"Kangaroo Mince Tacos",type:"dinner",cost:3.38,time:20,emoji:"🦘",desc:"Better iron than beef tacos for less money. Serves 2.",ing:["250g kangaroo mince","6 small corn tortillas or taco shells","¼ cabbage, shredded","1 tomato, diced","1 lime","Cumin, paprika, garlic powder, salt","Greek yoghurt or sour cream"],steps:["Season mince with cumin, paprika, garlic powder, salt","Brown in pan 6-8 min, breaking up","Shred cabbage, dice tomato, squeeze lime over","Warm tortillas","Build tacos: mince, cabbage slaw, tomato, yoghurt"],n:{cal:480,protein:36,fibre:7,vitA:82,vitC:28,vitD:0,vitK:32,folate:56,vitB12:2.5,choline:72,calcium:56,iron:5.5,magnesium:62,zinc:6.2,potassium:680,selenium:26,iodine:4,omega3:0.2},tags:["kangaroo","kid-friendly","quick"]},
  {id:"kg4",name:"Kangaroo Burger",type:"dinner",cost:3.64,time:20,emoji:"🦘",desc:"Juicier than it sounds. Add an egg to boost nutrients further.",ing:["250g kangaroo mince","2 wholegrain burger buns","2 slices cheddar","Lettuce, tomato, beetroot (tinned fine)","1 tbsp Worcestershire sauce","Salt, pepper, garlic powder"],steps:["Mix mince with Worcestershire sauce + seasoning","Form 2 patties","Cook in pan or BBQ 4-5 min each side","Add cheese last 1 min to melt","Toast buns","Build: bun, lettuce, patty, tomato, beetroot, cheese"],n:{cal:520,protein:40,fibre:4,vitA:48,vitC:8,vitD:3,vitK:15,folate:52,vitB12:3.2,choline:108,calcium:185,iron:5.5,magnesium:58,zinc:7.2,potassium:560,selenium:28,iodine:12,omega3:0.2},tags:["kangaroo","kid-friendly"]},
];

const BOOSTS = [
  {id:"egg",label:"+Egg",amount:"1 whole egg",em:"🥚",cost:0.65,n:{cal:80,protein:6,fibre:0,vitA:45,vitC:0,vitD:40,vitK:0,folate:22,vitB12:0.5,choline:125,calcium:25,iron:0.9,magnesium:5,zinc:0.5,potassium:60,selenium:8,iodine:15,omega3:0.03}},
  {id:"cheese",label:"+Cheese",amount:"30g block",em:"🧀",cost:0.39,n:{cal:120,protein:7,fibre:0,vitA:30,vitC:0,vitD:3,vitK:1,folate:5,vitB12:0.4,choline:5,calcium:220,iron:0.2,magnesium:8,zinc:1,potassium:25,selenium:4,iodine:10,omega3:0}},
  {id:"spinach",label:"+Spinach",amount:"60g raw",em:"🥬",cost:0.2,n:{cal:12,protein:1.5,fibre:1,vitA:150,vitC:8,vitD:0,vitK:150,folate:80,vitB12:0,choline:10,calcium:40,iron:1.5,magnesium:30,zinc:0.3,potassium:200,selenium:1,iodine:1,omega3:0.05}},
  {id:"seeds",label:"+Seeds",amount:"15g / 1 tbsp",em:"🌻",cost:0.26,n:{cal:60,protein:2,fibre:1,vitA:0,vitC:0,vitD:0,vitK:0,folate:15,vitB12:0,choline:5,calcium:10,iron:0.8,magnesium:25,zinc:0.8,potassium:50,selenium:5,iodine:0,omega3:0.03}},
  {id:"flax",label:"+Flaxseed",amount:"10g / 1 tbsp",em:"🫘",cost:0.13,n:{cal:55,protein:1.5,fibre:2.5,vitA:0,vitC:0,vitD:0,vitK:0,folate:6,vitB12:0,choline:5,calcium:18,iron:0.4,magnesium:28,zinc:0.3,potassium:55,selenium:2,iodine:0,omega3:1.6}},
  {id:"milk",label:"+Milk",amount:"250mL",em:"🥛",cost:0.39,n:{cal:130,protein:7,fibre:0,vitA:50,vitC:1,vitD:35,vitK:0,folate:10,vitB12:0.5,choline:15,calcium:240,iron:0.1,magnesium:20,zinc:0.8,potassium:300,selenium:3,iodine:30,omega3:0.02}},
  {id:"banana",label:"+Banana",amount:"1 medium",em:"🍌",cost:0.52,n:{cal:105,protein:1,fibre:3,vitA:5,vitC:9,vitD:0,vitK:1,folate:20,vitB12:0,choline:10,calcium:5,iron:0.3,magnesium:27,zinc:0.15,potassium:360,selenium:1,iodine:0,omega3:0.03}},
  {id:"yoghurt",label:"+Yoghurt",amount:"150g",em:"🫙",cost:0.52,n:{cal:100,protein:8,fibre:0,vitA:10,vitC:1,vitD:2,vitK:0,folate:7,vitB12:0.4,choline:10,calcium:130,iron:0.1,magnesium:12,zinc:0.7,potassium:180,selenium:4,iodine:20,omega3:0.01}},
];

function getBoostsForRecipe(recipe) {
  const n = recipe.name.toLowerCase();
  const d = (recipe.desc || '').toLowerCase();
  const type = recipe.type;
  const all = BOOSTS.map(b => b.id);
  // Smoothies / drinks
  if (n.includes('smoothie') || n.includes('shake')) return ['spinach','flax','milk','banana','yoghurt','seeds'];
  // Oats / weet-bix / porridge
  if (n.includes('oat') || n.includes('weet-bix') || n.includes('porridge') || n.includes('nice cream')) return ['seeds','flax','milk','banana','yoghurt'];
  // Yoghurt bowls / snack bowls
  if (n.includes('yoghurt') || (n.includes('bowl') && type === 'snack')) return ['seeds','flax','banana'];
  // Soup / stew / congee / dal / chilli
  if (n.includes('soup') || n.includes('stew') || n.includes('dal') || n.includes('congee') || n.includes('chilli') || n.includes('casserole')) return ['egg','spinach','yoghurt'];
  // Curry
  if (n.includes('curry')) return ['egg','spinach','yoghurt'];
  // Salad
  if (n.includes('salad') || n.includes('slaw')) return ['egg','cheese','seeds'];
  // Wrap / burrito / quesadilla / taco
  if (n.includes('wrap') || n.includes('burrito') || n.includes('quesadilla') || n.includes('taco')) return ['egg','cheese','spinach'];
  // Pasta / noodles / bolognese
  if (n.includes('pasta') || n.includes('noodle') || n.includes('bolognese') || n.includes('spaghetti')) return ['cheese','spinach'];
  // Stir-fry / fried rice
  if (n.includes('stir-fry') || n.includes('fried rice')) return ['egg','spinach'];
  // Toast / toastie / rice cakes
  if (n.includes('toast') || n.includes('toastie') || n.includes('rice cake')) return ['egg','cheese','spinach'];
  // Egg dishes (omelette, scramble, shakshuka, mug, baked eggs)
  if (n.includes('egg') || n.includes('omelette') || n.includes('scramble') || n.includes('shakshuka') || n.includes('frittata')) return ['cheese','spinach','milk'];
  // Rice bowls / one-pot rice
  if (n.includes('rice') && !n.includes('fried')) return ['egg','spinach'];
  // Meatballs / burger / pie / shepherd
  if (n.includes('meatball') || n.includes('burger') || n.includes('pie') || n.includes('shepherd')) return ['cheese','spinach'];
  // Trail mix / dates / nuts / seeds snack
  if (type === 'snack' && (n.includes('seed') || n.includes('nut') || n.includes('trail') || n.includes('date'))) return ['seeds','flax'];
  // Snack default
  if (type === 'snack') return ['seeds','flax','yoghurt'];
  // Breakfast default
  if (type === 'breakfast') return ['egg','seeds','flax','milk','yoghurt'];
  // Lunch default
  if (type === 'lunch') return ['egg','cheese','spinach','seeds'];
  // Dinner default
  return ['egg','cheese','spinach'];
}

const COMMON_FOODS = [
  {cat:"☕ Breakfast",items:[
    {name:"Vegemite toast (2 slices white)",cost:0.78,n:{protein:6,fibre:1.5,vitA:0,vitC:0,vitD:0,vitK:1,folate:50,vitB12:0,choline:5,calcium:30,iron:1.2,magnesium:15,zinc:0.5,potassium:80,selenium:5,iodine:5,omega3:0}},
    {name:"Coco Pops / Nutri-Grain + milk",cost:1.56,n:{protein:6,fibre:1,vitA:30,vitC:0,vitD:15,vitK:0,folate:30,vitB12:0.3,choline:10,calcium:180,iron:2.5,magnesium:20,zinc:0.8,potassium:200,selenium:4,iodine:25,omega3:0}},
    {name:"Flat white coffee",cost:6.5,n:{protein:6,fibre:0,vitA:30,vitC:0,vitD:10,vitK:0,folate:5,vitB12:0.3,choline:10,calcium:180,iron:0,magnesium:15,zinc:0.5,potassium:200,selenium:2,iodine:20,omega3:0}},
    {name:"Sausage McMuffin",cost:8.45,n:{protein:15,fibre:1,vitA:20,vitC:1,vitD:5,vitK:2,folate:15,vitB12:0.5,choline:40,calcium:100,iron:2,magnesium:20,zinc:1.5,potassium:180,selenium:10,iodine:10,omega3:0.02}},
    {name:"Up & Go (chocolate)",cost:3.25,n:{protein:8,fibre:2,vitA:75,vitC:5,vitD:25,vitK:2,folate:50,vitB12:0.5,choline:10,calcium:300,iron:1.5,magnesium:25,zinc:1,potassium:200,selenium:3,iodine:15,omega3:0}},
  ]},
  {cat:"🥪 Lunch",items:[
    {name:"Bakery meat pie",cost:7.8,n:{protein:12,fibre:1,vitA:10,vitC:1,vitD:2,vitK:3,folate:10,vitB12:0.5,choline:20,calcium:30,iron:2,magnesium:15,zinc:1.5,potassium:150,selenium:8,iodine:5,omega3:0.02}},
    {name:"Ham & cheese sandwich (white)",cost:5.2,n:{protein:16,fibre:2,vitA:20,vitC:2,vitD:3,vitK:3,folate:20,vitB12:0.4,choline:25,calcium:150,iron:1.5,magnesium:20,zinc:1.5,potassium:180,selenium:10,iodine:12,omega3:0.02}},
    {name:"Instant noodles (Mi Goreng)",cost:1.3,n:{protein:8,fibre:2,vitA:0,vitC:0,vitD:0,vitK:0,folate:10,vitB12:0,choline:5,calcium:15,iron:2,magnesium:15,zinc:0.5,potassium:80,selenium:5,iodine:2,omega3:0}},
    {name:"Subway 6-inch (chicken)",cost:13.0,n:{protein:22,fibre:3,vitA:30,vitC:10,vitD:2,vitK:15,folate:30,vitB12:0.3,choline:30,calcium:60,iron:2,magnesium:25,zinc:1.5,potassium:250,selenium:12,iodine:8,omega3:0.03}},
    {name:"Sushi (2 rolls)",cost:10.4,n:{protein:10,fibre:2,vitA:15,vitC:2,vitD:3,vitK:5,folate:15,vitB12:1.0,choline:15,calcium:20,iron:1,magnesium:20,zinc:0.8,potassium:150,selenium:8,iodine:30,omega3:0.1}},
  ]},
  {cat:"🍕 Dinner",items:[
    {name:"Frozen pizza (⅓ pizza)",cost:4.55,n:{protein:15,fibre:2,vitA:40,vitC:3,vitD:3,vitK:5,folate:15,vitB12:0.5,choline:20,calcium:180,iron:1.5,magnesium:20,zinc:1.5,potassium:200,selenium:10,iodine:10,omega3:0.02}},
    {name:"Fish & chips (takeaway)",cost:15.6,n:{protein:25,fibre:3,vitA:5,vitC:8,vitD:15,vitK:5,folate:15,vitB12:1.0,choline:40,calcium:30,iron:1.5,magnesium:30,zinc:1,potassium:400,selenium:20,iodine:25,omega3:0.2}},
    {name:"KFC 2-piece + chips",cost:15.6,n:{protein:28,fibre:2,vitA:10,vitC:5,vitD:3,vitK:5,folate:10,vitB12:0.3,choline:50,calcium:30,iron:1.5,magnesium:25,zinc:2,potassium:350,selenium:15,iodine:8,omega3:0.05}},
    {name:"Spag bol (jar sauce + white pasta)",cost:3.9,n:{protein:22,fibre:3,vitA:30,vitC:8,vitD:2,vitK:5,folate:25,vitB12:1.0,choline:30,calcium:30,iron:3,magnesium:30,zinc:3,potassium:350,selenium:12,iodine:5,omega3:0.05}},
    {name:"2 snags in white bread",cost:3.9,n:{protein:14,fibre:1,vitA:5,vitC:1,vitD:2,vitK:2,folate:15,vitB12:0.5,choline:20,calcium:20,iron:1.5,magnesium:12,zinc:1.5,potassium:150,selenium:5,iodine:5,omega3:0.02}},
  ]},
  {cat:"🥦 Vegetables (per serve)",items:[
    {name:"Broccoli (1 cup cooked, 150g)",cost:1.04,n:{protein:3.7,fibre:5.1,vitA:120,vitC:101,vitD:0,vitK:220,folate:168,vitB12:0,choline:42,calcium:62,iron:1.0,magnesium:33,zinc:0.7,potassium:457,selenium:2.5,iodine:3,omega3:0.2}},
    {name:"Carrot (1 large raw, 100g)",cost:0.26,n:{protein:0.9,fibre:2.8,vitA:835,vitC:6,vitD:0,vitK:13,folate:19,vitB12:0,choline:8,calcium:33,iron:0.3,magnesium:12,zinc:0.2,potassium:320,selenium:0.1,iodine:2,omega3:0}},
    {name:"Spinach (1 cup raw, 30g)",cost:0.52,n:{protein:0.9,fibre:0.7,vitA:141,vitC:8,vitD:0,vitK:145,folate:58,vitB12:0,choline:5,calcium:30,iron:0.8,magnesium:24,zinc:0.2,potassium:167,selenium:0.3,iodine:3,omega3:0.04}},
    {name:"Capsicum ½ red (80g)",cost:1.04,n:{protein:0.7,fibre:1.3,vitA:157,vitC:95,vitD:0,vitK:4,folate:24,vitB12:0,choline:5,calcium:5,iron:0.4,magnesium:9,zinc:0.2,potassium:166,selenium:0.1,iodine:1,omega3:0.03}},
    {name:"Zucchini (1 medium cooked, 200g)",cost:0.78,n:{protein:2.5,fibre:2.0,vitA:40,vitC:20,vitD:0,vitK:9,folate:57,vitB12:0,choline:14,calcium:32,iron:0.7,magnesium:38,zinc:0.6,potassium:512,selenium:0.3,iodine:2,omega3:0.1}},
    {name:"Cucumber (½, 150g)",cost:0.39,n:{protein:0.7,fibre:0.5,vitA:10,vitC:3,vitD:0,vitK:17,folate:8,vitB12:0,choline:7,calcium:20,iron:0.3,magnesium:14,zinc:0.2,potassium:193,selenium:0.2,iodine:1,omega3:0.05}},
    {name:"Celery (3 stalks, 90g)",cost:0.26,n:{protein:0.4,fibre:1.2,vitA:27,vitC:3,vitD:0,vitK:25,folate:24,vitB12:0,choline:5,calcium:36,iron:0.2,magnesium:9,zinc:0.1,potassium:200,selenium:0.1,iodine:1,omega3:0.05}},
    {name:"Iceberg lettuce (2 cups, 100g)",cost:0.26,n:{protein:0.9,fibre:1.2,vitA:36,vitC:4,vitD:0,vitK:24,folate:29,vitB12:0,choline:7,calcium:19,iron:0.5,magnesium:7,zinc:0.2,potassium:141,selenium:0.4,iodine:1,omega3:0.07}},
    {name:"Tomato (1 medium, 120g)",cost:0.65,n:{protein:1.1,fibre:1.5,vitA:42,vitC:17,vitD:0,vitK:10,folate:18,vitB12:0,choline:7,calcium:12,iron:0.4,magnesium:11,zinc:0.2,potassium:237,selenium:0.1,iodine:1,omega3:0.03}},
    {name:"Kale (1 cup raw, 67g)",cost:0.78,n:{protein:2.9,fibre:2.6,vitA:206,vitC:80,vitD:0,vitK:547,folate:19,vitB12:0,choline:15,calcium:91,iron:1.0,magnesium:23,zinc:0.3,potassium:299,selenium:0.6,iodine:2,omega3:0.12}},
    {name:"Sweet potato (1 medium baked, 130g)",cost:0.78,n:{protein:2.3,fibre:3.8,vitA:1100,vitC:22,vitD:0,vitK:2,folate:11,vitB12:0,choline:13,calcium:41,iron:0.8,magnesium:30,zinc:0.4,potassium:448,selenium:0.3,iodine:4,omega3:0.05}},
    {name:"Mushrooms (100g raw)",cost:1.04,n:{protein:3.1,fibre:1.0,vitA:0,vitC:2,vitD:7,vitK:0,folate:16,vitB12:0,choline:17,calcium:3,iron:0.4,magnesium:9,zinc:0.5,potassium:318,selenium:9,iodine:4,omega3:0}},
    {name:"Cauliflower (1 cup, 100g)",cost:0.65,n:{protein:2.0,fibre:2.0,vitA:0,vitC:46,vitD:0,vitK:16,folate:57,vitB12:0,choline:44,calcium:22,iron:0.5,magnesium:15,zinc:0.3,potassium:299,selenium:0.6,iodine:1,omega3:0.04}},
    {name:"Green peas (½ cup cooked, 80g)",cost:0.52,n:{protein:4.3,fibre:4.4,vitA:55,vitC:11,vitD:0,vitK:19,folate:50,vitB12:0,choline:22,calcium:22,iron:1.2,magnesium:23,zinc:0.8,potassium:217,selenium:1.8,iodine:1,omega3:0.05}},
    {name:"Asparagus (6 spears, 90g)",cost:1.3,n:{protein:2.9,fibre:2.8,vitA:45,vitC:7,vitD:0,vitK:46,folate:149,vitB12:0,choline:20,calcium:32,iron:2.9,magnesium:14,zinc:0.5,potassium:202,selenium:5,iodine:2,omega3:0.08}},
    {name:"Corn on the cob (1 cob, 90g)",cost:0.78,n:{protein:3.3,fibre:2.4,vitA:10,vitC:7,vitD:0,vitK:0,folate:46,vitB12:0,choline:29,calcium:3,iron:0.5,magnesium:26,zinc:0.5,potassium:243,selenium:0.7,iodine:1,omega3:0.02}},
    {name:"Beetroot (1 medium, 80g)",cost:0.52,n:{protein:1.2,fibre:1.9,vitA:2,vitC:5,vitD:0,vitK:0,folate:74,vitB12:0,choline:5,calcium:13,iron:0.7,magnesium:18,zinc:0.3,potassium:259,selenium:0.5,iodine:1,omega3:0.04}},
    {name:"Bok choy (1 cup cooked, 170g)",cost:0.78,n:{protein:2.6,fibre:1.7,vitA:361,vitC:44,vitD:0,vitK:57,folate:70,vitB12:0,choline:21,calcium:158,iron:1.8,magnesium:19,zinc:0.3,potassium:631,selenium:1.0,iodine:3,omega3:0.09}},
    {name:"Eggplant (1 cup cooked, 100g)",cost:0.65,n:{protein:0.8,fibre:2.5,vitA:4,vitC:1,vitD:0,vitK:3,folate:14,vitB12:0,choline:8,calcium:6,iron:0.3,magnesium:11,zinc:0.1,potassium:123,selenium:0.1,iodine:1,omega3:0.07}},
    {name:"Cabbage (1 cup raw, 90g)",cost:0.26,n:{protein:1.1,fibre:2.2,vitA:9,vitC:32,vitD:0,vitK:67,folate:38,vitB12:0,choline:10,calcium:40,iron:0.5,magnesium:12,zinc:0.2,potassium:170,selenium:0.4,iodine:3,omega3:0.07}},
  ]},
  {cat:"🍫 Snacks & Drinks",items:[
    {name:"Tim Tams (2 biscuits)",cost:0.65,n:{protein:1.5,fibre:0.5,vitA:5,vitC:0,vitD:0,vitK:1,folate:2,vitB12:0,choline:2,calcium:20,iron:0.5,magnesium:10,zinc:0.3,potassium:40,selenium:1,iodine:1,omega3:0}},
    {name:"Muesli bar",cost:1.04,n:{protein:3,fibre:1.5,vitA:0,vitC:0,vitD:0,vitK:0,folate:5,vitB12:0,choline:3,calcium:20,iron:1,magnesium:15,zinc:0.5,potassium:60,selenium:2,iodine:2,omega3:0.02}},
    {name:"Chips (small packet)",cost:2.6,n:{protein:2,fibre:1,vitA:0,vitC:5,vitD:0,vitK:3,folate:5,vitB12:0,choline:5,calcium:10,iron:0.5,magnesium:10,zinc:0.2,potassium:150,selenium:1,iodine:1,omega3:0}},
    {name:"Coke / soft drink (375mL)",cost:3.25,n:{protein:0,fibre:0,vitA:0,vitC:0,vitD:0,vitK:0,folate:0,vitB12:0,choline:0,calcium:0,iron:0,magnesium:0,zinc:0,potassium:5,selenium:0,iodine:0,omega3:0}},
    {name:"Orange juice (250mL)",cost:1.95,n:{protein:1,fibre:0,vitA:10,vitC:50,vitD:0,vitK:0,folate:25,vitB12:0,choline:5,calcium:15,iron:0.3,magnesium:10,zinc:0.1,potassium:225,selenium:0,iodine:1,omega3:0}},
  ]},
];

function FoodLogger({ logFood, rda }) {
  const [logSearch, setLogSearch] = useState("");
  const [logToast, setLogToast] = useState(null);
  const logAndToast = (item, mealType) => {
    logFood(item, mealType);
    const label = mealType === "breakfast" ? "🌅 Breakfast" : mealType === "lunch" ? "☀️ Lunch" : mealType === "snack" ? "🍿 Snack" : "🌙 Dinner";
    setLogToast(item.name + " → " + label);
    setTimeout(() => setLogToast(null), 2500);
  };
  const allItems = COMMON_FOODS.flatMap(cat => cat.items.map(item => ({ ...item, cat: cat.cat })));
  const filtered = logSearch.trim() ? allItems.filter(item => item.name.toLowerCase().includes(logSearch.toLowerCase())) : null;
  const renderItem = (item, j) => {
    const avgPct = Math.round(NKS.map(k => Math.min((item.n[k] || 0) / (rda[k] || 1) * 100, 100)).reduce((a, b) => a + b, 0) / NKS.length);
    const scoreColor = avgPct >= 15 ? "#f59e0b" : "#ef4444";
    return (
      <div key={j} style={{ padding: "8px 10px", background: "rgba(255,255,255,0.04)", borderRadius: 8, marginBottom: 4 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 14, color: "#e2e8f0", fontWeight: 600 }}>{item.name}</div>
            <div style={{ fontSize: 12, color: "#64748b", marginTop: 2 }}>
              {item.cat && <span>{item.cat} · </span>}${item.cost.toFixed(2)} · <span style={{ color: scoreColor, fontWeight: 700 }}>{avgPct}% nutrients</span>
            </div>
          </div>
          <div style={{ display: "flex", gap: 4, marginLeft: 8 }}>
            {[
              { t: "breakfast", emoji: "🌅", label: "Brekky" },
              { t: "lunch", emoji: "☀️", label: "Lunch" },
              { t: "dinner", emoji: "🌙", label: "Dinner" },
              { t: "snack", emoji: "🍿", label: "Snack" },
            ].map(({ t, emoji, label }) => (
              <button key={t} onClick={() => logAndToast(item, t)} title={"Log as " + t} style={{ padding: "4px 7px", borderRadius: 6, border: "1px solid rgba(255,255,255,0.12)", background: "rgba(255,255,255,0.06)", color: "#94a3b8", fontSize: 11, cursor: "pointer", display: "flex", flexDirection: "column", alignItems: "center", gap: 1 }}>
                <span style={{ fontSize: 14 }}>{emoji}</span>
                <span style={{ fontSize: 10, color: "#64748b" }}>{label}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    );
  };
  return (
    <div style={{ marginTop: 10 }}>
      {logToast && (
        <div style={{ background: "rgba(34,197,94,0.9)", borderRadius: 10, padding: "10px 14px", marginBottom: 10, fontSize: 13, fontWeight: 700, color: "#fff", textAlign: "center" }}>✓ Logged: {logToast}</div>
      )}
      <div style={{ background: "rgba(59,130,246,0.08)", border: "1px solid rgba(59,130,246,0.2)", borderRadius: 10, padding: "10px 12px", marginBottom: 10 }}>
        <div style={{ fontSize: 14, fontWeight: 700, color: "#60a5fa", marginBottom: 3 }}>🍔 Ate something not in the recipes?</div>
        <p style={{ fontSize: 13, color: "#94a3b8", margin: 0, lineHeight: 1.5 }}>These are everyday foods <em>outside</em> the recipe list. Search for what you actually had, then tap the meal slot to add it to your day — so your nutrient totals stay accurate.</p>
      </div>
      <input type="text" placeholder="🔍 Search foods (e.g. banana, toast, coffee)..." value={logSearch} onChange={e => setLogSearch(e.target.value)}
        style={{ width: "100%", padding: "9px 12px", borderRadius: 8, border: "1px solid rgba(255,255,255,0.12)", background: "rgba(255,255,255,0.06)", color: "#e2e8f0", fontSize: 13, marginBottom: 10, boxSizing: "border-box", outline: "none" }} />
      {filtered ? (
        filtered.length === 0 ? (
          <div style={{ textAlign: "center", padding: 16, color: "#64748b", fontSize: 14 }}>No foods found for "{logSearch}"</div>
        ) : (
          <div style={{ marginBottom: 12 }}>
            <div style={{ fontSize: 13, fontWeight: 700, color: "#64748b", marginBottom: 6 }}>Results for "{logSearch}"</div>
            {filtered.map((item, j) => renderItem(item, j))}
          </div>
        )
      ) : (
        COMMON_FOODS.map(cat => (
          <div key={cat.cat} style={{ marginBottom: 12 }}>
            <div style={{ fontSize: 14, fontWeight: 700, color: "#64748b", marginBottom: 6 }}>{cat.cat}</div>
            {cat.items.map((item, j) => renderItem(item, j))}
          </div>
        ))
      )}
      <div style={{ background: "rgba(239,68,68,0.08)", borderRadius: 10, padding: 12, border: "1px solid rgba(239,68,68,0.2)", marginTop: 4 }}>
        <div style={{ fontSize: 14, fontWeight: 700, color: "#ef4444", marginBottom: 4 }}>👀 Notice something?</div>
        <div style={{ fontSize: 13, color: "#94a3b8", lineHeight: 1.5 }}>A $6 bakery pie gives ~3% average nutrient coverage. Our $0.90 lentil soup gives ~18%. After logging, check your Dashboard to see which nutrients are still short — then browse Recipes to fill the gaps.</div>
      </div>
    </div>
  );
}

function NutrientBar({ name, cur, target, unit }) {
  const pct = Math.min((cur / target) * 100, 100);
  const color = pct >= 80 ? "#22c55e" : pct >= 50 ? "#f59e0b" : "#ef4444";
  return (
    <div style={{ marginBottom: 6 }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13, color: "#e2e8f0", marginBottom: 2 }}>
        <span style={{ fontWeight: 500 }}>{name}</span>
        <span style={{ opacity: 0.7 }}>{Math.round(cur)}/{target}{unit} ({Math.round(pct)}%)</span>
      </div>
      <div style={{ height: 7, borderRadius: 4, background: "rgba(255,255,255,0.08)", overflow: "hidden" }}>
        <div style={{ width: pct + "%", height: "100%", borderRadius: 4, background: color, transition: "width 0.4s" }} />
      </div>
    </div>
  );
}

const TYPICAL_MEALS = {
  breakfast: [
    { name: "Sausage McMuffin", emoji: "🍔", cost: 7.50, avg: 5 },
    { name: "Café bacon & egg roll", emoji: "🥚", cost: 10.50, avg: 6 },
    { name: "Bakery croissant", emoji: "🥐", cost: 6.50, avg: 3 },
    { name: "Servo hash browns (3)", emoji: "🟡", cost: 4.80, avg: 2 },
    { name: "McCafé muffin", emoji: "🍩", cost: 5.50, avg: 2 },
  ],
  lunch: [
    { name: "Bakery meat pie", emoji: "🥧", cost: 7.00, avg: 3 },
    { name: "Subway 6\" sub", emoji: "🥖", cost: 11.50, avg: 4 },
    { name: "Servo sausage roll", emoji: "🌭", cost: 5.50, avg: 2 },
    { name: "KFC snack box", emoji: "🍗", cost: 8.00, avg: 4 },
    { name: "Food court fried rice", emoji: "🍛", cost: 12.00, avg: 5 },
  ],
  dinner: [
    { name: "Frozen pizza (⅓)", emoji: "🍕", cost: 4.00, avg: 6 },
    { name: "Maccas Big Mac meal", emoji: "🍟", cost: 14.50, avg: 7 },
    { name: "Supermarket rotisserie chicken (¼)", emoji: "🍗", cost: 5.50, avg: 8 },
    { name: "Thai takeaway pad thai", emoji: "🍜", cost: 18.00, avg: 6 },
    { name: "Fish & chips (serve)", emoji: "🐟", cost: 12.00, avg: 5 },
  ],
  snack: { name: "Tim Tams + Coke", emoji: "🍫", cost: 3.00, avg: 1 },
};

function RecipeCard({ recipe, onAdd, rda, prof }) {
  const [open, setOpen] = useState(false);
  const [showNutrition, setShowNutrition] = useState(false);
  const [boostQtys, setBoostQtys] = useState({});
  const r = recipe;

  // Calculate nutrients including selected boosts (multiplied by quantity)
  const totalBoostQty = Object.values(boostQtys).reduce((a, b) => a + b, 0);
  const boostedN = {};
  NKS.forEach(k => {
    boostedN[k] = r.n[k] || 0;
    Object.entries(boostQtys).forEach(([bId, qty]) => { const b = BOOSTS.find(x => x.id === bId); if (b && b.n[k]) boostedN[k] += b.n[k] * qty; });
  });
  const boostedCal = (r.n.cal || 0) + Object.entries(boostQtys).reduce((s, [bId, qty]) => { const b = BOOSTS.find(x => x.id === bId); return s + (b ? (b.n.cal || 0) * qty : 0); }, 0);
  const boostedCost = r.cost + Object.entries(boostQtys).reduce((s, [bId, qty]) => { const b = BOOSTS.find(x => x.id === bId); return s + (b ? b.cost * qty : 0); }, 0);

  const cal = boostedCal;
  const calPct = rda && rda.cal ? Math.round((cal / rda.cal) * 100) : 0;

  const togBoost = (bId) => setBoostQtys(prev => {
    const cur = prev[bId] || 0;
    const next = cur >= 3 ? 0 : cur + 1;
    if (next === 0) { const { [bId]: _, ...rest } = prev; return rest; }
    return { ...prev, [bId]: next };
  });

  const nfRow = (label, value, unit, target, bold, border) => {
    const pct = target ? Math.round((value / target) * 100) : null;
    const color = pct === null ? "#94a3b8" : pct >= 80 ? "#22c55e" : pct >= 50 ? "#f59e0b" : pct >= 20 ? "#94a3b8" : "#ef4444";
    return (
      <div key={label} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "4px 0", borderBottom: border !== false ? "1px solid rgba(255,255,255,0.06)" : "none" }}>
        <span style={{ fontSize: 14, fontWeight: bold ? 700 : 400, color: "#e2e8f0" }}>{label}</span>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span style={{ fontSize: 14, color: "#94a3b8" }}>{Math.round(value * 10) / 10}{unit}</span>
          {pct !== null && (
            <div style={{ display: "flex", alignItems: "center", gap: 4, minWidth: 55, justifyContent: "flex-end" }}>
              <div style={{ width: 30, height: 5, borderRadius: 3, background: "rgba(255,255,255,0.08)", overflow: "hidden" }}>
                <div style={{ width: Math.min(pct, 100) + "%", height: "100%", borderRadius: 3, background: color }} />
              </div>
              <span style={{ fontSize: 13, fontWeight: 600, color, minWidth: 28, textAlign: "right" }}>{pct}%</span>
            </div>
          )}
        </div>
      </div>
    );
  };

  // Top nutrients including boosts for pills
  const topN = rda ? NKS.map(k => ({ k, nm: NK[k].name, pct: Math.round(((boostedN[k] || 0) / (rda[k] || 1)) * 100) })).filter(x => x.pct >= 15).sort((a, b) => b.pct - a.pct).slice(0, 6) : [];

  return (
    <div style={{ background: "rgba(255,255,255,0.06)", borderRadius: 12, padding: 14, marginBottom: 8, border: "1px solid rgba(255,255,255,0.08)" }}>
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", cursor: "pointer" }} onClick={() => { setOpen(!open); if (open) setShowNutrition(false); }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, flex: 1 }}>
          <span style={{ fontSize: 24 }}>{r.emoji}</span>
          <div>
            <div style={{ fontWeight: 600, fontSize: 14, color: "#f1f5f9" }}>{r.name}{r.tags.includes("sardine") ? <span style={{ marginLeft: 6, fontSize: 11, fontWeight: 700, background: "rgba(59,130,246,0.2)", color: "#60a5fa", borderRadius: 4, padding: "1px 5px" }}>⭐ BEST VALUE</span> : r.tags.includes("kangaroo") ? <span style={{ marginLeft: 6, fontSize: 11, fontWeight: 700, background: "rgba(251,146,60,0.15)", color: "#fb923c", borderRadius: 4, padding: "1px 5px" }}>🦘 ROO</span> : null}</div>
            <div style={{ fontSize: 13, color: "#94a3b8" }}>${boostedCost.toFixed(2)} · {r.time}min · {Math.round(cal)} kcal{totalBoostQty > 0 ? " · " + totalBoostQty + " boost" + (totalBoostQty > 1 ? "s" : "") : ""}{r.freezer ? " · ❄️" : ""}</div>
            <div style={{ fontSize: 12, color: "#64748b", marginTop: 2 }}>{open ? "▲ tap to close" : "▼ tap for ingredients, method & nutrition"}</div>
          </div>
        </div>
        <button onClick={e => { e.stopPropagation(); onAdd({ ...r, cost: boostedCost }, boostQtys); }} style={{ background: "#22c55e", color: "#fff", border: "none", borderRadius: 6, padding: "4px 10px", fontSize: 14, cursor: "pointer", fontWeight: 600, whiteSpace: "nowrap" }}>
          {totalBoostQty > 0 ? "+ Add ✨" : "+ Add"}
        </button>
      </div>

      {/* Nutrient pills */}
      {topN.length > 0 && (
        <div style={{ display: "flex", gap: 4, flexWrap: "wrap", marginTop: 6 }}>
          {topN.map(x => <span key={x.k} style={{ fontSize: 11, padding: "2px 6px", borderRadius: 8, background: x.pct >= 40 ? "rgba(34,197,94,0.15)" : "rgba(255,255,255,0.06)", color: x.pct >= 40 ? "#4ade80" : x.pct >= 20 ? "#fbbf24" : "#94a3b8" }}>{x.nm} {x.pct}%</span>)}
        </div>
      )}

      {/* VS Typical Meal comparison */}
      {rda && (() => {
        const myAvg = Math.round(NKS.map(k => Math.min(((boostedN[k] || 0) / (rda[k] || 1)) * 100, 100)).reduce((a, b) => a + b, 0) / NKS.length);
        const typRaw = TYPICAL_MEALS[r.type] || TYPICAL_MEALS.dinner;
        const typ = Array.isArray(typRaw)
          ? typRaw[r.name.split('').reduce((a, c) => a + c.charCodeAt(0), 0) % typRaw.length]
          : typRaw;
        const saved = typ.cost - boostedCost;
        const multi = typ.avg > 0 ? (myAvg / typ.avg).toFixed(1) : "∞";
        return (
          <div style={{ marginTop: 8, background: "rgba(0,0,0,0.2)", borderRadius: 8, padding: "8px 10px", fontSize: 13 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
              <div><span style={{ color: "#22c55e", fontWeight: 700 }}>✅ This:</span> <span style={{ color: "#94a3b8" }}>${boostedCost.toFixed(2)}</span></div>
              <div style={{ display: "flex", alignItems: "center", gap: 4 }}>
                <div style={{ width: 40, height: 5, borderRadius: 3, background: "rgba(255,255,255,0.08)", overflow: "hidden" }}>
                  <div style={{ width: Math.min(myAvg, 100) + "%", height: "100%", borderRadius: 3, background: "#22c55e" }} />
                </div>
                <span style={{ color: "#22c55e", fontWeight: 700 }}>{myAvg}%</span>
              </div>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
              <div><span style={{ color: "#ef4444", fontWeight: 700 }}>❌ {typ.emoji} {typ.name}:</span> <span style={{ color: "#94a3b8" }}>${typ.cost.toFixed(2)}</span></div>
              <div style={{ display: "flex", alignItems: "center", gap: 4 }}>
                <div style={{ width: 40, height: 5, borderRadius: 3, background: "rgba(255,255,255,0.08)", overflow: "hidden" }}>
                  <div style={{ width: Math.min(typ.avg, 100) + "%", height: "100%", borderRadius: 3, background: "#ef4444" }} />
                </div>
                <span style={{ color: "#ef4444", fontWeight: 700 }}>{typ.avg}%</span>
              </div>
            </div>
            <div style={{ color: "#f59e0b", fontWeight: 600, fontSize: 12 }}>
              {saved > 0 ? "Save $" + saved.toFixed(2) + " · " : ""}{multi}× more nutrition{saved > 0 ? " for less money" : ""}
            </div>
          </div>
        );
      })()}

      {open && (
        <div style={{ marginTop: 12, paddingTop: 12, borderTop: "1px solid rgba(255,255,255,0.06)" }}>
          <p style={{ fontSize: 14, color: "#94a3b8", margin: "0 0 10px" }}>{r.desc}</p>
          <div style={{ fontSize: 14, color: "#cbd5e1", marginBottom: 8 }}>
            <strong>Ingredients:</strong>
            <ul style={{ margin: "4px 0", paddingLeft: 18 }}>
              {r.ing.map((x, i) => <li key={i}>{x}</li>)}
              {Object.keys(boostQtys).length > 0 && Object.entries(boostQtys).map(([bId, qty]) => {
                const b = BOOSTS.find(x => x.id === bId);
                return b ? <li key={bId} style={{ color: "#4ade80", fontWeight: 600 }}>✨ {qty > 1 ? qty + "× " : ""}{b.label}{b.amount ? " (" + b.amount + ")" : ""}</li> : null;
              })}
            </ul>
          </div>
          <div style={{ fontSize: 14, color: "#cbd5e1" }}>
            <strong>Method:</strong>
            <ol style={{ margin: "4px 0", paddingLeft: 18 }}>
              {r.steps.map((x, i) => <li key={i}>{x}</li>)}
              {Object.keys(boostQtys).length > 0 && (
                <li style={{ color: "#4ade80", fontWeight: 600 }}>
                  ✨ Add boosters: {Object.entries(boostQtys).map(([bId, qty]) => {
                    const b = BOOSTS.find(x => x.id === bId);
                    return b ? (qty > 1 ? qty + "× " : "") + b.label.replace('+', '') : '';
                  }).filter(Boolean).join(', ')}
                </li>
              )}
            </ol>
          </div>
          {r.warnings && <div style={{ fontSize: 13, color: "#f59e0b", marginTop: 8 }}>⚠️ {r.warnings.join(" · ")}</div>}
          <div style={{ display: "flex", flexWrap: "wrap", gap: 4, marginTop: 8, marginBottom: 12 }}>
            {r.tags.map(t => <span key={t} style={{ fontSize: 12, padding: "2px 8px", borderRadius: 10, background: "rgba(139,92,246,0.15)", color: "#a78bfa" }}>{t}</span>)}
          </div>

          {/* Boosters — select before adding */}
          <div style={{ background: "rgba(255,255,255,0.04)", borderRadius: 10, padding: "10px 12px", marginBottom: 10 }}>
            <div style={{ fontSize: 13, fontWeight: 600, color: "#94a3b8", marginBottom: 8 }}>
              ✨ ADD BOOSTERS <span style={{ color: "#64748b", fontWeight: 400 }}>— updates nutrition live</span>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 4 }}>
              {BOOSTS.filter(b => getBoostsForRecipe(r).includes(b.id)).map(b => {
                const qty = boostQtys[b.id] || 0;
                const active = qty > 0;
                const borderColor = qty === 3 ? "#f59e0b" : "#22c55e";
                const bgColor = qty === 3 ? "rgba(245,158,11,0.12)" : "rgba(34,197,94,0.12)";
                const textColor = qty === 3 ? "#fbbf24" : "#4ade80";
                return (
                  <button key={b.id} onClick={() => togBoost(b.id)} style={{ display: "flex", alignItems: "center", gap: 6, padding: "6px 8px", borderRadius: 8, cursor: "pointer", border: active ? "1px solid " + borderColor : "1px solid rgba(255,255,255,0.08)", background: active ? bgColor : "transparent", color: active ? textColor : "#94a3b8", transition: "all 0.15s" }}>
                    <span style={{ fontSize: 16 }}>{b.em}</span>
                    <div style={{ flex: 1 }}>
                      <div style={{ fontSize: 13, fontWeight: 600 }}>{b.label}</div>
                      <div style={{ fontSize: 11, color: "#60a5fa", opacity: 0.85 }}>{b.amount}</div>
                      <div style={{ fontSize: 11, opacity: 0.7 }}>+${b.cost.toFixed(2)}{qty > 1 ? " ×" + qty + " = $" + (b.cost * qty).toFixed(2) : ""}</div>
                    </div>
                    {active && <span style={{ marginLeft: "auto", fontSize: 13, fontWeight: 800, color: textColor, minWidth: 20, textAlign: "center" }}>×{qty}</span>}
                  </button>
                );
              })}
            </div>
            {totalBoostQty > 0 && (
              <button onClick={() => setBoostQtys({})} style={{ width: "100%", marginTop: 6, padding: "4px", borderRadius: 6, border: "none", background: "transparent", color: "#64748b", fontSize: 13, cursor: "pointer" }}>Clear boosters</button>
            )}
          </div>

          {/* Nutrition Facts */}
          {rda && (
            <div>
              <button onClick={() => setShowNutrition(!showNutrition)} style={{ width: "100%", padding: 10, borderRadius: 8, border: showNutrition ? "1px solid rgba(59,130,246,0.4)" : "1px solid rgba(255,255,255,0.12)", background: showNutrition ? "rgba(59,130,246,0.1)" : "rgba(255,255,255,0.04)", color: showNutrition ? "#60a5fa" : "#94a3b8", fontSize: 13, fontWeight: 600, cursor: "pointer" }}>
                {showNutrition ? "▲ Hide Nutrition Facts" : "📋 Nutrition Facts"}
              </button>

              {showNutrition && (
                <div style={{ background: "rgba(0,0,0,0.3)", borderRadius: 12, border: "2px solid rgba(255,255,255,0.2)", padding: 16, marginTop: 8 }}>
                  <div style={{ fontSize: 18, fontWeight: 800, color: "#fff", borderBottom: "3px solid rgba(255,255,255,0.3)", paddingBottom: 6, marginBottom: 4 }}>Nutrition Facts</div>
                  <div style={{ fontSize: 12, color: "#64748b", marginBottom: 8 }}>Per serve{totalBoostQty > 0 ? " + " + totalBoostQty + " booster" + (totalBoostQty > 1 ? "s" : "") : ""}</div>

                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", borderBottom: "6px solid rgba(255,255,255,0.2)", paddingBottom: 6, marginBottom: 6 }}>
                    <div>
                      <div style={{ fontSize: 14, fontWeight: 700, color: "#e2e8f0" }}>Calories</div>
                      <div style={{ fontSize: 28, fontWeight: 800, color: "#fff" }}>{Math.round(cal)}</div>
                    </div>
                    <div style={{ textAlign: "right" }}>
                      <div style={{ fontSize: 12, color: "#64748b" }}>% Daily Value*</div>
                      <div style={{ fontSize: 16, fontWeight: 700, color: calPct >= 40 ? "#f59e0b" : "#94a3b8" }}>{calPct}%</div>
                    </div>
                  </div>

                  <div style={{ fontSize: 12, fontWeight: 600, color: "#64748b", marginBottom: 4, textTransform: "uppercase", letterSpacing: 1 }}>Macronutrients</div>
                  {nfRow("Protein", boostedN.protein, "g", rda.protein, true)}
                  {nfRow("Fibre", boostedN.fibre, "g", rda.fibre, true)}

                  <div style={{ fontSize: 12, fontWeight: 600, color: "#64748b", marginTop: 10, marginBottom: 4, textTransform: "uppercase", letterSpacing: 1 }}>Vitamins</div>
                  {nfRow("Vitamin A", boostedN.vitA, "μg", rda.vitA, false)}
                  {nfRow("Vitamin C", boostedN.vitC, "mg", rda.vitC, false)}
                  {nfRow("Vitamin D", boostedN.vitD, "IU", rda.vitD, false)}
                  {nfRow("Vitamin K", boostedN.vitK, "μg", rda.vitK, false)}
                  {nfRow("Folate (B9)", boostedN.folate, "μg", rda.folate, false)}
                  {nfRow("Vitamin B12", boostedN.vitB12, "μg", rda.vitB12, false)}
                  {nfRow("Choline", boostedN.choline, "mg", rda.choline, false)}

                  <div style={{ fontSize: 12, fontWeight: 600, color: "#64748b", marginTop: 10, marginBottom: 4, textTransform: "uppercase", letterSpacing: 1 }}>Minerals</div>
                  {nfRow("Calcium", boostedN.calcium, "mg", rda.calcium, false)}
                  {nfRow("Iron", boostedN.iron, "mg", rda.iron, false)}
                  {nfRow("Magnesium", boostedN.magnesium, "mg", rda.magnesium, false)}
                  {nfRow("Zinc", boostedN.zinc, "mg", rda.zinc, false)}
                  {nfRow("Potassium", boostedN.potassium, "mg", rda.potassium, false)}
                  {nfRow("Selenium", boostedN.selenium, "μg", rda.selenium, false)}
                  {nfRow("Iodine", boostedN.iodine, "μg", rda.iodine, false)}

                  <div style={{ fontSize: 12, fontWeight: 600, color: "#64748b", marginTop: 10, marginBottom: 4, textTransform: "uppercase", letterSpacing: 1 }}>Essential Fats</div>
                  {nfRow("Omega-3", boostedN.omega3, "g", rda.omega3, false, false)}

                  <div style={{ fontSize: 11, color: "#64748b", marginTop: 10, borderTop: "1px solid rgba(255,255,255,0.06)", paddingTop: 6 }}>* % Daily Value based on your profile ({prof ? prof.age + "yo " + (prof.sex === "female" ? "♀" : "♂") : "default"}). Green = 80%+, Amber = 50%+, Red = under 20%.</div>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function WeekMealRow({ meal, onRemove }) {
  const [showDetail, setShowDetail] = useState(false);
  return (
    <div style={{ background: "rgba(255,255,255,0.05)", borderRadius: 8, marginBottom: 4, overflow: "hidden" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "8px 10px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, flex: 1, cursor: "pointer" }} onClick={() => setShowDetail(v => !v)}>
          <span style={{ fontSize: 18 }}>{meal.recipe.emoji}</span>
          <div>
            <div style={{ fontSize: 14, fontWeight: 600, color: "#f1f5f9" }}>
              {meal.recipe.name}
              {meal.portion !== 1 && <span style={{ color: "#64748b" }}> ({meal.portion}×)</span>}
              <span style={{ fontSize: 11, color: "#64748b", marginLeft: 4 }}>{showDetail ? "▲" : "▼"}</span>
            </div>
            {Object.keys(meal.boosts || {}).length > 0 && <div style={{ fontSize: 11, color: "#4ade80" }}>✨ {Object.values(meal.boosts || {}).reduce((a,b)=>a+b,0)} booster{Object.values(meal.boosts || {}).reduce((a,b)=>a+b,0) > 1 ? 's' : ''}</div>}
          </div>
        </div>
        <button onClick={onRemove} style={{ background: "none", border: "none", color: "#ef4444", cursor: "pointer", fontSize: 16 }}>×</button>
      </div>
      {showDetail && (
        <div style={{ padding: "0 10px 10px", borderTop: "1px solid rgba(255,255,255,0.06)" }}>
          <div style={{ fontSize: 12, color: "#64748b", marginTop: 8, marginBottom: 4, fontWeight: 700, textTransform: "uppercase" }}>Ingredients</div>
          {meal.recipe.ing.map((ing, k) => <div key={k} style={{ fontSize: 13, color: "#94a3b8", paddingLeft: 8, lineHeight: 1.6 }}>• {ing}</div>)}
          <div style={{ fontSize: 12, color: "#64748b", marginTop: 8, marginBottom: 4, fontWeight: 700, textTransform: "uppercase" }}>Steps</div>
          {meal.recipe.steps.map((step, k) => <div key={k} style={{ fontSize: 13, color: "#94a3b8", paddingLeft: 8, lineHeight: 1.6 }}>{k + 1}. {step}</div>)}
        </div>
      )}
    </div>
  );
}

function PlannerCard({ meal, onRemove, onPortion, onBoost, rda, prof }) {
  const [open, setOpen] = useState(false);
  const [showNutrition, setShowNutrition] = useState(false);
  const r = meal.recipe;
  const mn = {};
  NKS.forEach(k => {
    mn[k] = (r.n[k] || 0) * meal.portion;
    Object.entries(meal.boosts || {}).forEach(([bId, qty]) => { const b = BOOSTS.find(x => x.id === bId); if (b && b.n[k]) mn[k] += b.n[k] * qty; });
  });
  let cal = (r.n.cal || 0) * meal.portion;
  Object.entries(meal.boosts || {}).forEach(([bId, qty]) => { const b = BOOSTS.find(x => x.id === bId); if (b && b.n.cal) cal += b.n.cal * qty; });
  let cost = r.cost * meal.portion;
  Object.entries(meal.boosts || {}).forEach(([bId, qty]) => { const b = BOOSTS.find(x => x.id === bId); if (b) cost += b.cost * qty; });
  const top = NKS.map(k => ({ k, nm: NK[k].name, pct: Math.round((mn[k] / (rda[k] || 1)) * 100) })).filter(x => x.pct > 0).sort((a, b) => b.pct - a.pct).slice(0, 5);
  const calPct = rda.cal ? Math.round((cal / rda.cal) * 100) : 0;

  const nfRow = (label, value, unit, target, bold, border) => {
    const pct = target ? Math.round((value / target) * 100) : null;
    const color = pct === null ? "#94a3b8" : pct >= 80 ? "#22c55e" : pct >= 50 ? "#f59e0b" : pct >= 20 ? "#94a3b8" : "#ef4444";
    return (
      <div key={label} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "4px 0", borderBottom: border !== false ? "1px solid rgba(255,255,255,0.06)" : "none" }}>
        <span style={{ fontSize: 14, fontWeight: bold ? 700 : 400, color: "#e2e8f0" }}>{label}</span>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span style={{ fontSize: 14, color: "#94a3b8" }}>{Math.round(value * 10) / 10}{unit}</span>
          {pct !== null && (
            <div style={{ display: "flex", alignItems: "center", gap: 4, minWidth: 55, justifyContent: "flex-end" }}>
              <div style={{ width: 30, height: 5, borderRadius: 3, background: "rgba(255,255,255,0.08)", overflow: "hidden" }}>
                <div style={{ width: Math.min(pct, 100) + "%", height: "100%", borderRadius: 3, background: color }} />
              </div>
              <span style={{ fontSize: 13, fontWeight: 600, color, minWidth: 28, textAlign: "right" }}>{pct}%</span>
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div style={{ background: "rgba(255,255,255,0.05)", borderRadius: 12, marginBottom: 8, border: open ? "1px solid rgba(34,197,94,0.3)" : "1px solid rgba(255,255,255,0.06)" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "10px 14px", cursor: "pointer" }} onClick={() => setOpen(!open)}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, flex: 1 }}>
          <span style={{ fontSize: 22 }}>{r.emoji}</span>
          <div>
            <div style={{ fontSize: 13, fontWeight: 600, color: "#f1f5f9" }}>{r.name}{meal.portion !== 1 ? " (" + meal.portion + "×)" : ""}</div>
            <div style={{ fontSize: 13, color: "#64748b" }}>${cost.toFixed(2)} · {Math.round(cal)} kcal</div>
          </div>
        </div>
        <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
          <span style={{ color: "#64748b", fontSize: 14 }}>{open ? "▲" : "▼"}</span>
          <button onClick={e => { e.stopPropagation(); onRemove(); }} style={{ background: "none", border: "none", color: "#ef4444", cursor: "pointer", fontSize: 18 }}>×</button>
        </div>
      </div>
      <div style={{ display: "flex", gap: 4, flexWrap: "wrap", padding: "0 14px 8px" }}>
        {top.map(x => <span key={x.k} style={{ fontSize: 11, padding: "2px 6px", borderRadius: 8, background: x.pct >= 40 ? "rgba(34,197,94,0.15)" : "rgba(255,255,255,0.06)", color: x.pct >= 40 ? "#4ade80" : x.pct >= 20 ? "#fbbf24" : "#94a3b8" }}>{x.nm} {x.pct}%</span>)}
      </div>
      {open && (
        <div style={{ padding: "0 14px 14px", borderTop: "1px solid rgba(255,255,255,0.06)" }}>
          <p style={{ fontSize: 14, color: "#94a3b8", margin: "10px 0" }}>{r.desc}</p>
          <div style={{ fontSize: 14, color: "#cbd5e1", marginBottom: 8 }}>
            <strong>Ingredients:</strong>
            <ul style={{ margin: "4px 0", paddingLeft: 18 }}>
              {r.ing.map((x, i) => <li key={i}>{x}</li>)}
              {Object.keys(meal.boosts || {}).length > 0 && Object.entries(meal.boosts || {}).map(([bId, qty]) => {
                const b = BOOSTS.find(x => x.id === bId);
                return b ? <li key={bId} style={{ color: "#4ade80", fontWeight: 600 }}>✨ {qty > 1 ? qty + "× " : ""}{b.label}{b.amount ? " (" + b.amount + ")" : ""}</li> : null;
              })}
            </ul>
          </div>
          <div style={{ fontSize: 14, color: "#cbd5e1", marginBottom: 10 }}>
            <strong>Method:</strong>
            <ol style={{ margin: "4px 0", paddingLeft: 18 }}>
              {r.steps.map((x, i) => <li key={i}>{x}</li>)}
              {Object.keys(meal.boosts || {}).length > 0 && (
                <li style={{ color: "#4ade80", fontWeight: 600 }}>
                  ✨ Add boosters: {Object.entries(meal.boosts || {}).map(([bId, qty]) => {
                    const b = BOOSTS.find(x => x.id === bId);
                    return b ? (qty > 1 ? qty + "× " : "") + b.label.replace('+', '') : '';
                  }).filter(Boolean).join(', ')}
                </li>
              )}
            </ol>
          </div>
          <div style={{ background: "rgba(255,255,255,0.04)", borderRadius: 10, padding: "10px 12px", marginBottom: 10 }}>
            <div style={{ fontSize: 13, fontWeight: 600, color: "#94a3b8", marginBottom: 8 }}>PORTION</div>
            <div style={{ display: "flex", gap: 6, justifyContent: "center", flexWrap: "wrap" }}>
              {[0.5, 0.75, 1, 1.25, 1.5, 2].map(p => (
                <button key={p} onClick={() => onPortion(p)} style={{ padding: "4px 10px", borderRadius: 6, fontSize: 13, cursor: "pointer", fontWeight: 600, border: meal.portion === p ? "1px solid #22c55e" : "1px solid rgba(255,255,255,0.1)", background: meal.portion === p ? "rgba(34,197,94,0.15)" : "transparent", color: meal.portion === p ? "#22c55e" : "#64748b" }}>{p}×</button>
              ))}
            </div>
          </div>
          <div style={{ background: "rgba(255,255,255,0.04)", borderRadius: 10, padding: "10px 12px", marginBottom: 10 }}>
            <div style={{ fontSize: 13, fontWeight: 600, color: "#94a3b8", marginBottom: 8 }}>BOOSTERS</div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 4 }}>
              {BOOSTS.filter(b => getBoostsForRecipe(r).includes(b.id)).map(b => {
                const qty = (meal.boosts || {})[b.id] || 0;
                const active = qty > 0;
                const borderColor = qty === 3 ? "#f59e0b" : "#22c55e";
                const bgColor = qty === 3 ? "rgba(245,158,11,0.12)" : "rgba(34,197,94,0.12)";
                const textColor = qty === 3 ? "#fbbf24" : "#4ade80";
                return (
                  <button key={b.id} onClick={() => onBoost(b.id)} style={{ display: "flex", alignItems: "center", gap: 6, padding: "6px 8px", borderRadius: 8, cursor: "pointer", border: active ? "1px solid " + borderColor : "1px solid rgba(255,255,255,0.08)", background: active ? bgColor : "transparent", color: active ? textColor : "#94a3b8" }}>
                    <span style={{ fontSize: 16 }}>{b.em}</span>
                    <div style={{ flex: 1 }}><div style={{ fontSize: 13, fontWeight: 600 }}>{b.label}</div><div style={{ fontSize: 11, color: "#60a5fa" }}>{b.amount}</div><div style={{ fontSize: 11, opacity: 0.7 }}>+${b.cost.toFixed(2)}{qty > 1 ? " ×" + qty : ""}</div></div>
                    {active && <span style={{ fontSize: 13, fontWeight: 800, color: textColor }}>×{qty}</span>}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Nutrition Facts Button */}
          <button onClick={() => setShowNutrition(!showNutrition)} style={{ width: "100%", padding: 10, borderRadius: 8, border: showNutrition ? "1px solid rgba(59,130,246,0.4)" : "1px solid rgba(255,255,255,0.12)", background: showNutrition ? "rgba(59,130,246,0.1)" : "rgba(255,255,255,0.04)", color: showNutrition ? "#60a5fa" : "#94a3b8", fontSize: 13, fontWeight: 600, cursor: "pointer", marginBottom: 10 }}>
            {showNutrition ? "▲ Hide Nutrition Facts" : "📋 Nutrition Facts"}
          </button>

          {/* Nutrition Facts Panel */}
          {showNutrition && (
            <div style={{ background: "rgba(0,0,0,0.3)", borderRadius: 12, border: "2px solid rgba(255,255,255,0.2)", padding: 16, marginBottom: 10 }}>
              <div style={{ fontSize: 18, fontWeight: 800, color: "#fff", borderBottom: "3px solid rgba(255,255,255,0.3)", paddingBottom: 6, marginBottom: 4 }}>Nutrition Facts</div>
              <div style={{ fontSize: 12, color: "#64748b", marginBottom: 8 }}>Per serve{meal.portion !== 1 ? " (" + meal.portion + "× portion)" : ""}{Object.keys(meal.boosts || {}).length > 0 ? " + " + Object.values(meal.boosts || {}).reduce((a,b)=>a+b,0) + " booster" + (Object.values(meal.boosts || {}).reduce((a,b)=>a+b,0) > 1 ? "s" : "") : ""}</div>

              {/* Calories header */}
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", borderBottom: "6px solid rgba(255,255,255,0.2)", paddingBottom: 6, marginBottom: 6 }}>
                <div>
                  <div style={{ fontSize: 14, fontWeight: 700, color: "#e2e8f0" }}>Calories</div>
                  <div style={{ fontSize: 28, fontWeight: 800, color: "#fff" }}>{Math.round(cal)}</div>
                </div>
                <div style={{ textAlign: "right" }}>
                  <div style={{ fontSize: 12, color: "#64748b" }}>% Daily Value*</div>
                  <div style={{ fontSize: 16, fontWeight: 700, color: calPct >= 40 ? "#f59e0b" : "#94a3b8" }}>{calPct}%</div>
                </div>
              </div>

              {/* Macros */}
              <div style={{ fontSize: 12, fontWeight: 600, color: "#64748b", marginBottom: 4, textTransform: "uppercase", letterSpacing: 1 }}>Macronutrients</div>
              {nfRow("Protein", mn.protein, "g", rda.protein, true)}
              {nfRow("Fibre", mn.fibre, "g", rda.fibre, true)}

              {/* Vitamins */}
              <div style={{ fontSize: 12, fontWeight: 600, color: "#64748b", marginTop: 10, marginBottom: 4, textTransform: "uppercase", letterSpacing: 1 }}>Vitamins</div>
              {nfRow("Vitamin A", mn.vitA, "μg", rda.vitA, false)}
              {nfRow("Vitamin C", mn.vitC, "mg", rda.vitC, false)}
              {nfRow("Vitamin D", mn.vitD, "IU", rda.vitD, false)}
              {nfRow("Vitamin K", mn.vitK, "μg", rda.vitK, false)}
              {nfRow("Folate (B9)", mn.folate, "μg", rda.folate, false)}
              {nfRow("Vitamin B12", mn.vitB12, "μg", rda.vitB12, false)}
              {nfRow("Choline", mn.choline, "mg", rda.choline, false)}

              {/* Minerals */}
              <div style={{ fontSize: 12, fontWeight: 600, color: "#64748b", marginTop: 10, marginBottom: 4, textTransform: "uppercase", letterSpacing: 1 }}>Minerals</div>
              {nfRow("Calcium", mn.calcium, "mg", rda.calcium, false)}
              {nfRow("Iron", mn.iron, "mg", rda.iron, false)}
              {nfRow("Magnesium", mn.magnesium, "mg", rda.magnesium, false)}
              {nfRow("Zinc", mn.zinc, "mg", rda.zinc, false)}
              {nfRow("Potassium", mn.potassium, "mg", rda.potassium, false)}
              {nfRow("Selenium", mn.selenium, "μg", rda.selenium, false)}
              {nfRow("Iodine", mn.iodine, "μg", rda.iodine, false)}

              {/* Fats */}
              <div style={{ fontSize: 12, fontWeight: 600, color: "#64748b", marginTop: 10, marginBottom: 4, textTransform: "uppercase", letterSpacing: 1 }}>Essential Fats</div>
              {nfRow("Omega-3 (ALA)", mn.omega3, "g", rda.omega3, false, false)}

              <div style={{ fontSize: 11, color: "#64748b", marginTop: 10, borderTop: "1px solid rgba(255,255,255,0.06)", paddingTop: 6 }}>* % Daily Value based on your personal profile ({prof.age}yo {prof.sex === "female" ? "♀" : "♂"}). Green = 80%+, Amber = 50%+, Red = under 20%.</div>
            </div>
          )}

          <button onClick={() => setOpen(false)} style={{ width: "100%", padding: 10, borderRadius: 8, border: "1px solid rgba(255,255,255,0.12)", background: "rgba(255,255,255,0.05)", color: "#94a3b8", fontSize: 13, fontWeight: 600, cursor: "pointer" }}>▲ Close</button>
        </div>
      )}
    </div>
  );
}

function FeedbackForm() {
  const [msg, setMsg] = useState("");
  const [status, setStatus] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!msg.trim()) return;
    setStatus("sending");
    try {
      const res = await fetch("https://formspree.io/f/xpqbkpnr", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ message: msg }),
      });
      if (res.ok) { setStatus("sent"); setMsg(""); }
      else setStatus("error");
    } catch { setStatus("error"); }
  };

  if (status === "sent") return (
    <div style={{ textAlign: "center", padding: "16px 0" }}>
      <div style={{ fontSize: 28, marginBottom: 8 }}>🙏</div>
      <div style={{ fontSize: 14, fontWeight: 700, color: "#22c55e" }}>Thanks! We got it.</div>
      <button onClick={() => setStatus(null)} style={{ marginTop: 10, background: "none", border: "none", color: "#64748b", fontSize: 14, cursor: "pointer" }}>Send another</button>
    </div>
  );

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        value={msg}
        onChange={e => setMsg(e.target.value)}
        placeholder="Found a bug? Want a recipe added? Just want to say hi? We read everything."
        rows={4}
        style={{ width: "100%", background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.12)", borderRadius: 10, color: "#f1f5f9", fontSize: 13, padding: 10, resize: "vertical", boxSizing: "border-box", fontFamily: "inherit" }}
      />
      {status === "error" && <div style={{ fontSize: 14, color: "#ef4444", marginBottom: 6 }}>Something went wrong — try again.</div>}
      <button
        type="submit"
        disabled={status === "sending" || !msg.trim()}
        style={{ marginTop: 8, width: "100%", padding: "10px 0", borderRadius: 10, background: msg.trim() ? "#22c55e" : "rgba(255,255,255,0.08)", border: "none", color: msg.trim() ? "#0f172a" : "#64748b", fontSize: 13, fontWeight: 700, cursor: msg.trim() ? "pointer" : "default" }}
      >
        {status === "sending" ? "Sending…" : "Send Feedback"}
      </button>
    </form>
  );
}

export default function App() {
  const [tab, setTab] = useState("profile");
  const [prevTab, setPrevTab] = useState(null);
  const [household, setHousehold] = useState([]);
  const [activeId, setActiveId] = useState(null);
  const [editing, setEditing] = useState(null);
  const [plan, setPlan] = useState({ breakfast: [], lunch: [], dinner: [], snack: [] });
  const [weekPlan, setWeekPlan] = useState({
    mon: { breakfast: [], lunch: [], dinner: [], snack: [] },
    tue: { breakfast: [], lunch: [], dinner: [], snack: [] },
    wed: { breakfast: [], lunch: [], dinner: [], snack: [] },
    thu: { breakfast: [], lunch: [], dinner: [], snack: [] },
    fri: { breakfast: [], lunch: [], dinner: [], snack: [] },
    sat: { breakfast: [], lunch: [], dinner: [], snack: [] },
    sun: { breakfast: [], lunch: [], dinner: [], snack: [] },
  });
  const [selectedDay, setSelectedDay] = useState(null);
  const [checked, setChecked] = useState({});
  const [filter, setFilter] = useState("all");
  const [showLog, setShowLog] = useState(false);
  const [learnOpen, setLearnOpen] = useState({});
  const [learnDemog, setLearnDemog] = useState("f_19");
  const [nameError, setNameError] = useState(false);
  const [showAllDiets, setShowAllDiets] = useState(false);
  const [simpleMode, setSimpleMode] = useState(() => { try { return localStorage.getItem("oe_simple") === "1"; } catch { return false; } });
  const setAndSaveCountry = (c) => { setCountry(c); };

  // Sanitize meal data on startup — fixes crashes from older localStorage format
  // where boosts was an array [] instead of an object {}
  useEffect(() => {
    const fixBoosts = (m) => ({ ...m, boosts: (m.boosts && !Array.isArray(m.boosts) && typeof m.boosts === 'object') ? m.boosts : {} });
    const fixDay = (day) => { const out = {}; ['breakfast','lunch','dinner','snack'].forEach(t => { out[t] = (day[t] || []).map(fixBoosts); }); return out; };
    setPlan(p => fixDay(p));
    setWeekPlan(w => { const out = {}; Object.keys(w || {}).forEach(d => { out[d] = fixDay(w[d] || {}); }); return out; });
  }, []);

  const go = (t) => { setPrevTab(tab); setTab(t); };
  const active = household.find(m => m.id === activeId) || household[0];
  const prof = active || { age: 30, sex: "female", pregnant: false, lactating: false };
  const rda = useMemo(() => getRDA(prof), [prof.age, prof.sex, prof.pregnant, prof.lactating]);
  const ready = household.length > 0;

  const calcN = useCallback((meal) => {
    const t = {};
    NKS.forEach(k => {
      t[k] = (meal.recipe.n[k] || 0) * meal.portion;
      Object.entries(meal.boosts || {}).forEach(([bId, qty]) => { const b = BOOSTS.find(x => x.id === bId); if (b && b.n[k]) t[k] += b.n[k] * qty; });
    });
    return t;
  }, []);

  const totals = useMemo(() => {
    const t = {};
    NKS.forEach(k => t[k] = 0);
    Object.values(plan).flat().forEach(m => {
      const mn = calcN(m);
      NKS.forEach(k => { t[k] += mn[k] || 0; });
    });
    return t;
  }, [plan, calcN]);

  const nMeals = Object.values(plan).flat().length;
  const dayCost = Object.values(plan).flat().reduce((s, m) => {
    let c = m.recipe.cost * m.portion;
    Object.entries(m.boosts || {}).forEach(([bId, qty]) => { const b = BOOSTS.find(x => x.id === bId); if (b) c += b.cost * qty; });
    return s + c;
  }, 0);

  const addMeal = (r, preBoosts = {}) => {
    const type = r.type === "breakfast" ? "breakfast" : r.type === "lunch" ? "lunch" : r.type === "snack" ? "snack" : "dinner";
    
    // If selectedDay is set, add to weekly plan
    if (selectedDay) {
      setWeekPlan(p => ({
        ...p,
        [selectedDay]: {
          ...p[selectedDay],
          [type]: [...p[selectedDay][type], { recipe: r, portion: 1, boosts: preBoosts }]
        }
      }));
      setSelectedDay(null); // Clear after adding
      go("weekly");
    } else {
      // Add to today's plan
      setPlan(p => ({ ...p, [type]: [...p[type], { recipe: r, portion: 1, boosts: preBoosts }] }));
      go("planner");
    }
  };

  const logFood = (item, mealType) => {
    const fakeRecipe = {
      id: "log_" + Date.now(), name: item.name, type: mealType, cost: item.cost,
      time: 0, emoji: "📝", desc: "Logged food", ing: [], steps: [], n: item.n,
      tags: ["logged"], logged: true
    };
    setPlan(p => ({ ...p, [mealType]: [...p[mealType], { recipe: fakeRecipe, portion: 1, boosts: [] }] }));
  };

  const removeMeal = (type, i) => setPlan(p => ({ ...p, [type]: p[type].filter((_, j) => j !== i) }));

  const setPort = (type, i, v) => setPlan(p => {
    const u = [...p[type]];
    u[i] = { ...u[i], portion: v };
    return { ...p, [type]: u };
  });

  const togBoost = (type, i, bId) => setPlan(p => {
    const u = [...p[type]];
    const m = u[i];
    const cur = (m.boosts || {})[bId] || 0;
    const next = cur >= 3 ? 0 : cur + 1;
    const newBoosts = next === 0
      ? (({ [bId]: _, ...rest }) => rest)(m.boosts || {})
      : { ...(m.boosts || {}), [bId]: next };
    u[i] = { ...m, boosts: newBoosts };
    return { ...p, [type]: u };
  });

  const MEAT_WORDS = ["beef","mince","pork","sausage","ham","liver","heart","sardine","salmon","tuna","fish"];
  const activeDiet = ready ? (prof.diet || "omnivore") : "omnivore";

  const suggestions = useMemo(() => {
    if (!nMeals) return [];
    const gaps = NKS.filter(k => (totals[k] / (rda[k] || 1)) < 0.5);
    if (!gaps.length) return [];
    // Filter suggestions by dietary preference
    let pool = RECIPES;
    if (activeDiet === "vegan") {
      pool = pool.filter(r => r.tags.includes("vegan"));
    } else if (activeDiet === "vegetarian") {
      pool = pool.filter(r =>
        !r.tags.includes("chicken") &&
        !r.tags.includes("organ-meat") &&
        !MEAT_WORDS.some(w => r.name.toLowerCase().includes(w) || (r.desc || "").toLowerCase().includes(w))
      );
    }
    return pool.map(r => {
      let sc = 0;
      gaps.forEach(g => { if (r.n[g] && rda[g]) sc += r.n[g] / rda[g]; });
      return { ...r, sc };
    }).filter(r => r.sc > 0).sort((a, b) => b.sc - a.sc).slice(0, 3);
  }, [totals, rda, nMeals, activeDiet]);
  const filtered = (() => {
    let base = filter === "all" ? RECIPES :
      filter === "vegetarian" ? RECIPES.filter(r => !r.tags.includes("chicken") && !r.tags.includes("organ-meat") && !MEAT_WORDS.some(w => r.name.toLowerCase().includes(w) || (r.desc || "").toLowerCase().includes(w))) :
      RECIPES.filter(r => r.type === filter || r.tags.includes(filter));
    if (!showAllDiets && activeDiet !== "omnivore") {
      if (activeDiet === "vegan") {
        base = base.filter(r => r.tags.includes("vegan"));
      } else if (activeDiet === "vegetarian") {
        base = base.filter(r =>
          !r.tags.includes("chicken") &&
          !r.tags.includes("organ-meat") &&
          !MEAT_WORDS.some(w => r.name.toLowerCase().includes(w) || (r.desc || "").toLowerCase().includes(w))
        );
      }
    }
    return base;
  })();
  const emj = (m) => { const base = m.age < 4 ? "👶" : m.age < 13 ? "🧒" : m.age < 18 ? "🧑" : m.sex === "female" ? (m.pregnant ? "🤰" : m.lactating ? "🤱" : "👩") : "👨"; return base + (m.tone || ""); };

  return (
    <div style={{ minHeight: "100vh", background: "linear-gradient(135deg,#0f172a,#1e293b,#0f172a)", color: "#e2e8f0", fontFamily: "'Segoe UI',system-ui,sans-serif" }}>
      <div style={{ padding: "14px 16px 6px", textAlign: "center" }}>
        <div style={{ fontSize: 12, letterSpacing: 3, textTransform: "uppercase", color: "#22c55e", fontWeight: 700 }}>free · australian · new zealand <span style={{ letterSpacing: 1, opacity: 0.7 }}>(+ suits worldwide)</span></div>
        <div style={{ fontSize: 19, fontWeight: 800, background: "linear-gradient(90deg,#22c55e,#3b82f6)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>Optimised Eats</div>
      </div>

      {/* Beta Banner */}
      <div style={{
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        color: "white",
        padding: "10px 16px",
        textAlign: "center",
        fontSize: "13px",
        fontWeight: "600",
        boxShadow: "0 2px 8px rgba(0,0,0,0.15)"
      }}>
        🧪 BETA — This app is free and evolving. Your feedback helps shape it!
      </div>

      {/* Progress Tabs */}
      {(() => {
        const steps = [
          { key: "profile", label: "Household", icon: "👤" },
          { key: "recipes", label: "Recipes", icon: "📖" },
          { key: "planner", label: "Planner", icon: "📅" },
          { key: "dashboard", label: "Nutrition", icon: "📊" },
          { key: "learn", label: "Learn", icon: "📚" },
        ];
        const stepMap = { profile: 0, recipes: 1, planner: 2, weekly: 2, shopping: 2, dashboard: 3, learn: 4 };
        const activeStep = stepMap[tab] ?? -1;
        if (tab === "home") return null;
        return (
          <div style={{ padding: "8px 12px 0", maxWidth: 480, margin: "0 auto" }}>
            <div style={{ display: "flex", gap: 3, background: "rgba(255,255,255,0.04)", borderRadius: 12, padding: "4px" }}>
              {steps.map((s, i) => {
                const isActive = activeStep === i;
                const isDone = activeStep > i;
                return (
                  <button key={s.key} onClick={() => setTab(s.key)}
                    style={{ flex: 1, background: isActive ? "linear-gradient(135deg,#22c55e,#16a34a)" : isDone ? "rgba(34,197,94,0.15)" : "transparent", border: "none", borderRadius: 9, padding: "6px 2px", cursor: "pointer", textAlign: "center", transition: "all 0.2s" }}>
                    <div style={{ fontSize: 11, fontWeight: 800, color: isActive ? "white" : isDone ? "#22c55e" : "#475569" }}>{i + 1}</div>
                    <div style={{ fontSize: 10, color: isActive ? "rgba(255,255,255,0.9)" : isDone ? "#22c55e" : "#475569", fontWeight: 600, marginTop: 1, whiteSpace: "nowrap", overflow: "hidden" }}>{s.label}</div>
                  </button>
                );
              })}
            </div>
            <div style={{ margin: "5px 4px 0", height: 3, background: "rgba(255,255,255,0.06)", borderRadius: 2, overflow: "hidden" }}>
              <div style={{ width: `${Math.max(0, ((activeStep + 1) / steps.length) * 100)}%`, height: "100%", background: "linear-gradient(90deg,#22c55e,#3b82f6)", borderRadius: 2, transition: "width 0.3s ease" }} />
            </div>
          </div>
        );
      })()}

      <div style={{ padding: "0 12px 140px", maxWidth: 480, margin: "0 auto" }}>

        {/* HOME */}
        {tab === "home" && (
          <div>
            {/* Hero */}
            <div style={{ textAlign: "center", padding: "20px 0 10px" }}>
              <div style={{ fontSize: 52 }}>🥗</div>
              <div style={{ fontSize: 22, fontWeight: 800, background: "linear-gradient(90deg,#22c55e,#3b82f6)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", marginTop: 6 }}>Optimised Eats</div>
              <div style={{ fontSize: 13, color: "#94a3b8", marginTop: 4, lineHeight: 1.5 }}>Eat better for less — personalised to your household</div>
            </div>

            {/* Country picker */}
            <div style={{ marginBottom: 18 }}>
              <div style={{ fontSize: 13, fontWeight: 700, color: "#64748b", textAlign: "center", marginBottom: 10, letterSpacing: 0.5 }}>
                {country ? "📍 Your region:" : "👇 Where are you shopping?"}
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
                {[
                  {
                    code: "AU", flag: "🇦🇺", name: "Australia",
                    stores: "Coles · Woolworths · Aldi",
                    color: "#f59e0b", border: "rgba(245,158,11,0.5)", bg: "rgba(245,158,11,0.12)",
                    bgActive: "rgba(245,158,11,0.22)",
                  },
                  {
                    code: "NZ", flag: "🇳🇿", name: "New Zealand",
                    stores: "Countdown · New World · Pak'nSave",
                    color: "#3b82f6", border: "rgba(59,130,246,0.5)", bg: "rgba(59,130,246,0.12)",
                    bgActive: "rgba(59,130,246,0.22)",
                  },
                ].map(c => {
                  const active = country === c.code;
                  return (
                    <button key={c.code} onClick={() => setAndSaveCountry(c.code)}
                      style={{
                        padding: "14px 10px", borderRadius: 14, cursor: "pointer", textAlign: "center",
                        border: active ? `2px solid ${c.border}` : "2px solid rgba(255,255,255,0.08)",
                        background: active ? c.bgActive : c.bg,
                        boxShadow: active ? `0 0 18px ${c.border}` : "none",
                        transition: "all 0.15s",
                      }}>
                      <div style={{ fontSize: 36 }}>{c.flag}</div>
                      <div style={{ fontSize: 15, fontWeight: 800, color: active ? c.color : "#e2e8f0", marginTop: 4 }}>{c.name}</div>
                      <div style={{ fontSize: 11, color: active ? c.color : "#64748b", marginTop: 3, lineHeight: 1.4 }}>{c.stores}</div>
                      {active && <div style={{ marginTop: 6, fontSize: 11, fontWeight: 700, color: c.color, background: `${c.border}30`, borderRadius: 20, padding: "2px 10px", display: "inline-block" }}>✓ Selected</div>}
                    </button>
                  );
                })}
              </div>
              {!country && (
                <div style={{ textAlign: "center", marginTop: 8, fontSize: 12, color: "#475569" }}>Tap your country to get started — sets store names &amp; pricing references</div>
              )}
            </div>

            {/* How it works */}
            <div style={{ background: "linear-gradient(135deg, rgba(59,130,246,0.12) 0%, rgba(34,197,94,0.08) 100%)", border: "1px solid rgba(59,130,246,0.25)", borderRadius: 14, padding: "14px 16px", marginBottom: 14 }}>
              <div style={{ fontSize: 13, fontWeight: 700, color: "#60a5fa", marginBottom: 10 }}>👋 How it works:</div>
              {[
                { step: "1", icon: "👤", label: "Add your household", desc: "Enter everyone who eats together — age, sex, and diet type. The app calculates personalised nutrient targets for each person based on official AU/NZ guidelines." },
                { step: "2", icon: "📖", label: "Browse recipes & build a plan", desc: "Go to Recipes and add meals to today's planner. Each recipe shows nutritional value, cost, and prep time. Boost recipes with extras like liver, eggs, or seeds." },
                { step: "3", icon: "📊", label: "Check your nutrient coverage", desc: "The Dashboard shows a live breakdown of how well your plan covers each nutrient against your personal RDI targets." },
                { step: "4", icon: "✅", label: "Fill the gaps cheaply", desc: "Low on iron or calcium? The app suggests the cheapest foods to fix it. Build a full day for under $10 per person." },
              ].map(s => (
                <div key={s.step} style={{ display: "flex", gap: 10, marginBottom: 10, alignItems: "flex-start" }}>
                  <div style={{ width: 24, height: 24, borderRadius: "50%", background: "rgba(59,130,246,0.2)", border: "1px solid rgba(59,130,246,0.4)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 13, fontWeight: 700, color: "#60a5fa", flexShrink: 0, marginTop: 1 }}>{s.step}</div>
                  <div>
                    <div style={{ fontSize: 14, fontWeight: 700, color: "#e2e8f0" }}>{s.icon} {s.label}</div>
                    <div style={{ fontSize: 13, color: "#64748b", lineHeight: 1.4, marginTop: 2 }}>{s.desc}</div>
                  </div>
                </div>
              ))}
            </div>

            {/* What makes this different */}
            <div style={{ background: "rgba(34,197,94,0.06)", border: "1px solid rgba(34,197,94,0.15)", borderRadius: 14, padding: "14px 16px", marginBottom: 14 }}>
              <div style={{ fontSize: 14, fontWeight: 700, color: "#22c55e", marginBottom: 10 }}>⚡ What makes Optimised Eats different:</div>
              {[
                ["🎯", "Personalised to your biology", "Targets are calculated from your exact age, sex, and life stage — not a generic adult average."],
                ["💰", "Optimised for your budget", "Every recipe is costed and ranked by nutritional value per dollar. Eat better for less."],
                ["🔬", "Science-backed, junk-free", "Based on Australian/NZ NRV guidelines. No influencer nonsense, no supplement upsells."],
                ["📅", "Plan a full week", "Build today's meals or plan 7 days ahead. Generate a shopping list with quantities auto-calculated."],
                ["🌍", "Works everywhere", "Recipes and nutrition science apply worldwide. Prices are in AU/NZ$ but the nutrient logic is universal."],
              ].map(([em, title, desc]) => (
                <div key={title} style={{ display: "flex", gap: 10, marginBottom: 8, alignItems: "flex-start" }}>
                  <span style={{ fontSize: 18, flexShrink: 0 }}>{em}</span>
                  <div>
                    <div style={{ fontSize: 14, fontWeight: 600, color: "#e2e8f0" }}>{title}</div>
                    <div style={{ fontSize: 13, color: "#64748b", lineHeight: 1.4 }}>{desc}</div>
                  </div>
                </div>
              ))}
            </div>

            {/* Quick links */}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, marginBottom: 14 }}>
              {[
                { label: "👤 Set up profile", sub: "Add your household", tab: "profile", color: "#3b82f6" },
                { label: "📖 Browse recipes", sub: "Find meals to add", tab: "recipes", color: "#22c55e" },
                { label: "📊 Dashboard", sub: "Check your coverage", tab: "dashboard", color: "#8b5cf6" },
                { label: "📅 Today's plan", sub: "Build today's meals", tab: "planner", color: "#f59e0b" },
              ].map(item => (
                <button key={item.tab} onClick={() => setTab(item.tab)} style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 12, padding: "12px 10px", cursor: "pointer", textAlign: "left" }}>
                  <div style={{ fontSize: 13, fontWeight: 700, color: item.color }}>{item.label}</div>
                  <div style={{ fontSize: 12, color: "#64748b", marginTop: 2 }}>{item.sub}</div>
                </button>
              ))}
            </div>

            {/* Free resources */}
            <div style={{ background: "rgba(0,0,0,0.2)", borderRadius: 14, padding: "12px 16px", marginBottom: 14 }}>
              <div style={{ fontSize: 14, fontWeight: 700, color: "#94a3b8", marginBottom: 8 }}>📚 FREE RESOURCES</div>
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                <a href="https://optimisedeats.com/guide/" target="_blank" rel="noopener noreferrer" style={{ background: "rgba(34,197,94,0.12)", color: "#4ade80", fontSize: 14, fontWeight: 600, padding: "7px 14px", borderRadius: 20, textDecoration: "none", border: "1px solid rgba(34,197,94,0.25)" }}>🗺️ Nutrition Guides</a>
                <a href="https://optimisedeats.com/budget-nutrition-guide.pdf" target="_blank" rel="noopener noreferrer" style={{ background: "rgba(59,130,246,0.12)", color: "#60a5fa", fontSize: 14, fontWeight: 600, padding: "7px 14px", borderRadius: 20, textDecoration: "none", border: "1px solid rgba(59,130,246,0.25)" }}>📄 PDF Guide</a>
                <a href="https://optimisedeats.com/budget-nutrition-ebook.epub" target="_blank" rel="noopener noreferrer" style={{ background: "rgba(139,92,246,0.12)", color: "#a78bfa", fontSize: 14, fontWeight: 600, padding: "7px 14px", borderRadius: 20, textDecoration: "none", border: "1px solid rgba(139,92,246,0.25)" }}>📚 EPUB</a>
                <a href="https://optimisedeats.com/guide/zh/" target="_blank" rel="noopener noreferrer" style={{ background: "rgba(239,68,68,0.12)", color: "#fca5a5", fontSize: 14, fontWeight: 600, padding: "7px 14px", borderRadius: 20, textDecoration: "none", border: "1px solid rgba(239,68,68,0.25)" }}>🇨🇳 中文版</a>
              </div>
            </div>

            {/* About */}
            <div style={{ fontSize: 13, color: "#64748b", lineHeight: 1.6, textAlign: "center", paddingBottom: 8 }}>
              Built with ❤️ to help real families eat better on a real budget.<br/>
              Nutrition targets based on AU/NZ NHMRC Nutrient Reference Values.
            </div>
          </div>
        )}

        {/* PROFILE */}
        {tab === "profile" && (
          <div>
            <div style={{ textAlign: "center", margin: "16px 0 20px" }}>
              {ready ? (
                <div style={{ display: "flex", justifyContent: "center", gap: 4, flexWrap: "wrap", marginBottom: 4 }}>
                  {household.map(m => (
                    <div key={m.id} style={{ fontSize: 36, lineHeight: 1 }}>{emj(m)}</div>
                  ))}
                </div>
              ) : (
                <div style={{ fontSize: 44 }}>👨‍👩‍👧‍👦</div>
              )}
              <h2 style={{ margin: "6px 0", fontSize: 17, fontWeight: 700 }}>Your Household</h2>
              <p style={{ margin: 0, fontSize: 14, color: "#94a3b8" }}>Add everyone who eats together.</p>
              {country && (
                <button onClick={() => go("home")} style={{ marginTop: 8, display: "inline-flex", alignItems: "center", gap: 5, background: country === "NZ" ? "rgba(59,130,246,0.15)" : "rgba(245,158,11,0.15)", border: country === "NZ" ? "1px solid rgba(59,130,246,0.35)" : "1px solid rgba(245,158,11,0.35)", borderRadius: 20, padding: "4px 12px", cursor: "pointer", fontSize: 13, fontWeight: 700, color: country === "NZ" ? "#60a5fa" : "#f59e0b" }}>
                  {country === "NZ" ? "🇳🇿" : "🇦🇺"} {country === "NZ" ? "New Zealand" : "Australia"} <span style={{ fontSize: 11, fontWeight: 400, opacity: 0.7 }}>· change</span>
                </button>
              )}
            </div>
            {/* Onboarding steps — only shown to new users */}
            {!ready && !editing && (
              <div style={{ background: "linear-gradient(135deg, rgba(59,130,246,0.12) 0%, rgba(34,197,94,0.08) 100%)", border: "1px solid rgba(59,130,246,0.25)", borderRadius: 14, padding: "14px 16px", marginBottom: 16 }}>
                <div style={{ fontSize: 13, fontWeight: 700, color: "#60a5fa", marginBottom: 10 }}>👋 Welcome to Optimised Eats — here's how it works:</div>
                {[
                  { step: "1", label: "Add your household", desc: "Enter everyone who eats together — their age, sex, and diet type. The app calculates personalised nutrient targets for each person.", done: false },
                  { step: "2", label: "Browse recipes & build a plan", desc: "Go to Recipes and add meals to today's planner. Each recipe shows its nutritional value, cost, and prep time.", done: false },
                  { step: "3", label: "Check your nutrient coverage", desc: "The Dashboard shows a live breakdown of how well your plan covers each nutrient against your personal RDI targets.", done: false },
                  { step: "4", label: "Fill the gaps", desc: "Low on calcium? The app will suggest cheap foods to fix it. Browse snacks and extras to reach 100% coverage.", done: false },
                ].map(s => (
                  <div key={s.step} style={{ display: "flex", gap: 10, marginBottom: 8, alignItems: "flex-start" }}>
                    <div style={{ width: 22, height: 22, borderRadius: "50%", background: "rgba(59,130,246,0.2)", border: "1px solid rgba(59,130,246,0.4)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 13, fontWeight: 700, color: "#60a5fa", flexShrink: 0, marginTop: 1 }}>{s.step}</div>
                    <div>
                      <div style={{ fontSize: 14, fontWeight: 700, color: "#e2e8f0" }}>{s.label}</div>
                      <div style={{ fontSize: 13, color: "#64748b", lineHeight: 1.4 }}>{s.desc}</div>
                    </div>
                  </div>
                ))}
                <div style={{ marginTop: 8, fontSize: 13, color: "#64748b", lineHeight: 1.4 }}>Start by tapping "Quick Start" below to add yourself, or use the "+" button to enter custom details.</div>
              </div>
            )}

            {/* Simple / Full mode toggle */}
            <div style={{ display: "flex", gap: 0, borderRadius: 10, overflow: "hidden", border: "1px solid rgba(255,255,255,0.1)", marginBottom: 16 }}>
              {[
                { val: false, label: "📊 Full app", desc: "Nutrients, gaps & detail" },
                { val: true,  label: "✨ Simple view", desc: "Just meals & cost" },
              ].map(opt => (
                <button key={String(opt.val)} onClick={() => { setSimpleMode(opt.val); try { localStorage.setItem("oe_simple", opt.val ? "1" : "0"); } catch {} }} style={{ flex: 1, padding: "10px 8px", background: simpleMode === opt.val ? (opt.val ? "rgba(139,92,246,0.25)" : "rgba(34,197,94,0.2)") : "rgba(255,255,255,0.03)", border: "none", cursor: "pointer", borderRight: !opt.val ? "1px solid rgba(255,255,255,0.08)" : "none" }}>
                  <div style={{ fontSize: 13, fontWeight: 700, color: simpleMode === opt.val ? (opt.val ? "#a78bfa" : "#4ade80") : "#64748b" }}>{opt.label}</div>
                  <div style={{ fontSize: 11, color: simpleMode === opt.val ? (opt.val ? "#c4b5fd" : "#86efac") : "#475569", marginTop: 2 }}>{opt.desc}</div>
                </button>
              ))}
            </div>

            {household.map(m => (
              <div key={m.id} style={{ background: activeId === m.id ? "rgba(34,197,94,0.08)" : "rgba(255,255,255,0.05)", borderRadius: 12, padding: "12px 16px", marginBottom: 8, border: activeId === m.id ? "1px solid rgba(34,197,94,0.3)" : "1px solid rgba(255,255,255,0.06)" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 10, cursor: "pointer", flex: 1 }} onClick={() => setActiveId(m.id)}>
                    <div style={{ width: 38, height: 38, borderRadius: "50%", background: "rgba(255,255,255,0.08)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 18 }}>{emj(m)}</div>
                    <div>
                      <div style={{ fontSize: 14, fontWeight: 700 }}>{m.name}</div>
                      <div style={{ fontSize: 13, color: "#94a3b8" }}>{m.age}yo {m.sex === "female" ? "♀" : "♂"} · {getRDA(m).cal}kcal{m.diet && m.diet !== "omnivore" ? ` · ${m.diet === "vegan" ? "🌱 Vegan" : "🥚 Vegetarian"}` : ""}</div>
                      {m.age >= 65 && <div style={{ fontSize: 12, color: "#f59e0b", marginTop: 2 }}>💪 Protein target raised for 65+ — muscle needs more to stay strong</div>}
                    </div>
                  </div>
                  <div style={{ display: "flex", gap: 4 }}>
                    <button onClick={() => setEditing({ ...m })} style={{ background: "none", border: "none", cursor: "pointer" }}>✏️</button>
                    {household.length > 1 && <button onClick={() => { setHousehold(h => h.filter(x => x.id !== m.id)); if (activeId === m.id) { const o = household.find(x => x.id !== m.id); if (o) setActiveId(o.id); } }} style={{ background: "none", border: "none", cursor: "pointer" }}>🗑️</button>}
                  </div>
                </div>
              </div>
            ))}

            {editing ? (
              <div style={{ background: "rgba(255,255,255,0.06)", borderRadius: 16, padding: 16, marginTop: 12, border: "1px solid rgba(59,130,246,0.3)" }}>
                <div style={{ fontSize: 13, fontWeight: 700, color: "#3b82f6", marginBottom: 12 }}>{editing.id ? "Edit" : "Add"} Member</div>
                <input type="text" value={editing.name} onChange={e => { setEditing({ ...editing, name: e.target.value }); setNameError(false); }} placeholder="Name (required)" style={{ width: "100%", padding: "8px 12px", borderRadius: 8, border: nameError ? "1px solid #ef4444" : "1px solid rgba(255,255,255,0.12)", background: nameError ? "rgba(239,68,68,0.06)" : "rgba(255,255,255,0.06)", color: "#f1f5f9", fontSize: 14, boxSizing: "border-box", marginBottom: nameError ? 4 : 10 }} />
                {nameError && <div style={{ fontSize: 13, color: "#ef4444", marginBottom: 10 }}>⚠️ Please enter a name before saving.</div>}
                <input type="number" min={1} max={100} value={editing.age} onChange={e => setEditing({ ...editing, age: e.target.value === "" ? "" : parseInt(e.target.value) || editing.age })} placeholder="Age" style={{ width: "100%", padding: "8px 12px", borderRadius: 8, border: "1px solid rgba(255,255,255,0.12)", background: "rgba(255,255,255,0.06)", color: "#f1f5f9", fontSize: 14, boxSizing: "border-box", marginBottom: 10 }} />
                <div style={{ display: "flex", gap: 8, marginBottom: 10 }}>
                  {["female", "male"].map(s => (
                    <button key={s} onClick={() => setEditing({ ...editing, sex: s })} style={{ flex: 1, padding: 8, borderRadius: 8, border: editing.sex === s ? "2px solid #22c55e" : "1px solid rgba(255,255,255,0.12)", background: editing.sex === s ? "rgba(34,197,94,0.15)" : "transparent", color: editing.sex === s ? "#22c55e" : "#94a3b8", cursor: "pointer", fontWeight: 600 }}>{s === "female" ? "♀ Female" : "♂ Male"}</button>
                  ))}
                </div>
                {editing.sex === "female" && editing.age >= 14 && (
                  <div style={{ display: "flex", gap: 6, marginBottom: 10 }}>
                    {[["none", "Standard"], ["pregnant", "🤰 Pregnant"], ["lactating", "🤱 Breastfeeding"]].map(([k, l]) => {
                      const a = k === "none" ? (!editing.pregnant && !editing.lactating) : k === "pregnant" ? editing.pregnant : editing.lactating;
                      return <button key={k} onClick={() => setEditing({ ...editing, pregnant: k === "pregnant", lactating: k === "lactating" })} style={{ flex: 1, padding: 6, borderRadius: 8, border: a ? "2px solid #22c55e" : "1px solid rgba(255,255,255,0.12)", background: a ? "rgba(34,197,94,0.15)" : "transparent", color: a ? "#22c55e" : "#94a3b8", cursor: "pointer", fontSize: 13, fontWeight: 600 }}>{l}</button>;
                    })}
                  </div>
                )}
                <div style={{ fontSize: 13, color: "#64748b", marginBottom: 5, fontWeight: 600 }}>Diet Type</div>
                <div style={{ display: "flex", gap: 6, marginBottom: 10 }}>
                  {[["omnivore", "🥩 Omnivore"], ["vegetarian", "🥚 Vegetarian"], ["vegan", "🌱 Vegan"]].map(([k, l]) => (
                    <button key={k} onClick={() => setEditing({ ...editing, diet: k })} style={{ flex: 1, padding: 6, borderRadius: 8, border: (editing.diet || "omnivore") === k ? "2px solid #22c55e" : "1px solid rgba(255,255,255,0.12)", background: (editing.diet || "omnivore") === k ? "rgba(34,197,94,0.15)" : "transparent", color: (editing.diet || "omnivore") === k ? "#22c55e" : "#94a3b8", cursor: "pointer", fontSize: 12, fontWeight: 600 }}>{l}</button>
                  ))}
                </div>
                <div style={{ fontSize: 13, color: "#64748b", marginBottom: 5, fontWeight: 600 }}>Choose Avatar</div>
                <div style={{ display: "flex", gap: 6, marginBottom: 10 }}>
                  {[["", "Default"], ["\u{1F3FB}", "Light"], ["\u{1F3FC}", "Med-Light"], ["\u{1F3FD}", "Medium"], ["\u{1F3FE}", "Brown"], ["\u{1F3FF}", "Dark"]].map(([tone, label]) => {
                    const active = (editing.tone || "") === tone;
                    const preview = (editing.age < 4 ? "👶" : editing.age < 13 ? "🧒" : editing.age < 18 ? "🧑" : editing.sex === "female" ? "👩" : "👨") + tone;
                    return (
                      <button key={label} onClick={() => setEditing({ ...editing, tone })} title={label} style={{ flex: 1, padding: "5px 2px", borderRadius: 8, border: active ? "2px solid #22c55e" : "1px solid rgba(255,255,255,0.12)", background: active ? "rgba(34,197,94,0.15)" : "transparent", cursor: "pointer", fontSize: 17, textAlign: "center", lineHeight: 1 }}>
                        {preview}
                      </button>
                    );
                  })}
                </div>
                <div style={{ display: "flex", gap: 8 }}>
                  <button onClick={() => { setEditing(null); setNameError(false); }} style={{ flex: 1, padding: 10, borderRadius: 8, border: "1px solid rgba(255,255,255,0.12)", background: "transparent", color: "#94a3b8", cursor: "pointer", fontWeight: 600 }}>Cancel</button>
                  <button onClick={() => { if (!editing.name.trim()) { setNameError(true); return; } setNameError(false); const saved = { ...editing, age: Math.max(1, parseInt(editing.age) || 1) }; if (household.find(m => m.id === saved.id)) { setHousehold(h => h.map(m => m.id === saved.id ? saved : m)); } else { const nm = { ...saved, id: Date.now() }; setHousehold(h => [...h, nm]); setActiveId(nm.id); } setEditing(null); }} style={{ flex: 2, padding: 10, borderRadius: 8, border: "none", background: "#22c55e", color: "#fff", cursor: "pointer", fontWeight: 700 }}>{household.find(m => m.id === editing.id) ? "Save" : "Add"}</button>
                </div>
              </div>
            ) : (
              <button onClick={() => setEditing({ name: "", age: 30, sex: "female", pregnant: false, lactating: false })} style={{ width: "100%", padding: 14, borderRadius: 12, border: "2px dashed rgba(255,255,255,0.15)", background: "transparent", color: "#94a3b8", fontSize: 14, cursor: "pointer", marginTop: 8, fontWeight: 600 }}>+ Add {ready ? "Member" : "Yourself"}</button>
            )}

            {!ready && !editing && (
              <div style={{ marginTop: 20 }}>
                <div style={{ fontSize: 14, color: "#64748b", marginBottom: 8, textAlign: "center" }}>Quick Start:</div>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 6 }}>
                  {[{ n: "Adult F", a: 30, s: "female", e: "👩" }, { n: "Adult M", a: 30, s: "male", e: "👨" }, { n: "Teen Girl", a: 15, s: "female", e: "👧" }, { n: "Teen Boy", a: 15, s: "male", e: "👦" }, { n: "Child", a: 6, s: "female", e: "🧒" }, { n: "Toddler", a: 2, s: "male", e: "👶" }].map(p => (
                    <button key={p.n} onClick={() => { const m = { name: p.n, age: p.a, sex: p.s, id: Date.now(), pregnant: false, lactating: false }; setHousehold(h => [...h, m]); setActiveId(m.id); }} style={{ padding: 10, borderRadius: 10, border: "1px solid rgba(255,255,255,0.08)", background: "rgba(255,255,255,0.04)", color: "#94a3b8", cursor: "pointer", textAlign: "center" }}>
                      <div style={{ fontSize: 22 }}>{p.e}</div>
                      <div style={{ fontSize: 13, fontWeight: 600 }}>{p.n}</div>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Vegan/Vegetarian supplement warnings */}
            {ready && !editing && !simpleMode && household.some(m => m.diet === "vegan" || m.diet === "vegetarian") && (
              <div style={{ marginTop: 12, background: "rgba(239,68,68,0.08)", border: "1px solid rgba(239,68,68,0.3)", borderRadius: 12, padding: 14 }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 }}>
                  <div style={{ fontSize: 13, fontWeight: 700, color: "#f87171" }}>⚠️ Supplement Checklist</div>
                  <button onClick={() => { setLearnOpen(p => ({...p, vegan: true})); go("learn"); }} style={{ fontSize: 12, color: "#60a5fa", background: "none", border: "none", cursor: "pointer", fontWeight: 600, padding: 0 }}>Full guide →</button>
                </div>
                {household.filter(m => m.diet === "vegan" || m.diet === "vegetarian").map(m => (
                  <div key={m.id} style={{ marginBottom: 12, paddingBottom: 12, borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
                    <div style={{ fontSize: 14, fontWeight: 700, color: "#e2e8f0", marginBottom: 6 }}>
                      {emj(m)} {m.name} — {m.diet === "vegan" ? "🌱 Vegan" : "🥚 Vegetarian"}
                      {m.age < 18 && <span style={{ fontSize: 12, color: "#f87171", marginLeft: 6, fontWeight: 700 }}>⚠️ Dependant — especially important</span>}
                    </div>
                    {m.diet === "vegan" ? (
                      <div style={{ display: "flex", flexDirection: "column", gap: 5 }}>
                        {[
                          { label: "Vitamin B12", urgency: "must", note: "500–1000μg cyanocobalamin daily. Zero in plant foods — irreversible nerve damage if deficient." },
                          { label: "Algae Omega-3 (DHA+EPA)", urgency: "must", note: "250–500mg algae oil daily. Flaxseed ALA does not convert enough." },
                          { label: "Vegan D3 (from lichen)", urgency: "high", note: "1000–2000 IU daily in winter or if mostly indoors." },
                          { label: "Iodine", urgency: "high", note: "Use iodised salt daily. Seaweed is unreliable." },
                          { label: "Calcium", urgency: "watch", note: "Fortified plant milk (300mg/250mL) + calcium-set tofu." },
                        ].map(s => (
                          <div key={s.label} style={{ display: "flex", gap: 8, alignItems: "flex-start", background: s.urgency === "must" ? "rgba(239,68,68,0.1)" : s.urgency === "high" ? "rgba(245,158,11,0.08)" : "rgba(255,255,255,0.04)", borderRadius: 8, padding: "6px 8px" }}>
                            <span style={{ fontSize: 10, fontWeight: 800, color: s.urgency === "must" ? "#f87171" : s.urgency === "high" ? "#f59e0b" : "#64748b", background: s.urgency === "must" ? "rgba(239,68,68,0.15)" : s.urgency === "high" ? "rgba(245,158,11,0.15)" : "rgba(255,255,255,0.07)", border: `1px solid ${s.urgency === "must" ? "rgba(239,68,68,0.35)" : s.urgency === "high" ? "rgba(245,158,11,0.35)" : "rgba(255,255,255,0.12)"}`, borderRadius: 5, padding: "2px 5px", marginTop: 1, flexShrink: 0, whiteSpace: "nowrap" }}>{s.urgency === "must" ? "Essential" : s.urgency === "high" ? "Highly recommended" : "Worth monitoring"}</span>
                            <div>
                              <div style={{ fontSize: 13, fontWeight: 700, color: "#e2e8f0" }}>{s.label}</div>
                              <div style={{ fontSize: 12, color: "#94a3b8", lineHeight: 1.4 }}>{s.note}</div>
                            </div>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div style={{ display: "flex", flexDirection: "column", gap: 5 }}>
                        {[
                          { label: "Vitamin B12", urgency: "high", note: "Eggs and dairy provide some, but levels are often low. Consider testing or supplementing." },
                          { label: "Omega-3 (DHA+EPA)", urgency: "high", note: "Limited in vegetarian diet. Algae oil is the most reliable source." },
                          { label: "Iron & Zinc", urgency: "watch", note: "Plant sources absorb at 2–5× lower rate. Always eat with Vitamin C. Soak legumes." },
                        ].map(s => (
                          <div key={s.label} style={{ display: "flex", gap: 8, alignItems: "flex-start", background: s.urgency === "high" ? "rgba(245,158,11,0.08)" : "rgba(255,255,255,0.04)", borderRadius: 8, padding: "6px 8px" }}>
                            <span style={{ fontSize: 10, fontWeight: 800, color: s.urgency === "high" ? "#f59e0b" : "#64748b", background: s.urgency === "high" ? "rgba(245,158,11,0.15)" : "rgba(255,255,255,0.07)", border: `1px solid ${s.urgency === "high" ? "rgba(245,158,11,0.35)" : "rgba(255,255,255,0.12)"}`, borderRadius: 5, padding: "2px 5px", marginTop: 1, flexShrink: 0, whiteSpace: "nowrap" }}>{s.urgency === "high" ? "Highly recommended" : "Worth monitoring"}</span>
                            <div>
                              <div style={{ fontSize: 13, fontWeight: 700, color: "#e2e8f0" }}>{s.label}</div>
                              <div style={{ fontSize: 12, color: "#94a3b8", lineHeight: 1.4 }}>{s.note}</div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
                <div style={{ fontSize: 12, color: "#64748b", lineHeight: 1.4 }}>This app tracks food nutrients only — supplements are not counted. Tap "Full guide →" above for dosing detail and sources.</div>
              </div>
            )}

            {ready && !editing && (
              <div style={{ marginTop: 16, background: "rgba(34,197,94,0.08)", borderRadius: 12, padding: 14, border: "1px solid rgba(34,197,94,0.2)" }}>
                <div style={{ fontSize: 13, fontWeight: 600, color: "#22c55e" }}>{household.length} people · ~{household.reduce((s, m) => s + (getRDA(m).cal || 0), 0).toLocaleString()} kcal/day</div>
                <button onClick={() => go("dashboard")} style={{ width: "100%", padding: 12, borderRadius: 10, border: "none", background: "linear-gradient(90deg,#22c55e,#16a34a)", color: "#fff", fontSize: 15, fontWeight: 700, cursor: "pointer", marginTop: 10 }}>View Dashboard →</button>
              </div>
            )}
          </div>
        )}

        {/* DASHBOARD */}
        {tab === "dashboard" && (
          <div>
            {!ready ? (
              <div style={{ textAlign: "center", marginTop: 40 }}>
                <p style={{ color: "#94a3b8" }}>Add household first.</p>
                <button onClick={() => go("profile")} style={{ padding: "10px 20px", borderRadius: 8, background: "#22c55e", color: "#fff", border: "none", cursor: "pointer", fontWeight: 600 }}>Set Up →</button>
              </div>
            ) : (
              <div>
                {prevTab && <button onClick={() => { setTab(prevTab); setPrevTab(null); }} style={{ background: "none", border: "none", color: "#3b82f6", cursor: "pointer", fontSize: 13, fontWeight: 600, padding: "8px 0" }}>← Back</button>}
                {household.length > 1 && (
                  <div style={{ display: "flex", gap: 6, justifyContent: "center", margin: "8px 0", flexWrap: "wrap" }}>
                    {household.map(m => <button key={m.id} onClick={() => setActiveId(m.id)} style={{ padding: "4px 12px", borderRadius: 20, fontSize: 14, cursor: "pointer", fontWeight: 600, border: activeId === m.id ? "2px solid #22c55e" : "1px solid rgba(255,255,255,0.1)", background: activeId === m.id ? "rgba(34,197,94,0.15)" : "transparent", color: activeId === m.id ? "#22c55e" : "#94a3b8" }}>{m.name}</button>)}
                  </div>
                )}
                <div style={{ textAlign: "center", margin: "8px 0" }}>
                  <div style={{ fontSize: 14, fontWeight: 700 }}>{active ? active.name : "You"}</div>
                  <div style={{ fontSize: 14, color: "#94a3b8" }}>{prof.sex === "female" ? "♀" : "♂"} {prof.age}yo · {nMeals} meal{nMeals !== 1 ? "s" : ""}</div>
                </div>

                {/* GUIDE HUB BANNER — dashboard */}
                {!simpleMode && <div style={{ margin: "0 0 16px", background: "linear-gradient(135deg, rgba(22,163,74,0.12), rgba(16,185,129,0.08))", border: "1px solid rgba(22,163,74,0.25)", borderRadius: 14, padding: 16 }}>
                  <div style={{ fontSize: 13, fontWeight: 800, color: "#22c55e", marginBottom: 4 }}>📖 Free Nutrition Guide</div>
                  <div style={{ fontSize: 14, color: "#86efac", lineHeight: 1.5, marginBottom: 12 }}>Deeper reading on every topic — nutrient gaps, pre-conception, pregnancy, kids, deficiency symptoms and 106 recipes.</div>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: 7, marginBottom: 10 }}>
                    {[
                      ["🔬 Nutrient Gaps", "/guide/nutrient-gaps/"],
                      ["🍟 Hidden Hunger", "/guide/hidden-hunger/"],
                      ["🤰 Pre-Conception", "/guide/pre-conception/"],
                      ["🍼 Pregnancy", "/guide/pregnancy/"],
                      ["👶 Kids", "/guide/kids/"],
                      ["📅 Life Stages", "/guide/life-stages/"],
                      ["😴 Sleep & Food", "/guide/sleep-nutrition/"],
                      ["🌱 Vegan", "/guide/vegan-nutrition/"],
                      ["🔍 Deficiency Signs", "/guide/deficiency-symptoms/"],
                      ["💪 Exercise", "/guide/exercise-nutrition/"],
                      ["💰 Budget Basics", "/guide/budget-basics/"],
                      ["🍽️ 106 Recipes", "/guide/recipes/"],
                    ].map(([label, href]) => (
                      <a key={href} href={`https://optimisedeats.com${href}`} target="_blank" rel="noopener noreferrer"
                        style={{ background: "rgba(22,163,74,0.18)", color: "#4ade80", fontSize: 13, fontWeight: 700, padding: "4px 11px", borderRadius: 20, textDecoration: "none", border: "1px solid rgba(22,163,74,0.28)" }}>
                        {label}
                      </a>
                    ))}
                    <a href="https://optimisedeats.com/guide/" target="_blank" rel="noopener noreferrer"
                      style={{ background: "#16a34a", color: "#fff", fontSize: 13, fontWeight: 700, padding: "4px 11px", borderRadius: 20, textDecoration: "none" }}>
                      All guides →
                    </a>
                    <a href="https://optimisedeats.com/guide/zh/" target="_blank" rel="noopener noreferrer"
                      style={{ background: "rgba(239,68,68,0.18)", color: "#fca5a5", fontSize: 13, fontWeight: 700, padding: "4px 11px", borderRadius: 20, textDecoration: "none", border: "1px solid rgba(239,68,68,0.28)" }}>
                      🇨🇳 中文版
                    </a>
                  </div>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: 7 }}>
                    <a href="https://optimisedeats.com/budget-nutrition-guide.pdf" target="_blank" rel="noopener noreferrer"
                      style={{ display: "inline-flex", alignItems: "center", gap: 6, background: "rgba(255,255,255,0.07)", border: "1px solid rgba(22,163,74,0.3)", color: "#86efac", fontSize: 13, fontWeight: 700, padding: "6px 12px", borderRadius: 8, textDecoration: "none" }}>
                      ⬇ PDF
                    </a>
                    <a href="https://optimisedeats.com/budget-nutrition-ebook.epub" target="_blank" rel="noopener noreferrer"
                      style={{ display: "inline-flex", alignItems: "center", gap: 6, background: "rgba(255,255,255,0.07)", border: "1px solid rgba(22,163,74,0.3)", color: "#86efac", fontSize: 13, fontWeight: 700, padding: "6px 12px", borderRadius: 8, textDecoration: "none" }}>
                      📚 EPUB
                    </a>
                  </div>
                </div>}

                {nMeals > 0 && (() => {
                  const pcts = NKS.map(k => Math.min((totals[k] / (rda[k] || 1)) * 100, 100));
                  const avg = Math.round(pcts.reduce((a, b) => a + b, 0) / pcts.length);
                  const met = pcts.filter(p => p >= 80).length;
                  const sc = avg >= 75 ? "#22c55e" : avg >= 40 ? "#f59e0b" : "#ef4444";
                  return (
                    <div style={{ textAlign: "center", margin: "12px 0 16px" }}>
                      <div style={{ display: "inline-flex", alignItems: "center", justifyContent: "center", width: 88, height: 88, borderRadius: "50%", border: "3px solid " + sc, background: sc + "15" }}>
                        <div>
                          <div style={{ fontSize: 26, fontWeight: 800, color: sc }}>{avg}%</div>
                          <div style={{ fontSize: 11, color: "#94a3b8" }}>avg coverage</div>
                        </div>
                      </div>
                      <div style={{ fontSize: 13, color: "#94a3b8", marginTop: 6 }}>{met}/{NKS.length} above 80%</div>
                      {avg < 60 && <div style={{ fontSize: 13, color: "#f59e0b", marginTop: 4 }}>💡 Add a snack to boost gaps</div>}
                    </div>
                  );
                })()}
                {nMeals === 0 && (
                  <div style={{ textAlign: "center", padding: 20 }}>
                    <div style={{ fontSize: 36 }}>🍽️</div>
                    <p style={{ fontSize: 13, color: "#94a3b8" }}>Add meals to see coverage.</p>
                    <button onClick={() => go("recipes")} style={{ padding: "8px 16px", borderRadius: 8, background: "#3b82f6", color: "#fff", border: "none", cursor: "pointer", fontWeight: 600 }}>Browse Recipes →</button>
                  </div>
                )}
                {nMeals > 0 && (
                  <div>
                    {!simpleMode && ["macro", "vit", "min", "fat"].map(cat => (
                      <div key={cat} style={{ marginBottom: 14 }}>
                        <div style={{ fontSize: 12, fontWeight: 700, textTransform: "uppercase", letterSpacing: 2, color: "#64748b", marginBottom: 6 }}>{cat === "vit" ? "vitamins" : cat === "min" ? "minerals" : cat === "fat" ? "essential fats" : "macros"}</div>
                        {NKS.filter(k => NK[k].cat === cat).map(k => <NutrientBar key={k} name={NK[k].name} cur={totals[k]} target={rda[k]} unit={NK[k].unit} />)}
                      </div>
                    ))}
                    {!simpleMode && suggestions.length > 0 && (
                      <div style={{ background: "rgba(59,130,246,0.08)", borderRadius: 12, padding: 14, border: "1px solid rgba(59,130,246,0.2)" }}>
                        <div style={{ fontSize: 14, fontWeight: 700, color: "#3b82f6", marginBottom: 8 }}>💡 Fill gaps with:</div>
                        {suggestions.map(r => (
                          <div key={r.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "6px 0" }}>
                            <span style={{ fontSize: 13 }}>{r.emoji} {r.name}</span>
                            <button onClick={() => addMeal(r)} style={{ background: "#3b82f6", color: "#fff", border: "none", borderRadius: 6, padding: "3px 8px", fontSize: 13, cursor: "pointer" }}>+ Add</button>
                          </div>
                        ))}
                      </div>
                    )}
                    {simpleMode && (
                      <div style={{ marginTop: 14, background: "rgba(139,92,246,0.08)", border: "1px solid rgba(139,92,246,0.2)", borderRadius: 12, padding: "10px 14px", display: "flex", alignItems: "center", justifyContent: "space-between", gap: 10 }}>
                        <div style={{ fontSize: 13, color: "#c4b5fd", lineHeight: 1.5 }}>✨ <strong>Simple view on</strong> — want to see vitamin & mineral detail?</div>
                        <button onClick={() => { setSimpleMode(false); try { localStorage.setItem("oe_simple", "0"); } catch {} }} style={{ background: "none", border: "none", color: "#a78bfa", fontSize: 13, fontWeight: 700, cursor: "pointer", whiteSpace: "nowrap", padding: 0 }}>Full app →</button>
                      </div>
                    )}
                    {!simpleMode && <div style={{ marginTop: 14, background: "rgba(34,197,94,0.07)", border: "1px solid rgba(34,197,94,0.2)", borderRadius: 12, padding: "10px 14px", display: "flex", alignItems: "center", justifyContent: "space-between", gap: 10 }}>
                      <div style={{ fontSize: 14, color: "#86efac", lineHeight: 1.5 }}>😌 <strong>Don't stress one off day</strong> — most nutrients balance out over the week.</div>
                      <button onClick={() => { setLearnOpen(p => ({ ...p, dailyweekly: true })); go("learn"); }} style={{ background: "none", border: "none", color: "#22c55e", fontSize: 13, fontWeight: 700, cursor: "pointer", whiteSpace: "nowrap", padding: 0 }}>Why? →</button>
                    </div>}
                  </div>
                )}
              </div>
            )}

          </div>
        )}

        {/* RECIPES */}
        {tab === "recipes" && (
          <div>
            {prevTab && <button onClick={() => { setTab(prevTab); setPrevTab(null); }} style={{ background: "none", border: "none", color: "#3b82f6", cursor: "pointer", fontSize: 13, fontWeight: 600, padding: "8px 0" }}>← Back</button>}
            {/* Nutrient gap mini box — shows when meals are planned and gaps exist (full mode only) */}
            {ready && nMeals > 0 && !simpleMode && (() => {
              const diet = activeDiet;
              const GAP_FOODS = {
                protein: diet === "vegan" ? "Lentils, chickpeas, tofu, tempeh, or pumpkin seeds" : diet === "vegetarian" ? "Eggs, Greek yoghurt, lentils, or cottage cheese" : "Eggs, canned tuna, lentils, or Greek yoghurt",
                fibre: "Oats, beans, apple, or a slice of wholegrain bread",
                omega3: diet === "vegan" ? "Algae oil supplement, walnuts, flaxseed, or chia seeds" : diet === "vegetarian" ? "Walnuts, flaxseed, chia seeds, or eggs" : "Sardines, salmon, or a small handful of walnuts",
                vitA: "Sweet potato or carrot — always eat with a little fat",
                vitC: "Red capsicum, orange, or kiwi fruit",
                vitD: diet === "vegan" ? "☀️ 15–30 min sun (best) — also check fortified plant milk or supplement" : "☀️ 15–30 min sun on arms/legs (best) — or sardines, eggs",
                vitK: "Spinach, kale, or broccoli",
                folate: "Lentils, spinach, or fortified cereal",
                vitB12: diet === "vegan" ? "⚠️ B12 is not in plant foods — a daily supplement or fortified foods are essential" : diet === "vegetarian" ? "Eggs, dairy, or fortified nutritional yeast — consider a supplement" : "Eggs, dairy, or meat",
                choline: diet === "vegan" ? "Tofu, quinoa, or broccoli (lower than eggs — consider a supplement)" : "2 eggs covers ~50% of your daily need",
                calcium: diet === "vegan" ? "Calcium-set tofu, fortified plant milk, or tahini" : "Milk, yoghurt, cheese, or sardines with bones",
                iron: diet === "vegan" ? "Lentils + Vit C always, pumpkin seeds, or spinach" : diet === "vegetarian" ? "Lentils + squeeze of lemon, spinach, or fortified cereal" : "Lentils + squeeze of lemon, beef mince, or spinach",
                magnesium: "Pumpkin seeds, spinach, dark chocolate, or black beans",
                zinc: diet === "vegan" ? "Pumpkin seeds, soaked oats, legumes (soak to improve absorption)" : diet === "vegetarian" ? "Pumpkin seeds, eggs, or soaked oats" : "Beef mince, pumpkin seeds, or soaked oats",
                potassium: "Banana, potato, yoghurt, or kidney beans",
                selenium: diet === "vegan" ? "1–2 Brazil nuts covers your whole day" : "1 Brazil nut covers your whole day — or canned tuna, eggs",
                iodine: diet === "vegan" ? "Iodised salt or a supplement (plant milks vary — check label)" : "Dairy, seafood, or iodised salt",
              };
              const gaps = NKS
                .map(k => ({ k, pct: Math.min((totals[k] / (rda[k] || 1)) * 100, 100) }))
                .filter(g => g.pct < 70)
                .sort((a, b) => a.pct - b.pct)
                .slice(0, 4);
              if (!gaps.length) return (
                <div style={{ background: "rgba(34,197,94,0.08)", border: "1px solid rgba(34,197,94,0.2)", borderRadius: 10, padding: "8px 12px", marginBottom: 10, fontSize: 13, color: "#86efac", fontWeight: 600 }}>
                  ✅ Looking good — today's meals cover your main nutrients!
                </div>
              );
              return (
                <div style={{ background: "rgba(245,158,11,0.08)", border: "1px solid rgba(245,158,11,0.2)", borderRadius: 12, padding: "10px 12px", marginBottom: 10 }}>
                  <div style={{ fontSize: 13, fontWeight: 700, color: "#f59e0b", marginBottom: 6 }}>⚡ Today's gaps — pick a snack to fill these:</div>
                  {gaps.map(g => (
                    <div key={g.k} style={{ padding: "4px 0", borderTop: "1px solid rgba(255,255,255,0.04)" }}>
                      <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                        <span style={{ fontSize: 13, fontWeight: 700, color: "#e2e8f0" }}>{NK[g.k].name}</span>
                        <span style={{ fontSize: 12, color: g.pct < 30 ? "#ef4444" : "#f59e0b", fontWeight: 700 }}>{Math.round(g.pct)}%</span>
                      </div>
                      <div style={{ fontSize: 12, color: "#60a5fa", marginTop: 1, lineHeight: 1.4 }}>{GAP_FOODS[g.k]}</div>
                    </div>
                  ))}
                </div>
              );
            })()}
            {/* Diet filter banner */}
            {activeDiet !== "omnivore" && (
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "rgba(34,197,94,0.08)", border: "1px solid rgba(34,197,94,0.2)", borderRadius: 10, padding: "7px 12px", marginBottom: 8 }}>
                <span style={{ fontSize: 13, color: "#86efac" }}>{activeDiet === "vegan" ? "🌱 Showing vegan recipes" : "🥚 Showing vegetarian recipes"} for {prof.name}</span>
                <button onClick={() => setShowAllDiets(v => !v)} style={{ fontSize: 12, color: showAllDiets ? "#22c55e" : "#64748b", background: "none", border: "none", cursor: "pointer", fontWeight: 600, padding: 0 }}>{showAllDiets ? "✓ Showing all" : "Show all →"}</button>
              </div>
            )}
            <div style={{ display: "flex", gap: 5, flexWrap: "wrap", justifyContent: "center", margin: "12px 0" }}>
              {[["all", "All"], ["breakfast", "🌅 Brekkie"], ["lunch", "☀️ Lunch"], ["dinner", "🌙 Dinner"], ["snack", "🍿 Snack"], ["vegetarian", "🥚 Veggie"], ["vegan", "🌱 Vegan"], ["chicken", "🍗 Chicken"], ["kangaroo", "🦘 Roo"], ["sardine", "🐟 Sardines"], ["organ-meat", "🫀 Organ"], ["hidden-nutrients", "🥷 Hidden"], ["freezer", "❄️ Freezer"], ["kid-friendly", "👶 Kids"]].map(([k, l]) => (
                <button key={k} onClick={() => setFilter(k)} style={{ padding: "4px 9px", borderRadius: 20, border: filter === k ? "1px solid #22c55e" : "1px solid rgba(255,255,255,0.1)", background: filter === k ? "rgba(34,197,94,0.15)" : "transparent", color: filter === k ? "#22c55e" : "#94a3b8", fontSize: 12, cursor: "pointer", fontWeight: 500 }}>{l}</button>
              ))}
            </div>
            {filter === "sardine" && (
              <div style={{ background: "rgba(59,130,246,0.1)", border: "1px solid rgba(59,130,246,0.3)", borderRadius: 12, padding: "10px 14px", marginBottom: 10 }}>
                <div style={{ fontSize: 13, fontWeight: 700, color: "#60a5fa", marginBottom: 4 }}>🐟 Why sardines?</div>
                <div style={{ fontSize: 13, color: "#94a3b8", lineHeight: 1.6 }}>Tinned sardines (~$1.50) are one of the most nutritious foods per dollar in Australia. A single tin delivers <strong style={{ color: "#e2e8f0" }}>250+ IU vitamin D</strong> (best dietary source), <strong style={{ color: "#e2e8f0" }}>~350mg calcium</strong> (eat the soft bones), <strong style={{ color: "#e2e8f0" }}>~9mcg B12</strong>, <strong style={{ color: "#e2e8f0" }}>1.4g omega-3</strong>, and <strong style={{ color: "#e2e8f0" }}>25g protein</strong> — all for less than a coffee.</div>
              </div>
            )}
            {filter === "kangaroo" && (
              <div style={{ background: "rgba(251,146,60,0.08)", border: "1px solid rgba(251,146,60,0.25)", borderRadius: 12, padding: "10px 14px", marginBottom: 10 }}>
                <div style={{ fontSize: 13, fontWeight: 700, color: "#fb923c", marginBottom: 4 }}>🦘 Why kangaroo?</div>
                <div style={{ fontSize: 13, color: "#94a3b8", lineHeight: 1.6 }}>Kangaroo is one of Australia's best kept nutrition secrets. It's <strong style={{ color: "#e2e8f0" }}>leaner than chicken breast</strong>, has <strong style={{ color: "#e2e8f0" }}>more iron than beef</strong>, and costs less per kilo. It's also free-range, wild-caught, and has the lowest environmental footprint of any red meat. Find it at Coles and Woolworths — usually $9–12/kg for mince.</div>
              </div>
            )}
            <div style={{ fontSize: 14, color: "#64748b", marginBottom: 8 }}>{filtered.length} recipes</div>
            {filtered.map(r => <RecipeCard key={r.id} recipe={r} onAdd={addMeal} rda={ready ? rda : null} prof={ready ? prof : null} />)}
          </div>
        )}

        {/* PLANNER */}
        {tab === "planner" && (
          <div>
            {prevTab && <button onClick={() => { setTab(prevTab); setPrevTab(null); }} style={{ background: "none", border: "none", color: "#3b82f6", cursor: "pointer", fontSize: 13, fontWeight: 600, padding: "8px 0" }}>← Back</button>}

            {/* ── DIARY HEADER ── */}
            {(() => {
              const today = new Date().toLocaleDateString("en-AU", { weekday: "short", day: "numeric", month: "short" });
              const pcts = NKS.map(k => Math.min((totals[k] / (rda[k] || 1)) * 100, 100));
              const avg = nMeals && ready ? Math.round(pcts.reduce((a, b) => a + b, 0) / pcts.length) : null;
              const scoreColor = avg === null ? "#64748b" : avg >= 75 ? "#22c55e" : avg >= 40 ? "#f59e0b" : "#ef4444";
              return (
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", margin: "12px 0 12px" }}>
                  <div>
                    <div style={{ fontSize: 17, fontWeight: 800 }}>🍽️ What I ate today</div>
                    <div style={{ fontSize: 13, color: "#64748b", marginTop: 2 }}>{today} · {nMeals} meal{nMeals !== 1 ? "s" : ""}{nMeals > 0 ? ` · $${dayCost.toFixed(2)}` : ""}</div>
                  </div>
                  <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
                    {avg !== null && (
                      <div style={{ fontSize: 13, fontWeight: 700, color: scoreColor, background: scoreColor + "18", border: `1px solid ${scoreColor}40`, borderRadius: 8, padding: "4px 9px" }}>{avg}% covered</div>
                    )}
                    {nMeals > 0 && <button onClick={() => setPlan({ breakfast: [], lunch: [], dinner: [], snack: [] })} style={{ fontSize: 12, color: "#ef4444", background: "none", border: "1px solid rgba(239,68,68,0.3)", borderRadius: 6, padding: "3px 8px", cursor: "pointer" }}>Clear</button>}
                  </div>
                </div>
              );
            })()}

            {/* ── MEAL LIST (first!) ── */}
            {!nMeals && (
              <div style={{ textAlign: "center", padding: 30, color: "#64748b" }}>
                <div style={{ fontSize: 48 }}>📋</div>
                <p style={{ marginBottom: 14 }}>Nothing logged yet today.</p>
                <button onClick={() => go("recipes")} style={{ padding: "10px 20px", borderRadius: 8, background: "#22c55e", color: "#fff", border: "none", cursor: "pointer", fontWeight: 600 }}>Browse Recipes →</button>
              </div>
            )}
            {["breakfast", "lunch", "dinner", "snack"].map(type => {
              const meals = plan[type];
              if (!meals.length) return null;
              const dot = type === "breakfast" ? "#f59e0b" : type === "lunch" ? "#38bdf8" : type === "snack" ? "#a78bfa" : "#818cf8";
              return (
                <div key={type} style={{ marginBottom: 14 }}>
                  <div style={{ fontSize: 12, fontWeight: 700, textTransform: "uppercase", letterSpacing: 2, color: "#64748b", marginBottom: 6, display: "flex", alignItems: "center", gap: 5 }}>
                    <span style={{ width: 7, height: 7, borderRadius: "50%", background: dot, display: "inline-block" }}></span>
                    {type === "breakfast" ? "🌅 Breakfast" : type === "lunch" ? "☀️ Lunch" : type === "snack" ? "🍿 Snack" : "🌙 Dinner"}
                  </div>
                  {meals.map((meal, i) => <PlannerCard key={type + "-" + i} meal={meal} onRemove={() => removeMeal(type, i)} onPortion={v => setPort(type, i, v)} onBoost={bId => togBoost(type, i, bId)} rda={rda} prof={prof} />)}
                </div>
              );
            })}

            {/* ── NEXT MEAL BUTTON ── */}
            {(() => {
              const has = { breakfast: plan.breakfast.length > 0, lunch: plan.lunch.length > 0, dinner: plan.dinner.length > 0, snack: plan.snack.length > 0 };
              const next = !has.breakfast ? { label: "Add Breakfast", emoji: "🌅", filter: "breakfast" }
                : !has.lunch ? { label: "Add Lunch", emoji: "☀️", filter: "lunch" }
                : !has.dinner ? { label: "Add Dinner", emoji: "🌙", filter: "dinner" }
                : !has.snack ? { label: "Add a Snack", emoji: "🍿", filter: "snack" }
                : null;
              if (!next) return (
                <div style={{ padding: "10px 14px", background: "rgba(34,197,94,0.08)", borderRadius: 10, border: "1px solid rgba(34,197,94,0.2)", textAlign: "center", marginBottom: 12 }}>
                  <span style={{ fontSize: 13, color: "#22c55e", fontWeight: 600 }}>✅ All meals covered!</span>
                </div>
              );
              return (
                <button onClick={() => { setFilter(next.filter); go("recipes"); }} style={{ width: "100%", marginBottom: 12, padding: "11px 14px", borderRadius: 10, border: "1px solid rgba(255,255,255,0.12)", background: "rgba(255,255,255,0.05)", color: "#e2e8f0", fontSize: 14, cursor: "pointer", fontWeight: 600, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                  <span>{next.emoji} {next.label}</span>
                  <span style={{ color: "#22c55e", fontSize: 16 }}>→</span>
                </button>
              );
            })()}

            {/* ── LOG FOOD (collapsible) ── */}
            <div style={{ background: "rgba(245,158,11,0.07)", border: "1px solid rgba(245,158,11,0.2)", borderRadius: 12, marginBottom: 14, overflow: "hidden" }}>
              <button onClick={() => setShowLog(s => !s)} style={{ width: "100%", display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px 14px", background: "none", border: "none", cursor: "pointer" }}>
                <span style={{ fontSize: 14, fontWeight: 700, color: "#f59e0b" }}>🍔 Ate something not in the recipes?</span>
                <span style={{ fontSize: 14, color: "#f59e0b", transition: "transform 0.2s", display: "inline-block", transform: showLog ? "rotate(180deg)" : "rotate(0deg)" }}>▼</span>
              </button>
              {showLog && <div style={{ padding: "0 14px 12px" }}><FoodLogger logFood={logFood} rda={rda} /></div>}
            </div>

            {/* ── NUTRIENT STATS (below the food) ── */}
            {nMeals > 0 && ready && (() => {
              const dayCal = Object.values(plan).flat().reduce((s, m) => { let c = (m.recipe.n.cal || 0) * m.portion; Object.entries(m.boosts || {}).forEach(([bId, qty]) => { const b = BOOSTS.find(x => x.id === bId); if (b && b.n.cal) c += b.n.cal * qty; }); return s + c; }, 0);
              const pcts = NKS.map(k => Math.min((totals[k] / (rda[k] || 1)) * 100, 100));
              const avg = Math.round(pcts.reduce((a, b) => a + b, 0) / pcts.length);
              const met = pcts.filter(p => p >= 80).length;
              const calPct = Math.round((dayCal / (rda.cal || 2000)) * 100);
              const keyNutrients = [
                { k: "protein", label: "Protein" }, { k: "calcium", label: "Calcium" },
                { k: "iron", label: "Iron" }, { k: "folate", label: "Folate" },
                { k: "vitC", label: "Vit C" }, { k: "vitD", label: "Vit D" },
                { k: "omega3", label: "Omega-3" }, { k: "fibre", label: "Fibre" },
              ].map(x => ({ ...x, pct: Math.round((totals[x.k] / (rda[x.k] || 1)) * 100) }));
              const gaps = keyNutrients.filter(n => n.pct < 50).map(n => n.label);
              const scoreColor = avg >= 75 ? "#22c55e" : avg >= 40 ? "#f59e0b" : "#ef4444";
              return (
                <div style={{ background: "rgba(0,0,0,0.25)", borderRadius: 14, padding: 14, border: "1px solid rgba(255,255,255,0.08)" }}>
                  <div style={{ fontSize: 12, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: 1, marginBottom: 10 }}>Today's Nutrients</div>
                  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 4, marginBottom: 8 }}>
                    <div style={{ background: "rgba(255,255,255,0.05)", borderRadius: 8, padding: "5px 8px", textAlign: "center" }}>
                      <div style={{ fontSize: 13, fontWeight: 700, color: "#22c55e" }}>${dayCost.toFixed(2)}</div>
                      <div style={{ fontSize: 11, color: "#64748b" }}>cost</div>
                    </div>
                    <div style={{ background: "rgba(255,255,255,0.05)", borderRadius: 8, padding: "5px 8px", textAlign: "center" }}>
                      <div style={{ fontSize: 13, fontWeight: 700, color: calPct > 110 ? "#f59e0b" : "#e2e8f0" }}>{Math.round(dayCal)}</div>
                      <div style={{ fontSize: 11, color: "#64748b" }}>/ {rda.cal} kcal</div>
                    </div>
                    <div style={{ background: "rgba(255,255,255,0.05)", borderRadius: 8, padding: "5px 8px", textAlign: "center" }}>
                      <div style={{ fontSize: 13, fontWeight: 700, color: scoreColor }}>{met}/{NKS.length}</div>
                      <div style={{ fontSize: 11, color: "#64748b" }}>at 80%+</div>
                    </div>
                  </div>
                  <div style={{ height: 5, borderRadius: 3, background: "rgba(255,255,255,0.08)", overflow: "hidden", marginBottom: 2 }}>
                    <div style={{ width: Math.min(calPct, 100) + "%", height: "100%", borderRadius: 3, background: calPct > 110 ? "#f59e0b" : "#3b82f6", transition: "width 0.4s" }} />
                  </div>
                  <div style={{ fontSize: 11, color: "#64748b", marginBottom: 10 }}>{calPct}% of daily calories</div>
                  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "6px 12px", borderTop: "1px solid rgba(255,255,255,0.06)", paddingTop: 10 }}>
                    {keyNutrients.map(n => {
                      const color = n.pct >= 80 ? "#22c55e" : n.pct >= 50 ? "#f59e0b" : "#ef4444";
                      return (
                        <div key={n.k}>
                          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, marginBottom: 2 }}>
                            <span style={{ color: "#94a3b8" }}>{n.label}</span>
                            <span style={{ color, fontWeight: 600 }}>{n.pct}%</span>
                          </div>
                          <div style={{ height: 4, borderRadius: 2, background: "rgba(255,255,255,0.08)", overflow: "hidden" }}>
                            <div style={{ width: Math.min(n.pct, 100) + "%", height: "100%", borderRadius: 2, background: color, transition: "width 0.4s" }} />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                  {gaps.length > 0
                    ? <div style={{ marginTop: 10, fontSize: 13, color: "#f59e0b" }}>⚠️ Still low: <strong>{gaps.join(", ")}</strong></div>
                    : <div style={{ marginTop: 10, fontSize: 13, color: "#22c55e", fontWeight: 600 }}>✅ All key nutrients looking good!</div>
                  }
                  <button onClick={() => go("dashboard")} style={{ width: "100%", marginTop: 10, padding: 9, borderRadius: 8, background: "#3b82f6", color: "#fff", border: "none", cursor: "pointer", fontWeight: 600, fontSize: 14 }}>View Full Nutrient Breakdown →</button>
                </div>
              );
            })()}
          </div>
        )}

        {/* WEEKLY PLAN */}
        {tab === "weekly" && ready && (
          <div>
            {prevTab && <button onClick={() => { setTab(prevTab); setPrevTab(null); }} style={{ background: "none", border: "none", color: "#3b82f6", cursor: "pointer", fontSize: 13, fontWeight: 600, padding: "8px 0" }}>← Back</button>}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
              <h2 style={{ margin: 0, fontSize: 18, fontWeight: 700 }}>Weekly Plan</h2>
              {(() => {
                const hasAny = Object.values(weekPlan).some(day => Object.values(day).flat().length > 0);
                return hasAny && (
                  <button 
                    onClick={() => setWeekPlan({
                      mon: { breakfast: [], lunch: [], dinner: [], snack: [] },
                      tue: { breakfast: [], lunch: [], dinner: [], snack: [] },
                      wed: { breakfast: [], lunch: [], dinner: [], snack: [] },
                      thu: { breakfast: [], lunch: [], dinner: [], snack: [] },
                      fri: { breakfast: [], lunch: [], dinner: [], snack: [] },
                      sat: { breakfast: [], lunch: [], dinner: [], snack: [] },
                      sun: { breakfast: [], lunch: [], dinner: [], snack: [] },
                    })}
                    style={{ fontSize: 13, color: "#ef4444", background: "none", border: "1px solid rgba(239,68,68,0.3)", borderRadius: 6, padding: "4px 10px", cursor: "pointer" }}
                  >
                    Clear Week
                  </button>
                );
              })()}
            </div>

            {/* Week summary cards */}
            {(() => {
              const totalMeals = Object.values(weekPlan).reduce((sum, day) => 
                sum + Object.values(day).flat().length, 0
              );
              
              const totalCost = Object.values(weekPlan).reduce((sum, day) => {
                const dayCost = Object.values(day).flat().reduce((s, meal) => {
                  let cost = meal.recipe.cost * meal.portion;
                  Object.entries(meal.boosts || {}).forEach(([bId, qty]) => {
                    const b = BOOSTS.find(x => x.id === bId);
                    if (b) cost += b.cost * qty;
                  });
                  return s + cost;
                }, 0);
                return sum + dayCost;
              }, 0);

              return (
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 8, marginBottom: 16 }}>
                  <div style={{ background: "rgba(34,197,94,0.1)", borderRadius: 10, padding: 10, textAlign: "center" }}>
                    <div style={{ fontSize: 20, fontWeight: 800, color: "#22c55e" }}>{totalMeals}</div>
                    <div style={{ fontSize: 12, color: "#64748b" }}>meals</div>
                  </div>
                  <div style={{ background: "rgba(34,197,94,0.1)", borderRadius: 10, padding: 10, textAlign: "center" }}>
                    <div style={{ fontSize: 20, fontWeight: 800, color: "#22c55e" }}>${totalCost.toFixed(0)}</div>
                    <div style={{ fontSize: 12, color: "#64748b" }}>week cost</div>
                  </div>
                  <div style={{ background: "rgba(34,197,94,0.1)", borderRadius: 10, padding: 10, textAlign: "center" }}>
                    <div style={{ fontSize: 20, fontWeight: 800, color: "#22c55e" }}>${totalMeals > 0 ? (totalCost / 7).toFixed(2) : '0.00'}</div>
                    <div style={{ fontSize: 12, color: "#64748b" }}>per day</div>
                  </div>
                </div>
              );
            })()}

            {/* Days of the week */}
            {[
              {key: "mon", label: "Monday"},
              {key: "tue", label: "Tuesday"},
              {key: "wed", label: "Wednesday"},
              {key: "thu", label: "Thursday"},
              {key: "fri", label: "Friday"},
              {key: "sat", label: "Saturday"},
              {key: "sun", label: "Sunday"},
            ].map(({key, label}) => {
              const DayCard = () => {
                const [expanded, setExpanded] = useState(false);
                const dayMeals = weekPlan[key];
                const allMeals = Object.values(dayMeals).flat();
                const dayCount = allMeals.length;
                
                const dayCost = allMeals.reduce((sum, meal) => {
                  let cost = meal.recipe.cost * meal.portion;
                  Object.entries(meal.boosts || {}).forEach(([bId, qty]) => {
                    const b = BOOSTS.find(x => x.id === bId);
                    if (b) cost += b.cost * qty;
                  });
                  return sum + cost;
                }, 0);
                
                return (
                  <div style={{ marginBottom: 8, background: "rgba(255,255,255,0.04)", borderRadius: 12, border: "1px solid rgba(255,255,255,0.08)", overflow: "hidden" }}>
                    <div onClick={() => setExpanded(!expanded)} style={{ padding: "12px 14px", cursor: "pointer", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                        <span style={{ fontSize: 14, fontWeight: 700, color: "#f1f5f9" }}>{label}</span>
                        {dayCount > 0 && (
                          <span style={{ fontSize: 12, padding: "2px 8px", background: "rgba(34,197,94,0.15)", color: "#4ade80", borderRadius: 10, fontWeight: 600 }}>
                            {dayCount}
                          </span>
                        )}
                      </div>
                      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                        {dayCount > 0 && (
                          <span style={{ fontSize: 14, color: "#22c55e", fontWeight: 600 }}>${dayCost.toFixed(2)}</span>
                        )}
                        <span style={{ color: "#64748b", fontSize: 14 }}>{expanded ? "▲" : "▼"}</span>
                      </div>
                    </div>

                    {expanded && (
                      <div style={{ padding: "0 14px 14px", borderTop: "1px solid rgba(255,255,255,0.06)" }}>
                        {["breakfast", "lunch", "dinner", "snack"].map(mealType => {
                          const meals = dayMeals[mealType];
                          if (meals.length === 0) return null;
                          
                          return (
                            <div key={mealType} style={{ marginTop: 10 }}>
                              <div style={{ fontSize: 12, fontWeight: 700, textTransform: "uppercase", letterSpacing: 1, color: "#64748b", marginBottom: 6 }}>
                                {mealType === "breakfast" ? "🌅" : mealType === "lunch" ? "☀️" : mealType === "snack" ? "🍿" : "🌙"} {mealType}
                              </div>
                              {meals.map((meal, i) => (
                                <WeekMealRow key={i} meal={meal} onRemove={() => setWeekPlan(prev => ({ ...prev, [key]: { ...prev[key], [mealType]: prev[key][mealType].filter((_, idx) => idx !== i) } }))} />
                              ))}
                            </div>
                          );
                        })}
                        <button 
                          onClick={() => {
                            setSelectedDay(key);
                            setTab("recipes");
                          }}
                          style={{ width: "100%", marginTop: 10, padding: "8px", borderRadius: 8, border: "1px solid rgba(255,255,255,0.1)", background: "rgba(34,197,94,0.08)", color: "#22c55e", fontSize: 14, fontWeight: 600, cursor: "pointer" }}
                        >
                          + Add Meal to {label}
                        </button>
                      </div>
                    )}
                  </div>
                );
              };
              return <DayCard key={key} />;
            })}

            {/* Empty state or shopping button */}
            {(() => {
              const totalMeals = Object.values(weekPlan).reduce((sum, day) => 
                sum + Object.values(day).flat().length, 0
              );
              
              if (totalMeals === 0) {
                return (
                  <div style={{ textAlign: "center", padding: "40px 20px", color: "#64748b" }}>
                    <div style={{ fontSize: 48 }}>📆</div>
                    <p style={{ margin: "10px 0" }}>No meals planned yet.</p>
                    <button onClick={() => setTab("recipes")} style={{ padding: "10px 20px", borderRadius: 8, background: "#22c55e", color: "#fff", border: "none", cursor: "pointer", fontWeight: 600 }}>
                      Browse Recipes →
                    </button>
                  </div>
                );
              }
              
              return (
                <button 
                  onClick={() => setTab("shopping")}
                  style={{ width: "100%", marginTop: 16, padding: "14px", borderRadius: 12, background: "linear-gradient(135deg, #22c55e 0%, #16a34a 100%)", color: "#fff", border: "none", cursor: "pointer", fontWeight: 700, fontSize: 14, boxShadow: "0 4px 12px rgba(34,197,94,0.3)" }}
                >
                  🛒 Generate Weekly Shopping List
                </button>
              );
            })()}
          </div>
        )}

        {/* SHOPPING */}
        {tab === "shopping" && (
          <div>
            {prevTab && <button onClick={() => { setTab(prevTab); setPrevTab(null); }} style={{ background: "none", border: "none", color: "#3b82f6", cursor: "pointer", fontSize: 13, fontWeight: 600, padding: "8px 0" }}>← Back</button>}
            <h2 style={{ margin: "12px 0 16px", fontSize: 18, fontWeight: 700, textAlign: "center" }}>Shopping List</h2>
            
            {/* Show shopping list from today's meals */}
            {nMeals > 0 && (() => {
              const fracs = {'½':0.5,'¼':0.25,'¾':0.75,'⅓':0.333,'⅔':0.667};
              const parseIng = (ing) => {
                const s = ing.replace(/^Optional:\s*/i, '').split('(')[0].trim();
                const m = s.match(/^([½¼¾⅓⅔]|\d+\.?\d*)\s*(g|ml|mL|L|kg|tbsp|tsp|cups?|tins?|dozen|slices?|pieces?)?\s+(.+)/i);
                if (m) {
                  const qty = fracs[m[1]] !== undefined ? fracs[m[1]] : parseFloat(m[1]) || 1;
                  return { name: m[3].trim(), qty, unit: (m[2] || '').toLowerCase() };
                }
                return { name: s, qty: 1, unit: '' };
              };
              const ingMap = {};
              Object.values(plan).flat().forEach(meal => {
                const mult = meal.portion * Math.max(household.length, 1);
                meal.recipe.ing.forEach(ing => {
                  const { name, qty, unit } = parseIng(ing);
                  const key = name.toLowerCase();
                  if (!ingMap[key]) ingMap[key] = { display: name, qty: 0, unit };
                  ingMap[key].qty += qty * mult;
                  if (!ingMap[key].unit && unit) ingMap[key].unit = unit;
                });
                Object.entries(meal.boosts || {}).forEach(([bId, qty]) => {
                  const b = BOOSTS.find(x => x.id === bId);
                  if (b) {
                    const bKey = b.label.toLowerCase();
                    if (!ingMap[bKey]) ingMap[bKey] = { display: b.label + (b.amount ? ` (${b.amount})` : ''), qty: 0, unit: '' };
                    ingMap[bKey].qty += qty * Math.max(household.length, 1);
                  }
                });
              });
              const sortedItems = Object.values(ingMap).sort((a, b) => a.display.localeCompare(b.display));
              return (
                <div style={{ marginBottom: 20 }}>
                  <div style={{ fontSize: 13, fontWeight: 700, textTransform: "uppercase", letterSpacing: 2, color: "#64748b", marginBottom: 8 }}>FROM TODAY'S MEALS{household.length > 1 ? " — " + household.length + " people" : ""}</div>
                  {sortedItems.map((item, j) => {
                    const ck = "today_" + j;
                    const qtyRounded = Math.round(item.qty * 10) / 10;
                    const qtyDisplay = item.unit ? `${qtyRounded}${item.unit}` : item.qty > 1 ? `×${Math.round(item.qty)}` : '';
                    return (
                      <div key={j} onClick={() => setChecked(p => ({ ...p, [ck]: !p[ck] }))} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "9px 12px", background: checked[ck] ? "rgba(34,197,94,0.08)" : "rgba(255,255,255,0.04)", borderRadius: 8, marginBottom: 3, cursor: "pointer" }}>
                        <div style={{ display: "flex", alignItems: "center", gap: 10, flex: 1 }}>
                          <div style={{ width: 18, height: 18, borderRadius: 4, border: checked[ck] ? "2px solid #22c55e" : "2px solid rgba(255,255,255,0.15)", background: checked[ck] ? "#22c55e" : "transparent", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>{checked[ck] && <span style={{ color: "#fff", fontSize: 13 }}>✓</span>}</div>
                          <span style={{ fontSize: 13, color: checked[ck] ? "#64748b" : "#e2e8f0", textDecoration: checked[ck] ? "line-through" : "none" }}>{item.display}</span>
                        </div>
                        {qtyDisplay && <span style={{ fontSize: 13, color: "#f59e0b", fontWeight: 600, marginRight: 8 }}>{qtyDisplay}</span>}
                      </div>
                    );
                  })}
                </div>
              );
            })()}

            {/* Show shopping list from weekly plan */}
            {(() => {
              const weekMealsCount = Object.values(weekPlan).reduce((sum, day) => 
                sum + Object.values(day).flat().length, 0
              );
              
              if (weekMealsCount === 0) return null;
              
              const fracs2 = {'½':0.5,'¼':0.25,'¾':0.75,'⅓':0.333,'⅔':0.667};
              const parseIng2 = (ing) => {
                const s = ing.replace(/^Optional:\s*/i, '').split('(')[0].trim();
                const m = s.match(/^([½¼¾⅓⅔]|\d+\.?\d*)\s*(g|ml|mL|L|kg|tbsp|tsp|cups?|tins?|dozen|slices?|pieces?)?\s+(.+)/i);
                if (m) {
                  const qty = fracs2[m[1]] !== undefined ? fracs2[m[1]] : parseFloat(m[1]) || 1;
                  return { name: m[3].trim(), qty, unit: (m[2] || '').toLowerCase() };
                }
                return { name: s, qty: 1, unit: '' };
              };
              const ingMap2 = {};
              Object.values(weekPlan).forEach(day => {
                Object.values(day).flat().forEach(meal => {
                  const mult = meal.portion * Math.max(household.length, 1);
                  meal.recipe.ing.forEach(ing => {
                    const { name, qty, unit } = parseIng2(ing);
                    const key = name.toLowerCase();
                    if (!ingMap2[key]) ingMap2[key] = { display: name, qty: 0, unit };
                    ingMap2[key].qty += qty * mult;
                    if (!ingMap2[key].unit && unit) ingMap2[key].unit = unit;
                  });
                  Object.entries(meal.boosts || {}).forEach(([bId, qty]) => {
                    const b = BOOSTS.find(x => x.id === bId);
                    if (b) {
                      const bKey = b.label.toLowerCase();
                      if (!ingMap2[bKey]) ingMap2[bKey] = { display: b.label + (b.amount ? ` (${b.amount})` : ''), qty: 0, unit: '' };
                      ingMap2[bKey].qty += qty * Math.max(household.length, 1);
                    }
                  });
                });
              });
              const sortedItems = Object.values(ingMap2).sort((a, b) => a.display.localeCompare(b.display));
              return (
                <div style={{ marginBottom: 20 }}>
                  <div style={{ fontSize: 13, fontWeight: 700, textTransform: "uppercase", letterSpacing: 2, color: "#64748b", marginBottom: 8 }}>📆 FROM THIS WEEK ({weekMealsCount} meals)</div>
                  {sortedItems.map((item, j) => {
                    const ck = "week_" + j;
                    const qtyRounded = Math.round(item.qty * 10) / 10;
                    const qtyDisplay = item.unit ? `${qtyRounded}${item.unit}` : item.qty > 1 ? `×${Math.round(item.qty)}` : '';
                    return (
                      <div key={j} onClick={() => setChecked(p => ({ ...p, [ck]: !p[ck] }))} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "9px 12px", background: checked[ck] ? "rgba(34,197,94,0.08)" : "rgba(255,255,255,0.04)", borderRadius: 8, marginBottom: 3, cursor: "pointer" }}>
                        <div style={{ display: "flex", alignItems: "center", gap: 10, flex: 1 }}>
                          <div style={{ width: 18, height: 18, borderRadius: 4, border: checked[ck] ? "2px solid #22c55e" : "2px solid rgba(255,255,255,0.15)", background: checked[ck] ? "#22c55e" : "transparent", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>{checked[ck] && <span style={{ color: "#fff", fontSize: 13 }}>✓</span>}</div>
                          <span style={{ fontSize: 13, color: checked[ck] ? "#64748b" : "#e2e8f0", textDecoration: checked[ck] ? "line-through" : "none" }}>{item.display}</span>
                        </div>
                        {qtyDisplay && <span style={{ fontSize: 13, color: "#f59e0b", fontWeight: 600, marginRight: 8 }}>{qtyDisplay}</span>}
                      </div>
                    );
                  })}
                </div>
              );
            })()}

            {nMeals === 0 && Object.values(weekPlan).reduce((sum, day) => sum + Object.values(day).flat().length, 0) === 0 && (
              <div style={{ textAlign: "center", padding: "40px 20px", color: "#64748b" }}>
                <div style={{ fontSize: 48 }}>🛒</div>
                <p style={{ margin: "10px 0" }}>No meals planned yet.</p>
                <p style={{ fontSize: 14, margin: "0 0 16px" }}>Add meals to your planner to generate a shopping list.</p>
                <button onClick={() => go("planner")} style={{ padding: "10px 20px", borderRadius: 8, background: "#22c55e", color: "#fff", border: "none", cursor: "pointer", fontWeight: 600 }}>Go to Planner →</button>
              </div>
            )}

            {/* Budget staples - always good to have */}
            <div style={{ marginTop: 24, paddingTop: 16, borderTop: "1px solid rgba(255,255,255,0.08)" }}>
              <div style={{ fontSize: 13, fontWeight: 700, textTransform: "uppercase", letterSpacing: 2, color: "#64748b", marginBottom: 8 }}>💰 BUDGET STAPLES (ALWAYS STOCK)</div>
              <div style={{ fontSize: 13, color: "#94a3b8", marginBottom: 10 }}>
                {activeDiet === "vegan" ? "🌱 Vegan pantry essentials:" : activeDiet === "vegetarian" ? "🥚 Vegetarian pantry essentials:" : "Keep these on hand for any recipe:"}
              </div>
              {(activeDiet === "vegan" ? [
                ["Oats (1kg)", 2.50], ["Brown rice (1kg)", 3.00], ["Lentils (1kg)", 3.50],
                ["Tinned tomatoes ×4", 4.00], ["Tinned beans ×4", 5.00], ["Frozen veg (1kg)", 2.80],
                ["Tofu — firm (600g)", 4.50], ["Plant milk (2L oat/soy)", 3.80], ["Bread (wholegrain)", 3.50],
                ["Onions (1kg)", 2.50], ["Carrots (1kg)", 2.00], ["Peanut butter", 3.50],
                ["Nutritional yeast", 4.00], ["Soy sauce", 2.50], ["Oil (canola/olive)", 4.00],
              ] : activeDiet === "vegetarian" ? [
                ["Eggs (1 dozen)", 6.50], ["Milk (2L)", 3.20], ["Bread (wholegrain)", 3.50],
                ["Oats (1kg)", 2.50], ["Brown rice (1kg)", 3.00], ["Lentils (1kg)", 3.50],
                ["Tinned tomatoes ×4", 4.00], ["Tinned beans ×4", 5.00], ["Frozen veg (1kg)", 2.80],
                ["Onions (1kg)", 2.50], ["Carrots (1kg)", 2.00], ["Cheese block (500g)", 5.00],
                ["Peanut butter", 3.50], ["Yoghurt (1kg)", 4.50], ["Oil (canola/olive)", 4.00],
              ] : [
                ["Eggs (1 dozen)", 6.50], ["Milk (2L)", 3.20], ["Bread (wholegrain)", 3.50],
                ["Oats (1kg)", 2.50], ["Brown rice (1kg)", 3.00], ["Lentils (1kg)", 3.50],
                ["Tinned tomatoes ×4", 4.00], ["Tinned beans ×4", 5.00], ["Frozen veg (1kg)", 2.80],
                ["Onions (1kg)", 2.50], ["Carrots (1kg)", 2.00], ["Cheese block (500g)", 5.00],
                ["Peanut butter", 3.50], ["Soy sauce", 2.50], ["Oil (canola/olive)", 4.00],
              ]).map(([item, cost], j) => {
                const ck = "staple_" + j;
                return (
                  <div key={j} onClick={() => setChecked(p => ({ ...p, [ck]: !p[ck] }))} style={{ display: "flex", justifyContent: "space-between", padding: "8px 12px", background: checked[ck] ? "rgba(34,197,94,0.08)" : "rgba(255,255,255,0.04)", borderRadius: 8, marginBottom: 3, cursor: "pointer" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                      <div style={{ width: 18, height: 18, borderRadius: 4, border: checked[ck] ? "2px solid #22c55e" : "2px solid rgba(255,255,255,0.15)", background: checked[ck] ? "#22c55e" : "transparent", display: "flex", alignItems: "center", justifyContent: "center" }}>{checked[ck] && <span style={{ color: "#fff", fontSize: 13 }}>✓</span>}</div>
                      <span style={{ fontSize: 14, color: checked[ck] ? "#64748b" : "#cbd5e1", textDecoration: checked[ck] ? "line-through" : "none" }}>{item}</span>
                    </div>
                    <span style={{ fontSize: 13, color: "#64748b" }}>${cost.toFixed(2)}</span>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* LEARN */}
        {tab === "learn" && (
          <div>
            {prevTab && <button onClick={() => { setTab(prevTab); setPrevTab(null); }} style={{ background: "none", border: "none", color: "#3b82f6", cursor: "pointer", fontSize: 13, fontWeight: 600, padding: "8px 0" }}>← Back</button>}
            <div style={{ textAlign: "center", margin: "16px 0 20px" }}>
              <div style={{ fontSize: 44 }}>📚</div>
              <h2 style={{ margin: "6px 0", fontSize: 17, fontWeight: 700 }}>Australian Nutrition Reality</h2>
              <p style={{ margin: 0, fontSize: 14, color: "#94a3b8" }}>Australian Bureau of Statistics (ABS) National Nutrition Survey 2023</p>
            </div>

            {/* About & Disclaimer */}
            <div style={{ marginBottom: 16 }}>
              <div onClick={() => setLearnOpen(p => ({...p, about: !p.about}))}
                style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "rgba(255,255,255,0.06)", borderRadius: 12, padding: "12px 16px", cursor: "pointer" }}>
                <span style={{ fontWeight: 700, fontSize: 14 }}>👋 About This App & Disclaimer</span>
                <span style={{ fontSize: 14, color: "#64748b" }}>{learnOpen.about ? "▲" : "▼"}</span>
              </div>
              {learnOpen.about && (
                <div style={{ background: "rgba(255,255,255,0.03)", borderRadius: 12, padding: "14px 16px", marginTop: 6 }}>
                  <div style={{ fontSize: 13, fontWeight: 700, color: "#e2e8f0", marginBottom: 8 }}>Hi, I'm Chris 👋</div>
                  <p style={{ fontSize: 14, color: "#94a3b8", lineHeight: 1.6, margin: "0 0 10px" }}>
                    I'm not a dietitian or a doctor — I'm someone who is obsessed with nutrition research. Over the last several years I've spent hundreds of hours reading & listening to peer-reviewed studies, NRV guidelines, micronutrient data, and population health reports.
                  </p>
                  <p style={{ fontSize: 14, color: "#94a3b8", lineHeight: 1.6, margin: "0 0 10px" }}>
                    I'm driven by one question: why is it so hard to eat well on a normal budget?
                  </p>
                  <p style={{ fontSize: 14, color: "#94a3b8", lineHeight: 1.6, margin: "0 0 10px" }}>
                    I built this app because the information I was finding was genuinely useful — but it was scattered, technical, and locked behind paywalls or written for researchers. People want to feed their families properly but the guidance is either too vague ("eat more vegetables") or too expensive in practice.
                  </p>
                  <p style={{ fontSize: 14, color: "#94a3b8", lineHeight: 1.6, margin: "0 0 14px" }}>
                    This is my attempt to turn years of self-directed research into something practical and free. I'm a researcher by curiosity, not by credential — and I think that's worth being upfront about. The science here is real, but I'm not infallible. Use this app as a starting point, not as the final word.
                  </p>
                  <div style={{ background: "rgba(245,158,11,0.1)", border: "1px solid rgba(245,158,11,0.25)", borderRadius: 10, padding: "10px 12px" }}>
                    <div style={{ fontSize: 14, fontWeight: 700, color: "#f59e0b", marginBottom: 4 }}>⚠️ Important Disclaimer</div>
                    <p style={{ fontSize: 13, color: "#94a3b8", lineHeight: 1.5, margin: "0 0 6px" }}>
                      This app is a general educational tool only. It is not medical advice, dietary advice, or a substitute for professional health guidance. Nutrient Reference Values are population-level guidelines — your individual needs may differ based on health conditions, medications, lifestyle, and other factors.
                    </p>
                    <p style={{ fontSize: 13, color: "#94a3b8", lineHeight: 1.5, margin: 0 }}>
                      Always consult a registered dietitian, GP, or qualified health professional before making significant changes to your diet, especially if you are pregnant, breastfeeding, managing a health condition, or have children with specific dietary needs.
                    </p>
                  </div>
                </div>
              )}
            </div>

            {/* Donate Section */}
            <div style={{ background: "linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%)", borderRadius: 16, padding: 20, margin: "20px 0", textAlign: "center" }}>
              <div style={{ fontSize: 24, marginBottom: 8 }}>💚</div>
              <div style={{ fontSize: 15, fontWeight: 700, color: "white", marginBottom: 6 }}>Support This Project</div>
              <div style={{ fontSize: 14, color: "rgba(255,255,255,0.9)", marginBottom: 14, lineHeight: 1.4 }}>This app is completely free. If it's helped you eat better for less, consider buying me a coffee! (I won't drink it within an hour of eating 😉)</div>
              <div style={{ display: "flex", gap: 8, justifyContent: "center", flexWrap: "wrap" }}>
                <a href="https://www.buymeacoffee.com/cbprojects" target="_blank" rel="noopener noreferrer" style={{ flex: "1 1 140px", maxWidth: "180px", padding: "10px 16px", borderRadius: 10, background: "rgba(255,255,255,0.95)", color: "#ec4899", fontSize: 13, fontWeight: 700, textDecoration: "none", display: "flex", alignItems: "center", justifyContent: "center", gap: 6 }}>
                  ☕ Buy Me a Coffee
                </a>
                <a href="https://paypal.me/cbprojectsaus" target="_blank" rel="noopener noreferrer" style={{ flex: "1 1 140px", maxWidth: "180px", padding: "10px 16px", borderRadius: 10, background: "rgba(255,255,255,0.95)", color: "#0070ba", fontSize: 13, fontWeight: 700, textDecoration: "none", display: "flex", alignItems: "center", justifyContent: "center", gap: 6 }}>
                  💙 Donate via PayPal
                </a>
              </div>
            </div>

            {/* GUIDE HUB BANNER */}
            <div style={{ background: "linear-gradient(135deg, rgba(22,163,74,0.15), rgba(16,185,129,0.1))", border: "1px solid rgba(22,163,74,0.3)", borderRadius: 14, padding: 16, marginBottom: 20 }}>
              <div style={{ fontSize: 13, fontWeight: 800, color: "#22c55e", marginBottom: 6 }}>📖 Free Nutrition Guide</div>
              <div style={{ fontSize: 14, color: "#86efac", lineHeight: 1.5, marginBottom: 12 }}>In-depth articles on every topic covered in this app — with full reference tables, deficiency symptoms, pre-conception advice and 106 recipes.</div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 10 }}>
                {[
                  ["🔬 Nutrient Gaps", "/guide/nutrient-gaps/"],
                  ["🍟 Hidden Hunger", "/guide/hidden-hunger/"],
                  ["🤰 Pre-Conception", "/guide/pre-conception/"],
                  ["🍼 Pregnancy", "/guide/pregnancy/"],
                  ["👶 Kids", "/guide/kids/"],
                  ["📅 Life Stages", "/guide/life-stages/"],
                  ["😴 Sleep & Food", "/guide/sleep-nutrition/"],
                  ["🌱 Vegan", "/guide/vegan-nutrition/"],
                  ["🔍 Deficiency Signs", "/guide/deficiency-symptoms/"],
                  ["💪 Exercise", "/guide/exercise-nutrition/"],
                  ["💰 Budget Basics", "/guide/budget-basics/"],
                  ["🍽️ 106 Recipes", "/guide/recipes/"],
                ].map(([label, href]) => (
                  <a key={href} href={`https://optimisedeats.com${href}`} target="_blank" rel="noopener noreferrer"
                    style={{ background: "rgba(22,163,74,0.2)", color: "#4ade80", fontSize: 13, fontWeight: 700, padding: "4px 10px", borderRadius: 20, textDecoration: "none", border: "1px solid rgba(22,163,74,0.3)" }}>
                    {label}
                  </a>
                ))}
                <a href="https://optimisedeats.com/guide/" target="_blank" rel="noopener noreferrer"
                  style={{ background: "#16a34a", color: "#fff", fontSize: 13, fontWeight: 700, padding: "4px 10px", borderRadius: 20, textDecoration: "none" }}>
                  All guides →
                </a>
                <a href="https://optimisedeats.com/guide/zh/" target="_blank" rel="noopener noreferrer"
                  style={{ background: "rgba(239,68,68,0.18)", color: "#fca5a5", fontSize: 13, fontWeight: 700, padding: "4px 10px", borderRadius: 20, textDecoration: "none", border: "1px solid rgba(239,68,68,0.28)" }}>
                  🇨🇳 中文版
                </a>
              </div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                <a href="https://optimisedeats.com/budget-nutrition-guide.pdf" target="_blank" rel="noopener noreferrer"
                  style={{ display: "inline-flex", alignItems: "center", gap: 6, background: "rgba(255,255,255,0.07)", border: "1px solid rgba(22,163,74,0.3)", color: "#86efac", fontSize: 13, fontWeight: 700, padding: "6px 12px", borderRadius: 8, textDecoration: "none" }}>
                  ⬇ PDF
                </a>
                <a href="https://optimisedeats.com/budget-nutrition-ebook.epub" target="_blank" rel="noopener noreferrer"
                  style={{ display: "inline-flex", alignItems: "center", gap: 6, background: "rgba(255,255,255,0.07)", border: "1px solid rgba(22,163,74,0.3)", color: "#86efac", fontSize: 13, fontWeight: 700, padding: "6px 12px", borderRadius: 8, textDecoration: "none" }}>
                  📚 EPUB
                </a>
              </div>
            </div>

            <div style={{ background: "rgba(239,68,68,0.12)", border: "1px solid rgba(239,68,68,0.3)", borderRadius: 16, padding: 20, marginBottom: 16, textAlign: "center" }}>
              <div style={{ fontSize: 44, fontWeight: 800, color: "#ef4444" }}>4.2%</div>
              <div style={{ fontSize: 13, color: "#fca5a5", fontWeight: 600 }}>of adults meet BOTH fruit AND veg recommendations</div>
            </div>
            <div style={{ fontSize: 13, fontWeight: 700, color: "#f59e0b", marginBottom: 10 }}>⚠️ People NOT Meeting Requirements:</div>
            {[
              { n: "Calcium", p: 60, d: "90% of teen girls & women 50+ fall short", c: "#ef4444" },
              { n: "Zinc (males)", p: 48, d: "Nearly half of all males", c: "#ef4444" },
              { n: "Iron (women 18-29)", p: 47, d: "Nearly half of young women", c: "#ef4444" },
              { n: "Magnesium", p: 31, d: "1 in 3 people", c: "#f59e0b" },
              { n: "Vitamin A", p: 23, d: "Almost 1 in 4", c: "#f59e0b" },
              { n: "Vitamin D", p: 21, d: "1 in 5 adults deficient", c: "#f59e0b" },
              { n: "Riboflavin B2", p: 20, d: "4.9 million Australians", c: "#f59e0b" },
              { n: "Thiamin B1", p: 16, d: "Getting worse since 2011", c: "#22c55e" },
            ].map(d => (
              <div key={d.n} style={{ marginBottom: 8, background: "rgba(255,255,255,0.04)", borderRadius: 10, padding: "8px 12px" }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 3 }}>
                  <span style={{ fontSize: 13, fontWeight: 600 }}>{d.n}</span>
                  <span style={{ fontSize: 15, fontWeight: 800, color: d.c }}>{d.p}%</span>
                </div>
                <div style={{ height: 5, borderRadius: 3, background: "rgba(255,255,255,0.08)", overflow: "hidden", marginBottom: 3 }}>
                  <div style={{ width: d.p + "%", height: "100%", borderRadius: 3, background: d.c }} />
                </div>
                <div style={{ fontSize: 13, color: "#94a3b8" }}>{d.d}</div>
              </div>
            ))}
            <div style={{ background: "rgba(34,197,94,0.08)", borderRadius: 12, padding: 14, margin: "16px 0" }}>
              <div style={{ fontSize: 13, fontWeight: 700, color: "#22c55e", marginBottom: 6 }}>✅ 5 Daily Habits</div>
              {["2 eggs — choline, B12, selenium", "Yoghurt or milk — calcium, iodine", "Citrus fruit — vitamin C", "Organ meat 1×/week — B12, vit A, folate, iron", "Seeds on anything — vit E, magnesium, zinc"].map((t, i) => (
                <div key={i} style={{ fontSize: 14, color: "#bbf7d0", marginBottom: 3 }}>• {t}</div>
              ))}
            </div>
            <div style={{ fontSize: 14, fontWeight: 700, margin: "16px 0 8px" }}>🔬 Absorption Tips</div>
            {[["✅ Iron + Vitamin C", "Boosts plant iron absorption"], ["✅ Fat + Vit A/D/E/K", "Need fat to absorb"], ["❌ Tea/Coffee + Iron", "Blocks 60%. Wait 1hr"], ["❌ Calcium + Iron", "They compete"]].map(([t, d], i) => (
              <div key={i} style={{ background: "rgba(255,255,255,0.04)", borderRadius: 8, padding: "6px 10px", marginBottom: 3 }}>
                <div style={{ fontSize: 14, fontWeight: 600 }}>{t}</div>
                <div style={{ fontSize: 13, color: "#94a3b8" }}>{d}</div>
              </div>
            ))}

            {/* DAILY VS WEEKLY */}
            <div style={{ marginTop: 20 }}>
              <div onClick={() => setLearnOpen(p => ({...p, dailyweekly: !p.dailyweekly}))}
                style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "rgba(255,255,255,0.06)", borderRadius: 12, padding: "12px 16px", cursor: "pointer" }}>
                <span style={{ fontWeight: 700, fontSize: 14 }}>😌 Daily vs Weekly — Does It Matter?</span>
                <span style={{ fontSize: 14, color: "#64748b" }}>{learnOpen.dailyweekly ? "▲" : "▼"}</span>
              </div>
              {learnOpen.dailyweekly && (
                <div style={{ background: "rgba(255,255,255,0.03)", borderRadius: "0 0 12px 12px", padding: "14px 16px", fontSize: 13, color: "#cbd5e1", lineHeight: 1.7 }}>
                  <p style={{ marginBottom: 12 }}>For most nutrients, hitting the target as a <strong style={{ color: "#f1f5f9" }}>weekly average is perfectly fine</strong>. Don't stress about one off day.</p>
                  {[
                    { emoji: "🟢", label: "Weekly average is fine", color: "#22c55e", items: [
                      ["Fat-soluble vitamins (A, D, E, K)", "Stored in your liver and body fat for weeks or months. Brief shortfalls are no problem."],
                      ["Minerals (calcium, magnesium, zinc)", "Your body regulates absorption and maintains stores. Consistent intake across the week is ideal but one low day self-corrects."],
                      ["Vitamin B12", "The liver stores 2–3 years' worth. Daily intake is less critical if your overall diet is adequate."],
                    ]},
                    { emoji: "🟡", label: "Aim for most days", color: "#f59e0b", items: [
                      ["Water-soluble vitamins (C, B-group)", "Excreted quickly, so daily intake matters more. That said, a day or two below target rarely causes problems in healthy people."],
                    ]},
                    { emoji: "🔴", label: "Daily consistency matters", color: "#ef4444", items: [
                      ["Iron", "Absorption is tightly regulated daily. You can't easily catch up — especially important for menstruating women. Try to hit iron targets most days."],
                    ]},
                  ].map(({ emoji, label, color, items }) => (
                    <div key={label} style={{ marginBottom: 14 }}>
                      <div style={{ fontSize: 14, fontWeight: 700, color, marginBottom: 6 }}>{emoji} {label}</div>
                      {items.map(([name, desc]) => (
                        <div key={name} style={{ background: "rgba(255,255,255,0.04)", borderRadius: 8, padding: "8px 10px", marginBottom: 4 }}>
                          <div style={{ fontSize: 14, fontWeight: 600, color: "#f1f5f9" }}>{name}</div>
                          <div style={{ fontSize: 13, color: "#94a3b8", marginTop: 2 }}>{desc}</div>
                        </div>
                      ))}
                    </div>
                  ))}
                  <div style={{ fontSize: 13, color: "#64748b", borderTop: "1px solid rgba(255,255,255,0.06)", paddingTop: 10, marginTop: 4 }}>Source: NHMRC Nutrient Reference Values for Australia and New Zealand</div>
                </div>
              )}
            </div>

            {/* WATER: ALL SOURCES COUNT */}
            <div style={{ marginTop: 20 }}>
              <div onClick={() => setLearnOpen(p => ({...p, water: !p.water}))}
                style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "rgba(255,255,255,0.06)", borderRadius: 12, padding: "12px 16px", cursor: "pointer" }}>
                <span style={{ fontWeight: 700, fontSize: 14 }}>💧 Water — All Sources Count</span>
                <span style={{ fontSize: 14, color: "#64748b" }}>{learnOpen.water ? "▲" : "▼"}</span>
              </div>
              {learnOpen.water && (
                <div style={{ background: "rgba(255,255,255,0.03)", borderRadius: "0 0 12px 12px", padding: "14px 16px", fontSize: 13, color: "#cbd5e1", lineHeight: 1.7 }}>
                  <p style={{ marginBottom: 10 }}>The daily fluid target (2.7–3.7 L depending on age and sex) includes <strong style={{ color: "#f1f5f9" }}>all fluid sources</strong> — not just plain water. Approximately 20–30% of daily intake comes from food alone.</p>
                  <div style={{ marginBottom: 12 }}>
                    <div style={{ fontSize: 14, fontWeight: 700, color: "#38bdf8", marginBottom: 6 }}>💧 High-water foods (% water by weight)</div>
                    {[
                      ["Cucumber / Lettuce / Zucchini", "94–96%"],
                      ["Tomato / Watermelon", "92–94%"],
                      ["Oranges / Milk", "87%"],
                      ["Plain yoghurt / Cooked oats", "84–85%"],
                      ["Eggs", "76%"],
                    ].map(([food, pct]) => (
                      <div key={food} style={{ display: "flex", justifyContent: "space-between", background: "rgba(255,255,255,0.04)", borderRadius: 6, padding: "5px 10px", marginBottom: 3 }}>
                        <span style={{ fontSize: 14 }}>{food}</span>
                        <span style={{ fontSize: 14, fontWeight: 700, color: "#38bdf8" }}>{pct}</span>
                      </div>
                    ))}
                  </div>
                  <div style={{ background: "rgba(56,189,248,0.08)", border: "1px solid rgba(56,189,248,0.2)", borderRadius: 8, padding: "10px 12px", marginBottom: 10, fontSize: 14 }}>
                    <strong style={{ color: "#38bdf8" }}>Practical example:</strong> A day with oats + milk at breakfast, two pieces of fruit, a salad lunch, and a vegetable-rich dinner contributes approximately 700–900 mL of water from food alone — before a single glass of water is consumed.
                  </div>
                  <p style={{ marginBottom: 10 }}>Tea and coffee count too — contrary to popular belief, moderate caffeine does <strong style={{ color: "#f1f5f9" }}>not</strong> cause net fluid loss. However, don't rely on heavily caffeinated drinks as your primary fluid source.</p>
                  <div style={{ marginBottom: 6 }}>
                    <div style={{ fontSize: 14, fontWeight: 700, color: "#fb923c", marginBottom: 6 }}>⚠️ Signs of under-hydration (appear before thirst)</div>
                    {["Urine darker than pale yellow", "Afternoon headaches", "Constipation", "Fatigue and difficulty concentrating"].map(s => (
                      <div key={s} style={{ background: "rgba(255,255,255,0.04)", borderRadius: 6, padding: "5px 10px", marginBottom: 3, fontSize: 14 }}>• {s}</div>
                    ))}
                  </div>
                  <div style={{ fontSize: 13, color: "#64748b", borderTop: "1px solid rgba(255,255,255,0.06)", paddingTop: 10, marginTop: 8 }}>Source: NHMRC Nutrient Reference Values for Australia and New Zealand</div>
                </div>
              )}
            </div>

            {/* TANNINS & IRON ABSORPTION */}
            <div style={{ marginTop: 20 }}>
              <div onClick={() => setLearnOpen(p => ({...p, tannins: !p.tannins}))}
                style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "rgba(255,255,255,0.06)", borderRadius: 12, padding: "12px 16px", cursor: "pointer" }}>
                <span style={{ fontWeight: 700, fontSize: 14 }}>☕ Tea, Coffee & Iron — What's Really Going On</span>
                <span style={{ fontSize: 14, color: "#64748b" }}>{learnOpen.tannins ? "▲" : "▼"}</span>
              </div>
              {learnOpen.tannins && (
                <div style={{ background: "rgba(255,255,255,0.03)", borderRadius: "0 0 12px 12px", padding: "14px 16px", fontSize: 13, color: "#cbd5e1", lineHeight: 1.7 }}>
                  <p style={{ marginBottom: 10 }}>It's not the caffeine — it's the <strong style={{ color: "#f1f5f9" }}>tannins</strong>. Tannins bind to non-haem iron (and zinc) in the gut, blocking absorption. This has nothing to do with caffeine — a decaf black tea has the same effect.</p>
                  <div style={{ marginBottom: 12 }}>
                    <div style={{ fontSize: 14, fontWeight: 700, color: "#ef4444", marginBottom: 6 }}>🚫 High-tannin foods that block iron absorption</div>
                    {[
                      ["Black tea", "Reduces iron absorption by up to 90% when drunk with a meal"],
                      ["Red wine", "Tannins + polyphenols — significant iron inhibitor"],
                      ["Coffee", "Chlorogenic acid reduces iron by 40–60% (less than black tea)"],
                      ["Dark chocolate 70%+", "Contains tannins — moderate impact"],
                      ["Some berries (esp. blueberries)", "Polyphenols with mild inhibitory effect"],
                      ["Some nuts (walnuts, pecans)", "Tannins in the skin — mild effect"],
                    ].map(([item, note]) => (
                      <div key={item} style={{ background: "rgba(255,255,255,0.04)", borderRadius: 6, padding: "6px 10px", marginBottom: 4 }}>
                        <div style={{ fontSize: 14, fontWeight: 700, color: "#f1f5f9" }}>{item}</div>
                        <div style={{ fontSize: 13, color: "#94a3b8" }}>{note}</div>
                      </div>
                    ))}
                  </div>
                  <div style={{ background: "rgba(34,197,94,0.08)", border: "1px solid rgba(34,197,94,0.2)", borderRadius: 8, padding: "10px 12px", marginBottom: 12, fontSize: 14 }}>
                    <strong style={{ color: "#22c55e" }}>The fix:</strong> Wait 1 hour before or after meals before having tea or coffee. Have your morning coffee before breakfast, or wait until mid-morning. This alone can meaningfully improve iron and zinc absorption — particularly important for women of reproductive age and vegetarians.
                  </div>
                  <div style={{ marginBottom: 12 }}>
                    <div style={{ fontSize: 14, fontWeight: 700, color: "#22c55e", marginBottom: 6 }}>✅ Low-tannin alternatives</div>
                    {[
                      ["Herbal teas (rooibos, chamomile, peppermint, ginger, hibiscus)", "Zero tannins — safe to drink with meals. Not from the tea plant."],
                      ["White tea", "Lowest tannin of true teas (young leaves, minimal processing)"],
                      ["Green tea (short steep)", "Low-moderate. Steep 1–2 min instead of 5 to reduce tannins"],
                      ["Carob", "Chocolate alternative with zero tannins, naturally sweet"],
                    ].map(([item, note]) => (
                      <div key={item} style={{ background: "rgba(255,255,255,0.04)", borderRadius: 6, padding: "6px 10px", marginBottom: 4 }}>
                        <div style={{ fontSize: 14, fontWeight: 700, color: "#f1f5f9" }}>{item}</div>
                        <div style={{ fontSize: 13, color: "#94a3b8" }}>{note}</div>
                      </div>
                    ))}
                  </div>
                  <div style={{ background: "rgba(56,189,248,0.08)", border: "1px solid rgba(56,189,248,0.2)", borderRadius: 8, padding: "8px 12px", fontSize: 14 }}>
                    <strong style={{ color: "#38bdf8" }}>Heme iron not affected:</strong> Tannins primarily block non-haem iron (from plants, fortified foods). Haem iron from meat is reduced by only 10–15%. This is one reason vegetarians and vegans have roughly double the iron requirements and need to be especially mindful.
                  </div>
                  <div style={{ borderTop: "1px solid rgba(255,255,255,0.06)", paddingTop: 10, marginTop: 10 }}>
                    <a href="https://optimisedeats.com/guide/nutrient-gaps/" target="_blank" rel="noopener noreferrer" style={{ display: "inline-flex", alignItems: "center", gap: 6, background: "rgba(59,130,246,0.12)", border: "1px solid rgba(59,130,246,0.3)", color: "#60a5fa", fontSize: 13, fontWeight: 700, padding: "7px 14px", borderRadius: 20, textDecoration: "none" }}>🔬 Nutrient Gaps Guide →</a>
                  </div>
                </div>
              )}
            </div>

            {/* PRE-CONCEPTION — BOTH PARTNERS */}
            <div style={{ marginTop: 20 }}>
              <div onClick={() => setLearnOpen(p => ({...p, precon: !p.precon}))}
                style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "rgba(255,255,255,0.06)", borderRadius: 12, padding: "12px 16px", cursor: "pointer" }}>
                <span style={{ fontWeight: 700, fontSize: 14 }}>👶 Pre-Conception Nutrition — Both Partners</span>
                <span style={{ fontSize: 14, color: "#64748b" }}>{learnOpen.precon ? "▲" : "▼"}</span>
              </div>
              {learnOpen.precon && (
                <div style={{ background: "rgba(255,255,255,0.03)", borderRadius: "0 0 12px 12px", padding: "14px 16px", fontSize: 13, color: "#cbd5e1", lineHeight: 1.7 }}>
                  <div style={{ background: "rgba(34,197,94,0.08)", border: "1px solid rgba(34,197,94,0.2)", borderRadius: 8, padding: "10px 12px", marginBottom: 12, fontSize: 14 }}>
                    <strong style={{ color: "#22c55e" }}>Start 6 months before you plan to conceive — both partners.</strong> Many critical developmental processes occur in the first 3–4 weeks of pregnancy, often before a woman knows she's pregnant.
                  </div>
                  {[
                    { emoji: "♀️", label: "Female partner", color: "#ec4899", items: [
                      ["Folate 400–800 mcg/day supplement", "Neural tube closure happens days 21–28 — before most women know they're pregnant. Every woman who could conceive should be supplementing. Diet alone isn't reliable enough."],
                      ["Build iron stores now", "Requirements nearly double in pregnancy (27 mg/day). Low ferritin entering pregnancy leaves almost no buffer."],
                      ["Iodine 150 mcg supplement", "NHMRC recommends supplementing from pre-conception through lactation. Australian soils are iodine-poor."],
                      ["DHA omega-3 200+ mg/day", "Sardines 2×/week or algae-based supplement. Maternal DHA depletion is strongly linked to postpartum depression."],
                    ]},
                    { emoji: "♂️", label: "Male partner", color: "#3b82f6", items: [
                      ["Zinc 14 mg/day", "Essential for testosterone and sperm development. 48% of Australian men fall short. Best sources: beef mince (8 mg/100g), pumpkin seeds (2.2 mg/30g)."],
                      ["Folate 400 mcg/day", "Required for sperm DNA synthesis. Low paternal folate is associated with chromosomal abnormalities in sperm."],
                      ["DHA omega-3", "Concentrated in the sperm midpiece — drives motility. Low DHA = poor sperm motility."],
                      ["Selenium 70 mcg/day", "Essential for sperm motility. 2 Brazil nuts = full daily requirement."],
                    ]},
                  ].map(({ emoji, label, color, items }) => (
                    <div key={label} style={{ marginBottom: 14 }}>
                      <div style={{ fontSize: 13, fontWeight: 700, color, marginBottom: 8 }}>{emoji} {label}</div>
                      {items.map(([name, desc]) => (
                        <div key={name} style={{ background: "rgba(255,255,255,0.04)", borderRadius: 8, padding: "8px 10px", marginBottom: 4 }}>
                          <div style={{ fontSize: 14, fontWeight: 600, color: "#f1f5f9" }}>{name}</div>
                          <div style={{ fontSize: 13, color: "#94a3b8", marginTop: 2 }}>{desc}</div>
                        </div>
                      ))}
                    </div>
                  ))}
                  <div style={{ borderTop: "1px solid rgba(255,255,255,0.06)", paddingTop: 10, marginTop: 4 }}>
                    <a href="https://optimisedeats.com/guide/pre-conception/" target="_blank" rel="noopener noreferrer" style={{ display: "inline-flex", alignItems: "center", gap: 6, background: "rgba(34,197,94,0.12)", border: "1px solid rgba(34,197,94,0.3)", color: "#4ade80", fontSize: 13, fontWeight: 700, padding: "7px 14px", borderRadius: 20, textDecoration: "none" }}>🤰 Full Pre-Conception Guide →</a>
                  </div>
                </div>
              )}
            </div>

            {/* CATABOLIC CYCLE */}
            <div style={{ marginBottom: 12 }}>
              <div onClick={() => setLearnOpen(p => ({...p, catabolic: !p.catabolic}))}
                style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "rgba(255,255,255,0.06)", borderRadius: learnOpen.catabolic ? "12px 12px 0 0" : 12, padding: "12px 16px", cursor: "pointer" }}>
                <span style={{ fontWeight: 700, fontSize: 14 }}>⚡ The Overnight Catabolic Cycle — Why Breakfast Protein Matters</span>
                <span style={{ fontSize: 14, color: "#64748b" }}>{learnOpen.catabolic ? "▲" : "▼"}</span>
              </div>
              {learnOpen.catabolic && (
                <div style={{ background: "rgba(255,255,255,0.03)", borderRadius: "0 0 12px 12px", padding: "14px 16px", fontSize: 13, color: "#cbd5e1", lineHeight: 1.7 }}>
                  <div style={{ background: "rgba(239,68,68,0.1)", border: "1px solid rgba(239,68,68,0.25)", borderRadius: 8, padding: "10px 12px", marginBottom: 14, fontSize: 14 }}>
                    <strong style={{ color: "#f87171" }}>You've been catabolic since ~10pm last night.</strong> Your body has been breaking down muscle protein to fuel the brain overnight. Your first meal is the switch — but only if it hits the threshold.
                  </div>
                  {[
                    ["The overnight fast — what's actually happening", "During an 8–12 hour overnight fast, the body runs gluconeogenesis — manufacturing glucose from amino acids stripped from muscle tissue. This is unavoidable. The cortisol awakening response then peaks ~30–45 min after waking, amplifying catabolism further. You're in maximum muscle breakdown at 7am every morning."],
                    ["The leucine threshold — what flips the switch", "Muscle protein synthesis is triggered by the mTOR pathway, activated by the amino acid leucine. The threshold is ~3g leucine per meal — roughly 30–40g of complete protein. Below this threshold, the anabolic switch barely activates. You're not building muscle; you're just slowing the breakdown slightly."],
                    ["Toast and cereal don't cut it", "2 slices of toast: ~8g protein, ~0.5g leucine. Bowl of corn flakes and milk: ~9g protein. A banana: ~1g protein. None of these cross the threshold. If your next meal is lunch, you've been catabolic for 14–16 hours straight — every single day."],
                    ["What actually works (and costs under $1.60)", "2 eggs + 200g Greek yoghurt = ~32g protein, ~2.7g leucine (YES). 3 eggs + 250mL milk = ~30g protein (YES). 2 eggs + 100g cottage cheese on toast = ~33g protein (YES). Greek yoghurt + oats + pumpkin seeds = ~28g protein (YES). These are the breakfasts that flip the switch."],
                    ["Older adults: the stakes are even higher", "Anabolic resistance raises the leucine threshold to 3.5–4g per meal — requiring 35–40g of protein to trigger the same muscle-building response. A low-protein breakfast in an older adult isn't just suboptimal — it's contributing to sarcopenia one morning at a time, compounded over years. Fix: 3 eggs + 200g Greek yoghurt = ~38g protein, ~$1.60."],
                    ["The less active = less food myth", "Many older adults reduce food intake because they're less active — but protein requirements don't decrease with reduced activity. They actually increase, because the muscle-building machinery becomes less efficient (anabolic resistance). Less food + higher threshold = accelerated muscle loss. This is one of the most clinically significant and least understood nutrition mistakes in ageing."],
                  ].map(([title, detail]) => (
                    <div key={title} style={{ marginBottom: 12 }}>
                      <div style={{ fontWeight: 700, color: "#e2e8f0", marginBottom: 3 }}>{title}</div>
                      <div>{detail}</div>
                    </div>
                  ))}
                  <div style={{ marginTop: 12, paddingTop: 10, borderTop: "1px solid rgba(255,255,255,0.08)" }}>
                    <a href="https://optimisedeats.com/guide/exercise-nutrition/" target="_blank" rel="noopener noreferrer" style={{ display: "inline-flex", alignItems: "center", gap: 6, background: "rgba(34,197,94,0.12)", border: "1px solid rgba(34,197,94,0.3)", color: "#4ade80", fontSize: 13, fontWeight: 700, padding: "7px 14px", borderRadius: 20, textDecoration: "none" }}>💪 Exercise & Nutrition Guide →</a>
                  </div>
                </div>
              )}
            </div>

            {/* HIDDEN HUNGER */}
            <div style={{ marginBottom: 12 }}>
              <div onClick={() => setLearnOpen(p => ({...p, hiddenhunger: !p.hiddenhunger}))}
                style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "rgba(255,255,255,0.06)", borderRadius: learnOpen.hiddenhunger ? "12px 12px 0 0" : 12, padding: "12px 16px", cursor: "pointer" }}>
                <span style={{ fontWeight: 700, fontSize: 14 }}>🍟 Hidden Hunger — Ultra-Processed Foods & Dependants</span>
                <span style={{ fontSize: 14, color: "#64748b" }}>{learnOpen.hiddenhunger ? "▲" : "▼"}</span>
              </div>
              {learnOpen.hiddenhunger && (
                <div style={{ background: "rgba(255,255,255,0.03)", borderRadius: "0 0 12px 12px", padding: "14px 16px", fontSize: 13, color: "#cbd5e1", lineHeight: 1.7 }}>
                  <div style={{ background: "rgba(239,68,68,0.1)", border: "1px solid rgba(239,68,68,0.25)", borderRadius: 8, padding: "10px 12px", marginBottom: 14, fontSize: 14 }}>
                    <strong style={{ color: "#f87171" }}>Hidden Hunger:</strong> Children overfed on calories but starved of vitamins and minerals. Ultra-processed foods fill the stomach while stripping the nutrient profile.
                  </div>
                  {[
                    ["2.57× deficiency risk (SENDO Project, 2023)", "Children with the highest ultra-processed food intake had 2.57 times higher odds of being deficient in 3+ essential micronutrients simultaneously. The proportion facing multiple deficiencies jumped from 23% on whole-food diets to 35% on high-processed diets."],
                    ["16 of 17 micronutrients are lower in UPF", "A comprehensive nutritional analysis found 16 of 17 key micronutrients significantly lower in ultra-processed foods — and 10 of those failed to reach even half the level found in whole foods. Depleted: B12, Vit D, Vit E, iron, magnesium, selenium, zinc and more."],
                    ["Dopamine hijacking — why kids demand junk", "The fat + sugar combinations engineered into children's snacks trigger supra-additive dopamine firing in the mid-brain. This shifts eating from hunger-driven to cue-driven — the same mechanism underlying addiction. The child isn't being difficult; their reward system has been captured."],
                    ["10% more UPF = measurable drop in executive function", "Every 10% increase in daily energy from ultra-processed foods predicts a significant decline in working memory, impulse control, and attention — independently of socioeconomic status or BMI."],
                    ["ARFID: when texture uniformity backfires", "Processed foods are engineered to be perfectly uniform every time. Real foods vary. This trains children to expect predictability and can trigger Avoidant/Restrictive Food Intake Disorder (ARFID) — where whole-food textures cause genuine distress. It starts young and worsens without intervention."],
                  ].map(([title, desc]) => (
                    <div key={title} style={{ background: "rgba(255,255,255,0.04)", borderRadius: 8, padding: "8px 10px", marginBottom: 6 }}>
                      <div style={{ fontSize: 14, fontWeight: 700, color: "#f1f5f9", marginBottom: 2 }}>{title}</div>
                      <div style={{ fontSize: 13, color: "#94a3b8", lineHeight: 1.5 }}>{desc}</div>
                    </div>
                  ))}
                  <div style={{ marginTop: 12, padding: "10px 12px", background: "rgba(34,197,94,0.07)", borderRadius: 8, fontSize: 14 }}>
                    <div style={{ fontWeight: 700, color: "#22c55e", marginBottom: 4 }}>Priority nutrients depleted by UPF diets in dependants</div>
                    {[
                      ["🦷 Zinc", "Stunted growth, frequent infections, poor attention. Stripped by refining; blocked by phytates in processed grains."],
                      ["🧠 Vitamin B12", "Developmental delays, neurological irritability, anaemia. UPF replaces animal protein with refined carbs that contain zero B12."],
                      ["⚡ Magnesium & B vitamins", "Mood swings, anxiety, sleep problems. High refined sugar burns through magnesium and B vitamins just to metabolise the glucose."],
                      ["🦴 Vitamin D & Calcium", "Weak enamel, poor bone density, delayed teething. Sugary drinks displace dairy and whole-food calcium sources."],
                    ].map(([n, d]) => (
                      <div key={n} style={{ marginBottom: 6 }}>
                        <span style={{ fontWeight: 700, color: "#86efac" }}>{n}:</span> <span style={{ color: "#94a3b8" }}>{d}</span>
                      </div>
                    ))}
                  </div>
                  <div style={{ borderTop: "1px solid rgba(255,255,255,0.06)", paddingTop: 10, marginTop: 10 }}>
                    <a href="https://optimisedeats.com/guide/hidden-hunger/" target="_blank" rel="noopener noreferrer" style={{ display: "inline-flex", alignItems: "center", gap: 6, background: "rgba(251,146,60,0.12)", border: "1px solid rgba(251,146,60,0.3)", color: "#fb923c", fontSize: 13, fontWeight: 700, padding: "7px 14px", borderRadius: 20, textDecoration: "none" }}>🍟 Full Hidden Hunger Guide →</a>
                  </div>
                </div>
              )}
            </div>

            {/* NRV DAILY REFERENCE TABLES */}
            <div style={{ marginTop: 20 }}>
              <div onClick={() => setLearnOpen(p => ({...p, nrv: !p.nrv}))}
                style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "rgba(255,255,255,0.06)", borderRadius: 12, padding: "12px 16px", cursor: "pointer" }}>
                <span style={{ fontWeight: 700, fontSize: 14 }}>📊 Daily Nutrient Targets (Nutrient Reference Values)</span>
                <span style={{ fontSize: 14, color: "#64748b" }}>{learnOpen.nrv ? "▲" : "▼"}</span>
              </div>
              {learnOpen.nrv && (() => {
                const d = getRDA(DEMOG_MAP[learnDemog]);
                const demogs = [
                  ["Girl 9-13","f_9"],["Boy 9-13","m_9"],["Teen F 14-18","f_14"],["Teen M 14-18","m_14"],
                  ["Woman 19-50","f_19"],["Man 19-50","m_19"],["Woman 51-70","f_51"],["Man 51+","m_51"],
                  ["Woman 70+","f_71"],["Man 70+","m_71"],["Pregnant","preg"],["Lactating","lact"]
                ];
                const sections = [
                  { label: "⚡ Energy & Macros", rows: [
                    ["Energy",d.cal,"kcal/day"],["Protein",d.protein,"g/day"],
                    ["Fibre",d.fibre,"g/day"],["Omega-3 (ALA)",d.omega3,"g/day"]
                  ]},
                  { label: "🍊 Vitamins", rows: [
                    ["Vitamin A",d.vitA,"μg RAE"],["Vitamin C",d.vitC,"mg"],
                    ["Vitamin D",d.vitD,"IU"],["Vitamin K",d.vitK,"μg"],
                    ["Folate",d.folate,"μg DFE"],["Vitamin B12",d.vitB12,"μg"],
                    ["Choline",d.choline,"mg"]
                  ]},
                  { label: "🪨 Minerals", rows: [
                    ["Calcium",d.calcium,"mg"],["Iron",d.iron,"mg"],
                    ["Magnesium",d.magnesium,"mg"],["Zinc",d.zinc,"mg"],
                    ["Potassium",d.potassium,"mg"],["Selenium",d.selenium,"μg"],
                    ["Iodine",d.iodine,"μg"]
                  ]}
                ];
                return (
                  <div style={{ background: "rgba(255,255,255,0.03)", borderRadius: 12, padding: "12px 14px", marginTop: 6 }}>
                    <p style={{ fontSize: 13, color: "#94a3b8", margin: "0 0 8px", lineHeight: 1.4 }}>National Health and Medical Research Council (NHMRC) Australian Nutrient Reference Values (2006, updated 2017). Fat-soluble vitamins (A, D, E, K) store in the body — weekly averages are fine. Water-soluble vitamins and minerals need consistent daily intake.</p>
                    <div style={{ background: "rgba(245,158,11,0.08)", border: "1px solid rgba(245,158,11,0.2)", borderRadius: 8, padding: "8px 10px", marginBottom: 10 }}>
                      <div style={{ fontSize: 13, fontWeight: 700, color: "#f59e0b", marginBottom: 4 }}>💪 Protein targets for 65+ are set higher than the official NRV</div>
                      <p style={{ fontSize: 13, color: "#94a3b8", margin: 0, lineHeight: 1.5 }}>The standard NRV protein recommendation (0.75–0.84g/kg) was developed for younger adults. Research consistently shows that older adults experience <strong style={{ color: "#e2e8f0" }}>anabolic resistance</strong> — muscles become less efficient at using protein to maintain and rebuild tissue. The PROT-AGE Study Group and multiple systematic reviews recommend <strong style={{ color: "#e2e8f0" }}>1.0–1.2g/kg/day</strong> for healthy adults 65+, and up to 1.5g/kg during illness or recovery. This app uses those higher targets for members aged 65 and over. Spreading protein across meals (aim for 25–30g per sitting) improves uptake further.</p>
                    </div>
                    <div style={{ display: "flex", flexWrap: "wrap", gap: 5, marginBottom: 14 }}>
                      {demogs.map(([lbl, key]) => (
                        <button key={key} onClick={() => setLearnDemog(key)}
                          style={{ padding: "4px 9px", borderRadius: 20, fontSize: 12, border: "none", cursor: "pointer",
                            background: learnDemog === key ? "#3b82f6" : "rgba(255,255,255,0.08)",
                            color: learnDemog === key ? "#fff" : "#94a3b8",
                            fontWeight: learnDemog === key ? 700 : 400 }}>
                          {lbl}
                        </button>
                      ))}
                    </div>
                    {sections.map(sec => (
                      <div key={sec.label} style={{ marginBottom: 12 }}>
                        <div style={{ fontSize: 13, fontWeight: 700, textTransform: "uppercase", letterSpacing: 1, color: "#64748b", marginBottom: 5 }}>{sec.label}</div>
                        {sec.rows.map(([name, val, unit]) => (
                          <div key={name} style={{ display: "flex", justifyContent: "space-between", padding: "5px 8px", background: "rgba(255,255,255,0.03)", borderRadius: 6, marginBottom: 2 }}>
                            <span style={{ fontSize: 14, color: "#cbd5e1" }}>{name}</span>
                            <span style={{ fontSize: 14, fontWeight: 700, color: "#e2e8f0" }}>{val} <span style={{ fontSize: 12, color: "#64748b", fontWeight: 400 }}>{unit}</span></span>
                          </div>
                        ))}
                      </div>
                    ))}
                    <div style={{ fontSize: 12, color: "#64748b", marginTop: 6, lineHeight: 1.5 }}>* Carbs: 45–65% of energy (Acceptable Macronutrient Distribution Range) · Fat: 20–35% · Sodium: 460–920mg Adequate Intake (max 2,300mg) · Water: 2.1L women / 2.6L men/day · RAE = Retinol Activity Equivalents · DFE = Dietary Folate Equivalents · ALA = Alpha-Linolenic Acid</div>
                  </div>
                );
              })()}
            </div>

            {/* MOVEMENT & EXERCISE */}
            <div style={{ marginTop: 12 }}>
              <div onClick={() => setLearnOpen(p => ({...p, ex: !p.ex}))}
                style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "rgba(255,255,255,0.06)", borderRadius: 12, padding: "12px 16px", cursor: "pointer" }}>
                <span style={{ fontWeight: 700, fontSize: 14 }}>🏃 Movement & Exercise</span>
                <span style={{ fontSize: 14, color: "#64748b" }}>{learnOpen.ex ? "▲" : "▼"}</span>
              </div>
              {learnOpen.ex && (
                <div style={{ background: "rgba(255,255,255,0.03)", borderRadius: 12, padding: "12px 14px", marginTop: 6 }}>
                  <p style={{ fontSize: 13, color: "#94a3b8", margin: "0 0 12px", lineHeight: 1.4 }}>Australian Physical Activity &amp; Sedentary Behaviour Guidelines (Dept Health, 2021). Two types of activity are required for optimal health: cardio AND strength training.</p>
                  {[
                    { emoji: "🧒", group: "Children 5–17",
                      cardio: "60 min moderate-to-vigorous EVERY day",
                      strength: "Muscle &amp; bone strengthening 3×/week (running, jumping, climbing, sport)",
                      sit: "Limit recreational screen time — break up sitting regularly" },
                    { emoji: "🧑", group: "Adults 18–64",
                      cardio: "150–300 min moderate OR 75–150 min vigorous per week",
                      strength: "Muscle-strengthening 2×/week (weights, resistance bands, yoga, heavy gardening)",
                      sit: "Break up long sitting as often as possible — even a 2 min walk counts" },
                    { emoji: "🧓", group: "Older Adults 65+",
                      cardio: "150–300 min moderate/week (walking, swimming, cycling, tai chi)",
                      strength: "2×/week + balance exercises (vital for fall prevention)",
                      sit: "Move more, sit less — any activity at any intensity benefits health" },
                  ].map(g => (
                    <div key={g.group} style={{ background: "rgba(255,255,255,0.04)", borderRadius: 10, padding: "10px 12px", marginBottom: 8 }}>
                      <div style={{ fontSize: 13, fontWeight: 700, marginBottom: 6 }}>{g.emoji} {g.group}</div>
                      <div style={{ fontSize: 13, color: "#86efac", marginBottom: 3 }} dangerouslySetInnerHTML={{__html: "❤️ Cardio — " + g.cardio}} />
                      <div style={{ fontSize: 13, color: "#93c5fd", marginBottom: 3 }} dangerouslySetInnerHTML={{__html: "💪 Strength — " + g.strength}} />
                      <div style={{ fontSize: 13, color: "#fcd34d" }} dangerouslySetInnerHTML={{__html: "🪑 Sitting — " + g.sit}} />
                    </div>
                  ))}
                  <div style={{ fontSize: 13, fontWeight: 700, color: "#f59e0b", margin: "14px 0 8px" }}>🥗 How Exercise Changes Your Nutrient Needs</div>
                  {[
                    ["🥩 Protein", "Increases to 1.2–1.7g/kg for active adults (vs 0.75–0.8g/kg sedentary). Weight training demands the higher end. Budget hit: eggs + lentils + sardines cover this cheaply."],
                    ["💧 Electrolytes", "Sweat depletes sodium, potassium, and magnesium. After hard sessions: banana + pinch of salt + water beats sports drinks at 1/20th the cost."],
                    ["☀️ Vitamin D", "Critical for muscle function and strength gains. 15–30 min sun on arms/legs most days covers most Australians — supplement in winter or if mostly indoors."],
                    ["🩸 Iron", "Intense exercise (especially running) raises iron loss via foot-strike haemolysis and sweat. Active women are most at risk — include heme iron (meat, liver) at least weekly."],
                    ["🥜 Magnesium", "Lost in sweat and required for muscle contraction. Pumpkin seeds, dark leafy greens, and legumes are cheapest sources — costs under $0.30/day."],
                    ["⏰ Timing", "Protein within 2 hrs post-workout maximises muscle repair. Carbs before/during long sessions fuel performance. A boiled egg + glass of milk is a $0.90 recovery meal."],
                  ].map(([title, desc]) => (
                    <div key={title} style={{ background: "rgba(255,255,255,0.03)", borderRadius: 8, padding: "8px 10px", marginBottom: 4 }}>
                      <div style={{ fontSize: 14, fontWeight: 700, marginBottom: 2 }}>{title}</div>
                      <div style={{ fontSize: 13, color: "#94a3b8", lineHeight: 1.4 }}>{desc}</div>
                    </div>
                  ))}
                  <div style={{ background: "rgba(34,197,94,0.08)", borderRadius: 10, padding: "10px 12px", marginTop: 10 }}>
                    <div style={{ fontSize: 14, fontWeight: 700, color: "#22c55e", marginBottom: 4 }}>💡 Budget Active Person — Weekly Habits</div>
                    {[
                      "2× strength sessions (bodyweight = completely free)",
                      "Daily 30 min walk (free, and it adds up to 150 min/week)",
                      "Post-workout: 2 boiled eggs + glass of milk ≈ $0.90 recovery",
                      "Weekly sardine meal — omega-3 + vitamin D + protein in one hit"
                    ].map((t, i) => (
                      <div key={i} style={{ fontSize: 13, color: "#bbf7d0", marginBottom: 2 }}>• {t}</div>
                    ))}
                  </div>
                  <div style={{ fontSize: 12, color: "#64748b", marginTop: 8 }}>Source: Dept of Health Aust Physical Activity Guidelines 2021 · National Health &amp; Medical Research Council (NHMRC) Nutrient Reference Values (NRVs) · American College of Sports Medicine (ACSM) Exercise &amp; Nutrition Position Stands · DHA = docosahexaenoic acid · EPA = eicosapentaenoic acid · ALA = alpha-linolenic acid</div>
                </div>
              )}
            </div>


            {/* GAP-FILLER FOODS */}
            <div style={{ marginTop: 12 }}>
              <div onClick={() => setLearnOpen(p => ({...p, gaps: !p.gaps}))}
                style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "rgba(255,255,255,0.06)", borderRadius: 12, padding: "12px 16px", cursor: "pointer" }}>
                <span style={{ fontWeight: 700, fontSize: 14 }}>🎯 Gap-Filler Foods (No Offal)</span>
                <span style={{ fontSize: 14, color: "#64748b" }}>{learnOpen.gaps ? "▲" : "▼"}</span>
              </div>
              {learnOpen.gaps && (
                <div style={{ background: "rgba(255,255,255,0.03)", borderRadius: 12, padding: "12px 14px", marginTop: 6 }}>
                  <p style={{ fontSize: 13, color: "#94a3b8", margin: "0 0 12px", lineHeight: 1.4 }}>The 6 nutrients Australians consistently miss — and the cheapest non-offal foods that fix each one. Pair plant iron &amp; zinc sources with Vitamin C to boost absorption by up to 3×. RDI = Recommended Daily Intake.</p>
                  {[
                    { gap: "Calcium", short: "60% of Australians", color: "#ef4444", icon: "🦴",
                      foods: [
                        { name: "Milk", amount: "250mL glass", per: "~300mg", cost: "$0.40", tip: "30% of adult RDI in one glass" },
                        { name: "Yoghurt", amount: "200g tub", per: "~250mg", cost: "$0.60", tip: "Also covers iodine & B12" },
                        { name: "Cheese", amount: "30g slice", per: "~200mg", cost: "$0.40", tip: "Dense calcium per gram" },
                        { name: "Sardines (with bones)", amount: "1 tin (95g)", per: "~350mg", cost: "$1.50", tip: "Eat the soft bones — that's where it is" },
                        { name: "Calcium-set tofu", amount: "100g", per: "~350mg", cost: "$0.60", tip: "Check label — must say calcium sulfate" },
                      ]
                    },
                    { gap: "Zinc (males)", short: "48% of men", color: "#f97316", icon: "⚡",
                      foods: [
                        { name: "Beef mince", amount: "100g cooked", per: "~8mg", cost: "$1.00", tip: "Covers most of the 11mg male RDI alone" },
                        { name: "Pumpkin seeds", amount: "30g / 2 tbsp", per: "~2.2mg", cost: "$0.30", tip: "Best budget plant zinc — add to anything" },
                        { name: "Oats", amount: "1 cup dry (80g)", per: "~2.3mg", cost: "$0.10", tip: "Surprisingly good — soak overnight to reduce phytates" },
                        { name: "Chickpeas", amount: "1 cup cooked (160g)", per: "~2.5mg", cost: "$0.20", tip: "Soak dried chickpeas to boost absorption" },
                        { name: "Eggs", amount: "2 whole eggs", per: "~1.3mg", cost: "$0.60", tip: "Pairs well with other zinc sources" },
                      ]
                    },
                    { gap: "Iron (women 18–29)", short: "47% of young women", color: "#ec4899", icon: "🩸",
                      foods: [
                        { name: "Lentils", amount: "1 cup cooked (200g)", per: "~6.6mg", cost: "$0.20", tip: "Highest plant iron per dollar — eat with Vit C" },
                        { name: "Weet-Bix", amount: "2 biscuits", per: "~2.6mg", cost: "$0.20", tip: "Fortified — good daily base" },
                        { name: "Beef mince", amount: "100g cooked", per: "~3.2mg heme", cost: "$1.00", tip: "Heme iron absorbs 2–3× better than plant iron" },
                        { name: "Spinach (cooked)", amount: "1 cup (180g)", per: "~3.6mg", cost: "$0.30", tip: "Always cook + add lemon juice or capsicum" },
                        { name: "Kidney beans", amount: "1 cup cooked (170g)", per: "~3.9mg", cost: "$0.20", tip: "Versatile — chilli, soup, stew" },
                      ],
                      note: "💡 Always pair plant iron with Vitamin C — a squeeze of lemon or handful of capsicum can triple absorption"
                    },
                    { gap: "Magnesium", short: "31% of adults", color: "#a855f7", icon: "⚗️",
                      foods: [
                        { name: "Pumpkin seeds", amount: "30g / 2 tbsp", per: "~160mg", cost: "$0.30", tip: "Almost half the female RDI in one handful" },
                        { name: "Spinach (cooked)", amount: "1 cup (180g)", per: "~157mg", cost: "$0.30", tip: "Double win — iron + magnesium together" },
                        { name: "Black beans", amount: "1 cup cooked (172g)", per: "~120mg", cost: "$0.20", tip: "Also great for iron, zinc, and fibre" },
                        { name: "Brown rice", amount: "1 cup cooked (195g)", per: "~84mg", cost: "$0.15", tip: "Easy daily base — swap from white rice" },
                        { name: "Banana", amount: "1 medium (118g)", per: "~32mg", cost: "$0.30", tip: "Also covers potassium + quick carbs" },
                      ]
                    },
                    { gap: "Vitamin D", short: "21% of adults", color: "#eab308", icon: "☀️",
                      foods: [
                        { name: "Sun exposure", amount: "15–30 min daily", per: "600–1000 IU", cost: "FREE", tip: "Arms & legs exposed — most Australians get enough most of the year" },
                        { name: "Sardines", amount: "1 tin (95g)", per: "~250 IU", cost: "$1.50", tip: "Best dietary source by far" },
                        { name: "Eggs", amount: "2 whole eggs", per: "~80–100 IU", cost: "$0.60", tip: "Yolk only — don't skip it" },
                        { name: "UV mushrooms", amount: "100g (gills-up in sun 30 min)", per: "~400+ IU", cost: "$0.50", tip: "Genuinely works — place gills-up in direct sun before cooking" },
                        { name: "Fortified milk", amount: "250mL glass", per: "~40 IU", cost: "$0.40", tip: "Lower but contributes to daily total" },
                      ]
                    },
                    { gap: "Vitamin A", short: "23% of adults", color: "#f59e0b", icon: "👁️",
                      foods: [
                        { name: "Sweet potato", amount: "1 medium baked (130g)", per: "~960μg RAE", cost: "$0.40", tip: "Covers the ENTIRE adult RDI — always eat with fat" },
                        { name: "Carrots", amount: "½ cup cooked (78g)", per: "~665μg RAE", cost: "$0.20", tip: "Nearly a full day's worth — roast in a little oil" },
                        { name: "Kale (cooked)", amount: "½ cup (65g)", per: "~885μg RAE", cost: "$0.30", tip: "Also excellent for Vit K and calcium" },
                        { name: "Spinach (cooked)", amount: "½ cup (90g)", per: "~472μg RAE", cost: "$0.20", tip: "Pair with oil or butter for absorption" },
                        { name: "Red capsicum", amount: "½ cup raw (75g)", per: "~117μg RAE", cost: "$0.40", tip: "Also highest Vit C content of any veg" },
                      ],
                      note: "💡 Beta-carotene (plant Vit A) needs dietary fat to absorb. Always cook or serve with oil, butter, or avocado"
                    },
                  ].map(gap => (
                    <div key={gap.gap} style={{ marginBottom: 14, background: "rgba(255,255,255,0.03)", borderRadius: 12, padding: "10px 12px" }}>
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
                        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                          <span style={{ fontSize: 18 }}>{gap.icon}</span>
                          <span style={{ fontSize: 13, fontWeight: 700 }}>{gap.gap}</span>
                        </div>
                        <span style={{ fontSize: 12, color: gap.color, fontWeight: 700, background: "rgba(255,255,255,0.05)", padding: "2px 8px", borderRadius: 20 }}>{gap.short} fall short</span>
                      </div>
                      {gap.foods.map(f => (
                        <div key={f.name} style={{ display: "flex", alignItems: "flex-start", gap: 8, padding: "5px 0", borderTop: "1px solid rgba(255,255,255,0.04)" }}>
                          <div style={{ flex: 1 }}>
                            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                              <span style={{ fontSize: 14, fontWeight: 600, color: "#e2e8f0" }}>{f.name}</span>
                              <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
                                <span style={{ fontSize: 13, fontWeight: 700, color: gap.color }}>{f.per}</span>
                                <span style={{ fontSize: 12, color: "#64748b" }}>{f.cost}</span>
                              </div>
                            </div>
                            <div style={{ fontSize: 12, color: "#60a5fa", marginTop: 1 }}>{f.amount}</div>
                            <div style={{ fontSize: 12, color: "#64748b", marginTop: 1, lineHeight: 1.3 }}>{f.tip}</div>
                          </div>
                        </div>
                      ))}
                      {gap.note && (
                        <div style={{ marginTop: 6, padding: "6px 8px", background: "rgba(34,197,94,0.08)", borderRadius: 6, fontSize: 13, color: "#86efac", lineHeight: 1.4 }}>{gap.note}</div>
                      )}
                    </div>
                  ))}
                  <div style={{ background: "rgba(59,130,246,0.08)", borderRadius: 10, padding: "10px 12px", marginTop: 4 }}>
                    <div style={{ fontSize: 14, fontWeight: 700, color: "#60a5fa", marginBottom: 6 }}>⚡ The Non-Offal Daily Stack</div>
                    {[
                      ["2 eggs", "Vit D, B12, zinc, choline", "~$0.60"],
                      ["250mL milk or 200g yoghurt", "Calcium, iodine, B12, zinc", "~$0.50"],
                      ["30g pumpkin seeds", "Magnesium, zinc, iron", "~$0.30"],
                      ["Sweet potato or carrot (with fat)", "Vitamin A", "~$0.30"],
                      ["Lentils or beans 3–4×/week", "Iron, zinc, magnesium, folate", "~$0.20/serve"],
                      ["Sardines 1–2×/week", "Vit D, calcium, omega-3", "~$1.50/serve"],
                      ["Beef mince 1–2×/week", "Zinc, heme iron", "~$1.00/serve"],
                    ].map(([food, covers, cost]) => (
                      <div key={food} style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", padding: "4px 0", borderTop: "1px solid rgba(255,255,255,0.04)" }}>
                        <div style={{ flex: 1 }}>
                          <span style={{ fontSize: 13, fontWeight: 600, color: "#e2e8f0" }}>{food}</span>
                          <div style={{ fontSize: 12, color: "#94a3b8" }}>{covers}</div>
                        </div>
                        <span style={{ fontSize: 12, color: "#64748b", marginLeft: 8, whiteSpace: "nowrap" }}>{cost}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* VEGAN & VEGETARIAN SUPPLEMENTS */}
            <div style={{ marginTop: 12 }}>
              <div onClick={() => setLearnOpen(p => ({...p, vegan: !p.vegan}))}
                style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "rgba(34,197,94,0.08)", borderRadius: 12, padding: "12px 16px", cursor: "pointer", border: "1px solid rgba(34,197,94,0.2)" }}>
                <span style={{ fontWeight: 700, fontSize: 14 }}>🌱 Vegan & Vegetarian — What to Supplement</span>
                <span style={{ fontSize: 14, color: "#64748b" }}>{learnOpen.vegan ? "▲" : "▼"}</span>
              </div>
              {learnOpen.vegan && (
                <div style={{ background: "rgba(255,255,255,0.03)", borderRadius: 12, padding: "12px 14px", marginTop: 6 }}>
                  <p style={{ fontSize: 13, color: "#94a3b8", margin: "0 0 12px", lineHeight: 1.5 }}>Plant-based diets have real health benefits, but several nutrients are either absent from plant foods entirely or absorbed so poorly that food alone isn't enough. These aren't fringe concerns — the research is clear and consistent. Supplementing these correctly is just as important as the food you eat.</p>

                  <div style={{ background: "rgba(239,68,68,0.1)", border: "1px solid rgba(239,68,68,0.3)", borderRadius: 10, padding: "10px 12px", marginBottom: 10 }}>
                    <div style={{ fontSize: 14, fontWeight: 700, color: "#f87171", marginBottom: 6 }}>🚨 Must Supplement — Cannot Get Reliably from Plants</div>
                    {[
                      {
                        name: "Vitamin B12",
                        why: "Zero bioavailable B12 exists in plant foods. Deficiency causes irreversible nerve damage and anaemia — and it develops silently over years. Every vegan must supplement.",
                        dose: "500–1000μg cyanocobalamin daily, or 2000μg weekly. Higher doses needed because absorption drops as dose increases.",
                        cost: "~$5–10/month",
                        note: "Vegetarians who eat eggs and dairy get some B12, but levels are often still low — worth testing and supplementing if below range."
                      },
                      {
                        name: "Omega-3 (DHA & EPA)",
                        why: "Plants only provide ALA (alpha-linolenic acid). The body converts ALA to DHA (docosahexaenoic acid) and EPA (eicosapentaenoic acid) at roughly 5–10% efficiency — far too little for brain health, inflammation control, and cardiovascular protection.",
                        dose: "250–500mg algae-based DHA+EPA daily. Algae oil is the direct vegan source fish get their omega-3 from.",
                        cost: "~$15–25/month",
                        note: "Flaxseed, chia, and walnuts are good for ALA but don't solve the DHA/EPA gap. Algae oil is the only vegan solution."
                      },
                    ].map(s => (
                      <div key={s.name} style={{ marginBottom: 10, paddingBottom: 10, borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
                        <div style={{ fontSize: 13, fontWeight: 700, color: "#fca5a5", marginBottom: 3 }}>{s.name}</div>
                        <div style={{ fontSize: 13, color: "#94a3b8", lineHeight: 1.5, marginBottom: 4 }}>{s.why}</div>
                        <div style={{ fontSize: 13, background: "rgba(239,68,68,0.08)", borderRadius: 6, padding: "5px 8px", marginBottom: 4 }}>
                          <span style={{ color: "#f87171", fontWeight: 600 }}>Dose: </span>
                          <span style={{ color: "#94a3b8" }}>{s.dose}</span>
                        </div>
                        {s.note && <div style={{ fontSize: 12, color: "#64748b", lineHeight: 1.4, fontStyle: "italic" }}>{s.note}</div>}
                      </div>
                    ))}
                  </div>

                  <div style={{ background: "rgba(245,158,11,0.08)", border: "1px solid rgba(245,158,11,0.2)", borderRadius: 10, padding: "10px 12px", marginBottom: 10 }}>
                    <div style={{ fontSize: 14, fontWeight: 700, color: "#f59e0b", marginBottom: 6 }}>⚠️ Often Low — Supplement or Monitor Closely</div>
                    {[
                      {
                        name: "Vitamin D3",
                        why: "Most vitamin D3 supplements are animal-derived. Look for vegan D3 (from lichen). Vegans tend to have lower D levels, especially in winter or with indoor lifestyles.",
                        dose: "1000–2000 IU daily in winter, or test blood levels (25-OH-D) and dose to maintain 75–100 nmol/L.",
                        cost: "~$5–10/month"
                      },
                      {
                        name: "Iodine",
                        why: "The main dietary iodine sources are dairy and seafood. Vegans who don't regularly eat seaweed or iodised salt often fall short. Deficiency affects thyroid function and in pregnancy is serious.",
                        dose: "150μg/day from iodised salt or supplement. Seaweed is unreliable — iodine content varies enormously by type and batch.",
                        cost: "Cheapest — iodised salt costs nothing extra"
                      },
                      {
                        name: "Calcium",
                        why: "Vegans who don't consume fortified plant milks or calcium-set tofu regularly often fall well short of the 1000mg/day target.",
                        dose: "Aim for fortified plant milk (300mg/250mL) + calcium-set tofu. Supplement 500mg/day if diet is still low.",
                        cost: "~$5/month if supplementing"
                      },
                    ].map(s => (
                      <div key={s.name} style={{ marginBottom: 8, paddingBottom: 8, borderBottom: "1px solid rgba(255,255,255,0.05)" }}>
                        <div style={{ fontSize: 13, fontWeight: 700, color: "#fcd34d", marginBottom: 3 }}>{s.name}</div>
                        <div style={{ fontSize: 13, color: "#94a3b8", lineHeight: 1.5, marginBottom: 4 }}>{s.why}</div>
                        <div style={{ fontSize: 13, background: "rgba(245,158,11,0.08)", borderRadius: 6, padding: "5px 8px" }}>
                          <span style={{ color: "#f59e0b", fontWeight: 600 }}>Dose: </span>
                          <span style={{ color: "#94a3b8" }}>{s.dose}</span>
                        </div>
                      </div>
                    ))}
                  </div>

                  <div style={{ background: "rgba(59,130,246,0.08)", border: "1px solid rgba(59,130,246,0.2)", borderRadius: 10, padding: "10px 12px", marginBottom: 10 }}>
                    <div style={{ fontSize: 14, fontWeight: 700, color: "#60a5fa", marginBottom: 6 }}>💡 Watch Absorption — Plant Sources Are Weaker</div>
                    {[
                      { name: "Iron", note: "Plant iron (non-heme) absorbs at 2–5% vs 15–35% for meat iron. Always eat plant iron with Vitamin C and avoid tea/coffee for 1 hour either side. Target roughly double the standard RDI." },
                      { name: "Zinc", note: "Phytates in legumes and wholegrains block zinc absorption. Soaking and sprouting helps. Vegans need around 50% more zinc from food than omnivores to reach the same absorbed amount." },
                      { name: "Protein completeness", note: "Individual plant proteins are typically low in one or more essential amino acids. Eating a variety across the day (legumes + grains + nuts/seeds) covers all amino acids — you don't need to combine at every meal." },
                    ].map(s => (
                      <div key={s.name} style={{ marginBottom: 6, paddingBottom: 6, borderBottom: "1px solid rgba(255,255,255,0.05)" }}>
                        <div style={{ fontSize: 14, fontWeight: 700, color: "#93c5fd", marginBottom: 2 }}>{s.name}</div>
                        <div style={{ fontSize: 13, color: "#94a3b8", lineHeight: 1.5 }}>{s.note}</div>
                      </div>
                    ))}
                  </div>

                  <div style={{ background: "rgba(34,197,94,0.08)", borderRadius: 10, padding: "10px 12px" }}>
                    <div style={{ fontSize: 14, fontWeight: 700, color: "#22c55e", marginBottom: 6 }}>✅ Vegan Daily Stack</div>
                    {[
                      ["B12 supplement", "500–1000μg cyanocobalamin", "Non-negotiable"],
                      ["Algae oil", "250–500mg DHA+EPA", "Brain & heart health"],
                      ["Vegan D3 (lichen)", "1000–2000 IU", "Especially winter"],
                      ["Iodised salt", "Use daily in cooking", "Thyroid function"],
                      ["Fortified plant milk", "300mg calcium per 250mL", "Check the label"],
                      ["Calcium-set tofu", "100g = 350mg calcium", "Must say calcium sulfate"],
                      ["Vitamin C with every meal", "Lemon, capsicum, kiwi", "Boosts iron & zinc"],
                    ].map(([item, amount, note]) => (
                      <div key={item} style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", padding: "4px 0", borderTop: "1px solid rgba(255,255,255,0.04)" }}>
                        <div style={{ flex: 1 }}>
                          <span style={{ fontSize: 13, fontWeight: 600, color: "#e2e8f0" }}>{item}</span>
                          <div style={{ fontSize: 12, color: "#94a3b8" }}>{note}</div>
                        </div>
                        <span style={{ fontSize: 12, color: "#64748b", marginLeft: 8, textAlign: "right", maxWidth: 100 }}>{amount}</span>
                      </div>
                    ))}
                  </div>
                  <div style={{ fontSize: 12, color: "#64748b", marginTop: 10, lineHeight: 1.5 }}>Sources: NHMRC Nutrient Reference Values · Melina et al. (2016) Position of the Academy of Nutrition and Dietetics: Vegetarian Diets, J Acad Nutr Diet · Sanders (2009) DHA status of vegetarians · Saunders et al. (2013) Iodine in plant-based diets, Med J Australia</div>


                  <div style={{ borderTop: "1px solid rgba(255,255,255,0.06)", paddingTop: 10, marginTop: 10 }}>
                    <a href="https://optimisedeats.com/guide/vegan-nutrition/" target="_blank" rel="noopener noreferrer" style={{ display: "inline-flex", alignItems: "center", gap: 6, background: "rgba(34,197,94,0.12)", border: "1px solid rgba(34,197,94,0.3)", color: "#4ade80", fontSize: 13, fontWeight: 700, padding: "7px 14px", borderRadius: 20, textDecoration: "none" }}>🌱 Vegan Nutrition Guide →</a>
                  </div>
                </div>
              )}
            </div>

            {/* REFERENCES */}
            <div style={{ marginTop: 12 }}>
              <div onClick={() => setLearnOpen(p => ({...p, refs: !p.refs}))}
                style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "rgba(255,255,255,0.06)", borderRadius: 12, padding: "12px 16px", cursor: "pointer" }}>
                <span style={{ fontWeight: 700, fontSize: 14 }}>📎 References & Sources</span>
                <span style={{ fontSize: 14, color: "#64748b" }}>{learnOpen.refs ? "▲" : "▼"}</span>
              </div>
              {learnOpen.refs && (
                <div style={{ background: "rgba(255,255,255,0.03)", borderRadius: 12, padding: "12px 14px", marginTop: 6 }}>
                  <p style={{ fontSize: 13, color: "#94a3b8", margin: "0 0 12px", lineHeight: 1.5 }}>All nutrition statistics, recommendations, and reference values used in this app come from the following peer-reviewed and government sources.</p>
                  {[
                    {
                      title: "Australian Bureau of Statistics — National Nutrition Survey",
                      desc: "Source for all deficiency prevalence statistics (calcium 60%, zinc 48%, iron 47%, etc.) and the 4.2% fruit+veg figure.",
                      url: "https://www.abs.gov.au/statistics/health/health-conditions-and-risks/australian-health-survey-usual-nutrient-intakes/latest-release",
                      label: "ABS Nutrient Intakes Report"
                    },
                    {
                      title: "NHMRC — Nutrient Reference Values for Australia and New Zealand",
                      desc: "All Recommended Dietary Intakes (RDIs), Adequate Intakes (AIs), and Estimated Average Requirements (EARs) used in this app's nutrient tracking.",
                      url: "https://www.nhmrc.gov.au/health-advice/food-and-nutrition/nutrient-reference-values",
                      label: "NHMRC NRVs (2006, updated 2017)"
                    },
                    {
                      title: "Australian Government — Physical Activity Guidelines",
                      desc: "Exercise recommendations for children (5–17), adults (18–64), and older adults (65+) shown in the Movement section.",
                      url: "https://www.health.gov.au/topics/physical-activity-and-exercise/physical-activity-and-exercise-guidelines-for-all-australians",
                      label: "Dept of Health PA Guidelines 2021"
                    },
                    {
                      title: "ACSM — Exercise and Nutrition Position Stands",
                      desc: "Basis for protein targets for active adults (1.2–1.7g/kg), timing recommendations, and electrolyte guidance in the Exercise section.",
                      url: "https://www.acsm.org/education-resources/trending-topics-resources/physical-activity-guidelines",
                      label: "American College of Sports Medicine"
                    },
                    {
                      title: "Melina et al. (2016) — Position of the Academy of Nutrition and Dietetics: Vegetarian Diets",
                      desc: "The primary peer-reviewed reference for vegan and vegetarian nutrition, covering B12, omega-3, iron, zinc, iodine, and calcium needs. Published in Journal of the Academy of Nutrition and Dietetics.",
                      url: "https://www.jandonline.org/article/S2212-2672(16)31192-3/fulltext",
                      label: "J Acad Nutr Diet 2016 — Vegetarian Diets"
                    },
                    {
                      title: "PROT-AGE Study Group — Meeting Protein Needs of Older Adults",
                      desc: "Multi-disciplinary consensus paper recommending 1.0–1.2g protein/kg/day for adults 65+, and up to 1.5g/kg during illness — the basis for this app's higher protein targets for older members.",
                      url: "https://www.jamda.com/article/S1525-8610(13)00321-0/fulltext",
                      label: "JAMDA 2013 — PROT-AGE Study Group"
                    },
                  ].map(ref => (
                    <div key={ref.title} style={{ marginBottom: 10, background: "rgba(255,255,255,0.03)", borderRadius: 8, padding: "8px 10px" }}>
                      <div style={{ fontSize: 14, fontWeight: 700, color: "#e2e8f0", marginBottom: 2 }}>{ref.title}</div>
                      <div style={{ fontSize: 13, color: "#94a3b8", lineHeight: 1.4, marginBottom: 4 }}>{ref.desc}</div>
                      <a href={ref.url} target="_blank" rel="noopener noreferrer" style={{ fontSize: 13, color: "#60a5fa", textDecoration: "none" }}>→ {ref.label}</a>
                    </div>
                  ))}
                  <div style={{ marginTop: 10, fontSize: 12, color: "#64748b", lineHeight: 1.5 }}>Food prices are based on publicly available {country === "NZ" ? "Countdown, New World and Pak'nSave" : "Coles and Woolworths"} homebrand pricing as of May 2026. Prices vary by region and over time — use as a guide only. This app does not provide medical or dietary advice; always consult a qualified health professional for individual needs.</div>
                </div>
              )}
            </div>

            <div style={{ background: "rgba(34,197,94,0.06)", border: "1px solid rgba(34,197,94,0.15)", borderRadius: 16, padding: 20, margin: "20px 0" }}>
              <div style={{ fontSize: 15, fontWeight: 700, color: "#f1f5f9", marginBottom: 6 }}>💬 Send Feedback</div>
              <div style={{ fontSize: 14, color: "#64748b", marginBottom: 14 }}>Found a bug? Want a recipe? Just want to say hi? We read everything.</div>
              <FeedbackForm />
            </div>
            <div style={{ textAlign: "center", padding: 20, fontSize: 13, color: "#64748b" }}>
              <div>Australian Bureau of Statistics 2023 · NHMRC Nutrient Reference Values · Australian Government Physical Activity Guidelines</div>
              <div style={{ marginTop: 4 }}>Food prices based on {country === "NZ" ? "Countdown, New World & Pak'nSave" : "Coles & Woolworths"} homebrand — last updated May 2026</div>
            </div>
          </div>
        )}

      </div>

      {/* Nutrient Nudge Box */}
      {(() => {
        if (!["recipes","planner","snacks"].includes(tab)) return null;
        if (nMeals === 0) return null;
        const lowNutrients = NKS
          .filter(k => rda[k] && rda[k] > 0 && (totals[k] || 0) / rda[k] < 0.5)
          .map(k => ({ key: k, name: NK[k].name, pct: Math.round((totals[k] || 0) / rda[k] * 100) }))
          .sort((a, b) => a.pct - b.pct)
          .slice(0, 3);
        if (lowNutrients.length === 0) return null;
        return (
          <div style={{ position: "fixed", bottom: 88, left: "50%", transform: "translateX(-50%)", maxWidth: 480, width: "calc(100% - 24px)", zIndex: 100, background: "rgba(120,53,15,0.95)", backdropFilter: "blur(12px)", border: "1px solid rgba(251,146,60,0.4)", borderRadius: 12, padding: "10px 14px", display: "flex", alignItems: "center", gap: 10 }}>
            <span style={{ fontSize: 20, flexShrink: 0 }}>⚠️</span>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ fontSize: 13, fontWeight: 700, color: "#fed7aa", marginBottom: 3 }}>Today's plan is low in:</div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 5 }}>
                {lowNutrients.map(n => (
                  <span key={n.key} style={{ fontSize: 12, background: "rgba(251,146,60,0.2)", border: "1px solid rgba(251,146,60,0.35)", borderRadius: 6, padding: "2px 7px", color: "#fdba74", fontWeight: 600 }}>
                    {n.name} {n.pct}%
                  </span>
                ))}
              </div>
            </div>
            <button onClick={() => { go("learn"); }} style={{ background: "rgba(251,146,60,0.25)", border: "1px solid rgba(251,146,60,0.4)", borderRadius: 8, padding: "5px 10px", fontSize: 12, fontWeight: 700, color: "#fed7aa", cursor: "pointer", whiteSpace: "nowrap", flexShrink: 0 }}>Fix it →</button>
          </div>
        );
      })()}

      {/* Bottom Disclaimer */}
      <div style={{ position: "fixed", bottom: 52, left: 0, right: 0, background: "rgba(15,23,42,0.98)", borderTop: "1px solid rgba(255,255,255,0.06)", padding: "5px 16px", display: "flex", alignItems: "center", justifyContent: "center", gap: 6, zIndex: 100 }}>
        <span style={{ fontSize: 11, color: "#64748b", lineHeight: 1.4 }}>⚠️ Not medical advice. Always consult a GP or dietitian.</span>
        <button onClick={() => { setTab("learn"); setLearnOpen(p => ({ ...p, about: true })); window.scrollTo(0,0); }} style={{ background: "none", border: "none", color: "#3b82f6", fontSize: 11, cursor: "pointer", padding: 0, fontWeight: 600, whiteSpace: "nowrap" }}>Full disclaimer →</button>
      </div>

      {/* Bottom Nav */}
      <div style={{ position: "fixed", bottom: 0, left: 0, right: 0, background: "rgba(15,23,42,0.95)", backdropFilter: "blur(12px)", borderTop: "1px solid rgba(255,255,255,0.06)", padding: "6px 0", display: "flex", justifyContent: "center", zIndex: 101 }}>
        <div style={{ display: "flex", maxWidth: 480, width: "100%", justifyContent: "space-around" }}>
          {[["home", "🏠", "Home"], ["profile", "👤", "Profile"], ["dashboard", "📊", "Dash"], ["recipes", "📖", "Recipes"], ["planner", "📅", "Today"], ["weekly", "📆", "Week"], ["shopping", "🛒", "Shop"], ["learn", "📚", "Learn"]].map(([t, ic, lb]) => (
            <button key={t} onClick={() => setTab(t)} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 1, background: "none", border: "none", cursor: "pointer", padding: "5px 4px", color: tab === t ? "#22c55e" : "#64748b" }}>
              <span style={{ fontSize: 18 }}>{ic}</span>
              <span style={{ fontSize: 11, fontWeight: tab === t ? 700 : 500 }}>{lb}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
