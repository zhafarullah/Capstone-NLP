# data_prep_hybrid.py

import pandas as pd
import json
import re

# 1) Load CSV recipe Anda
df = pd.read_csv('/content/drive/MyDrive/nama_file.csv')

# 2) Ekstrak daftar unique ingredients
INGREDIENTS = sorted(
    df['pure_name']
      .dropna()
      .astype(str)
      .str.strip()
      .str.lower()
      .unique()
      .tolist()
)

# 3) Ekstrak otomatis UNITS & QUANTITIES dari kolom
raw_units = df['unit'].dropna().astype(str).str.lower().str.strip()
raw_qtys  = df['quantity'].dropna().astype(str).str.lower().str.strip()

auto_units = set(raw_units.unique().tolist())
auto_qtys  = set(raw_qtys.unique().tolist())

# 4) Daftar manual tambahan (sinonim, plural, verbal, fractions, etc)
MANUAL_UNITS = {
    # Volume (US)
    'tsp':      'tsp',  'teaspoon': 'tsp',  'teaspoons': 'tsp',
    'tbsp':     'tbsp', 'tablespoon':'tbsp','tablespoons':'tbsp',
    'cup':      'cup',  'cups':      'cup',  'c':    'cup',
    'pt':       'pt',   'pint':      'pt',   'pints':'pt',
    'qt':       'qt',   'quart':     'qt',   'quarts':'qt',
    'gal':      'gal',  'gallon':    'gal',  'gallons':'gal',

    # SI Volume
    'ml':       'ml',   'milliliter':'ml','milliliters':'ml','millilitre':'ml','millilitres':'ml',
    'l':        'l',    'liter':     'l',    'liters':'l','litre':'l','litres':'l',
    'dl':       'dl',   'deciliter':'dl','deciliters':'dl','decilitre':'dl','decilitres':'dl',

    # Massa/Berat
    'mg':       'mg',   'milligram':'mg','milligrams':'mg',
    'g':        'g',    'gram':      'g',    'grams':'g',
    'kg':       'kg',   'kilogram':  'kg',   'kilograms':'kg',
    'oz':       'oz',   'ounce':     'oz',   'ounces':'oz',
    'lb':       'lb',   'lbs':       'lb',   'pound':'lb','pounds':'lb',

    # Hitungan / satuan lain
    'piece':    'piece','pieces':    'piece',
    'slice':    'slice','slices':    'slice',
    'can':      'can',  'cans':      'can',
    'jar':      'jar',  'jars':      'jar',
    'bottle':   'bottle','bottles':  'bottle',
    'package':  'package','packages': 'package',
    'packet':   'packet','packets':  'packet',
    'bunch':    'bunch','bunches':   'bunch',
    'stalk':    'stalk','stalks':    'stalk',
    'clove':    'clove','cloves':    'clove',
    'leaf':     'leaf', 'leaves':    'leaf',
    'sprig':    'sprig','sprigs':    'sprig',
    'head':     'head', 'heads':     'head',
    'fillet':   'fillet','fillets':  'fillet',
    'stick':    'stick','sticks':    'stick',
    'bar':      'bar',  'bars':      'bar',
    'cube':     'cube', 'cubes':     'cube',
    'strip':    'strip','strips':    'strip',
    'drop':     'drop', 'drops':     'drop',
    'sheet':    'sheet','sheets':    'sheet',
    'ear':      'ear',  'ears':      'ear',
    'bulb':     'bulb', 'bulbs':     'bulb',
}

MANUAL_QTY = {
    'half', 'one and a half', 'one', 'two', 'three', 'four',
    'five', 'six', 'seven', 'eight', 'nine', 'ten',
    'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
    'quarter', 'third', 'three quarters', '1/2', '1/3', '1/4', '3/4', '1/8'
}

# 5) Normalize plural <-> singular (very basic)
def normalize_unit(u):
    u = u.lower().strip()
    # remove trailing 's' for simple plurals, but keep exceptions
    if u.endswith('es') and not u.endswith('ches'):
        u = u[:-2]
    elif u.endswith('s') and not u.endswith(('ss','us')):
        u = u[:-1]
    return u

# apply normalization to auto_units and MANUAL_UNITS
norm_auto_units = { normalize_unit(u) for u in auto_units }
norm_manual_units = { normalize_unit(u) for u in MANUAL_UNITS }

# 6) Combine & sort
UNITS = sorted(norm_auto_units.union(norm_manual_units))
QUANTITIES = sorted(auto_qtys.union(MANUAL_QTY), key=lambda x: (len(x), x))

# 7) (Optional) remove any bad tokens (e.g., purely numeric placeholders)
pattern_clean = re.compile(r'^[\d\-/\s]+$')
UNITS = [u for u in UNITS if not pattern_clean.match(u)]
QUANTITIES = [q for q in QUANTITIES if not pattern_clean.match(q)]

# 8) Save to JSON
with open('vocab_lists.json', 'w') as f:
    json.dump({
        "INGREDIENTS": INGREDIENTS,
        "UNITS":       UNITS,
        "QUANTITIES":  QUANTITIES
    }, f, indent=2)

print(f"Ingredients: {len(INGREDIENTS)}, Units: {len(UNITS)}, Quantities: {len(QUANTITIES)}")
