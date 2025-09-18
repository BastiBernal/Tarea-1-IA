from utils import get_maze

def make_on_step(shared_state, pause=0.05, should_stop=None):
    def on_step(visited, frontier, path):
        if should_stop and should_stop():
            return
        with shared_state.lock:
            shared_state.data['visited'] = set(visited)
            shared_state.data['frontier'] = set(frontier)
            shared_state.data['path'] = list(path)
        if should_stop and should_stop():
            return
        if pause and pause > 0:
            import time
            time.sleep(pause)
    return on_step

def make_get_grid_func(maze, shared_state, start, goal):
    def get_grid():
        with shared_state.lock:
            return get_maze(
                maze,
                visited=shared_state.data['visited'],
                frontier=shared_state.data['frontier'],
                path=shared_state.data['path'],
                start=start,
                goal=goal
            )
    return get_grid