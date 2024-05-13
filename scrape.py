
import requests
import concurrent.futures
from bs4 import BeautifulSoup
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
undefined_generation = []
pokemon_map = {}

def fetch_pokemon_data(pokemon_name, pokemon_url):
    """Helper function fetch pokemon data from pokeapi.co"""
    r = requests.get(pokemon_url)
    r_json = r.json()
    pokemon_id = r_json['id']
    if len(r_json['game_indices']) == 0:
        undefined_generation.append(pokemon_name)
      
    for game in r_json['game_indices']:
        return pokemon_name, pokemon_id, indices_to_generation[game['version']['name']]

def fetch_pokemon_names() -> dict:
    """Fetches all pokemon names from pokeapi.co"""
    r = requests.get("https://pokeapi.co/api/v2/pokemon?limit=10&offset=0")
    r_json = r.json()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for pokemon in r_json['results']:
            pokemon_name = pokemon["name"]
            pokemon_url = pokemon['url']
            pokemon_map[pokemon_name] = {"url": pokemon_url}
            futures.append(executor.submit(fetch_pokemon_data, pokemon_name, pokemon_url))

        for future in concurrent.futures.as_completed(futures):
            pokemon_name, pokemon_id, generation = future.result()
            pokemon_map[pokemon_name]["id"] = pokemon_id
            pokemon_map[pokemon_name]["gen"] = generation

def scrape():
    for name, data in pokemon_map.items():
        url = f'https://www.smogon.com/dex/{data["gen"]}/pokemon/{name}/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup.prettify())
fetch_pokemon_names()
scrape()