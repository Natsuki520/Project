"""搜索方法 3：Dijkstra + 奖励点最优取舍

计分公式（作业规定）: Score = 3 * N_bonus - Distance，目标是让 Score 最大。
Distance 的口径已跟老师确认：按地形成本累加（草地2 / 泥地5 / 水域10），
不是数移动次数。所以走一格泥地要扣 5 分，不是一格。

为什么不能全捡：绕路去捡远处的奖励点，多花的成本可能超过 3，那就是净亏。
challenge3 实测：全捡 5 个得 -25 分，只捡 3 个反而得 -9 分（这就是最优解）。

因为选路和计分的口径现在完全一致（都是成本），Dijkstra 求出的最低成本路径
正好就是扣分最少的路径，不需要再单独维护一套步数。

所以分两步：
    1. 从起点、终点、每个奖励点各跑一次全图 Dijkstra，建一张"成本表"，
       查出这些关键点两两之间的最低成本。
    2. 在成本表上挑出值得捡的奖励点和访问顺序。
       不超过 14 个用动态规划求精确最优，超过就退回贪心。

坐标约定: (row, column)，与 map_reader.get_map_info() 保持一致。
"""

import heapq   #最小堆，用来做优先队列

DIRECT = [(-1, 0), (1, 0), (0, -1), (0, 1)]    #方向：上，下，左，右


def _dijkstra_from(cost_map, src, counters):
    """从 src 出发跑一次全图 Dijkstra，返回 (dist, parent)。

    dist[g]    src 到 g 的最低地形成本（= 作业里的 Distance），到不了的格子不在里面
    parent[g]  最优路径上 g 的上一格，src 自己的 parent 是 None

    堆里放 (已花的成本, 格子坐标)，每次弹出成本最小的那个往外扩展。
    存下 parent 后，任意两点间的路径都能直接倒推，不必为每段重新搜索。
    """
    rows = len(cost_map)      #地图的行数
    cols = len(cost_map[0])   #地图的列数

    heap = [(0, src)]         #堆元素是 (到达该格的总成本, 格子坐标)
    dist = {src: 0}           #已知的最低成本表
    parent = {src: None}      #回溯表{当前格子：它的上一格}
    visited = set()           #已确定最优的格子

    while heap:
        curr_cost, node = heapq.heappop(heap)   #先取成本最小的格子
        counters["search_step"] += 1    #计数器+1

        if node in visited:     #过期记录，已被更优路线覆盖
            continue
        visited.add(node)

        row, col = node
        for d_row, d_col in DIRECT:
            next_row = row + d_row
            next_col = col + d_col

            # 1. 边界检查，防止数组越界
            if not (0 <= next_row < rows and 0 <= next_col < cols):
                continue

            # 2. 障碍检查（障碍的 cost 是 None，不能进入）
            step_cost = cost_map[next_row][next_col]
            if step_cost is None:
                continue

            next_pos = (next_row, next_col)
            if next_pos in visited:
                continue

            # 3. 松弛：走这条路成本更低，就更新并重新入堆
            new_cost = curr_cost + step_cost
            if next_pos not in dist or new_cost < dist[next_pos]:
                dist[next_pos] = new_cost
                parent[next_pos] = node
                heapq.heappush(heap, (new_cost, next_pos))

    return dist, parent


def _trace(parent, dst):
    """顺着 parent 表倒推出到 dst 的路径，到不了返回 None"""
    if dst not in parent:
        return None

    path = []   #定义路径，预留空间
    node = dst  #回溯路径探索点

    while node is not None:     #回溯探索循环
        path.append(node)
        node = parent[node]

    path.reverse()    #倒序输出（回溯是从终点到起点，需翻转成起点到终点）
    return path


def _walk(self, cost_map, path):
    """指挥机器人沿 path 真实行走，返回成功移动的步数"""
    move_step = 0

    for next_pos in path[1:]:
        curr_row, curr_col = self.position
        next_row, next_col = next_pos

        #比较行号列号，反推该往哪个方向走
        if next_row == curr_row - 1:
            direction = "up"
        elif next_row == curr_row + 1:
            direction = "down"
        elif next_col == curr_col - 1:
            direction = "left"
        else:
            direction = "right"

        if self.move(direction, cost_map):
            move_step += 1

    return move_step


def _total_cost(cost_map, path):
    """累加一条路径的地形成本（不含起点，起点不需要再走一次）"""
    total = 0
    for row, col in path[1:]:
        cell = cost_map[row][col]
        if cell is not None:
            total += cell
    return total


def _exact_route(start, goal, bonus_list, dist, base_score):
    """奖励点不超过 14 个时，用动态规划求精确最优解。

    dp[mask][i] = 已捡了 mask 这批、最后停在 bonus_list[i] 的最低成本。
    mask 是二进制位图，第 i 位是 1 表示第 i 个奖励点捡过了。
    14 个点共 2^14 = 16384 种组合，穷举得过来；再多就指数爆炸，得改用贪心。
    """
    n = len(bonus_list)
    INF = float("inf")
    size = 1 << n       #2 的 n 次方，即所有组合的总数

    dp = [[INF] * n for _ in range(size)]        #成本表，初始都是无穷大
    parent = [[None] * n for _ in range(size)]   #回溯表，用来倒推访问顺序

    #初始状态：只捡了第 i 个奖励点
    for i in range(n):
        dp[1 << i][i] = dist[start][bonus_list[i]]

    #逐个状态向外扩展
    for mask in range(size):
        for i in range(n):
            if dp[mask][i] == INF or not (mask >> i) & 1:
                continue        #这个状态没算过，或者第 i 个根本不在 mask 里

            curr = dp[mask][i]
            from_i = dist[bonus_list[i]]    #从第 i 个点出发到各处的成本

            for j in range(n):
                if (mask >> j) & 1:        #第 j 个已经捡过了
                    continue
                leg = from_i.get(bonus_list[j])
                if leg is None:           #从 i 到不了 j
                    continue

                nxt = mask | (1 << j)      #把第 j 位标记为已捡
                total = curr + leg
                if total < dp[nxt][j]:
                    dp[nxt][j] = total
                    parent[nxt][j] = i

    #遍历所有组合，挑 Score 最高的那个
    best_score = base_score     #基准：一个都不捡，直冲终点
    best_mask = 0
    best_last = None

    for mask in range(1, size):
        picked = bin(mask).count("1")       #这个组合捡了几个
        for i in range(n):
            if dp[mask][i] == INF:
                continue
            to_goal = dist[bonus_list[i]].get(goal)
            if to_goal is None:
                continue

            score = 3 * picked - (dp[mask][i] + to_goal)    #作业公式，Distance 用成本
            if score > best_score:
                best_score = score
                best_mask = mask
                best_last = i

    if best_last is None:
        return base_score, []       #捡任何一个都亏分，那就直冲终点

    #把最优组合的访问顺序倒推出来
    order = []
    mask, last = best_mask, best_last
    while last is not None:
        order.append(bonus_list[last])
        prev = parent[mask][last]
        mask ^= (1 << last)     #把第 last 位清掉，回到上一个状态
        last = prev
    order.reverse()

    return best_score, order


def _greedy_route(start, goal, bonus_list, dist, base_score):
    """奖励点太多、动态规划算不动时退回贪心。

    做法：每轮挑"插入后多花成本最少"的那个加进路线，每加一个就重算总分，
    并记住分数最高的那一刻，最后返回那个时刻的路线，后面亏分的部分丢掉。

    为什么不能一遇到负收益就停：
        一片扎堆的奖励点，单看每一个都是亏的——比如都在离主路 3 格远的
        另一行，下去再上来多花 6 点成本只值 3 分。但一起捡能摊薄那趟往返：
        第一个亏 3 分，后面每个只多花 1 点成本却净赚 2 分，整体反而大赚。
    """
    curr = start
    remaining = list(bonus_list)    #还没捡的奖励点
    order = []                      #已定的访问顺序
    distance = dist[start][goal]    #当前路线的总成本
    best_score = base_score         #基准：一个都不捡，直冲终点
    best_order = []

    while remaining:
        #从 curr 直接去终点的成本，作为"这一段不绕路"的基准
        base = dist[curr].get(goal)
        if base is None:
            break

        best_pick = None
        best_added = None
        for b in remaining:
            to_b = dist[curr].get(b)
            to_goal = dist[b].get(goal)
            if to_b is None or to_goal is None:
                continue
            added = to_b + to_goal - base    #绕道 b 比直接去终点多花这么多成本
            if best_added is None or added < best_added:
                best_added = added
                best_pick = b

        if best_pick is None:
            break       #剩下的全都到不了，收工

        order.append(best_pick)
        remaining.remove(best_pick)
        distance += best_added
        curr = best_pick

        #每加一个就重新评分，只在分数创新高时才更新最佳路线
        score = 3 * len(order) - distance
        if score > best_score:
            best_score = score
            best_order = list(order)

    return best_score, best_order


def _plan_route(start, goal, bonus_list, dist):
    """规划奖励点的取舍与访问顺序，返回 (score, order)。

    order 是奖励点坐标列表，可能为空；终点到不了时返回 (None, [])。
    """
    base = dist[start].get(goal)
    if base is None:
        return None, []     #终点到不了，整趟任务失败

    #只保留"起点到得了、且从它到得了终点"的奖励点，
    #被墙围死的那种捡了也回不来，直接排除
    usable = [b for b in bonus_list
              if dist[start].get(b) is not None
              and dist.get(b, {}).get(goal) is not None]

    if not usable:
        return -base, []    #没有可捡的，Score 就是负的直线成本

    if len(usable) <= 14:
        return _exact_route(start, goal, usable, dist, -base)     #精确求解
    return _greedy_route(start, goal, usable, dist, -base)        #退回贪心


def search3(self, cost_map, goal, bonuses=None):
    """搜索方法 3：按 Score = 3*N_bonus - Distance 最大化来规划路线。

    bonuses 是奖励点坐标列表，从 get_map_info() 拿到。
    不传或传 None 时就是单纯的最低成本最短路。

    返回:
        找到路径 -> 完整路径 [(row, col), ...]，第一个元素是起点。
        找不到   -> None

    除了返回值，还会改变机器人状态：指挥它沿路径真实行走，
    把最终得分写进 self.score，并把各项指标记进 self.metrics。
    """
    start = self.position   #起始点 ---> robot.py

    #起点和终点本身不会是奖励点，先剔掉以防地图数据异常
    bonus_list = [b for b in (bonuses or []) if b != start and b != goal]

    counters = {"search_step": 0}     #跨多次搜索累计的搜索步数

    #第一步：建成本表
    #关键点 = 起点 + 终点 + 所有奖励点，每个跑一次全图 Dijkstra，
    #就能查出任意两个关键点之间的最低成本。一共只搜 n+2 次。
    dist = {}       #成本表，用来算 Score
    parent = {}     #回溯表，留着第三步倒推路径用
    for key in [start, goal] + bonus_list:
        d, p = _dijkstra_from(cost_map, key, counters)
        dist[key] = d
        parent[key] = p

    #第二步：规划最优顺序
    planned_score, order = _plan_route(start, goal, bonus_list, dist)

    if planned_score is None:
        #终点到不了，任务失败，机器人原地不动
        self.record("search_step", counters["search_step"])
        self.record("move_step", 0)       #记录robot移动步数=0
        self.record("path_length", 0)     #记录路径长度=0
        self.record("total_cost", 0)
        self.record("bonus_collected", 0)
        self.record("final_score", 0)
        return None

    #第三步：按规划的顺序逐段走过去
    #每段路径直接从第一步存的 parent 表倒推，不用重新搜索
    full_path = [start]
    for target in order + [goal]:     #先捡完奖励点，最后去终点
        segment = _trace(parent[self.position], target)
        if segment is None:
            break       #理论上不会发生，成本表已确认可达，留作保险

        _walk(self, cost_map, segment)    #让机器人真正沿路径行走
        #拼接时跳过第一个元素，它就是当前位置，上一段已经记过了
        full_path.extend(segment[1:])

    #第四步：按实际走过的路径计分
    #不直接用 len(order)：某段路可能顺路经过计划外的奖励点，
    #作业规定"访问到就给 3 分"，这种白捡的也要算进去
    bonus_set = set(bonus_list)
    bonus_hit = len({p for p in full_path if p in bonus_set})    #实际踩到几个

    distance = _total_cost(cost_map, full_path)         #Distance = 地形成本累加
    steps = len(full_path) - 1                          #移动步数，另记进指标
    self.score = 3 * bonus_hit - distance               #作业公式

    self.record("search_step", counters["search_step"])
    self.record("move_step", steps)
    self.record("path_length", steps)
    self.record("total_cost", distance)     #这一项现在就是 Distance
    self.record("bonus_collected", bonus_hit)
    self.record("final_score", self.score)

    return full_path
