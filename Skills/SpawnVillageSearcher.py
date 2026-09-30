import cubiomespi
from cubiomespi import Generator, MCVersion, Structure, Dimension
import random

# Skill: Village Near Spawn Searching
# You have to write a simple code as the user prompt, and long if needed.
# to return the seed or anything else, you have to use print(x) and don't forget to add it!
# Get to know cubiomespi better before start.

version = MCVersion.MC_1_20  # Here you can put the version of minecraft (as user message)

# Loop over random seeds until a village is found near spawn
for _ in range(10000):
    seed = random.randint(1, 2147483647)
    world = Generator(version, seed, Dimension.DIM_OVERWORLD)

    spawn_x, spawn_z = cubiomespi.get_spawn_pos(world)
    spawn_cx = spawn_x >> 4
    spawn_cz = spawn_z >> 4

    village_pos = cubiomespi.get_structure_pos(Structure.Village, world, spawn_cx, spawn_cz)

    if village_pos:
        v_x, v_z = village_pos[0] * 16, village_pos[1] * 16
        distance = ((spawn_x - v_x) ** 2 + (spawn_z - v_z) ** 2) ** 0.5

        if distance <= 150:
            print(f"هذا هو الـseed: {seed}")
            print(f"احداثيات البدايه: {spawn_x} ~ {spawn_z}")
            print(f"احداثيات القريه: {v_x} ~ {v_z}")
            print(f"المسافه: {round(distance, 2)} بلوك")
            break
