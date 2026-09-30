import cubiomespi
from cubiomespi import Generator, MCVersion, Dimension

# Skill: Selecting the Correct Minecraft Version
# You have to write a simple code as the user prompt, and long if needed.
# to return the seed or anything else, you have to use print(x) and don't forget to add it!
# Get to know cubiomespi better before start.

# Use this skill when the user mentions a specific Minecraft version
# Map the user's requested version text to the correct MCVersion constant, examples:
# "1.20" -> MCVersion.MC_1_20
# "1.19" -> MCVersion.MC_1_19
# "1.18" -> MCVersion.MC_1_18 (لو موجوده في النسخه)

version = MCVersion.MC_1_20  # <-- غيّرها حسب طلب اليوزر
seed = 123456789

world = Generator(version, seed, Dimension.DIM_OVERWORLD)
spawn_x, spawn_z = cubiomespi.get_spawn_pos(world)

print(f"تم استخدام النسخه المطلوبه بنجاح")
print(f"الـseed: {seed}")
print(f"احداثيات البدايه: {spawn_x} ~ {spawn_z}")
