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