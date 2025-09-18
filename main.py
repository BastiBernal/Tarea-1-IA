from config import MAZE, START, GOAL, ALGORITHM
from shared import SharedState
from callback import make_on_step, make_get_grid_func
from algorithm_runner import AlgorithmRunner
from grid_visualizer import MainWindow
from a_star import a_star
from iddfs import iddfs
from PySide6.QtWidgets import QApplication
import sys

def main():
    shared_state = SharedState()
    app = QApplication(sys.argv)
    get_grid_func = make_get_grid_func(MAZE, shared_state, START, GOAL)
    w = MainWindow(MAZE, get_grid_func)


    algorithm = a_star if ALGORITHM == "a_star" else iddfs

    runner = AlgorithmRunner(
        algorithm_func=algorithm,
        get_grid_func=get_grid_func,
        on_step=None,
        interval=0.05
    )

    runner.on_step = make_on_step(shared_state, pause=0.05, should_stop=runner.stop_event.is_set)
    runner.start(MAZE, START, GOAL)
    app.aboutToQuit.connect(runner.stop)

    w.show()
    app.exec()

if __name__ == "__main__":
    main()