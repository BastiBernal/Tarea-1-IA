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

# Configuración estática de algoritmos
ALGORITHMS = ("A*", "GA")
GA_POPULATION_SIZE = 300
GA_GENERATION_N = 300
GA_INDIVIDUAL_MUTATION_P = 0.80
OPTIMIZE = True

# Columnas del dataset de resultados
FIELDNAMES = [
    "algorithm",
    "maze_size",
    "walls",
    "crazy_value",
    "time_ms",
    "peak_memory_kb",
    "solution_length",
    "run",
    "timeout_reached",
]


class ExperimentApp:

    def __init__(self, *,
        mazes: Iterable[Any],
        runs_per_maze: int = 1,
        output_csv: str = "experiments/results.csv",
        max_time_s: Optional[float] = None,
    ) -> None:
        self.mazes = list(mazes)
        self.start_selector = self._default_start_selector
        self.goal_selector = self._default_goal_selector
        self.runs_per_maze = runs_per_maze
        self.output_csv = os.path.join(os.getcwd(), output_csv)
        self.max_time_s = max_time_s
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
            optimize=OPTIMIZE
        )

    def _run_single(self, *, maze: Any, algorithm: str) -> Dict[str, Any]:
        # Obtener start y goal desde el selector provisto
        base_grid = maze if hasattr(maze, "shape") else getattr(maze, "maze", maze)
        start = self.start_selector(maze)
        goal = self.goal_selector(maze, start)

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
        if algorithm == "A*":
            if _should_stop is None:
                path = a_star(base_grid, start, goal)
            else:
                path = a_star(base_grid, start, goal, None, _should_stop)
        elif algorithm == "GA":
            ga_fn = self._build_ga()
            if _should_stop is None:
                path = ga_fn(base_grid, start, goal, None, None)
            else:
                path = ga_fn(base_grid, start, goal, None, _should_stop)
        else:
            raise ValueError(f"Algoritmo no soportado en ExperimentApp: {algorithm}. Solo 'A*' y 'GA'.")
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
            "maze_size": int(getattr(base_grid, "shape", (0, 0))[0]) if hasattr(base_grid, "shape") else None,
            "walls": walls_count,
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
                    row = self._run_single(maze=maze, algorithm=algo)
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