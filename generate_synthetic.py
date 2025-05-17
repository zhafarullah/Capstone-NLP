import json
import random
import re

with open('vocab_lists.json') as f:
    lists = json.load(f)
INGREDIENTS = [i.lower() for i in lists['INGREDIENTS']]
UNITS       = [u.lower() for u in lists['UNITS']]
QUANTITIES  = [q.lower() for q in lists['QUANTITIES']]

# 2. Templates (20 each)
SINGLE_TEMPLATES = [
    "I have {qty} {unit} of {ing}.",
    "There is {qty} {unit} {ing} in my fridge.",
    "Bought {qty} {unit} {ing} today.",
    "I need {qty} {unit} of {ing}.",
    "Used {qty} {unit} {ing} for cooking.",
    "Only {qty} {unit} {ing} left in the pantry.",
    "Added {qty} {unit} of {ing} to the shopping list.",
    "Store {qty} {unit} {ing} properly.",
    "The recipe requires {qty} {unit} of {ing}.",
    "Could you get me {qty} {unit} of {ing}?",
    "I have just bought {qty} {unit} of {ing}.",
    "There are about {qty} {unit} {ing} in stock.",
    "Please measure {qty} {unit} of {ing}.",
    "Grab {qty} {unit} of {ing} from the store.",
    "Keep {qty} {unit} {ing} refrigerated.",
    "I’m low on {ing}, only {qty} {unit} left.",
    "My pantry contains {qty} {unit} {ing}.",
    "Can’t find more than {qty} {unit} of {ing}.",
    "Let’s use {qty} {unit} {ing} now.",
    "How many {unit} of {ing}? I have {qty}."
]

TWO_TEMPLATES = [
    "I have {qty1} {unit1} of {ing1} and {qty2} {unit2} of {ing2}.",
    "There is {qty1} {unit1} {ing1} plus {qty2} {unit2} {ing2} in my fridge.",
    "Bought {qty1} {unit1} {ing1} & {qty2} {unit2} {ing2} today.",
    "Need {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2}.",
    "Used up {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2}.",
    "Only {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2} left.",
    "Added {qty1} {unit1} {ing1} & {qty2} {unit2} {ing2} to list.",
    "Stock: {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2}.",
    "Grab {qty1} {unit1} {ing1} & {qty2} {unit2} {ing2}.",
    "Pantry has {qty1} {unit1} {ing1} plus {qty2} {unit2} {ing2}.",
    "Measure {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2}.",
    "Don’t forget {qty1} {unit1} {ing1} & {qty2} {unit2} {ing2}.",
    "I just bought {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2}.",
    "There are {qty1} {unit1} {ing1} & {qty2} {unit2} {ing2}.",
    "Need to buy {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}.",
    "Only {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}.",
    "Use {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2}.",
    "My stock: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}.",
    "Keep {qty1} {unit1} {ing1} + {qty2} {unit2} {ing2}.",
    "List {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}."
]

THREE_TEMPLATES = [
    "I have {qty1} {unit1} of {ing1}, {qty2} {unit2} of {ing2}, and {qty3} {unit3} of {ing3}.",
    "There is {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3} in my kitchen.",
    "Bought {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3} today.",
    "We need {qty1} {unit1} of {ing1}, {qty2} {unit2} of {ing2}, plus {qty3} {unit3} of {ing3}.",
    "Stock includes {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}.",
    "Added {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3} to the list.",
    "Currently, I have {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}.",
    "Remember to buy {qty1} {unit1} of {ing1}, {qty2} {unit2} of {ing2}, and {qty3} {unit3} of {ing3}.",
    "We’ve got {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3} in the fridge.",
    "Use {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3} for the recipe.",
    "My list: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "Grab {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "Ensure {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "Pantry holds {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "Only {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "Bought: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "List includes {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "I need {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "Please get {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "My kitchen: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}."
]

FOUR_TEMPLATES = [
    "I have {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}.",
    "Stock: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Bought {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}.",
    "Need {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3} & {qty4} {unit4} {ing4}.",
    "Added {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Kitchen has {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Please get {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Pantry: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Remember {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Use {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "List: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "My stock: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "I need {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Grab {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Bought: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Only {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Added: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "There are {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Kitchen list: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Need to stock {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}."
]

FIVE_TEMPLATES = [
    "I have {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4} and {qty5} {unit5} {ing5}.",
    "Stock: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Bought {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4} & {qty5} {unit5} {ing5}.",
    "Need {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Added {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, and {qty5} {unit5} {ing5}.",
    "Kitchen has {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Grab {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Pantry: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Remember {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Use {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "List: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "My stock: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Need {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Bought: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Only {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Added: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, and {qty5} {unit5} {ing5}.",
    "There are {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Kitchen list: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Need to stock {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}."
]

def clean_token(t: str) -> str:
    return re.sub(r'^[^\w]+|[^\w]+$', '', t).lower()

def tag_sequence(tokens, tags, seq_tokens, prefix):
    cleaned = [clean_token(t) for t in tokens]
    seq = [t.lower() for t in seq_tokens]
    L, M = len(cleaned), len(seq)
    for i in range(L - M + 1):
        if cleaned[i:i+M] == seq:
            tags[i] = f"B-{prefix}"
            for j in range(1, M):
                tags[i+j] = f"I-{prefix}"
            return True
    return False

def generate_examples(templates, n_items):
    examples = []
    total = 5000 if n_items == 1 else 2000
    for _ in range(total):
        # sample qty/unit/ing pairs
        q = [random.choice(QUANTITIES) for _ in range(n_items)]
        u = [random.choice(UNITS) for _ in range(n_items)]
        i = [random.choice(INGREDIENTS) for _ in range(n_items)]
        # build kwargs dasar
        kwargs = {f"qty{j+1}": q[j] for j in range(n_items)}
        kwargs.update({f"unit{j+1}": u[j] for j in range(n_items)})
        kwargs.update({f"ing{j+1}": i[j] for j in range(n_items)})
        # jika 1 item, tambahkan juga kunci tanpa angka
        if n_items == 1:
            kwargs['qty']  = q[0]
            kwargs['unit'] = u[0]
            kwargs['ing']  = i[0]
        # format text
        text = random.choice(templates).format(**kwargs).lower()
        toks = text.replace(",", "").rstrip(".").split()
        tags = ["O"] * len(toks)
        # tag each sequence
        success = True
        for j in range(n_items):
            if not tag_sequence(toks, tags, q[j].split(), "QUANTITY"):    success = False
            if not tag_sequence(toks, tags, u[j].split(), "UNIT"):        success = False
            if not tag_sequence(toks, tags, i[j].split(), "INGREDIENT"):  success = False
        if success:
            examples.append({"tokens": toks, "tags": tags})
    return examples

# 4. Generate all examples
examples = []
examples += generate_examples(SINGLE_TEMPLATES, 1)
examples += generate_examples(TWO_TEMPLATES,   2)
examples += generate_examples(THREE_TEMPLATES, 3)
examples += generate_examples(FOUR_TEMPLATES,  4)
examples += generate_examples(FIVE_TEMPLATES,  5)

# 5. Save synthetic dataset
with open('synthetic_ner.json', 'w') as f:
    json.dump(examples, f, indent=2)

print(f"Generated {len(examples)} synthetic examples.")