"""Robot class for the Autonomous Robot Navigation project.

Student task:
    Complete move(), search1(), search2(), search3(), and record().

Important:
    search1(), search2(), and search3() are DIFFERENT SEARCH METHODS.
    They are not fixed to Challenge 1, Challenge 2, and Challenge 3.

You may add extra attributes or helper methods if your algorithm needs them.
"""
from BFS import search1 as bfs_search1
from DFS import search2 as dfs_search2
from Dijkstra import search3 as dijkstra_search3

class Robot:
    def __init__(self, position):
        # Teacher code: basic robot state
        self.position = position
        self.path = [position]
        self.score = 0
        self.metrics = {}

    def move(self, direction, cost_map):
        """Move the robot one cell.

        direction:
            "up", "down", "left", or "right"

        cost_map:
            Nested list.
            A number means the cell can be visited.
            None means obstacle.

        Return:
            True if the move is successful.
            False if the move is invalid.
        """

        # TODO:
        # 1. Calculate the new position.
        # 2. Check the map boundary.
        # 3. Check whether the new cell is an obstacle.
        # 4. Update self.position.
        # 5. Add the new position to self.path.

        # Coordinates are (row, column).
        direction_delta = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1),
        }

        # 1. Calculate the new position.
        if direction not in direction_delta:
            return False

        delta_row, delta_col = direction_delta[direction]
        row, col = self.position
        new_row = row + delta_row
        new_col = col + delta_col

        # 2. Check the map boundary.
        if not (0 <= new_row < len(cost_map)):
            return False
        if not (0 <= new_col < len(cost_map[new_row])):
            return False

        # 3. Check whether the new cell is an obstacle.
        if cost_map[new_row][new_col] is None:
            return False

        # 4. Update self.position.
        self.position = (new_row, new_col)

        # 5. Add the new position to self.path.
        self.path.append(self.position)

        return True

    def record(self, name, value):
        """记录性能指标"""
        self.metrics[name] = value

    def search1(self, cost_map, goal):
        """Search Method 1.

        Implement one search algorithm of your choice.

        Example choices:
            Breadth-First Search
            Depth-First Search
            Dijkstra's Algorithm
            A* Search

        You may use this method on any challenge map.
        """

        return bfs_search1(self, cost_map, goal)

    def search2(self, cost_map, goal):
        """Search Method 2.

        Implement a second search algorithm.
        It should be different from search1().
        """

        return dfs_search2(self, cost_map, goal)

    def search3(self, cost_map, goal, bonuses=None):
        """Search Method 3.

        Implement a third search method.

        This method may consider bonus points if your design needs them.
        """

        return dijkstra_search3(self, cost_map, goal, bonuses)
