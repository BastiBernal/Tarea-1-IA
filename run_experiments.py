import os
import pandas as pd

from experiments.experiment_runner import ExperimentApp
from maze.maze import *

if __name__ == "__main__":
    mazes = []

    ruta_principal = "maze/laberintos"

    for carpeta_actual, subcarpetas, archivos in os.walk(ruta_principal):
        for archivo in archivos:
            mazes.append(load_maze(f'{carpeta_actual}/{archivo}'))
        app = ExperimentApp(mazes=mazes,
                            runs_per_maze=1,
                            max_time_s=40,
                            wall_movement=True,
                            movement_interval_ms=1
                            )
        app.run_experiments()

    print(mazes)
