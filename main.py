
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


            example_json = json.dumps({"FileName": "VillageInSpawn.py", "SourceCode": example_code1}, ensure_ascii=False)

            developer = client.chat.completions.create(
                model=_developer_model,
                messages=[
                    {"role": "system", "content": f"You're a Developer, and creating python file with cubiomespi lib to help the user find a seed he wants in minecraft: ONLY Json, no extra text because your response goes to json.loads(), no markdown. Skills to learn from:\n{a_codes}"},
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