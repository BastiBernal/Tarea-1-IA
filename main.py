from core.app import SimulationApp
from experiments.experiment_runner import ExperimentApp
from maze.maze import Maze
from maze.maze_generators import DFSStrategy
from typing import List
import numpy as np
import random as rd

if __name__ == "__main__":
    option = input("Elija una opción:\n1. Ejecutar Simulación\n2. Ejecutar Experimentos\nIngrese 1 o 2: ")
    if option == '1':
        SimulationApp().run()
    elif option == '2':
        maze = Maze(
            30,
            int(3),
            int(5),
            DFSStrategy(),
            crazy_value=float(0.0),
            start=(1, 1),
        )
        print(len(maze.goals))
        app = ExperimentApp(
            mazes=[maze],
            runs_per_maze=2,
            max_time_s=10.0,
            wall_movement=False,
            movement_interval_ms=1
        )
        results = app.run_experiments()
        dataframe = app.get_results_df()