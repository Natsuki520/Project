import os
from robot import Robot
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
from map_reader import (
    read_txt_map,
    convert_to_cost_map,
    validate_raw_map,
    validate_cost_map,
    get_map_info,
)

rounds = 3
repeat = 100

ALGO_LIST = [
    ("BFS", "search1"),
    ("DFS", "search2"),
    ("Dijkstra", "search3"),
]


def pad(text, width):
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
    """测出某个算法在这张图上的单次平均耗时（毫秒），返回 rounds 轮里最快的一轮。"""
    best_ms = None

    for _ in range(rounds):
        clock_start = time.perf_counter()

        for _ in range(repeat):
            run_once(method_name, cost_map, start, goal, bonuses)

        clock_end = time.perf_counter()
        avg_ms = (clock_end - clock_start) / repeat * 1000

        if best_ms is None or avg_ms < best_ms:
            best_ms = avg_ms

    return best_ms


def run():
    """运行 Challenge 4 性能对比。

    由 main.py 调用。地图缺失时给出提示并返回，不崩溃。
    """
    map_path = os.path.join(BASE_DIR, "maps", "challenge4.txt")
    if not os.path.exists(map_path):
        print("未找到 maps/challenge4.txt，跳过 Challenge 4 对比")
        return

    challenge4_raw = read_txt_map(map_path)
    validate_raw_map(challenge4_raw)

    challenge4_map = convert_to_cost_map(challenge4_raw)
    validate_cost_map(challenge4_raw, challenge4_map)

    challenge4_start, challenge4_goal, challenge4_bonuses = get_map_info(
        challenge4_raw
    )

    MAP_LIST = [
        ("Challenge 4", challenge4_map, challenge4_start, challenge4_goal, challenge4_bonuses),
    ]

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
