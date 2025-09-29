# Para la aplicacion principal y la gestion de la simulacion
import sys
import threading
from PySide6.QtCore import QTimer, QCoreApplication, Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QApplication

# Algoritmos
from core.algorithm_factory import *

# Core
from core.algorithm_runner import AlgorithmRunner
from core.callback import make_get_grid_func, make_on_step
from core.game_runner import GameRunner
from core.shared import SharedState

# Laberinto
from maze.maze import Maze
from maze.maze_generators import DFSStrategy
from maze.player import MazePlayer

# Configuracion por defecto
from utils.config import MAZE, START, GOAL

# Vistas
from views.grid_visualizer import MainWindow
from views.menu_window import MenuWindow
from typing import Callable


class SimulationApp:
    """
    Aplicación principal para la simulación de algoritmos de búsqueda en laberintos.
    Reune la interfaz de usuario, la configuración del laberinto y la ejecución del algoritmo seleccionado.
    Maneja el ciclo de vida de la simulación, incluyendo el inicio, la detención y la limpieza de recursos.
    """

    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.menu = MenuWindow()

        self.simulation_window = None
        self.runner: AlgorithmRunner | None = None
        self.walls_timer: QTimer | None = None

        self.menu.start_simulation = self.start_simulation
        quit_shortcut = QShortcut(QKeySequence("Esc"), self.menu) # Esc para salir
        quit_shortcut.activated.connect(self.app.quit)

        self.app.aboutToQuit.connect(self._cleanup)

    def _cleanup(self) -> None:
        """
        Maneja la limpieza de recursos al cerrar la aplicación.
        """
        print("Cerrando aplicacion.")
        if self.runner and hasattr(self.runner, "stop"):
            QTimer.singleShot(0, self.runner.stop)
        if self.walls_timer:
            QTimer.singleShot(0, self.walls_timer.stop)

    def _choose_algorithm(self, args) -> Callable:
        """
        Elige el algoritmo de búsqueda basado en los argumentos proporcionados.
        """
        algo = args.get("algorithm", "A*")
        if algo == "GA":
            return make_ga_algorithm(
                population_size=int(args.get("population_size", 300)),
                generation_n=int(args.get("generation_n", 300)),
                individual_mutation_p=float(args.get("individual_mutation_p", 0.8)),
            )
        if algo == "IDDFS":
            return make_iddfs_algorithm()
        else:
            return make_a_star_algorithm()

    def _build_simulation(self, args):
        """
        Construye y configura la simulación basada en los parámetros proporcionados.
        Configura el laberinto, el algoritmo, los callbacks y la interfaz de usuario.
        """
        shared_state = SharedState()

        maze = Maze(
            100,
            int(args.get("wall_n", 4500)),
            int(args.get("goal_n", 5)),
            DFSStrategy(),
            crazy_value=float(args.get("crazy_val", 0.005)),
            start=(1, 1),
        )

        # Configurar laberinto y funcion de obtencion de cuadrícula
        goal_for_algorithm = GOAL[0] if isinstance(GOAL, list) else GOAL
        if maze:
            base_grid = maze.maze
            goal_for_algorithm = maze.getGoal(*maze.start)
            get_grid_func = make_get_grid_func(base_grid, shared_state, maze.start, maze.goals)
        else:
            base_grid = MAZE
            get_grid_func = make_get_grid_func(base_grid, shared_state, START, GOAL)

        w = MainWindow(base_grid, get_grid_func)

        algorithm_func = self._choose_algorithm(args)

        stop_event = threading.Event()

        # Configurar y crear el ejecutor del algoritmo
        runner = AlgorithmRunner(
            algorithm_func=algorithm_func,
            get_grid_func=get_grid_func,
            on_step=lambda visited, frontier, path: make_on_step(
                shared_state,
                pause=0.01,
                should_stop=lambda: runner.stop_event.is_set(),
            )(visited, frontier, path),
            interval=0.05,
        )
        runner.stop_event = stop_event

        def on_window_close():
            """
            Maneja el cierre de la ventana de simulación
            """
            stop_event.set()
            QTimer.singleShot(0, lambda: runner.stop() if hasattr(runner, "stop") else None)
            #QTimer.singleShot(0, lambda: walls_timer.stop())

        def close_event_handler(event):
            """
            Maneja el evento de cierre de la ventana.
            """
            on_window_close()
            event.accept()

        w.closeEvent = close_event_handler

        def _show_dead_screen():
            w.trigger_dead.emit()

        def _on_victory():
            print("Victoria alcanzada")

        player = MazePlayer(maze, runner, life_turns=400, on_game_over=_show_dead_screen, on_victory=_on_victory)
        game_runner = GameRunner(player)
        game_runner.start()
        #runner.start(base_grid, START if not maze else maze.start, goal_for_algorithm)

        quit_shortcut = QShortcut(QKeySequence("Esc"), w)
        quit_shortcut.activated.connect(
            lambda: (
                stop_event.set(),
                QTimer.singleShot(0, lambda: runner.stop() if hasattr(runner, "stop") else None),
                #QTimer.singleShot(0, lambda: walls_timer.stop()),
                QCoreApplication.quit(),
            )
        )

        # Atajo para cerrar la pantalla de muerte
        debug_dead = QShortcut(QKeySequence("Ctrl+D"), w)
        debug_dead.activated.connect(lambda: QTimer.singleShot(0, w.hide_dead_screen))

        w.show()
        return w, runner 

    def start_simulation(self) -> None:
        # Cerrar cualquier simulación previa
        if self.simulation_window:
            self.simulation_window.close()
        if self.runner and hasattr(self.runner, "stop"):
            QTimer.singleShot(0, self.runner.stop)
        if self.walls_timer:
            QTimer.singleShot(0, self.walls_timer.stop)

        try:
            self.simulation_window, self.runner  = self._build_simulation(
                self.menu.simulation_args
            )
        except Exception as e:
            print(f"Error iniciando simulación: {e}")

    def run(self) -> None:
        self.menu.show()
        sys.exit(self.app.exec())


def main():
    SimulationApp().run()