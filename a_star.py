import numpy as np
import heapq

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0              # Start to current node cost
        self.h = 0              # Heuristic cost to goal
        self.f = 0              # Total cost

    def __eq__(self, other):
        return self.position == other.position
    
    def __lt__(self, other):
        return self.f < other.f

def manhattan_distance(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

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

def a_star(maze, start, goal):
    start_node = Node(start)
    goal_node = Node(goal)

    open_list = []
    closed_list = set()

    heapq.heappush(open_list, start_node)

    open_list = []
    closed_list = dict()  # clave: posición, valor: costo g

    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)

        # Si ya visitamos este nodo con menor o igual costo, lo ignoramos
        if current_node.position in closed_list and current_node.g >= closed_list[current_node.position]:
            continue
        closed_list[current_node.position] = current_node.g

        if current_node == goal_node:
            return reconstruct_path(current_node)

        for move in valid_move(maze, current_node.position):
            neighbor = Node(move, current_node)
            neighbor.g = current_node.g + 1
            neighbor.h = manhattan_distance(neighbor.position, goal_node.position)
            neighbor.f = neighbor.g + neighbor.h

            # Si ya visitamos este nodo con menor o igual costo, lo ignoramos
            if move in closed_list and neighbor.g >= closed_list[move]:
                continue

            # Si el nodo ya está en open_list con un menor g, lo ignoramos
            skip = False
            for open_node in open_list:
                if neighbor == open_node and neighbor.g >= open_node.g:
                    skip = True
                    break
            if skip:
                continue

            heapq.heappush(open_list, neighbor)

    return []  # No path found

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
    path = a_star(maze, start, goal)
    print("Camino:", path)