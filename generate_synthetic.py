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
    "How many {unit} of {ing}? I have {qty}.",
    "Found {qty} {unit} of {ing} in the cabinet.",
    "I kept {qty} {unit} of {ing} in the freezer.",
    "Still got {qty} {unit} of {ing} from last week.",
    "Don’t forget, I’ve got {qty} {unit} {ing}.",
    "Is {qty} {unit} of {ing} enough for the recipe?",
    "I’m planning to use {qty} {unit} of {ing}.",
    "I think we’ve got {qty} {unit} of {ing} at home.",
    "I found {qty} {unit} {ing} in the basket.",
    "I always keep {qty} {unit} {ing} around.",
    "Still remaining: {qty} {unit} of {ing}.",
    "Don’t use more than {qty} {unit} of {ing}.",
    "Got {qty} {unit} {ing} from the market.",
    "Let’s cook something using {qty} {unit} {ing}.",
    "How to cook with {qty} {unit} {ing}?",
    "I picked up {qty} {unit} of {ing} today.",
    "Leftovers include {qty} {unit} of {ing}.",
    "Check if we have {qty} {unit} {ing}.",
    "Tonight I want to use {qty} {unit} {ing}.",
    "I bought {qty} {unit} {ing} for dinner.",
    "There’s still {qty} {unit} {ing} unopened.",
    "We might as well use {qty} {unit} {ing}.",
    "From last grocery: {qty} {unit} {ing}.",
    "We’ve saved {qty} {unit} {ing} for later.",
    "Fridge inventory shows {qty} {unit} {ing}.",
    "Use {qty} {unit} {ing} before it expires.",
    "I’m planning meals with {qty} {unit} {ing}.",
    "Stock includes just {qty} {unit} of {ing}.",
    "Today I’ll cook with {qty} {unit} {ing}.",
    "Used {qty} {unit} {ing} in last dish.",
    "I forgot I had {qty} {unit} {ing}.",
    "How to store {qty} {unit} {ing} properly?"
]


TWO_TEMPLATES = [
    "I have {qty1} {unit1} of {ing1} and {qty2} {unit2} of {ing2}.",
    "Bought {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2} today.",
    "There is {qty1} {unit1} {ing1} plus {qty2} {unit2} {ing2} in the fridge.",
    "I need {qty1} {unit1} {ing1}, and also {qty2} {unit2} {ing2}.",
    "Used {qty1} {unit1} {ing1} with {qty2} {unit2} {ing2}.",
    "Only {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2} left.",
    "Added {qty1} {unit1} {ing1} & {qty2} {unit2} {ing2} to the list.",
    "Fridge contains {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2}.",
    "Can we use {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2} tonight?",
    "Grab {qty1} {unit1} {ing1}, and {qty2} {unit2} {ing2} from the shelf.",
    "My stock: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}.",
    "Don’t forget {qty1} {unit1} {ing1} + {qty2} {unit2} {ing2}.",
    "Kitchen list: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}.",
    "Still got {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2}.",
    "I bought {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2} yesterday.",
    "Pantry contains {qty1} {unit1} {ing1} & {qty2} {unit2} {ing2}.",
    "We need {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2} for the dish.",
    "Use {qty1} {unit1} {ing1} with {qty2} {unit2} {ing2}.",
    "Still remaining: {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2}.",
    "Try mixing {qty1} {unit1} {ing1} with {qty2} {unit2} {ing2}.",
    "I found {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2} in the fridge.",
    "We’ve got {qty1} {unit1} {ing1} plus {qty2} {unit2} {ing2}.",
    "Use up {qty1} {unit1} {ing1}, and {qty2} {unit2} {ing2}.",
    "I stored {qty1} {unit1} {ing1} & {qty2} {unit2} {ing2}.",
    "Keep {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2} fresh.",
    "These are available: {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2}.",
    "I’ll be using {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2}.",
    "Got leftover {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}.",
    "Prepare {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2} please.",
    "Don’t waste {qty1} {unit1} {ing1} or {qty2} {unit2} {ing2}.",
    "Bought both {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2}.",
    "Enough with {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2}.",
    "Let’s make something using {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}.",
    "Want to cook with {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2}.",
    "How about a recipe for {qty1} {unit1} {ing1} & {qty2} {unit2} {ing2}?",
    "Don’t forget the {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2}.",
    "My grocery bag has {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}.",
    "Two things I have: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}.",
    "I only have {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2}.",
    "What can I make with {qty1} {unit1} {ing1} & {qty2} {unit2} {ing2}?",
    "Cooking plan: {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2}.",
    "On the table: {qty1} {unit1} {ing1} + {qty2} {unit2} {ing2}.",
    "Ready to cook with {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}.",
    "Kitchen counter: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}.",
    "Recipe ideas for {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2}?",
    "Bag contents: {qty1} {unit1} {ing1} + {qty2} {unit2} {ing2}.",
    "Leftover: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}.",
    "I have both {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2}.",
    "Need to use {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2} quickly."
]


THREE_TEMPLATES = [
    "I have {qty1} {unit1} of {ing1}, {qty2} {unit2} of {ing2}, and {qty3} {unit3} of {ing3}.",
    "There is {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3} in my kitchen.",
    "Bought {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3} today.",
    "We need {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, plus {qty3} {unit3} {ing3}.",
    "Fridge holds {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}.",
    "Used {qty1} {unit1} {ing1}, then added {qty2} {unit2} {ing2} and {qty3} {unit3} {ing3}.",
    "List includes {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "Currently stocked: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "Don’t forget to use {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}.",
    "Let’s cook using {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "Remaining: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}.",
    "Pantry has {qty1} {unit1} {ing1}, also {qty2} {unit2} {ing2} and {qty3} {unit3} {ing3}.",
    "The last items I bought were {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "Add to recipe: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "Ingredients to use: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}.",
    "What can I cook with {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}?",
    "I want to cook using {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2} and {qty3} {unit3} {ing3}.",
    "Prep includes {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2} and {qty3} {unit3} {ing3}.",
    "Only items available: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "Kitchen stock: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}.",
    "Need these for the recipe: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "I'm planning to cook with {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}.",
    "Can I make a dish with {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2} and {qty3} {unit3} {ing3}?",
    "What to make with {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}?",
    "In the fridge: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "Don’t waste {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}.",
    "Let’s clean out {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}.",
    "We still have {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "Try a recipe with {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}.",
    "All I got left are {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}.",
    "Main items: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "Found in pantry: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}.",
    "Planning lunch with {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "Please use {qty1} {unit1} {ing1}, then {qty2} {unit2} {ing2} and {qty3} {unit3} {ing3}.",
    "Last meal used {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}.",
    "Keep {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3} cold.",
    "My food plan: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, then {qty3} {unit3} {ing3}.",
    "On the menu: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}.",
    "Available today: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "To finish: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}.",
    "Cooking suggestion: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, plus {qty3} {unit3} {ing3}.",
    "Almost expired: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "Let’s try soup with {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}.",
    "I picked these up: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}.",
    "I need to cook {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}.",
    "Have we used {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}?",
    "Dish idea: {qty1} {unit1} {ing1}, then {qty2} {unit2} {ing2}, and top with {qty3} {unit3} {ing3}.",
    "We can make something tasty using {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}.",
    "Let’s finish off {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2} and {qty3} {unit3} {ing3}.",
    "My ingredients for today are: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}."
]


FOUR_TEMPLATES = [
    "I have {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}.",
    "Stocked: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "I bought {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}.",
    "Recipe needs {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}.",
    "Pantry holds {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}.",
    "Planning to cook with {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "These four are left: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}.",
    "Main ingredients today: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Cooking with {qty1} {unit1} {ing1}, then {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and finally {qty4} {unit4} {ing4}.",
    "Please grab {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}.",
    "Check fridge for {qty1} {unit1} {ing1}, also {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}.",
    "What dishes can I make using {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}?",
    "Last purchase: {qty1} {unit1} {ing1}, and {qty2} {unit2} {ing2}, plus {qty3} {unit3} {ing3} & {qty4} {unit4} {ing4}.",
    "Leftovers: {qty1} {unit1} {ing1}, also {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}.",
    "All I’ve got: {qty1} {unit1} {ing1}, with {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}.",
    "Inventory: {qty1} {unit1} {ing1} - {qty2} {unit2} {ing2} - {qty3} {unit3} {ing3} - {qty4} {unit4} {ing4}.",
    "Use these for lunch: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Don’t forget to finish {qty1} {unit1} {ing1} & {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "These need to be cooked: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, then {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Fridge shows: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and more: {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Ready for meal prep: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, then {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "I’m out of everything except {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "What can I do with only {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, plus {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}?",
    "Kitchen list: {qty1} {unit1} {ing1}, and also {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Just unpacked: {qty1} {unit1} {ing1}, and {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, plus {qty4} {unit4} {ing4}.",
    "Fresh today: {qty1} {unit1} {ing1}, then {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and finally {qty4} {unit4} {ing4}.",
    "Still got these: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Meal planner: {qty1} {unit1} {ing1} + {qty2} {unit2} {ing2} + {qty3} {unit3} {ing3} + {qty4} {unit4} {ing4}.",
    "Ingredients in fridge: {qty1} {unit1} {ing1}, with {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Preparing food with {qty1} {unit1} {ing1}, also {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "I only have {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4} left.",
    "Items still usable: {qty1} {unit1} {ing1} - {qty2} {unit2} {ing2} - {qty3} {unit3} {ing3} - {qty4} {unit4} {ing4}.",
    "My kitchen list: {qty1} {unit1} {ing1}, also {qty2} {unit2} {ing2}, then {qty3} {unit3} {ing3}, finally {qty4} {unit4} {ing4}.",
    "To cook today: {qty1} {unit1} {ing1}, followed by {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}.",
    "Here’s what I have: {qty1} {unit1} {ing1} / {qty2} {unit2} {ing2} / {qty3} {unit3} {ing3} / {qty4} {unit4} {ing4}.",
    "Remaining for dinner: {qty1} {unit1} {ing1}, and {qty2} {unit2} {ing2}, then {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Use up these four: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Need to cook all: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Pantry cleanout includes: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}.",
    "Cook using only: {qty1} {unit1} {ing1}, with {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}.",
    "Meal prep: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, then {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}.",
    "What can I do with {qty1} {unit1} {ing1}, also {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}?",
    "Need these four: {qty1} {unit1} {ing1}, and {qty2} {unit2} {ing2}, with {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "Found today: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, with {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "On hand: {qty1} {unit1} {ing1} and {qty2} {unit2} {ing2}, also {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}.",
    "Dinner idea with {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, then {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}.",
    "I’m using all of these: {qty1} {unit1} {ing1}, then {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}."
]


FIVE_TEMPLATES = [
    "I have {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, and {qty5} {unit5} {ing5}.",
    "My pantry holds {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, and {qty5} {unit5} {ing5}.",
    "Bought these: {qty1} {unit1} {ing1}, then {qty2} {unit2} {ing2}, plus {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, and {qty5} {unit5} {ing5}.",
    "Cooking tonight with {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Meal plan includes: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, and {qty5} {unit5} {ing5}.",
    "Here are the ingredients: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, then {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, and {qty5} {unit5} {ing5}.",
    "For the recipe, I’ve got {qty1} {unit1} {ing1}, also {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Let’s cook something using {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}, then {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Grocery list includes: {qty1} {unit1} {ing1}, plus {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Found these in my fridge: {qty1} {unit1} {ing1}, and also {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Everything I have now: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, and {qty5} {unit5} {ing5}.",
    "Tonight’s menu: {qty1} {unit1} {ing1}, plus {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}, then {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Using all these: {qty1} {unit1} {ing1}, then {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "I want to make a dish using {qty1} {unit1} {ing1}, with {qty2} {unit2} {ing2}, plus {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, and {qty5} {unit5} {ing5}.",
    "Need to use up: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Please grab: {qty1} {unit1} {ing1}, also {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Trying to finish off {qty1} {unit1} {ing1}, then {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "All leftovers include: {qty1} {unit1} {ing1}, along with {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Main ingredients left: {qty1} {unit1} {ing1}, plus {qty2} {unit2} {ing2}, with {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, and {qty5} {unit5} {ing5}.",
    "I only have {qty1} {unit1} {ing1}, then {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, and {qty5} {unit5} {ing5}.",
    "Meal plan: use {qty1} {unit1} {ing1}, then cook with {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and finish with {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "I picked up these today: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, and {qty5} {unit5} {ing5}.",
    "Try a dish that includes: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, with {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, and {qty5} {unit5} {ing5}.",
    "Everything is here: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}, then {qty4} {unit4} {ing4}, and {qty5} {unit5} {ing5}.",
    "Let’s combine {qty1} {unit1} {ing1} + {qty2} {unit2} {ing2} + {qty3} {unit3} {ing3} + {qty4} {unit4} {ing4} + {qty5} {unit5} {ing5}.",
    "Cooking idea with: {qty1} {unit1} {ing1}, then {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and also {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Check my stock: {qty1} {unit1} {ing1}, also {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}, then {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Kitchen inventory: {qty1} {unit1} {ing1}, with {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and more: {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "What can I cook with {qty1} {unit1} {ing1}, and {qty2} {unit2} {ing2}, and also {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}?",
    "Still got these: {qty1} {unit1} {ing1}, and also {qty2} {unit2} {ing2}, with {qty3} {unit3} {ing3}, then {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Just came from shopping with {qty1} {unit1} {ing1}, plus {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Let’s prepare everything using: {qty1} {unit1} {ing1}, followed by {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}, then {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "My full list: {qty1} {unit1} {ing1}, also {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, then {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Dinner prep involves: {qty1} {unit1} {ing1}, plus {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}, with {qty4} {unit4} {ing4}, and {qty5} {unit5} {ing5}.",
    "Meal ingredients today: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, then {qty3} {unit3} {ing3}, followed by {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Pantry status: {qty1} {unit1} {ing1}, also {qty2} {unit2} {ing2}, then {qty3} {unit3} {ing3}, and {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Try combining these five: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, {qty3} {unit3} {ing3}, {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "All fresh: {qty1} {unit1} {ing1}, then {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}, followed by {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "I’m preparing a dish using: {qty1} {unit1} {ing1}, also {qty2} {unit2} {ing2}, then {qty3} {unit3} {ing3}, and also {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Let's clear the fridge: {qty1} {unit1} {ing1}, {qty2} {unit2} {ing2}, and {qty3} {unit3} {ing3}, then {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}.",
    "Clean-out ingredients: {qty1} {unit1} {ing1}, and {qty2} {unit2} {ing2}, also {qty3} {unit3} {ing3}, plus {qty4} {unit4} {ing4}, {qty5} {unit5} {ing5}."
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
    total = 3000 if n_items == 1 else 3000
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