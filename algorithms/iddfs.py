from algorithms.node import Node
from utils.utils import reconstruct_path
from utils.utils import valid_move

def depth_limited_search(maze, current_node, goal_node, depth, visited, on_step=None, path=None, should_stop=None):
    """
    Realiza una búsqueda en profundidad limitada en el laberinto.
    Args:
        maze (np.array): La cuadrícula del laberinto.
        current_node (Node): El nodo actual en la búsqueda.
        goal_node (Node): El nodo objetivo.
        depth (int): La profundidad límite para la búsqueda.
        visited (set): Conjunto de posiciones ya visitadas.
        on_step (func, optional): Función de callback para cada paso.
        path (list, optional): Camino actual desde el inicio hasta el nodo actual.
        should_stop (func, optional): Función que indica si se debe detener la búsqueda.
    """
    if should_stop and should_stop():
        return None
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
        if should_stop and should_stop():
            return None
        if move not in visited:
            neighbor = Node(move, current_node)
            result = depth_limited_search(maze, neighbor, goal_node, depth - 1, visited, on_step, path, should_stop)
            if result is not None:
                return result

    visited.remove(current_node.position)
    path.pop()
    return None

def iddfs(maze, start, goal, max_depth=50, on_step=None, should_stop=None):
    """
    Realiza una búsqueda en profundidad iterativa en el laberinto.
    Args:
        maze (np.array): La cuadrícula del laberinto.
        start (tuple): La posición de inicio.
        goal (tuple): La posición objetivo.
        max_depth (int, optional): La profundidad máxima de búsqueda.
        on_step (func, optional): Función de callback para cada paso.
        should_stop (func, optional): Función que indica si se debe detener la búsqueda.
    """
    start_node = Node(start)
    goal_node = Node(goal)

    for depth in range(max_depth):
        if should_stop and should_stop():
            return None
        visited = set()
        result = depth_limited_search(maze, start_node, goal_node, depth, visited, on_step, should_stop=should_stop)
        if result is not None:
            return result

    return None # No hay camino