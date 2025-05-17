import json
import numpy as np
import pandas as pd
import re
import ast
from fractions import Fraction
import textwrap
from pprint import pprint
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import pickle

# — Load machine learning artifacts
model = load_model('best_ner_bilstm.h5')
tok2idx = pickle.load(open('tok2idx.pkl', 'rb'))
le = pickle.load(open('label_encoder.pkl', 'rb'))

# — Constants
MAXLEN = 50

# — Load recipe dataset (ubah path sesuai lokasi file Anda)
df_exploded = pd.read_csv(
    'nama_file.csv',
    converters={
        'Cleaned_Ingredients': lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    }
)

# — Faktor konversi satuan (basis gram/ml)
UNIT_FACTORS = {
    'kg':1000, 'kilo':1000, 'g':1, 'gram':1,
    'l':1000, 'ml':1, 'pound':453.592, 'lb':453.592,
    'ounce':28.3495, 'oz':28.3495,
    'teaspoon':4.92892, 'tsp':4.92892,
    'tablespoon':14.7868, 'tbsp':14.7868,
    'cup':240, 'cups':240, 'quart':946.353, 'pt':473.176
}

# — Helper: konversi string kuantitas → angka
def parse_number(q):
    q = q.strip().lower()
    if '/' in q:
        try:
            return float(Fraction(q))
        except:
            pass
    WORD2NUM = {'half':0.5, 'one':1, 'two':2, 'three':3, 'four':4}
    if q in WORD2NUM:
        return WORD2NUM[q]
    try:
        return float(q)
    except:
        return None

# — Fungsi NER: parse ingredients dari teks input
def parse_ingredients(text):
    toks = text.lower().replace(',', '').split()
    seq = [tok2idx.get(w, tok2idx['UNK']) for w in toks]
    pad = pad_sequences([seq], maxlen=MAXLEN, padding='post', value=tok2idx['PAD'])
    preds = model.predict(pad)[0]
    labs = le.inverse_transform(preds.argmax(-1))[:len(toks)]

    items = []
    cur_item = {'quantity': None, 'unit': None, 'ingredient': None}
    ent_tokens, ent_type = [], None

    for w, tag in zip(toks, labs):
        if tag != 'O':
            typ = tag.split('-',1)[1].lower()
            if ent_type != typ:
                if ent_tokens and ent_type:
                    cur_item[ent_type] = " ".join(ent_tokens)
                    ent_tokens = []
                ent_type = typ
                ent_tokens = [w]
            else:
                ent_tokens.append(w)
        else:
            if ent_tokens and ent_type:
                cur_item[ent_type] = " ".join(ent_tokens)
                ent_tokens = []
                ent_type = None
        if all(cur_item.values()):
            items.append(cur_item.copy())
            cur_item = {'quantity': None, 'unit': None, 'ingredient': None}

    if ent_tokens and ent_type:
        cur_item[ent_type] = " ".join(ent_tokens)
    if all(cur_item.values()):
        items.append(cur_item)

    return items

# — Fungsi rekomendasi resep berdasarkan bahan parsed
def recommend_recipes(text, top_n=5):
    items = parse_ingredients(text)
    pprint(items)
    if not items:
        return pd.DataFrame(columns=['Title_Cleaned', 'Instructions_Cleaned', 'Cleaned_Ingredients'])

    title_sets = []
    for it in items:
        qty_num = parse_number(it['quantity'])
        unit = it['unit'].lower()
        ing = it['ingredient']
        mask_name = df_exploded['name'].str.contains(re.escape(ing), case=False, na=False)

        factor_in = UNIT_FACTORS.get(unit)
        factors = df_exploded['unit'].map(UNIT_FACTORS)
        if factor_in and qty_num is not None:
            avail = qty_num * factor_in
            mask_conv = mask_name & factors.notna() & ((df_exploded['quantity'] * factors) <= avail)
        else:
            mask_conv = pd.Series(False, index=df_exploded.index)

        if qty_num is not None:
            mask_fb = mask_name & \
                      (df_exploded['unit'].str.lower() == unit) & \
                      (df_exploded['quantity'] <= qty_num)
        else:
            mask_fb = pd.Series(False, index=df_exploded.index)

        mask = mask_conv | mask_fb
        titles = set(df_exploded.loc[mask, 'Title_Cleaned'])
        if titles:
            title_sets.append(titles)

    if not title_sets:
        return pd.DataFrame(columns=['Title_Cleaned', 'Instructions_Cleaned', 'Cleaned_Ingredients'])

    common = set.intersection(*title_sets)
    if not common:
        return pd.DataFrame(columns=['Title_Cleaned', 'Instructions_Cleaned', 'Cleaned_Ingredients'])

    df_meta = (
        df_exploded
        .drop_duplicates(subset=['Title_Cleaned'])
        .loc[:, ['Title_Cleaned', 'Instructions_Cleaned', 'Cleaned_Ingredients']]
    )

    return df_meta[df_meta['Title_Cleaned'].isin(common)].head(top_n)

# — Main program: input dan cetak hasil rekomendasi
def main():
    text = input("Masukkan bahan makanan: ")
    res = recommend_recipes(text, top_n=5)
    split_pattern = re.compile(r'(?<!\b\d)(?<!tsp)(?<!tbsp)\.\s+')

    if res.empty:
        print("Maaf, tidak ada resep yang cocok.")
        return

    for _, row in res.iterrows():
        print(f"\n=== {row['Title_Cleaned']} ===\n")
        print("Instructions:")
        instr = row['Instructions_Cleaned'].strip()
        parts = split_pattern.split(instr)
        for part in parts:
            sent = part.strip().rstrip('.')
            if not sent:
                continue
            wrapped = textwrap.fill(sent, width=80)
            for i, line in enumerate(wrapped.split('\n')):
                prefix = "- " if i == 0 else "  "
                print(f"  {prefix}{line}")
        print("\nIngredients:")
        for ing in row['Cleaned_Ingredients']:
            print(f"  - {ing}")
        print("\n" + "="*40)

if __name__ == "__main__":
    main()
