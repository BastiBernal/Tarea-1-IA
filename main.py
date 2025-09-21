from utils.config import MAZE, START, GOAL, ALGORITHM
from core.shared import SharedState
from core.callback import make_on_step, make_get_grid_func
from core.algorithm_runner import AlgorithmRunner
from views.grid_visualizer import MainWindow
from algorithms.a_star import a_star
from algorithms.iddfs import iddfs
from PySide6.QtWidgets import QApplication
from genetic_algorithm import genetic_algorithm as ga
import sys

def main():
    shared_state = SharedState()
    app = QApplication(sys.argv)
    get_grid_func = make_get_grid_func(MAZE, shared_state, START, GOAL)
    w = MainWindow(MAZE, get_grid_func)

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

    runner.start(MAZE, START, GOAL)
    app.aboutToQuit.connect(runner.stop)

    w.show()
    app.exec()

if __name__ == "__main__":
    main()