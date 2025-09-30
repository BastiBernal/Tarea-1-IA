from algorithms.node import Node
from utils.utils import reconstruct_path
from utils.utils import valid_move

def depth_limited_search(maze, current_node, goal_node, depth, visited, on_step=None, path=None, should_stop=None):
    """
    Versión iterativa de DFS con límite de profundidad usando una pila explícita.
    Args:
        maze (np.array): La cuadrícula del laberinto.
        current_node (Node): El nodo actual en la búsqueda.
        goal_node (Node): El nodo objetivo.
        depth (int): La profundidad límite para la búsqueda.
        visited (set): Conjunto de posiciones ya visitadas (por camino actual).
        on_step (func, optional): Callback por paso.
        path (list, optional): Camino acumulado para visualización.
        should_stop (func, optional): Señal de cancelación.
    """
    if should_stop and should_stop():
        return None
    if path is None:
        path = []
    # Pila de marcos: (node, depth_remaining, iterator_de_vecinos)
    stack = []
    # Inicializar con el nodo inicial
    path.append(current_node.position)
    visited.add(current_node.position)
    if on_step:
        on_step(visited.copy(), set(), path.copy())
    if current_node == goal_node:
        return reconstruct_path(current_node)
    if depth <= 0:
        # retroceder
        visited.remove(current_node.position)
        path.pop()
        return None
    stack.append((current_node, depth, iter(valid_move(maze, current_node.position))))
    while stack:
        if should_stop and should_stop():
            return None
        node, d_left, neighbors = stack[-1]
        try:
            move = next(neighbors)
        except StopIteration:
            # backtrack
            stack.pop()
            visited.remove(node.position)
            path.pop()
            continue
        if move in visited:
            continue
        neighbor = Node(move, node)
        # avanzar
        path.append(neighbor.position)
        visited.add(neighbor.position)
        if on_step:
            on_step(visited.copy(), set(), path.copy())
        if neighbor == goal_node:
            return reconstruct_path(neighbor)
        if d_left - 1 <= 0:
            # no podemos profundizar más; deshacer avance
            visited.remove(neighbor.position)
            path.pop()
            continue
        # apilar siguiente marco con sus vecinos
        stack.append((neighbor, d_left - 1, iter(valid_move(maze, neighbor.position))))

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
    base_grid = getattr(maze, "maze", maze)

    start_node = Node(start)
    goal_node = Node(goal)

    for depth in range(max_depth):
        if should_stop and should_stop():
            return None
        visited = set()
        result = depth_limited_search(base_grid, start_node, goal_node, depth, visited, on_step, should_stop=should_stop)
        if result is not None:
            return result

    return None # No hay camino