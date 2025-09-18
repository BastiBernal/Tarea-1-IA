import numpy as np
import heapq
from node import AStarNode
from utils import reconstruct_path
from utils import valid_move

def manhattan_distance(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

def a_star(maze, start, goal, on_step=None):
    start_node = AStarNode(start)
    goal_node = AStarNode(goal)

    open_list = []
    closed_list = dict()  # clave: posición, valor: costo g

    heapq.heappush(open_list, start_node)

    visited = set()
    frontier = set([start])

    while open_list:
        current_node = heapq.heappop(open_list)
        frontier.discard(current_node.position)
        visited.add(current_node.position)

        # Callback para visualización
        if on_step:
            path_so_far = reconstruct_path(current_node)
            on_step(visited, [n.position for n in open_list], path_so_far)

        # Si ya visitamos este nodo con menor o igual costo, lo ignoramos
        if current_node.position in closed_list and current_node.g >= closed_list[current_node.position]:
            continue
        closed_list[current_node.position] = current_node.g

        if current_node == goal_node:
            return reconstruct_path(current_node)

        for move in valid_move(maze, current_node.position):
            neighbor = AStarNode(move, current_node)
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
            frontier.add(move)

    return []  # No path found