import cubiomespi
from cubiomespi import Generator, MCVersion, Structure, Dimension
import multiprocessing as mp
import random
import os

# Skill: Multiprocessing Seed Search (use this pattern for HEAVY searches only)
# Use this skill when the search is expensive/rare, for example:
#   - Multiple structures required together (village + stronghold nearby, etc)
#   - Very specific/tight conditions (exact coordinates, small distance threshold)
#   - Any task where a normal single-loop search would likely take too long / timeout
# For simple single-condition searches (one structure near spawn, one biome), do NOT
# use this skill — a plain for-loop is faster to start and simpler.
#
# IMPORTANT: Never hardcode a worker count. Always detect the machine's cores
# automatically with get_max_workers() and leave 1 core free for the system/bot.
# You have to write the seed-checking logic inside `check_seed()`.
# `check_seed()` must return a dict with the result if found, or None if not found.
# to return the seed or anything else, you have to use print(x) and don't forget to add it!

SEEDS_PER_WORKER = 200000  # عدد الـseeds اللي كل عامل هيفحصها


def get_max_workers():
    """
    بيجيب عدد الـcores الحقيقي بتاع الجهاز تلقائيا، وبيسيب واحد فاضي
    للنظام والبوت نفسه. لو الجهاز عنده core أو 2 بس، بيشغل واحد بس عشان
    مايهنجش الجهاز.
    """
    total_cores = os.cpu_count() or 1
    return max(1, total_cores - 1)


def check_seed(seed, version):
    """
    عدّل الفنكشن دي حسب الشرط المطلوب من المستخدم.
    لازم ترجع dict فيه كل المعلومات لو لقيت نتيجة، أو None لو مفيش.
    """
    world = Generator(version, seed, Dimension.DIM_OVERWORLD)

    spawn_x, spawn_z = cubiomespi.get_spawn_pos(world)
    spawn_cx, spawn_cz = spawn_x >> 4, spawn_z >> 4

    village_pos = cubiomespi.get_structure_pos(Structure.Village, world, spawn_cx, spawn_cz)
    if not village_pos:
        return None

    v_x, v_z = village_pos[0] * 16, village_pos[1] * 16
    distance = ((spawn_x - v_x) ** 2 + (spawn_z - v_z) ** 2) ** 0.5

    if distance <= 150:
        return {
            "seed": seed,
            "spawn": (spawn_x, spawn_z),
            "village": (v_x, v_z),
            "distance": round(distance, 2),
        }
    return None


def worker(version, seed_start, seed_end, result_queue, stop_event):
    for seed in range(seed_start, seed_end):
        if stop_event.is_set():
            return
        result = check_seed(seed, version)
        if result:
            result_queue.put(result)
            stop_event.set()
            return


def parallel_search(version, max_workers=None, seeds_per_worker=SEEDS_PER_WORKER):
    if max_workers is None:
        max_workers = get_max_workers()  # بيتحدد تلقائيا حسب الجهاز
    result_queue = mp.Queue()
    stop_event = mp.Event()
    processes = []

    for i in range(max_workers):
        # كل عامل ياخد نطاق عشوائي مختلف عشان مايكرروش نفس الـseeds
        seed_start = random.randint(1, 2147483647 - seeds_per_worker)
        seed_end = seed_start + seeds_per_worker

        p = mp.Process(target=worker, args=(version, seed_start, seed_end, result_queue, stop_event))
        p.start()
        processes.append(p)

    for p in processes:
        p.join(timeout=60)

    stop_event.set()  # وقف أي عامل لسه شغال
    for p in processes:
        if p.is_alive():
            p.terminate()

    if not result_queue.empty():
        return result_queue.get()
    return None


if __name__ == "__main__":
    version = MCVersion.MC_1_20  # Here you can put the version of minecraft (as user message)

    result = parallel_search(version)

    if result:
        print(f"هذا هو الـseed: {result['seed']}")
        print(f"احداثيات البدايه: {result['spawn'][0]} ~ {result['spawn'][1]}")
        print(f"احداثيات القريه: {result['village'][0]} ~ {result['village'][1]}")
        print(f"المسافه: {result['distance']} بلوك")
    else:
        print("لم يتم العثور على نتيجه مناسبه، جرب زود عدد المحاولات")