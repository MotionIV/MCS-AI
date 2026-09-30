import cubiomespi
from cubiomespi import Generator, MCVersion, Structure, Dimension
import random

# Skill: Multiple Structures in the Same Seed
# You have to write a simple code as the user prompt, and long if needed.
# to return the seed or anything else, you have to use print(x) and don't forget to add it!
# Get to know cubiomespi better before start.

# Use this when the user wants a seed containing 2+ structures near each other
# example: "عاوز seed فيه village و stronghold جنب بعض"

version = MCVersion.MC_1_20  # Here you can put the version of minecraft (as user message)

structures_wanted = [Structure.Village, Structure.Desert_Pyramid]  # الهياكل المطلوبه
search_range = 5  # نطاق البحث بالتشنكس حوالين النقطه

for _ in range(10000):
    seed = random.randint(1, 2147483647)
    world = Generator(version, seed, Dimension.DIM_OVERWORLD)

    found_positions = []
    all_found = True

    for structure in structures_wanted:
        pos = cubiomespi.get_structure_pos(structure, world, 0, 0)
        if pos:
            found_positions.append((structure, pos))
        else:
            all_found = False
            break

    if all_found and len(found_positions) == len(structures_wanted):
        print(f"هذا هو الـseed: {seed}")
        for structure, (cx, cz) in found_positions:
            print(f"{cubiomespi.convert_to_string(structure, Structure)}: {cx * 16} ~ {cz * 16}")
        break
