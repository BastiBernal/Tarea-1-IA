import threading

class SharedState:
    """
    Clase para compartir el estado de la búsqueda entre el algoritmo y la interfaz gráfica.
    Utiliza un bloqueo para asegurar que el acceso a los datos sea seguro en entornos multihilo.
    """
    def __init__(self):
        self.data = {
            'visited': set(),
            'frontier': set(),
            'path': [],
        }
        self.lock = threading.Lock()