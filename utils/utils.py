import numpy as np

def reconstruct_path(current_node):
    """
    Devuelve el camino desde el nodo actual hasta el nodo inicial.
    """
    path = []
    while current_node:
        path.append(current_node.position)
        current_node = current_node.parent
    return path[::-1]

def eliminar_ciclos(secuencia):
    """
    Elimina ciclos de una secuencia de tuplas (x, y) que representan posiciones en una matriz.
    Solo se permiten movimientos arriba, abajo, izquierda y derecha.
    """
    visitados = {}
    resultado = []

    for i, pos in enumerate(secuencia):
        if pos in visitados:
            # Se encontró un ciclo: eliminar desde la última vez que se vio hasta ahora
            inicio_ciclo = visitados[pos]
            resultado = resultado[:inicio_ciclo]
            # Actualizar el diccionario de visitados
            visitados = {p: idx for idx, p in enumerate(resultado)}
        visitados[pos] = len(resultado)
        resultado.append(pos)

    return resultado

def valid_move(maze, position):
    """
    Devuelve una lista de movimientos válidos desde la posición dada en el laberinto.
    """
    x, y = position
    rows, cols = maze.shape

    possible_moves = [
        (0, 1), (0, -1),       # Derecha, Izquierda
        (1, 0), (-1, 0)        # Abajo, Arriba
    ]

    return [
        (x + nx, y + ny) for nx, ny in possible_moves
        if 0 <= x + nx < rows and 0 <= y + ny < cols
        and (maze[x + nx, y + ny] == 0 or maze[x + nx, y + ny] == 5)
    ]

def get_maze(base_maze, visited=None, frontier=None, path=None, start=None, goals=None, agent=None, adventurer=None):
    """
    Devuelve una representación del laberinto con los nodos visitados, frontera y camino resaltados, según aplique.
    """
    # Copia la grilla base para no modificar el original
    grid = np.array(base_maze)
    
    # Marca nodos visitados
    if visited:
        for pos in visited:
            x, y = pos
            if grid[x, y] == 0:
                grid[x, y] = 3

    # Marca frontera
    if frontier:
        for pos in frontier:
            x, y = pos
            if grid[x, y] == 0:
                grid[x, y] = 6

    # Marca camino solución
    if path:
        for pos in path:
            x, y = pos
            if grid[x, y] == 0 or grid[x, y] == 3 or grid[x, y] == 6:
                grid[x, y] = 2

    # Marca inicio y meta
    if start:
        x, y = start
        grid[x, y] = 4
    if goals:
        for goal in goals:
            x, y = goal
            grid[x, y] = 5

    # Marca agente actual
    if agent:
        x, y = agent
        grid[x, y] = 7

    # Marca aventurero
    if adventurer:
        x, y = adventurer
        grid[x, y] = 8

    return grid

def get_test_maze():
    """
    Devuelve un laberinto de prueba.
    """
    return np.array([
        [0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
        [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
        [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0],
        [1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
        [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1],
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
        [1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1],
        [0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0],
        [1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0],
        [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0],
        [1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1],
        [0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
        [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
    ])

def get_test_maze_10x10():
    """
    Devuelve un laberinto de prueba de 10x10.
    """
    return np.array([
        [0, 0, 0, 0, 1, 0, 1, 1, 0, 0],
        [1, 0, 1, 1, 1, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 1, 1],
        [1, 1, 0, 0, 1, 0, 1, 1, 0, 0],
        [1, 1, 1, 0, 1, 0, 1, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
        [1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 1, 1, 1, 5]
    ])

def get_test_maze_5x5():
    """
    Devuelve un laberinto de prueba de 5x5.
    """
    return np.array([
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 0, 5]
    ])

def get_test_maze_15x15():
    """
    Devuelve un laberinto de prueba de 15x15.
    """
    return np.array([
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0],
        [1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0],
        [0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0],
        [1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
        [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
        [1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 5]
    ])