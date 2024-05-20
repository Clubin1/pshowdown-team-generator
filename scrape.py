import requests
import concurrent.futures
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
from selenium.common.exceptions import TimeoutException


LIMIT = 10000
OFFSET = 0
DATA_FILE = "pokemon_data.json"


class Pokemon:
    def __init__(self):
        self.name = ""
        self.moves = []
        self.item = ""
        self.ability = ""
        self.nature = ""
        self.evs = []


class PokemonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Pokemon):
            return {
                'name': obj.name,
                'moves': obj.moves,
                'item': obj.item,
                'ability': obj.ability,
                'nature': obj.nature,
                'evs': obj.evs
            }
        return super().default(obj)


generations = {"rb", "gs", "rs", "dp", "bw", "xy", "sm", "ss", "sv"}
pokemon_map = {}


def fetch_pokemon_names(url):
    print(f"Fetching Pokemon names from {url}")
    response = requests.get(url)
    data = response.json()
    print(f"Fetched {len(data['results'])} Pokemon names")
    return data['results']


def populate_pokemon_map():
    print("Populating Pokemon map...")
    base_url = f'https://pokeapi.co/api/v2/pokemon?limit={LIMIT}&offset={OFFSET}'

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(fetch_pokemon_names, base_url)
        pokemon_list = future.result()

    for pokemon in pokemon_list:
        pokemon_name = pokemon["name"]
        pokemon_url = pokemon['url']
        pokemon_map[pokemon_name] = {"url": pokemon_url}
    print(f"Pokemon map populated with {len(pokemon_map)} entries")


def try_get_pokemon_info(name, data, driver):
    print(f"Getting info for {name}...")

    for gen in reversed(list(generations)):
        print(f"Trying generation {gen} for {name}")
        driver.get(f'https://www.smogon.com/dex/{gen}/pokemon/{name}/')
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "PokemonFamily")))
            print(f"Generation {gen} found for {name}")
        except TimeoutException:
            print(f"Generation {gen} not found for {name}")
            continue
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        moveset_div = soup.find('div', class_='MovesetInfo')
        moveset_table = moveset_div.find('table') if moveset_div else None
        move_rows = moveset_table.find_all('tr') if moveset_table else []

        evconfig_elem = soup.select_one('ul.evconfig')
        item_elem = soup.select_one('.ItemList li a span:nth-of-type(3)')
        ability_elem = soup.select_one('.AbilityList a span')
        nature_elem = soup.select_one('.NatureList li')

        if all([moveset_div, moveset_table, move_rows, evconfig_elem, item_elem, ability_elem, nature_elem]):
            pokemon = Pokemon()
            pokemon.name = name

            moves = []
            for row in move_rows:
                move_link = row.find('a', class_='MoveLink')
                if move_link:
                    move_name = move_link.text.strip()
                    moves.append(move_name)
            pokemon.moves = moves

            ev_values = [li.text.strip() for li in evconfig_elem.select('li')]
            pokemon.evs = ev_values

            pokemon.item = item_elem.text.strip()
            pokemon.ability = ability_elem.text.strip()
            pokemon.nature = nature_elem.text.strip()

            return pokemon

    return None


def scrape_pokemon(name, data, driver):
    print(f"Scraping {name}...")
    pokemon = try_get_pokemon_info(name, data, driver)
    if pokemon:
        print(f"Scraped {name}")
    else:
        print(f"No valid data found for {name}")
    return pokemon


def save_data(pokemon_data):
    print(f"Saving data to {DATA_FILE}")
    with open(DATA_FILE, 'w') as file:
        json.dump(pokemon_data, file, cls=PokemonEncoder, indent=4)
    print("Data saved")


def scrape():
    print("Starting scraping process...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(
        "/Users/jtubay/Desktop/chromedriver-mac-arm64/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    pokemon_data = {}

    for name, data in pokemon_map.items():
        pokemon = scrape_pokemon(name, data, driver)
        if pokemon:
            pokemon_data[pokemon.name] = pokemon

    driver.quit()
    save_data(pokemon_data)
    print("Scraping process completed")


print("Starting Pokemon scraper...")
populate_pokemon_map()
scrape()
print("Pokemon scraper finished")
