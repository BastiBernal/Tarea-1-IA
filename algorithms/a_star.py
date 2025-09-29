import heapq
from algorithms.node import AStarNode
from utils.utils import reconstruct_path
from utils.utils import valid_move

def manhattan_distance(start, goal):
    """
    Por defecto usada en A* para 4 direcciones (arriba, abajo, izquierda, derecha).
    """
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

def a_star(maze, start, goal, on_step=None, should_stop=None, replan: bool = False):
    """
    Implementación del algoritmo A* para encontrar el camino más corto en un laberinto.
    Args:
        maze (np.array): La cuadrícula del laberinto.
        start (tuple): La posición de inicio.
        goal (tuple): La posición objetivo.
        on_step (func, optional): Función de callback para cada paso.
        should_stop (func, optional): Función que indica si se debe detener la búsqueda.
    """
    start_node = AStarNode(start)
    goal_node = AStarNode(goal)

    open_list = []
    closed_list = dict()  # position -> best g
    closed_nodes = dict() # position -> AStarNode
    # Usar un heap para la lista abierta para eficiencia
    heapq.heappush(open_list, start_node)

    visited = set()
    frontier = set([start])

    while open_list:
        if should_stop and should_stop():
            return []
        current_node = heapq.heappop(open_list)
        frontier.discard(current_node.position)
        visited.add(current_node.position)

        # Callback para visualización
        if on_step:
            path_so_far = reconstruct_path(current_node)
            on_step(visited, [n.position for n in open_list], path_so_far)

        # Si ya visitamos este nodo con menor o igual costo, lo ignoramos
        if current_node.position in closed_list and current_node.g >= closed_list[current_node.position]:
            # Intentar replan si se vació la frontera tras descartar
            if replan and not open_list:
                reseeded = False
                for pos, node in sorted(closed_nodes.items(), key=lambda kv: (kv[1].f, kv[1].g)):
                    for move in valid_move(maze, pos):
                        neighbor = AStarNode(move, node)
                        neighbor.g = node.g + 1
                        neighbor.h = manhattan_distance(neighbor.position, goal_node.position)
                        neighbor.f = neighbor.g + neighbor.h

                        if move in closed_list and neighbor.g >= closed_list[move]:
                            continue
                        worse_or_equal = False
                        for open_node in open_list:
                            if neighbor == open_node and neighbor.g >= open_node.g:
                                worse_or_equal = True
                                break
                        if worse_or_equal:
                            continue

                        heapq.heappush(open_list, neighbor)
                        frontier.add(move)
                        reseeded = True

                if on_step and reseeded:
                    on_step(set(closed_list.keys()), [n.position for n in open_list], [])
                if reseeded:
                    continue  # seguir el bucle con la nueva frontera
                else:
                    break     # salir del while -> no hay camino
            continue  # ya estaba peor o igual, pasar al siguiente

        closed_list[current_node.position] = current_node.g
        closed_nodes[current_node.position] = current_node

        # Si llegamos al objetivo, reconstruimos y devolvemos el camino
        if current_node == goal_node:
            return reconstruct_path(current_node)

        for move in valid_move(maze, current_node.position):
            if should_stop and should_stop():
                return []
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

        # Si tras expandir se vació la frontera, intentar replan
        if replan and not open_list:
            reseeded = False
            for pos, node in sorted(closed_nodes.items(), key=lambda kv: (kv[1].f, kv[1].g)):
                for move in valid_move(maze, pos):
                    neighbor = AStarNode(move, node)
                    neighbor.g = node.g + 1
                    neighbor.h = manhattan_distance(neighbor.position, goal_node.position)
                    neighbor.f = neighbor.g + neighbor.h

                    if move in closed_list and neighbor.g >= closed_list[move]:
                        continue

                    worse_or_equal = False
                    for open_node in open_list:
                        if neighbor == open_node and neighbor.g >= open_node.g:
                            worse_or_equal = True
                            break
                    if worse_or_equal:
                        continue

                    heapq.heappush(open_list, neighbor)
                    frontier.add(move)
                    reseeded = True

            if on_step and reseeded:
                on_step(set(closed_list.keys()), [n.position for n in open_list], [])

            if reseeded:
                continue
            else:
                break  # sin opciones, terminar

    return []  # no hay camino