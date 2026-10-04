
import discord
from discord.ext import commands 
import json
from groq import Groq as G
import os
import ast
import subprocess

DATA_FILE = "data.json"
def read_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

client = G(api_key=read_data()["GROQ_TOKEN"])


intents = discord.Intents.default()
intents.message_content = True

_run = read_data()["WORK_IN_ANY_CHANNEL"]
_channel_id = read_data()["BOT_CHANNEL_ID"]
_developer_model = read_data()["DEVELOPER_MODEL"]
_simple_model = read_data()["SIMPLE_MODEL"]

def get_skill_names():
    names = "\n".join(os.listdir("Skills"))
    return names


bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_message(message: discord.Message):
    content = message.content.replace(bot.user.mention, "")
    sender = message.author

    if bot.user.mentioned_in(message) and (message.channel.id == _channel_id or _run):
        async with message.channel.typing():
            skill_searcher = client.chat.completions.create(
                model=_simple_model,
                messages=[
                    {"role": "system", "content": f"You're AI for searching for skills based in user message\nTake the user message and return the names (list) \n IMPORTANT: StructureSearcher.py and StrongholdSearcher.py are not the same!\nIMPORTANT: Use Multiprocess.py ONLY for heavy/multi-condition searches (e.g. two structures near each other, very tight distance requirements). For simple single-structure searches, do NOT include it.\nReturn 'USER_MESSAGING' is the user asking or normal messaging\nSkills: {get_skill_names()}"},
                    {"role": "user", "content": "User Prompt: عاوز قاريه جنب السبون"},
                    {"role": "assistant", "content": "['SpawnSearcher.py', 'StructureSearcher.py']"},

                    {"role": "user", "content": "User Prompt: عاوز stronghold في بايوم الصحراء"},
                    {"role": "assistant", "content": "['BiomeSearcher.py', 'StructureSearcher.py']"},

                    {"role": "user", "content": "User Prompt: عاوز قاريه في احداثيات ديه: 50 ~ 90"},
                    {"role": "assistant", "content": "['StructureSearcher.py']"},

                    {"role": "user", "content": "User Prompt: عاوز seed فيه قريه وتحتها stronghold"},
                    {"role": "assistant", "content": "['StructureSearcher.py', 'StrongholdSearcher.py', 'Multiprocess.py']"},

                    {"role": "user", "content": "اهلا عامل ايه؟"},
                    {"role": "assistant", "content": "USER_MESSAGING"},

                    {"role": "user", "content": "هل بتعرف تعمل سيدات ماين كرافت؟"},
                    {"role": "assistant", "content": "USER_MESSAGING"},


                    {"role": "user", "content": f"User Prompt: {content}"}
                ]
            )

            if skill_searcher.choices[0].message.content.startswith("USER_MESSAGING"):
                simple_IA = client.chat.completions.create(
                    model=_simple_model,
                    messages=[
                        {"role": "system", "content": f"You're AI for minecraft seed finding, the user will ask you questions and you will answer it, nothing else. max message length is 100 and discord limit is 2000 or fewer"},
                        {"role": "user", "content": "User: (Mohammed)\nMessage: اهلا"},
                        {"role": "assistant", "content": "اهلا ايه اخبارك؟ لو عندك اي سوأل وعاوزني اجاوبك عليه قلي"},

                        {"role": "user", "content": f"User: ({sender.display_name})\nMessage: {content}"}
                    ]
                )

                await message.reply(simple_IA.choices[0].message.content)

                return

            task_message: discord.Message = await message.reply("هبدء ابحث عن السكيلز المناسبه...")

            print(skill_searcher.choices[0].message.content)

            a_list = ast.literal_eval(skill_searcher.choices[0].message.content)
            a_codes = ""

            for file_name in a_list:
                a_codes += f"{file_name}:\n"
                with open(f"Skills\\{file_name}", "r", encoding="utf-8") as f:
                    a_codes += f"{f.read()}"


            example_code1 = """import cubiomespi
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
    """



            ref_api = """= MAIN CLASSES =
cubiomespi.BastionType -> <class 'type'>
cubiomespi.BiomeGroups -> <class 'type'>
cubiomespi.BiomeID -> <class 'type'>
cubiomespi.Dimension -> <class 'type'>
cubiomespi.Generator -> <class 'type'>
cubiomespi.MCVersion -> <class 'type'>
cubiomespi.Structure -> <class 'type'>
cubiomespi.util -> <class 'type'>
= ALL FUNCTIONS =
cubiomespi.find_closest_structure(g: cubiomespi.cubiomes.Generator, structure: cubiomespi.cubiomes.Structure, cx: int, cz: int, limit: int) -> tuple[int, int]
cubiomespi.find_structure_in_range(g: cubiomespi.cubiomes.Generator, structure: cubiomespi.cubiomes.Structure, srx: int, srz: int, erx: int, erz: int) -> list[tuple[int, int]]
cubiomespi.get_bastion_variant(g: cubiomespi.cubiomes.Generator, x: int, z: int) -> cubiomespi.cubiomes.BastionType
cubiomespi.get_biome_at(g: cubiomespi.cubiomes.Generator, x: int, y: int, z: int) -> cubiomespi.cubiomes.BiomeID
cubiomespi.get_spawn_pos(g: cubiomespi.cubiomes.Generator) -> tuple[int, int]
cubiomespi.get_stronghold_pos(g: cubiomespi.cubiomes.Generator, count) -> list[tuple[int, int]]
cubiomespi.get_structure_pos(structure: cubiomespi.cubiomes.Structure, g: cubiomespi.cubiomes.Generator, rx: int, rz: int) -> tuple[int, int]
cubiomespi.is_viable_structure_pos(structure: cubiomespi.cubiomes.Structure, g: cubiomespi.cubiomes.Generator, x: int, z: int) -> bool
= IN CLASSES =
cubiomespi.BastionType.BRIDGE -> <class 'int'>
cubiomespi.BastionType.HOUSING -> <class 'int'>
cubiomespi.BastionType.STABLES -> <class 'int'>
cubiomespi.BastionType.TREASURE -> <class 'int'>
cubiomespi.BastionType._name -> <class 'str'>
cubiomespi.BiomeGroups.Beaches -> <class 'list'>
cubiomespi.BiomeGroups.DesertBiomes -> <class 'list'>
cubiomespi.BiomeGroups.Forests -> <class 'list'>
cubiomespi.BiomeGroups.Oceans -> <class 'list'>
(Everything is type <int>):
cubiomespi.BiomeID.badlands
cubiomespi.BiomeID.badlands_plateau
cubiomespi.BiomeID.bamboo_jungle
cubiomespi.BiomeID.bamboo_jungle_hills
cubiomespi.BiomeID.basalt_deltas
cubiomespi.BiomeID.beach
cubiomespi.BiomeID.birchForest
cubiomespi.BiomeID.birchForestHills
cubiomespi.BiomeID.birch_forest
cubiomespi.BiomeID.birch_forest_hills
cubiomespi.BiomeID.cherry_grove
cubiomespi.BiomeID.coldBeach
cubiomespi.BiomeID.coldDeepOcean
cubiomespi.BiomeID.coldOcean
cubiomespi.BiomeID.coldTaiga
cubiomespi.BiomeID.coldTaigaHills
cubiomespi.BiomeID.cold_ocean
cubiomespi.BiomeID.crimson_forest
cubiomespi.BiomeID.dark_forest
cubiomespi.BiomeID.dark_forest_hills
cubiomespi.BiomeID.deepOcean
cubiomespi.BiomeID.deep_cold_ocean
cubiomespi.BiomeID.deep_dark
cubiomespi.BiomeID.deep_frozen_ocean
cubiomespi.BiomeID.deep_lukewarm_ocean
cubiomespi.BiomeID.deep_ocean
cubiomespi.BiomeID.deep_warm_ocean
cubiomespi.BiomeID.desert
cubiomespi.BiomeID.desertHills
cubiomespi.BiomeID.desert_hills
cubiomespi.BiomeID.desert_lakes
cubiomespi.BiomeID.dripstone_caves
cubiomespi.BiomeID.end_barrens
cubiomespi.BiomeID.end_highlands
cubiomespi.BiomeID.end_midlands
cubiomespi.BiomeID.eroded_badlands
cubiomespi.BiomeID.extremeHills
cubiomespi.BiomeID.extremeHillsEdge
cubiomespi.BiomeID.extremeHillsPlus
cubiomespi.BiomeID.flower_forest
cubiomespi.BiomeID.forest
cubiomespi.BiomeID.forestHills
cubiomespi.BiomeID.frozenDeepOcean
cubiomespi.BiomeID.frozenOcean
cubiomespi.BiomeID.frozenRiver
cubiomespi.BiomeID.frozen_ocean
cubiomespi.BiomeID.frozen_peaks
cubiomespi.BiomeID.frozen_river
cubiomespi.BiomeID.giant_spruce_taiga
cubiomespi.BiomeID.giant_spruce_taiga_hills
cubiomespi.BiomeID.giant_tree_taiga
cubiomespi.BiomeID.giant_tree_taiga_hills
cubiomespi.BiomeID.gravelly_mountains
cubiomespi.BiomeID.grove
cubiomespi.BiomeID.hell
cubiomespi.BiomeID.iceMountains
cubiomespi.BiomeID.icePlains
cubiomespi.BiomeID.ice_spikes
cubiomespi.BiomeID.jagged_peaks
cubiomespi.BiomeID.jungle
cubiomespi.BiomeID.jungleEdge
cubiomespi.BiomeID.jungleHills
cubiomespi.BiomeID.jungle_edge
cubiomespi.BiomeID.jungle_hills
cubiomespi.BiomeID.lukewarmDeepOcean
cubiomespi.BiomeID.lukewarmOcean
cubiomespi.BiomeID.lukewarm_ocean
cubiomespi.BiomeID.lush_caves
cubiomespi.BiomeID.mangrove_swamp
cubiomespi.BiomeID.meadow
cubiomespi.BiomeID.megaTaiga
cubiomespi.BiomeID.megaTaigaHills
cubiomespi.BiomeID.mesa
cubiomespi.BiomeID.mesaPlateau
cubiomespi.BiomeID.mesaPlateau_F
cubiomespi.BiomeID.modified_badlands_plateau
cubiomespi.BiomeID.modified_gravelly_mountains
cubiomespi.BiomeID.modified_jungle
cubiomespi.BiomeID.modified_jungle_edge
cubiomespi.BiomeID.modified_wooded_badlands_plateau
cubiomespi.BiomeID.mountain_edge
cubiomespi.BiomeID.mountains
cubiomespi.BiomeID.mushroomIsland
cubiomespi.BiomeID.mushroomIslandShore
cubiomespi.BiomeID.mushroom_field_shore
cubiomespi.BiomeID.mushroom_fields
cubiomespi.BiomeID.nether_wastes
cubiomespi.BiomeID.none
cubiomespi.BiomeID.ocean
cubiomespi.BiomeID.old_growth_birch_forest
cubiomespi.BiomeID.old_growth_pine_taiga
cubiomespi.BiomeID.old_growth_spruce_taiga
cubiomespi.BiomeID.plains
cubiomespi.BiomeID.rainforest
cubiomespi.BiomeID.river
cubiomespi.BiomeID.roofedForest
cubiomespi.BiomeID.savanna
cubiomespi.BiomeID.savannaPlateau
cubiomespi.BiomeID.savanna_plateau
cubiomespi.BiomeID.seasonal_forest
cubiomespi.BiomeID.shattered_savanna
cubiomespi.BiomeID.shattered_savanna_plateau
cubiomespi.BiomeID.shrubland
cubiomespi.BiomeID.sky
cubiomespi.BiomeID.small_end_islands
cubiomespi.BiomeID.snowy_beach
cubiomespi.BiomeID.snowy_mountains
cubiomespi.BiomeID.snowy_plains
cubiomespi.BiomeID.snowy_slopes
cubiomespi.BiomeID.snowy_taiga
cubiomespi.BiomeID.snowy_taiga_hills
cubiomespi.BiomeID.snowy_taiga_mountains
cubiomespi.BiomeID.snowy_tundra
cubiomespi.BiomeID.soul_sand_valley
cubiomespi.BiomeID.sparse_jungle
cubiomespi.BiomeID.stoneBeach
cubiomespi.BiomeID.stone_shore
cubiomespi.BiomeID.stony_peaks
cubiomespi.BiomeID.stony_shore
cubiomespi.BiomeID.sunflower_plains
cubiomespi.BiomeID.swamp
cubiomespi.BiomeID.swamp_hills
cubiomespi.BiomeID.swampland
cubiomespi.BiomeID.taiga
cubiomespi.BiomeID.taigaHills
cubiomespi.BiomeID.taiga_hills
cubiomespi.BiomeID.taiga_mountains
cubiomespi.BiomeID.tall_birch_forest
cubiomespi.BiomeID.tall_birch_hills
cubiomespi.BiomeID.the_end
cubiomespi.BiomeID.the_void
cubiomespi.BiomeID.warmDeepOcean
cubiomespi.BiomeID.warmOcean
cubiomespi.BiomeID.warm_ocean
cubiomespi.BiomeID.warped_forest
cubiomespi.BiomeID.windswept_forest
cubiomespi.BiomeID.windswept_gravelly_hills
cubiomespi.BiomeID.windswept_hills
cubiomespi.BiomeID.windswept_savanna
cubiomespi.BiomeID.wooded_badlands
cubiomespi.BiomeID.wooded_badlands_plateau
cubiomespi.BiomeID.wooded_hills
cubiomespi.BiomeID.wooded_mountains
cubiomespi.Dimension.DIM_END
cubiomespi.Dimension.DIM_NETHER
cubiomespi.Dimension.DIM_OVERWORLD
cubiomespi.Dimension.DIM_UNDEF
cubiomespi.MCVersion.MC_1_0_0
cubiomespi.MCVersion.MC_1_10_2
cubiomespi.MCVersion.MC_1_11_2
cubiomespi.MCVersion.MC_1_12_2
cubiomespi.MCVersion.MC_1_13_2
cubiomespi.MCVersion.MC_1_14_4
cubiomespi.MCVersion.MC_1_15_2
cubiomespi.MCVersion.MC_1_16_1
cubiomespi.MCVersion.MC_1_16_5
cubiomespi.MCVersion.MC_1_17_1
cubiomespi.MCVersion.MC_1_18_2
cubiomespi.MCVersion.MC_1_19
cubiomespi.MCVersion.MC_1_19_2
cubiomespi.MCVersion.MC_1_1_0
cubiomespi.MCVersion.MC_1_20
cubiomespi.MCVersion.MC_1_2_5
cubiomespi.MCVersion.MC_1_3_2
cubiomespi.MCVersion.MC_1_4_7
cubiomespi.MCVersion.MC_1_5_2
cubiomespi.MCVersion.MC_1_6_4
cubiomespi.MCVersion.MC_1_7_10
cubiomespi.MCVersion.MC_1_8_9
cubiomespi.MCVersion.MC_1_9_4
cubiomespi.Structure.Ancient_City
cubiomespi.Structure.Bastion
cubiomespi.Structure.Desert_Pyramid
cubiomespi.Structure.Desert_Well
cubiomespi.Structure.End_City
cubiomespi.Structure.End_Gateway
cubiomespi.Structure.FEATURE_NUM
cubiomespi.Structure.Feature
cubiomespi.Structure.Fortress
cubiomespi.Structure.Geode
cubiomespi.Structure.Igloo
cubiomespi.Structure.Jungle_Pyramid
cubiomespi.Structure.Jungle_Temple
cubiomespi.Structure.Mansion
cubiomespi.Structure.Mineshaft
cubiomespi.Structure.Monument
cubiomespi.Structure.Ocean_Ruin
cubiomespi.Structure.Outpost
cubiomespi.Structure.Ruined_Portal
cubiomespi.Structure.Ruined_Portal_N
cubiomespi.Structure.Shipwreck
cubiomespi.Structure.Swamp_Hut
cubiomespi.Structure.Trail_Ruin
cubiomespi.Structure.Treasure
cubiomespi.Structure.Village
(More):
cubiomespi.util.convert_to_string -> <class 'function'>
cubiomespi.util.distance_between_points -> <class 'function'>
cubiomespi.util.distance_between_structures -> <class 'function'>
cubiomespi.util.distance_from_00 -> <class 'function'>"""

            example_json = json.dumps({"FileName": "VillageInSpawn.py", "SourceCode": example_code1}, ensure_ascii=False)

            developer = client.chat.completions.create(
                model=_developer_model,
                messages=[
                    {"role": "system", "content": f"You're a Developer, and creating python file with cubiomespi lib to help the user find a seed he wants in minecraft: ONLY Json, no extra text because your response goes to json.loads(), no markdown. Skills to learn from:\nCubiomespi:\n{ref_api}\n\nExample:\n{a_codes}"},
                    {"role": "user", "content": "User Prompt: عاوز قاريه جنب السبون"},
                    {"role": "assistant", "content": example_json},

        
                    {"role": "user", "content": f"User Prompt: {content}"}
                ]
            )
            print(developer.choices[0].message.content)
            await task_message.edit(content="دلوقتي هبدء اعمل سكربت البحث")

            try:
                parse_before_cleaning = developer.choices[0].message.content
                parse = json.loads(parse_before_cleaning.replace("```", ""))


                with open(f"Temp\\{parse["FileName"]}", "w", encoding="utf-8") as temp_file:
                    temp_file.write(parse["SourceCode"])
            except Exception as e:
                await message.reply("حصل حاجه غريبه... ممكن تعيد محاوله؟")
                await task_message.delete()
                print(f"PARSE ERR: {e}")
                return
                

            await task_message.edit(content="بدأت البحث! استنا شويه")
            try:
                result = subprocess.run(
                    ["python", f"Temp\\{parse["FileName"]}"],
                    capture_output=True,
                    timeout=100,
                    text=True,
                    encoding="utf-8",
                    env={**os.environ, "PYTHONIOENCODING": "utf-8"}
                )

                print(f"ERR: {result.stderr}")
                if result.returncode != 0:
                    await task_message.delete()
                    await message.reply("حصلت مشكله... برجاء اعادة محاوله")
                    return

                output = result.stdout.strip()
                if output:
                    await message.reply(output)

            

            except subprocess.TimeoutExpired:
                await message.reply("مقدرتش الاقي الـseed بسبب البحث طول معايا... جرب تاني")

            os.remove(f"Temp\\{parse["FileName"]}")

        

bot.run(read_data()["BOT_TOKEN"])
