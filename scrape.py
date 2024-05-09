"""
scrape smogon for pokemon movesets, stats, and items and output to a json file where the key is the pokemon ID and the value is the entire pokemon object
for ex
{
    "1": {
        "name": "bulbasaur",
        "types": ["grass"],
        "moves": ["tackle", "growl", "sleeptalk"],
        "items": ["leftovers"],
        "weight": "1.0kg",
        "height": "0.5m",
        "base_experience": "10",
        "abilities": ["run-fast", "clear-body"],
        "catch_rate": "100%",
        "base_cpp": "40",
        "base_stamina": "40",
        "base_attack": "40",
        "base_defense": "40",
        "base_speed": "40",
        "base_hp": "40",
        "id": "1",
        "image": "bulbasaur.png"
    }
}
to determine if the pokemon is a baby pokemon, when scraping only add the pokemon if it is at the deepest list level 
<h2 data-reactid = ".0.1.1.2.2.0" >
Evolutions < /h2 > 
<ul class = "PokemonFamily" data-reactid = ".0.1.1.2.2.1" >
   <li data-reactid = ".0.1.1.2.2.1.0" >
      <div data-reactid = ".0.1.1.2.2.1.0.0" >
         <a href = "/dex/sm/pokemon/pichu/" data-reactid = ".0.1.1.2.2.1.0.0.0" > 
         <span data-reactid = ".0.1.1.2.2.1.0.0.0.0" > 
         <span class = "PokemonSprite is-normalized-width" data-reactid = ".0.1.1.2.2.1.0.0.0.0.0" > 
         <span class = "sprite-pichu" data-reactid = ".0.1.1.2.2.1.0.0.0.0.0.0" > </span > </span > 
         <span data-reactid = ".0.1.1.2.2.1.0.0.0.0.2" > Pichu < /span > </span > </a > 
         <ul class = "PokemonFamily" data-reactid = ".0.1.1.2.2.1.0.0.1" >
            <li data-reactid = ".0.1.1.2.2.1.0.0.1.0" >
               <div data-reactid = ".0.1.1.2.2.1.0.0.1.0.0" >
                  <a href = "/dex/sm/pokemon/pikachu/" data-reactid = ".0.1.1.2.2.1.0.0.1.0.0.0" > <span data-reactid = ".0.1.1.2.2.1.0.0.1.0.0.0.0" > <span class = "PokemonSprite is-normalized-width" data-reactid = ".0.1.1.2.2.1.0.0.1.0.0.0.0.0" > <span class = "sprite-pikachu" data-reactid = ".0.1.1.2.2.1.0.0.1.0.0.0.0.0.0" > </span > </span > <span data-reactid = ".0.1.1.2.2.1.0.0.1.0.0.0.0.2" > Pikachu < /span > </span > </a > 
                  <ul class = "PokemonFamily" data-reactid = ".0.1.1.2.2.1.0.0.1.0.0.1" >
                     <li data-reactid = ".0.1.1.2.2.1.0.0.1.0.0.1.0" >
                        <div data-reactid = ".0.1.1.2.2.1.0.0.1.0.0.1.0.0" > <span class = "is-selected" data-reactid = ".0.1.1.2.2.1.0.0.1.0.0.1.0.0.0" > <span class = "PokemonSprite is-normalized-width" data-reactid = ".0.1.1.2.2.1.0.0.1.0.0.1.0.0.0.0" > <span class = "sprite-raichu" data-reactid = ".0.1.1.2.2.1.0.0.1.0.0.1.0.0.0.0.0" > </span > </span > <span data-reactid = ".0.1.1.2.2.1.0.0.1.0.0.1.0.0.0.2" > Raichu < /span > </span > </div >
                     </li >
                     <li data-reactid = ".0.1.1.2.2.1.0.0.1.0.0.1.1" >
                        <div data-reactid = ".0.1.1.2.2.1.0.0.1.0.0.1.1.0" > <a href = "/dex/sm/pokemon/raichu-alola/" data-reactid = ".0.1.1.2.2.1.0.0.1.0.0.1.1.0.0" > <span data-reactid = ".0.1.1.2.2.1.0.0.1.0.0.1.1.0.0.0" > <span class = "PokemonSprite is-normalized-width" data-reactid = ".0.1.1.2.2.1.0.0.1.0.0.1.1.0.0.0.0" > <span class = "sprite-raichu-alola" data-reactid = ".0.1.1.2.2.1.0.0.1.0.0.1.1.0.0.0.0.0" > </span > </span > <span data-reactid = ".0.1.1.2.2.1.0.0.1.0.0.1.1.0.0.0.2" > Raichu-Alola < /span > </span > </a > </div >
                     </li >
                  </ul >
               </div >
            </li >
         </ul >
      </div >
   </li >
</ul >
for example the deepest list items are the final evolutions of the pokemon, so if the current pokemon we are at is not the deepest, dont add to the list

to get all visitable pokemon, using pokeapi.co and iterate the result object for all names of the pokemon. From there, visit the smogon page for each pokemon and parse
the moveset, items, stats, etc.
"""

import requests
indices_to_generation = {
    "red": "rb",
    "blue": "rb",
    "yellow": "rb",
    "gold": "gs",
    "silver": "gs",
    "crystal": "gs",
    "ruby": "rs",
    "sapphire": "rs",
    "emerald": "rs",
    "firered": "rb",
    "leafgreen": "rb",
    "diamond": "dp",
    "pearl": "dp",
    "platinum": "dp",
    "heartgold": "gs",
    "soulsilver": "gs",
    "black": "bw",
    "white": "bw",
    "black-2": "b2w2",
    "white-2": "b2w2",
    "x": "xy",
    "y": "xy",
    "sun": "sm",
    "moon": "sm",
    "sword": "ss",
    "shield": "ss"
}


def fetch_pokemon_names() -> list[str]:
    """Fetches all pokemon names from pokeapi.co"""
    r = requests.get("https://pokeapi.co/api/v2/pokemon?limit=10&offset=0")
    r_json = r.json()
    pokemon_map = {}
    pokemon_gen_map = {}

    for pokemon in r_json['results']:
        pokemon_map[pokemon["name"]] = {"url": pokemon['url']}

    for k, v in pokemon_map.items():
        r = requests.get(v["url"])
        r_json = r.json()
        for game in r_json['game_indices']:
            # if no game indices then add it to an unmarked list for now
            pokemon_gen_map[k] = indices_to_generation[game['version']['name']]
            break

    for k, v in pokemon_gen_map.items():
        pokemon_map[k]["gen"] = v

    print(pokemon_map)
print(fetch_pokemon_names())
