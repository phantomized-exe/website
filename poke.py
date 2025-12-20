import requests
import io # needed to process the bytes that we will download the sprite in
from pathlib import Path # if you want to create a cache of sprites
import tkinter as tk
from PIL import Image, ImageTk # allows us to manipulate images
import random
import json
import time


# ---------- constants ----------
POKE_COUNT = 1025                              # adjust if new pokemon come out (is this a thing?)
API_URL    = "https://pokeapi.co/api/v2/pokemon/{}" # we will use {} later for substitution with .format()
POKE_ID = random.randint(0,POKE_COUNT)

TYPE_COLORS = {
    'normal': '#A8A77A',
    'fire': '#EE8130',
    'water': '#6390F0',
    'grass': '#7AC74C',
    'electric': '#F7D02C',
    'ice': '#96D9D6',
    'fighting': '#C22E28',
    'poison': '#A33EA1',
    'ground': '#E2BF65',
    'flying': '#A98FF3',
    'psychic': '#F95587',
    'bug': '#A6B91A',
    'rock': '#B6A136',
    'ghost': '#735797',
    'dragon': '#6F35FC',
    'steel': '#B7B7CE',
    'dark': '#705746',
    'fairy': '#D685AD',
}

# ---------- create our own dictionary of pokemon info ----------
def rand_poke():
    POKE_COUNT = 1025                              # adjust if new pokemon come out (is this a thing?)
    API_URL    = "https://pokeapi.co/api/v2/pokemon/{}" # we will use {} later for substitution with .format()
    POKE_ID = random.randint(1, POKE_COUNT)
    request = requests.get(API_URL.format(POKE_ID),timeout=10)
    request.raise_for_status()
    data = request.json()
    formatted_data = {
        "id":           POKE_ID,
        "name":         data["name"].title(),
        "types":        [t["type"]["name"] for t in data["types"]], 
        "weight_kg":    data["weight"]/10,
        "sprite":       data["sprites"]["front_default"],
        "abilities":    [a["ability"]["name"] for a in data.get("abilities", [])],
        "attacks":      [m["move"]["name"] for m in data.get("moves", [])],
        
    }
    return formatted_data

with open('old_backgrounds.json', 'r') as old_backgrounds_file:
    old_backgrounds = json.load(old_backgrounds_file)

#print(old_backgrounds)
for i, j in enumerate(old_backgrounds):
    if i == 0:
        old_background1 = j
    else:
        old_background2 = j
random_pokemon = rand_poke()
while True:
    print(len(random_pokemon["types"]))
    print(random_pokemon['types'])
    if len(random_pokemon["types"]) == 1:
        new_background1 = TYPE_COLORS[random_pokemon['types'][0]]
        new_background2 = TYPE_COLORS[random_pokemon['types'][0]]
    else:
        for i, j in enumerate(random_pokemon['types']):
            #print(j)
            #print(TYPE_COLORS.get(j, '#FFFFFF'))
            if i == 0:
                new_background1 = TYPE_COLORS[j]
            else:
                new_background2 = TYPE_COLORS[j]

    css = 'style.css'
    with open(css) as mycss:
        mystring = mycss.read()
    new_background = mystring.replace(f'background-image: linear-gradient(to right, {old_background1}, {old_background2})', f'background-image: linear-gradient(to right, {new_background1}, {new_background2})')

    background_list = []
    old_background1 = new_background1
    background_list.append(new_background1)
    if len(random_pokemon["types"]) == 2:
        old_background2 = new_background2
        background_list.append(new_background2)
    else:
        old_background2 = new_background1
        background_list.append(new_background1)
    with open('old_backgrounds.json', 'w') as old_backgrounds_file:
        json.dump(background_list, old_backgrounds_file)

    random_pokemon['types'] = [" " + i.capitalize() for i in random_pokemon["types"]]
    random_pokemon['abilities'] = [" " + i.capitalize() for i in random_pokemon.get("abilities")]
    random_pokemon['attacks'] = [" " + i.capitalize() for i in random_pokemon.get("attacks")]
    poke_json = open("pokemon.json", "w")
    json.dump(random_pokemon, poke_json)
    random_pokemon = rand_poke()
    time.sleep(5)
    with open(css, 'w') as mycss:
        mycss.write(new_background)