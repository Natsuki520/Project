"""Main program.

Teacher code only loads the three provided maps.

Students should write their own:
    - Robot creation
    - Search method calls
    - Performance comparison
    - Result output
    - Visualization
"""

from map_reader import (
    read_txt_map,
    convert_to_cost_map,
    validate_raw_map,
    validate_cost_map,
    get_map_info,
)

import os

# __file__ 是这个 main.py 文件自己的路径。
# os.path.dirname(...) 取出它所在的文件夹，
# 这样无论从哪个目录启动程序，地图路径都以 main.py 的位置为基准，
# 不会再出现"从上级目录运行就找不到 maps/challenge1.txt"的报错。
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# Challenge 1
# ============================================================

challenge1_raw = read_txt_map(os.path.join(BASE_DIR, "maps", "challenge1.txt"))
validate_raw_map(challenge1_raw)

challenge1_map = convert_to_cost_map(challenge1_raw)
validate_cost_map(challenge1_raw, challenge1_map)

challenge1_start, challenge1_goal, challenge1_bonuses = get_map_info(
    challenge1_raw
)


# ============================================================
# Challenge 2
# ============================================================

challenge2_raw = read_txt_map(os.path.join(BASE_DIR, "maps", "challenge2.txt"))
validate_raw_map(challenge2_raw)

challenge2_map = convert_to_cost_map(challenge2_raw)
validate_cost_map(challenge2_raw, challenge2_map)

challenge2_start, challenge2_goal, challenge2_bonuses = get_map_info(
    challenge2_raw
)


# ============================================================
# Challenge 3
# ============================================================

challenge3_raw = read_txt_map(os.path.join(BASE_DIR, "maps", "challenge3.txt"))
validate_raw_map(challenge3_raw)

challenge3_map = convert_to_cost_map(challenge3_raw)
validate_cost_map(challenge3_raw, challenge3_map)

challenge3_start, challenge3_goal, challenge3_bonuses = get_map_info(
    challenge3_raw
)


# ============================================================
# STUDENT WORK
# ============================================================
#
# From here, write your own code.
#
# Example tasks:
#   1. Create Robot objects.
#   2. Run different search methods.
#   3. Compare performance.
#   4. Print or visualize your results.
#

import time

from robot import Robot

# ============================================================
# 算法性能对比：三种算法在三张地图上谁最快
# ============================================================
# 三个指标回答不同的问题：
#   耗时(ms)     真实墙上时间，直观但受机器性能影响，换台电脑就变了
#   搜索格子数   确定性数字，同一张图跑一万次都一样，写报告优先用它
#   路线步数     找出来的路线好不好
#

ROUNDS = 3      # 计时重复 3 轮，取最快的一轮
REPEAT = 10    # 每轮内部把同一个算法连跑 10 次取平均

# 单次搜索只要几十微秒，和计时器精度差不多，只测一次误差太大；
# 连跑取平均能压掉误差，多轮取最小值代表没被打扰时的真实速度

# 三张地图打包成列表，方便循环处理
MAP_LIST = [
    ("Challenge 1", challenge1_map, challenge1_start, challenge1_goal, challenge1_bonuses),
    ("Challenge 2", challenge2_map, challenge2_start, challenge2_goal, challenge2_bonuses),
    ("Challenge 3", challenge3_map, challenge3_start, challenge3_goal, challenge3_bonuses),
]

# 三种算法，以及它们在 Robot 类里对应的方法名
ALGO_LIST = [
    ("BFS", "search1"),
    ("DFS", "search2"),
    ("Dijkstra", "search3"),
]


def pad(text, width):
    """按终端显示宽度补空格，让表格对齐。
    中文占 2 格、英文数字占 1 格，所以不能直接用 len()。"""
    text = str(text)
    display_width = sum(2 if ord(ch) > 127 else 1 for ch in text)
    return text + " " * max(0, width - display_width)


def run_once(method_name, cost_map, start, goal, bonuses):
    """新建一个机器人跑一次指定算法，返回这个机器人。
    每次都要新建：搜索会让机器人真实行走，跑完 position 已经在终点了。"""
    robot = Robot(start)

    if method_name == "search3":
        robot.search3(cost_map, goal, bonuses)   # 只有 search3 收 bonuses 参数
    elif method_name == "search2":
        robot.search2(cost_map, goal)
    else:
        robot.search1(cost_map, goal)

    return robot


def time_method(method_name, cost_map, start, goal, bonuses):
    """测出某个算法在这张图上的单次平均耗时（毫秒），返回 ROUNDS 轮里最快的一轮。"""
    best_ms = None

    for _ in range(ROUNDS):
        clock_start = time.perf_counter()

        for _ in range(REPEAT):
            run_once(method_name, cost_map, start, goal, bonuses)

        clock_end = time.perf_counter()
        avg_ms = (clock_end - clock_start) / REPEAT * 1000

        if best_ms is None or avg_ms < best_ms:
            best_ms = avg_ms

    return best_ms


print("=" * 80)
print("算法性能对比")
print("=" * 80)

summary = {}   # 记录每张图的三个冠军，最后汇总

for map_name, cost_map, start, goal, bonuses in MAP_LIST:
    print()
    print("【%s】 地图 %d x %d   起点 %s   终点 %s   奖励点 %d 个"
          % (map_name, len(cost_map), len(cost_map[0]), start, goal, len(bonuses)))
    print()

    rows = []

    for algo_name, method_name in ALGO_LIST:
        elapsed_ms = time_method(method_name, cost_map, start, goal, bonuses)

        # 计时结束后再单独跑一次，拿到干净的 metrics
        robot = run_once(method_name, cost_map, start, goal, bonuses)
        m = robot.metrics

        # 三个算法统一按作业公式计分：Score = 3 * N_bonus - Distance
        # Distance 按地形成本累加（老师已确认），不是数移动步数
        # N_bonus 从实际走过的路径上数，BFS/DFS 顺路踩到的也算，对比才公平
        bonus_hit = len([p for p in robot.path if p in set(bonuses)])
        steps = len(robot.path) - 1
        distance = sum(c for c in (cost_map[r][c] for r, c in robot.path[1:])
                       if c is not None)
        final_score = 3 * bonus_hit - distance

        rows.append({
            "name": algo_name,
            "ms": elapsed_ms,
            "search_step": m.get("search_step", 0),
            "path_length": m.get("path_length", 0),
            "total_cost": m.get("total_cost", "-"),
            "cost": distance,          # 三个算法统一算出的地形成本，用于计分与排名
            "bonus": bonus_hit,
            "final_score": final_score,
            "reached": robot.position == goal,
        })

    print(pad("算法", 12) + pad("耗时(ms)", 13) + pad("搜索格子", 12)
          + pad("路线步数", 12) + pad("总成本", 10) + pad("奖励点", 9)
          + pad("最终得分", 11) + "到终点")
    print("-" * 80)

    for r in rows:
        print(pad(r["name"], 12)
              + pad("%.4f" % r["ms"], 13)
              + pad(r["search_step"], 12)
              + pad(r["path_length"], 12)
              + pad(r["total_cost"], 10)
              + pad(r["bonus"], 9)
              + pad(r["final_score"], 11)
              + ("是" if r["reached"] else "否"))

    # min(...) 找出列表里某一项最小的那一条记录
    fastest = min(rows, key=lambda r: r["ms"])
    fewest = min(rows, key=lambda r: r["search_step"])
    shortest = min(rows, key=lambda r: r["path_length"])
    # 得分是越大越好，所以这里用 max
    best_score = max(rows, key=lambda r: r["final_score"])

    print()
    print("  跑得最快(耗时)    : %s   %.4f ms" % (fastest["name"], fastest["ms"]))
    print("  检查格子最少      : %s   %d 格" % (fewest["name"], fewest["search_step"]))
    print("  路线最短(步数)    : %s   %d 步" % (shortest["name"], shortest["path_length"]))
    print("  最终得分最高      : %s   %d 分（捡 %d 个奖励点，地形成本 %d）"
          % (best_score["name"], best_score["final_score"],
             best_score["bonus"], best_score["cost"]))

    summary[map_name] = (fastest["name"], fewest["name"],
                         shortest["name"], best_score["name"], best_score["final_score"])


print()
print("=" * 80)
print("汇总")
print("=" * 80)
print()
print(pad("地图", 16) + pad("耗时最快", 14) + pad("检查格子最少", 18)
      + pad("路线最短", 14) + "得分最高")
print("-" * 80)

for map_name in summary:
    t, s, p, b, b_score = summary[map_name]
    print(pad(map_name, 16) + pad(t, 14) + pad(s, 18)
          + pad(p, 14) + "%s (%d分)" % (b, b_score))

try:
       
        import main_for_challenge4
        main_for_challenge4.run()
except FileNotFoundError:
        print("未找到 challenge4 地图文件，跳过该模块")

