import cubiomespi
from cubiomespi import Generator, MCVersion, Structure, Dimension
import random

# Skill: Distance Between Two Points/Structures
# You have to write a simple code as the user prompt, and long if needed.
# to return the seed or anything else, you have to use print(x) and don't forget to add it!
# Get to know cubiomespi better before start.

# Use this when the user asks how far something is, or wants a seed where
# two things are within/at a specific distance of each other.

version = MCVersion.MC_1_20  # Here you can put the version of minecraft (as user message)

point_a = (0, 0)     # النقطه الاولى (ممكن تبقى السبون)
point_b_structure = Structure.Village  # الهيكل التاني اللي عايزين نحسب المسافه ليه

for _ in range(10000):
    seed = random.randint(1, 2147483647)
    world = Generator(version, seed, Dimension.DIM_OVERWORLD)

    ax, az = point_a
    pos = cubiomespi.get_structure_pos(point_b_structure, world, ax >> 4, az >> 4)

    if pos:
        bx, bz = pos[0] * 16, pos[1] * 16
        distance = cubiomespi.distance_between_points(ax, az, bx, bz)

        print(f"الـseed: {seed}")
        print(f"النقطه الاولى: {ax} ~ {az}")
        print(f"النقطه التانيه: {bx} ~ {bz}")
        print(f"المسافه بينهم: {round(distance, 2)} بلوك")
        break
