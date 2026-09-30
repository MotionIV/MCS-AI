import cubiomespi
from cubiomespi import Generator, MCVersion, Dimension, BiomeID
import random

# Skill: Biome Searching
# You have to write a simple code as the user prompt, and long if needed.
# to return the seed or anything else, you have to use print(x) and don't forget to add it!
# Get to know cubiomespi better before start.

version = MCVersion.MC_1_20  # Here you can put the version of minecraft (as user message)
target_biome = BiomeID.desert  # Here you put the biome the user asked for

for _ in range(10000):
    seed = random.randint(1, 2147483647)
    world = Generator(version, seed, Dimension.DIM_OVERWORLD)

    spawn_x, spawn_z = cubiomespi.get_spawn_pos(world)
    biome = cubiomespi.get_biome_at(world, spawn_x, 63, spawn_z)

    if biome == target_biome:
        print(f"هذا هو الـseed: {seed}")
        print(f"الاحداثيات: {spawn_x} ~ {spawn_z}")
        break
