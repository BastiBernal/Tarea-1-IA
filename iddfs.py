import numpy as np
from node import Node
from utils import reconstruct_path
from utils import valid_move

def depth_limited_search(maze, current_node, goal_node, depth, visited):
    if current_node == goal_node:
        return reconstruct_path(current_node)
    if depth <= 0:
        return None

    visited.add(current_node.position)

    for move in valid_move(maze, current_node.position):
        if move not in visited:
            neighbor = Node(move, current_node)
            result = depth_limited_search(maze, neighbor, goal_node, depth - 1, visited)
            if result is not None:
                return result

    visited.remove(current_node.position)
    return None

def iddfs(maze, start, goal, max_depth=50):
    start_node = Node(start)
    goal_node = Node(goal)

    for depth in range(max_depth):
        visited = set()
        result = depth_limited_search(maze, start_node, goal_node, depth, visited)
        if result is not None:
            return result

    return None

# Ejemplo de uso
if __name__ == "__main__":
    maze = np.array([
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0]
    ])
    start = (0, 0)
    goal = (4, 4)
    path = iddfs(maze, start, goal)
    print("Camino:", path)