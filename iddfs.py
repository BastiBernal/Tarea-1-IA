import numpy as np
from node import Node
from utils import reconstruct_path
from utils import valid_move

def depth_limited_search(maze, current_node, goal_node, depth, visited, on_step=None, path=None):
    if path is None:
        path = []
    path.append(current_node.position)
    if on_step:
        on_step(visited.copy(), set(), path.copy())

    if current_node == goal_node:
        return reconstruct_path(current_node)
    if depth <= 0:
        path.pop()
        return None

    visited.add(current_node.position)

    for move in valid_move(maze, current_node.position):
        if move not in visited:
            neighbor = Node(move, current_node)
            result = depth_limited_search(maze, neighbor, goal_node, depth - 1, visited, on_step, path)
            if result is not None:
                return result

    visited.remove(current_node.position)
    path.pop()
    return None

def iddfs(maze, start, goal, max_depth=50, on_step=None):
    start_node = Node(start)
    goal_node = Node(goal)

    for depth in range(max_depth):
        visited = set()
        result = depth_limited_search(maze, start_node, goal_node, depth, visited, on_step)
        if result is not None:
            return result

    return None