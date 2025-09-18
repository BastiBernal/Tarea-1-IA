import numpy as np
import sys
import threading
from a_star import a_star
from iddfs import iddfs
from interfaz_grilla import MainWindow
from utils import get_test_maze
from algorithm_runner import AlgorithmRunner
from PySide6.QtWidgets import QApplication

def main():

    # Configuración de ejemplo
    maze = get_test_maze()
    start = (0, 0)
    goal = (29, 29)

    # Estado compartido y lock
    shared_state = {
        'visited': set(),
        'frontier': set(),
        'path': [],
        'done': False
    }
    state_lock = threading.Lock()

    def a_star_thread():
        def on_step(visited, frontier, path):
            with state_lock:
                shared_state['visited'] = set(visited)
                shared_state['frontier'] = set(frontier)
                shared_state['path'] = list(path)
            import time; time.sleep(0.1)
        path = a_star(maze, start, goal, on_step=on_step)
        with state_lock:
            shared_state['path'] = path
            shared_state['done'] = True

    def iddfs_thread():
        def on_step(visited, frontier, path):
            with state_lock:
                shared_state['visited'] = set(visited)
                shared_state['frontier'] = set(frontier)
                shared_state['path'] = list(path)
            import time; time.sleep(0.00001)
        path = iddfs(maze, start, goal, max_depth=100, on_step=on_step)
        with state_lock:
            shared_state['path'] = path
            shared_state['done'] = True

    t = threading.Thread(target=iddfs_thread, daemon=True)
    t.start()

    app = QApplication(sys.argv)
    w = MainWindow(maze)

    # Evento para detener el temporizador visual al cerrar la app
    stop_event = threading.Event()

    from utils import get_maze, visual_timer

    def get_grid_for_visual():
        with state_lock:
            return get_maze(
                maze,
                visited=shared_state['visited'],
                frontier=shared_state['frontier'],
                path=shared_state['path'],
                start=start,
                goal=goal
            )

    def update_gui(grid):
        w.maze_widget.set_grid(grid)
    w.update()

    # Hilo del temporizador visual
    visual_thread = threading.Thread(
        target=visual_timer,
        args=(0.05, get_grid_for_visual, update_gui, stop_event),
        daemon=True
    )
    visual_thread.start()

    w.show()
    app.exec()
    stop_event.set()  # Detener el temporizador al cerrar la app

if __name__ == "__main__":
    main()