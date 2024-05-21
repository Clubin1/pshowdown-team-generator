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
from threading import Lock

LIMIT = 100000
OFFSET = 0
DATA_FILE = "pokemon_data_new.json"

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

generations = ["rb", "gs", "rs", "dp", "bw", "xy", "sm", "ss", "sv"]
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

    for gen in reversed(generations):
        print(f"Trying generation {gen} for {name}")
        driver.get(f'https://www.smogon.com/dex/{gen}/pokemon/{name}/')
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "DexBody")))
            print(f"Generation {gen} found for {name}")
        except TimeoutException:
            print(f"Generation {gen} not found for {name}")
            continue

        try:
            export_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ExportButton"))
            )
            driver.execute_script("arguments[0].click();", export_button)
            textarea = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.TAG_NAME, "textarea"))
            )
            pokemon_info = textarea.get_attribute("value")
            print(f"Pokemon info found for {name} in generation {gen}")
            return pokemon_info
        except (TimeoutException, Exception) as e:
            print(f"Error finding or clicking export button: {str(e)}")
            continue

    print(f"No valid data found for {name}")
    return None

def scrape_pokemon(index, name, data):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service("/Users/jtubay/Desktop/chromedriver-mac-arm64/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    pokemon_info = try_get_pokemon_info(name, data, driver)
    driver.quit()

    if pokemon_info:
        print(f"Scraped {name}")
        return (index, {name: pokemon_info})
    else:
        print(f"No valid data found for {name}")
        return (index, None)

def scrape():
    print("Starting scraping process...")

    results = []
    lock = Lock()

    def append_result(result):
        with lock:
            results.append(result)

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(scrape_pokemon, i, name, data) for i, (name, data) in enumerate(pokemon_map.items())]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            append_result(result)

    results.sort(key=lambda x: x[0])
    pokemon_data = {k: v for _, d in results if d for k, v in d.items()}

    save_data(pokemon_data)
    print("Scraping process completed")

def save_data(pokemon_data):
    print(f"Saving data to {DATA_FILE}")
    with open(DATA_FILE, 'w') as file:
        json.dump(pokemon_data, file, cls=PokemonEncoder, indent=4)
    print("Data saved")

print("Starting Pokemon scraper...")
populate_pokemon_map()
scrape()
print("Pokemon scraper finished")
