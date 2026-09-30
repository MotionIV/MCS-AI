import cubiomespi
from cubiomespi import Generator, MCVersion, Structure, Dimension
import random

# Skill: Structure Searching (near specific coordinates)
# You have to write a simple code as the user prompt, and long if needed.
# to return the seed or anything else, you have to use print(x) and don't forget to add it!
# Get to know cubiomespi better before start.

version = MCVersion.MC_1_20  # Here you can put the version of minecraft (as user message)
target_structure = Structure.Village  # The structure the user wants (There is no Structure.Stronghold!)

wanted_x, wanted_z = 50, 90  # The coordinates the user mentioned
wanted_cx, wanted_cz = wanted_x >> 4, wanted_z >> 4

for _ in range(10000):
    seed = random.randint(1, 2147483647)
    world = Generator(version, seed, Dimension.DIM_OVERWORLD)

    structure_pos = cubiomespi.get_structure_pos(target_structure, world, wanted_cx, wanted_cz)

    if structure_pos:
        s_x, s_z = structure_pos[0] * 16, structure_pos[1] * 16
        distance = ((wanted_x - s_x) ** 2 + (wanted_z - s_z) ** 2) ** 0.5

        if distance <= 150:
            print(f"هذا هو الـseed: {seed}")
            print(f"احداثيات الهيكل: {s_x} ~ {s_z}")
            print(f"المسافه من النقطه المطلوبه: {round(distance, 2)} بلوك")
            break
