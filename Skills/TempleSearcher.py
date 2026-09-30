import cubiomespi
from cubiomespi import Generator, MCVersion, Structure, Dimension
import random

# Skill: Temple / Pyramid Searching (Desert or Jungle)
# You have to write a simple code as the user prompt, and long if needed.
# to return the seed or anything else, you have to use print(x) and don't forget to add it!
# Get to know cubiomespi better before start.

version = MCVersion.MC_1_20  # Here you can put the version of minecraft (as user message)

# غيّرها حسب طلب اليوزر: Desert_Pyramid او Jungle_Temple
target_structure = Structure.Desert_Pyramid

for _ in range(10000):
    seed = random.randint(1, 2147483647)
    world = Generator(version, seed, Dimension.DIM_OVERWORLD)

    spawn_x, spawn_z = cubiomespi.get_spawn_pos(world)
    pos = cubiomespi.get_structure_pos(target_structure, world, spawn_x >> 4, spawn_z >> 4)

    if pos:
        t_x, t_z = pos[0] * 16, pos[1] * 16
        distance = cubiomespi.distance_between_points(spawn_x, spawn_z, t_x, t_z)

        if distance <= 300:
            print(f"هذا هو الـseed: {seed}")
            print(f"احداثيات المعبد: {t_x} ~ {t_z}")
            print(f"المسافه من السبون: {round(distance, 2)} بلوك")
            break
