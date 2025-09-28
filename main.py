from maze.maze_generators import DFSStrategy
from utils.config import MAZE, START, GOAL, ALGORITHM
from core.shared import SharedState
from core.callback import make_on_step, make_get_grid_func
from core.algorithm_runner import AlgorithmRunner
from views.grid_visualizer import MainWindow
from views.menu_window import MenuWindow
from algorithms.a_star import a_star
from algorithms.iddfs import iddfs
from algorithms.genetic_algorithm import genetic_algorithm as ga
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from PySide6.QtGui import QKeySequence, QShortcut
from maze.maze import Maze
import sys


def run_simulation(
        algorithm,
        walls_n, 
        goals_n, 
        crazy_value=0.005,
        start=(0,0), 
        true_goal=None, 
        population_size=300, 
        generation_n=300, 
        mutation_p=0.80
    ):
    shared_state = SharedState()
    # --------------------------------------------------------------

    maze = Maze(100, walls_n, goals_n, DFSStrategy(), crazy_value=crazy_value , start=(1, 1))
    goal_for_algorithm = GOAL[0] if isinstance(GOAL, list) else GOAL

    if maze:
        base_grid = maze.maze
        goal_for_algorithm = maze.getGoal(*maze.start)
        get_grid_func = make_get_grid_func(base_grid, shared_state, maze.start, maze.goals)
    else:
        base_grid = MAZE
        get_grid_func = make_get_grid_func(base_grid, shared_state, START, GOAL)

    # --------------------------------------------------------------

    w = MainWindow(base_grid, get_grid_func)

    # Timer de paredes dinámicas (cambia el laberinto cada X ms)
    walls_timer = QTimer()
    walls_timer.setInterval(5000) # = 5 segundos
    walls_timer.timeout.connect(lambda: maze.mover_paredes())
    walls_timer.start()

    algorithms = {
        "A*": a_star,
        "IDDFS": iddfs, 
        "GA": ga
    }

    runner = AlgorithmRunner(
        algorithm_func=algorithms[algorithm],
        get_grid_func=get_grid_func,
        on_step=lambda visited, frontier, path: make_on_step(
            shared_state,
            pause=0.01, # Pausa de 10 ms entre cada paso
            should_stop=lambda: runner.stop_event.is_set()
        )(visited, frontier, path),
        interval=0.05 # Intervalo de 50 ms entre actualizaciones de la interfaz gráfica (20 fps)
    )

    # Connect window close event to stop algorithm and timer
    def on_window_close():
        print("Simulation window closing - stopping algorithm and timer")
        runner.stop()
        walls_timer.stop()
    
    # Override the closeEvent of the window
    original_close_event = w.closeEvent

    def close_event_handler(event):
        on_window_close()
        if original_close_event:
            original_close_event(event)
        else:
            event.accept()
    
    w.closeEvent = close_event_handler
    
    # Start the algorithm
    runner.start(base_grid, START if not maze else maze.start, goal_for_algorithm)

    quit_shortcut = QShortcut(QKeySequence("Esc"), w)
    quit_shortcut.activated.connect(QApplication.instance().quit)

    w.show()

    return w, runner, walls_timer

def main():
    app = QApplication(sys.argv)
    
    # Create and show menu window
    menu = MenuWindow()
    
    # Store references to simulation components
    simulation_window = None
    runner = None
    walls_timer = None
    
    # Function to start simulation from menu
    def start_simulation():
        nonlocal simulation_window, runner, walls_timer
        
        args = menu.simulation_args
        
        # Close any existing simulation
        if simulation_window:
            simulation_window.close()
        if runner:
            runner.stop()
        if walls_timer:
            walls_timer.stop()
        
        # Start new simulation
        simulation_window, runner, walls_timer = run_simulation(
            args['algorithm'],
            args['wall_n'],
            args['goal_n'],
            args['population_size'],
            args['generation_n'],
            args['individual_mutation_p']
        )

    quit_shortcut = QShortcut(QKeySequence("Esc"), menu)
    quit_shortcut.activated.connect(app.quit)
    
    # Connect the menu to start simulation
    menu.start_simulation = start_simulation
    
    menu.show()
    
    # Clean up on exit
    def cleanup():
        if runner:
            runner.stop()
        if walls_timer:
            walls_timer.stop()
    
    app.aboutToQuit.connect(cleanup)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()