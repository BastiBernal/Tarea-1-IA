from maze.maze_generators import DFSStrategy
from utils.config import MAZE, START, GOAL, ALGORITHM
from core.shared import SharedState
from core.callback import make_on_step, make_get_grid_func
from core.algorithm_runner import AlgorithmRunner
from views.grid_visualizer import MainWindow
from algorithms.a_star import a_star
from algorithms.iddfs import iddfs
from algorithms.genetic_algorithm import genetic_algorithm as ga
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from PySide6.QtGui import QKeySequence, QShortcut
from maze.maze import Maze
import sys

def main():
    shared_state = SharedState()
    app = QApplication(sys.argv)

    # --------------------------------------------------------------

    maze = Maze(100, 10, 3, DFSStrategy(), crazy_value=0.005, start=(1, 1))

    
    goal_for_algorithm = GOAL[0] if isinstance(GOAL, list) else GOAL
    if maze:
        base_grid = maze.maze
        goal_for_algorithm = maze.getGoal(*maze.start)
        get_grid_func = make_get_grid_func(base_grid, shared_state, maze.start, maze.goals)
    else:
        base_grid = MAZE
        get_grid_func = make_get_grid_func(base_grid, shared_state, START, GOAL)

    # --------------------------------------------------------------

    w = MainWindow(base_grid, get_grid_func)

    # Timer de paredes dinámicas (cambia el laberinto cada X ms)
    walls_timer = QTimer()
    walls_timer.setInterval(5000) # = 10 segundos
    walls_timer.timeout.connect(lambda: maze.mover_paredes())
    walls_timer.start()
    app._walls_timer = walls_timer  # type: ignore[attr-defined]

    algorithms = {
        "A*": a_star,
        "IDDFS": iddfs, 
        "GA": ga
    }

    runner = AlgorithmRunner(
        algorithm_func=algorithms[ALGORITHM],
        get_grid_func=get_grid_func,
        on_step=lambda visited, frontier, path: make_on_step(
            shared_state,
            pause=0.01, # Pausa de 10 ms entre cada paso
            should_stop=lambda: runner.stop_event.is_set()
        )(visited, frontier, path),
        interval=0.05 # Intervalo de 50 ms entre actualizaciones de la interfaz gráfica (20 fps)
    )

    # Atajo para salir de la aplicación
    quit_shortcut = QShortcut(QKeySequence("Esc"), w)
    quit_shortcut.activated.connect(app.quit)

    runner.start(base_grid, START if not maze else maze.start, goal_for_algorithm)
    app.aboutToQuit.connect(runner.stop)
    app.aboutToQuit.connect(walls_timer.stop)

    w.show()
    app.exec()

if __name__ == "__main__":
    main()