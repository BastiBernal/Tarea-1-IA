import os
import pandas as pd

from experiments.experiment_runner import ExperimentApp
from maze.maze import *

if __name__ == "__main__":
    mazes = []

    ruta_principal = "maze/laberintos"

    for carpeta_actual, subcarpetas, archivos in os.walk(ruta_principal):
        if carpeta_actual == ruta_principal:
            continue
        for archivo in archivos:
            mazes.append(load_maze(f'{carpeta_actual}/{archivo}'))
        print(carpeta_actual)
        app = ExperimentApp(mazes=mazes,
                            runs_per_maze=5,
                            output_csv=f"experiments/results/{os.path.basename(os.path.normpath(carpeta_actual))}_experiment.csv",
                            max_time_s=30,
                            wall_movement=True,
                            movement_interval_ms=2
                            )
        app.run_experiments()
        mazes = []


