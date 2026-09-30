import cubiomespi
from cubiomespi import Generator, MCVersion, Dimension
import random

# Skill: Stronghold Searching
# You have to write a simple code as the user prompt, and long if needed.
# to return the seed or anything else, you have to use print(x) and don't forget to add it!
# Get to know cubiomespi better before start.

version = MCVersion.MC_1_20  # Here you can put the version of minecraft (as user message)

seed = random.randint(1, 2147483647)
world = Generator(version, seed, Dimension.DIM_OVERWORLD)


# Gets the nearest N strongholds
# NOTE: get_stronghold_pos returns BLOCK coordinates directly, NOT chunk coordinates.
# Do NOT multiply by 16 here (unlike get_structure_pos which returns chunk coords).
strongholds = cubiomespi.get_stronghold_pos(world, 3)

if strongholds:
    print(f"هذا هو الـseed: {seed}")
    for i, (sx, sz) in enumerate(strongholds):
        print(f"الستروانج هولد رقم {i+1}: {sx} ~ {sz}")
