import threading

class SharedState:
    def __init__(self):
        self.data = {
            'visited': set(),
            'frontier': set(),
            'path': [],
            'done': False
        }
        self.lock = threading.Lock()