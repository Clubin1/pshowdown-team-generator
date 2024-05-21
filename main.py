import argparse
import sys
import random
import json
import pyperclip

gen_to_pokeids = {
    1: (0, 150),
    2: (151, 250),
    3: (251, 385),
    4: (386, 492),
    5: (493, 648),
    6: (649, 720),
    7: (721, 808),
    8: (809, 904),
    9: (905, 1024),
    10: (0, 1024),
}


def main():
    args = parse_args(sys.argv[1:])
    generate_pokemon(args)


def parse_args(args):
    parser = argparse.ArgumentParser(
        description='Generate Pokemon based on specified criteria.')
    parser.add_argument('-g', '--generation', type=int,
                        help='Specify the generation of the Pokemon to generate.')
    parser.add_argument('-l', '--legendaries', action=argparse.BooleanOptionalAction,
                        default=False, help='Include legendary/mythic Pokemon.')
    parser.add_argument('-b', '--babies', action=argparse.BooleanOptionalAction,
                        default=False, help='Allow baby Pokemon in the generated list.')
    parser.add_argument('-lc', '--legendary_count', type=int, choices=range(1, 7),
                        default=1, help='Specify the number of legendaries to generate (1-6, default: 1).')
    return parser.parse_args(args)


legendaries = {144, 145, 146, 243, 244, 380, 379, 378, 377, 245, 381, 480, 481, 482, 485, 640, 639, 638, 488, 486, 641, 642, 645, 772, 773, 793, 785, 786, 787, 788, 798, 794, 795, 796, 797, 806, 805, 804, 803, 799, 891, 892, 894, 895, 896, 1003, 1002, 1001, 905,
               897, 1004, 1014, 1015, 1016, 1017, 150, 259, 250, 382, 383, 643, 487, 484, 483, 384, 644, 716, 717, 718, 800, 792, 791, 888, 889, 890, 898, 1007, 1008, 151, 251, 385, 386, 489, 494, 493, 492, 491, 490, 647, 648, 649, 719, 720, 808, 807, 802, 801, 721, 809, 893}


def generate_pokemon(args):
    """
    Generates a list of Pokemon based on the specified arguments.
    TODO: Implement the logic for including/exluding baby pokemon
    """
    print(args.generation)
    print(args.legendaries)
    print(args.babies)
    print(args.legendary_count)

    if args.generation == 99:
        args.generation = 10

    if args.generation not in gen_to_pokeids:
        print(f'Generation {args.generation} not found.')
        return

    pokeids = gen_to_pokeids[args.generation]
    pokemon = []
    generated_ids = set()
    legendary_count = 0

    available_legendaries = sum(1 for i in range(
        pokeids[0], pokeids[1] + 1) if i in legendaries)

    if args.legendaries and args.legendary_count > available_legendaries:
        print(
            f"Warning: Requested legendary count ({args.legendary_count}) exceeds available legendaries ({available_legendaries}) in generation {args.generation}.")
        print(f"Adjusting legendary count to {available_legendaries}.")
        args.legendary_count = available_legendaries

    while len(pokemon) < 6:
        poke_id = random.randint(pokeids[0], pokeids[1])

        if poke_id in generated_ids:
            continue

        if args.legendaries:
            if legendary_count < args.legendary_count and poke_id in legendaries:
                pokemon.append(poke_id)
                legendary_count += 1
                generated_ids.add(poke_id)
            elif legendary_count == args.legendary_count and poke_id not in legendaries:
                pokemon.append(poke_id)
                generated_ids.add(poke_id)
        else:
            if poke_id not in legendaries:
                pokemon.append(poke_id)
                generated_ids.add(poke_id)

    print(pokemon)
    transform_json_to_showdown_format(pokemon)


def transform_json_to_showdown_format(pokemon_list):
    """
    Reads the JSON file and transforms the selected Pokemon into the Pokemon Showdown format.
    """
    with open("pokemon_data_new.json", "r") as f:
        data = json.load(f)

    output = ""
    for i, pokemon in enumerate(data):
        if i in pokemon_list:
            output += data[pokemon] + "\n\n"

    print(output)
    pyperclip.copy(output.strip())
    print("Pokemon Showdown format copied to clipboard!")


if __name__ == '__main__':
    main()
