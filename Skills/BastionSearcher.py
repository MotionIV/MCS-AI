import cubiomespi
from cubiomespi import Generator, MCVersion, Structure, Dimension
import random

# Skill: Bastion Remnant Searching (Nether)
# You have to write a simple code as the user prompt, and long if needed.
# to return the seed or anything else, you have to use print(x) and don't forget to add it!
# Get to know cubiomespi better before start.

version = MCVersion.MC_1_20  # Here you can put the version of minecraft (as user message)

for _ in range(10000):
    seed = random.randint(1, 2147483647)
    nether_world = Generator(version, seed, Dimension.DIM_NETHER)

    pos = cubiomespi.get_structure_pos(Structure.Bastion_Remnant, nether_world, 0, 0)

    if pos:
        b_x, b_z = pos[0] * 16, pos[1] * 16
        variant = cubiomespi.get_bastion_variant(nether_world, b_x, b_z)

        print(f"هذا هو الـseed: {seed}")
        print(f"احداثيات الباستيون: {b_x} ~ {b_z}")
        print(f"نوع الباستيون: {cubiomespi.convert_to_string(variant, cubiomespi.BastionType)}")
        break
