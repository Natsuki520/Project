def search2(self, cost_map, goal):
    """Search Method 2: Depth-First Search (DFS).

    在 cost_map 上从 self.position 搜索到 goal 的一条路径，
    找到后驱动 self.move() 让机器人真正沿路径行走。

    与 BFS 的区别：
        BFS 用队列（先进先出），逐层向外扩展，找到的一定是格子数最少的路径。
        DFS 用栈（后进先出），一条路走到底再回头，
        找到的只是一条可行路径，通常不是最短的。

    坐标约定: (row, column)，与 map_reader.get_map_info() 保持一致。

    返回:
        找到路径 -> 路径列表 [(row, col), ...]，第一个元素是起点。
        找不到   -> None
    """
    #搜索初始化：
    #方向按 (delta_row, delta_col) 表示：上，下，左，右
    direct = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    start = self.position   #起始点 ---> robot.py

    #读取地图边界：
    side_width = len(cost_map)      #地图的行数
    side_long = len(cost_map[0])    #地图的列数

    #最好的情况：起点即为终点：
    if start == goal:
        self.record("search_step", 0)     #记录搜索步数=0
        self.record("move_step", 0)       #记录robot移动步数=0
        self.record("path_length", 0)     #记录路径长度=0
        return [start]    #路径只含起点

    #DFS数据结构初始化：
    stack = [start]    #后进先出，实现"一条路走到底"
    visited = set([start])    #入栈时就标记，避免同一格被重复扩展
    recall_path = {start: None}    #回溯的路径{当前格子：它的上一格}
    found = False   #是否已经找到终点
    search_step = 0     #初始化查找步数

    #main循环，进行搜索：
    while stack:
        dealing_step = stack.pop()  #关键：pop() 取最后一个，与 BFS 的 popleft() 相反
        search_step += 1    #计数器+1

        if dealing_step == goal:  #当处理格子是终点时，循环结束
            found = True
            break

        #遍历邻居节点
        curr_row, curr_col = dealing_step
        #逆序压栈：这样"上"最后入栈、最先被取出，路径方向更直观，结果也可复现
        for d_row, d_col in reversed(direct):
            next_row = curr_row + d_row
            next_col = curr_col + d_col

            # 1. 边界检查，防止数组越界
            if 0 <= next_row < side_width and 0 <= next_col < side_long:
                next_pos = (next_row, next_col)
                # 2. 未访问过，且不是障碍（障碍的 cost 是 None）
                if next_pos not in visited and cost_map[next_row][next_col] is not None:
                    visited.add(next_pos)
                    recall_path[next_pos] = dealing_step
                    stack.append(next_pos)

    # 路径回溯与结果返回
    if not found:
        self.record("search_step", search_step)
        self.record("move_step", 0)
        self.record("path_length", 0)
        return None

    path = []   #定义路径，预留空间
    dl_step = goal  #回溯路径探索点

    while dl_step is not None:  #回溯探索循环
        path.append(dl_step)
        dl_step = recall_path[dl_step]

    path.reverse()    #倒序输出（回溯是从终点到起点，需翻转成起点到终点）

    self.record("search_step", search_step)

    #让机器人真正沿路径行走：
    move_step = 0
    for next_pos in path[1:]:
        curr_row, curr_col = self.position
        next_row, next_col = next_pos

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

    self.record("move_step", move_step)
    self.record("path_length", len(path) - 1)

    return path
