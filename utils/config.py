from utils.utils import get_test_maze, get_test_maze_10x10, get_test_maze_15x15, get_test_maze_5x5

# Configuración del laberinto de prueba

MAZE = get_test_maze_10x10()
START = (0, 0)

GOAL = [(MAZE.shape[0] - 1, MAZE.shape[1] - 1)]
ALGORITHM = "A*"

