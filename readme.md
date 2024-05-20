Script that generates Pokemon Showdown formatted lists from a JSON file of Pokemon data. 

First step is to scrape the pokemon names from pokeapi.co, then scrape smogon for the movesets, items, stats, etc.

Last step is to transform the JSON file into a Showdown formatted list based off the user parameters no what sort of team to generate.

Currently supports
- Generation selection
- Allowing legendaries, if so how many
- Allowing baby pokemon, NOT IMPLEMENTED YET