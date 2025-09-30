# Medición de tiempo y memoria
import time
import tracemalloc

# Estructuras
from typing import Iterable, List, Tuple, Dict, Any, Optional

# Para manejar rutas y archivos
import os

# Algoritmos
from core.algorithm_factory import make_ga_algorithm
from algorithms.a_star import a_star

# Para el dataframe
import pandas as pd

# Hilo del laberinto
import threading

import copy

# Configuración estática de algoritmos
ALGORITHMS = ("A*", "GA Fast", "GA Optimal")
GA_POPULATION_SIZE = 300
GA_GENERATION_N = 300
GA_INDIVIDUAL_MUTATION_P = 0.80
#OPTIMIZE = False

# Columnas del dataset de resultados
FIELDNAMES = [
    "algorithm",
    "maze_size",
    "walls",
    "goals",
    "crazy_value",
    "time_ms",
    "peak_memory_kb",
    "solution_length",
    "timeout_reached",
    "run",
]


class ExperimentApp:

    def __init__(self, *,
        mazes: Iterable[Any],
        runs_per_maze: int = 1,
        output_csv: str = "experiments/results.csv",
        max_time_s: Optional[float] = None,
        wall_movement: Optional[bool] = False,
        movement_interval_ms: int = 5,
    ) -> None:
        self.mazes = list(mazes)
        self.start_selector = self._default_start_selector
        self.goal_selector = self._default_goal_selector
        self.runs_per_maze = runs_per_maze
        self.output_csv = os.path.join(os.getcwd(), output_csv)
        self.max_time_s = max_time_s
        self.wall_movement = wall_movement
        self.movement_interval_ms = int(movement_interval_ms)
        self.df: pd.DataFrame = pd.DataFrame(columns=FIELDNAMES)

    @staticmethod
    def _default_start_selector(maze: Any) -> Tuple[int, int]:
        if hasattr(maze, "start") and isinstance(getattr(maze, "start"), tuple):
            return getattr(maze, "start")
        return (0, 0)

    @staticmethod
    def _default_goal_selector(maze: Any, start: Tuple[int, int]) -> Tuple[int, int]:
        if hasattr(maze, "getGoal") and callable(getattr(maze, "getGoal")):
            try:
                goal = maze.getGoal(start[0], start[1])
                if isinstance(goal, tuple):
                    return goal
            except Exception:
                pass
        if hasattr(maze, "shape"):
            return (maze.shape[0] - 1, maze.shape[1] - 1)
        return start

    def _build_ga(self):
        return make_ga_algorithm(
            population_size=GA_POPULATION_SIZE,
            generation_n=GA_GENERATION_N,
            individual_mutation_p=GA_INDIVIDUAL_MUTATION_P,
            experimental = True
        )

    def _run_single(self, *, maze: Any, algorithm: str) -> Dict[str, Any]:
        # Obtener start y goal desde el selector provisto
        #maze = maze if hasattr(maze, "shape") else getattr(maze, "maze", maze)
        start = self.start_selector(maze)
        goal = self.goal_selector(maze, start)
        goals = len(maze.goals)

        dyn_stop: Optional[threading.Event] = None
        dyn_thread: Optional[threading.Thread] = None
        if self.wall_movement and hasattr(maze, "mover_paredes") and callable(getattr(maze, "mover_paredes")):
            dyn_stop = threading.Event()

            def _mutator_loop():
                interval = max(0.0, float(self.movement_interval_ms) / 1000.0)
                next_t = time.perf_counter() + interval
                while not dyn_stop.is_set():
                    now = time.perf_counter()
                    sleep_s = max(0.0, next_t - now)
                    dyn_stop.wait(timeout=sleep_s)
                    if dyn_stop.is_set():
                        break
                    try:
                        maze.mover_paredes()
                    except Exception:
                        pass
                    next_t += interval

            dyn_thread = threading.Thread(target=_mutator_loop, name="MazeMutator", daemon=True)
            dyn_thread.start()

        # Medir tiempo y memoria
        tracemalloc.start()
        # Configurar timeout (opcional)
        if self.max_time_s is not None:
            deadline = time.perf_counter() + self.max_time_s
            def _should_stop() -> bool:
                return time.perf_counter() >= deadline
        else:
            _should_stop = None  # type: ignore

        t0 = time.perf_counter()
        path = []
        try:
            if algorithm == "A*":
                if _should_stop is None and self.wall_movement:
                    path = a_star(maze, start, goal, replan=True)
                elif _should_stop is None:
                    path = a_star(maze, start, goal)
                elif _should_stop is not None and self.wall_movement:
                    path = a_star(maze, start, goal, replan=True, should_stop=_should_stop)
                else:
                    path = a_star(maze, start, goal, None, _should_stop)
            elif algorithm == "GA Fast":
                ga_fn = self._build_ga()
                if _should_stop is None:
                    path = ga_fn(maze, start, goal, False, None, None)
                else:
                    path = ga_fn(maze, start, goal, False, None, _should_stop)
            elif algorithm == "GA Optimal":
                ga_fn = self._build_ga()
                if _should_stop is None:
                    path = ga_fn(maze, start, goal, True, None, None)
                else:
                    path = ga_fn(maze, start, goal, True, None, _should_stop)
            else:
                raise ValueError(f"Algoritmo no soportado en ExperimentApp: {algorithm}. Solo 'A*' y 'GA'.")
        finally:
            if dyn_stop is not None:
                try:
                    dyn_stop.set()
                    if dyn_thread is not None:
                        dyn_thread.join(timeout=1.0)
                except Exception:
                    pass
        t1 = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        solution_length = len(path) if path else -1
        time_ms = (t1 - t0) * 1000.0
        peak_kb = peak / 1024.0

        walls_count = None
        crazy_val = None
        if hasattr(maze, "walls"):
            try:
                walls_count = len(getattr(maze, "walls"))
            except Exception:
                walls_count = None
        if hasattr(maze, "crazy_value"):
            try:
                crazy_val = float(getattr(maze, "crazy_value"))
            except Exception:
                crazy_val = None

        return {
            "algorithm": algorithm,
            "maze_size": int(getattr(maze, "shape", (0, 0))[0]) if hasattr(maze, "shape") else maze.size,
            "walls": walls_count,
            "goals": goals,
            "crazy_value": crazy_val,
            "time_ms": round(time_ms, 3),
            "peak_memory_kb": round(peak_kb, 3),
            "solution_length": solution_length,
            "timeout_reached": self.max_time_s is not None and (t1 - t0) >= self.max_time_s,
        }

    def run_experiments(self) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []

        for maze in self.mazes:
            for algo in ALGORITHMS:
                for run_idx in range(self.runs_per_maze):
                    maze_copy = copy.deepcopy(maze)
                    row = self._run_single(maze=maze_copy, algorithm=algo)
                    row["algorithm"] = algo
                    row["run"] = run_idx
                    results.append(row)

        # Construir y guardar DataFrame
        self.df = pd.DataFrame(results)
        for col in FIELDNAMES:
            if col not in self.df.columns:
                self.df[col] = None
        self.df = self.df[FIELDNAMES]
        self._write_csv(self.df)
        print(f"Resultados escritos en {self.output_csv}")
        return results

    def _write_csv(self, rows: Any) -> None:
        if rows is None:
            return
        if isinstance(rows, pd.DataFrame):
            df = rows
        else:
            df = pd.DataFrame(rows)
        if df.empty:
            return
        for col in FIELDNAMES:
            if col not in df.columns:
                df[col] = None
        df = df[FIELDNAMES]
        out_dir = os.path.dirname(self.output_csv)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        df.to_csv(self.output_csv, index=False, encoding="utf-8")

    def get_results_df(self) -> pd.DataFrame:
        return self.df.copy()