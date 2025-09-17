import numpy as np

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent

    def __eq__(self, other):
        return self.position == other.position

def valid_move(maze, position):
    x, y = position
    rows, cols = maze.shape

    possible_moves = [
        (0, 1), (0, -1),       # Right, Left
        (1, 0), (-1, 0)        # Down, Up
    ]

    return [
        (x + nx, y + ny) for nx, ny in possible_moves
        if 0 <= x + nx < rows and 0 <= y + ny < cols
        and maze[x + nx, y + ny] != 1
    ]

def reconstruct_path(current_node):
    path = []
    while current_node:
        path.append(current_node.position)
        current_node = current_node.parent
    return path[::-1]

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