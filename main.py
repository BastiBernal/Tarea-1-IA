import threading
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
    
    # Crear un stop event 
    stop_event = threading.Event()

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

    # Conectar la ventana con el algoritmo y timer para pararlos cuando se cierra
    runner.stop_event = stop_event

    def on_window_close():
        print("Simulation window closing - stopping algorithm and timer")
        stop_event.set()  # 
        
        # Asegurar que corra en el hilo principal
        QTimer.singleShot(0, lambda: runner.stop() if hasattr(runner, 'stop') else None)
        QTimer.singleShot(0, lambda: walls_timer.stop())
    
    # Override el evento
    def close_event_handler(event):
        on_window_close()
        event.accept()
    
    w.closeEvent = close_event_handler
    
    # Inciar algoritmo
    runner.start(base_grid, START if not maze else maze.start, goal_for_algorithm)

    quit_shortcut = QShortcut(QKeySequence("Esc"), w)
    quit_shortcut.activated.connect(lambda: (
        stop_event.set(),
        QTimer.singleShot(0, lambda: runner.stop() if hasattr(runner, 'stop') else None),
        QTimer.singleShot(0, lambda: walls_timer.stop()),
        QApplication.instance().quit()
    ))

    w.show()

    return w, runner, walls_timer

def main():
    app = QApplication(sys.argv)
    menu = MenuWindow()
    
    # Guardar referencias a la instancia de simulacion
    simulation_window = None
    runner = None
    walls_timer = None
    

    def start_simulation():
        nonlocal simulation_window, runner, walls_timer
        
        args = menu.simulation_args
        
        # Parar y eliminar la info de la simulacion anterior 
        if simulation_window:
            simulation_window.close()
        if runner and hasattr(runner, 'stop'):
            QTimer.singleShot(0, runner.stop)
        if walls_timer:
            QTimer.singleShot(0, walls_timer.stop)
        
        # Iniciar nueva simulacion
        try:
            simulation_window, runner, walls_timer = run_simulation(
                args['algorithm'],
                args['wall_n'],
                args['goal_n'],
                args['crazy_val'],
                (0, 0),
                None,
                args['population_size'],
                args['generation_n'],
                args['individual_mutation_p']
            )
        except Exception as e:
            print(f"Error starting simulation: {e}")

    quit_shortcut = QShortcut(QKeySequence("Esc"), menu)
    quit_shortcut.activated.connect(app.quit)
    
    # Pasarle la funcion de simulacion a la ventana de menu, para que la corra
    menu.start_simulation = start_simulation
    
    menu.show()
    
    # Funcion para cerrar aplicacion
    def cleanup():
        print('Cerrando aplicacion.')
        if runner and hasattr(runner, 'stop'):
            QTimer.singleShot(0, runner.stop)
        if walls_timer:
            QTimer.singleShot(0, walls_timer.stop)
    
    app.aboutToQuit.connect(cleanup)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()