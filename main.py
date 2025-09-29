from core.app import SimulationApp
from experiments.experiment_runner import ExperimentApp
from utils.utils import get_test_maze, get_test_maze_5x5, get_test_maze_10x10
from typing import List
import numpy as np

if __name__ == "__main__":
    option = input("Elija una opción:\n1. Ejecutar Simulación\n2. Ejecutar Experimentos\nIngrese 1 o 2: ")
    if option == '1':
        SimulationApp().run()
    elif option == '2':
        mazes: List[np.ndarray] = [
            get_test_maze_5x5(),
            get_test_maze_10x10(),
            get_test_maze(),
        ]
        app = ExperimentApp(
            mazes=mazes,
            runs_per_maze=5,
            max_time_s=10.0,
        )
        results = app.run_experiments()
        dataframe = app.get_results_df()