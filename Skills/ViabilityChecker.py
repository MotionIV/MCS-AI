import cubiomespi
from cubiomespi import Generator, MCVersion, Structure, Dimension
import random

# Skill: Checking if a Structure is Viable at Specific Coordinates
# You have to write a simple code as the user prompt, and long if needed.
# to return the seed or anything else, you have to use print(x) and don't forget to add it!
# Get to know cubiomespi better before start.

# Use this when the user gives EXACT coordinates and a seed (or wants one found)
# and asks "هل الهيكل ده ممكن يطلع هنا؟"

version = MCVersion.MC_1_20  # Here you can put the version of minecraft (as user message)
target_structure = Structure.Village  # الهيكل المطلوب التأكد منه

wanted_x, wanted_z = 100, 200  # الاحداثيات اللي اليوزر حددها

for _ in range(10000):
    seed = random.randint(1, 2147483647)
    world = Generator(version, seed, Dimension.DIM_OVERWORLD)

    is_viable = cubiomespi.is_viable_structure_pos(target_structure, world, wanted_x, wanted_z)

    if is_viable:
        print(f"هذا هو الـseed: {seed}")
        print(f"الهيكل بيظهر فعلا عند الاحداثيات: {wanted_x} ~ {wanted_z}")
        break
