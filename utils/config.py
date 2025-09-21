<<<<<<< HEAD:config.py
from utils import get_test_maze, get_test_maze_10x10
=======
from utils.utils import get_test_maze
>>>>>>> 4fc6119f0db95b8b9242206e7bd5c995b40d2267:utils/config.py

# Configuración del laberinto de prueba

MAZE = get_test_maze()
START = (0, 0)
GOAL = (MAZE.shape[0] - 1, MAZE.shape[1] - 1)
ALGORITHM = "GA"
# ALGORITHM = "A*"