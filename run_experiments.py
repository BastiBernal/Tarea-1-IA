import os
import pandas as pd
from maze.maze import load_maze

if __name__ == "__main__":
    mazes = []

    ruta_principal = "maze/laberintos"

    for carpeta_actual, subcarpetas, archivos in os.walk(ruta_principal):
        for archivo in archivos:
            mazes.append(load_maze(archivo))

    #print(len(mazes))

    data = pd.read_csv("experiments/results.csv")
    print(data)