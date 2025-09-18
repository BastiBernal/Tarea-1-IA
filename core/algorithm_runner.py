import threading

class AlgorithmRunner:
    """
    Clase para ejecutar un algoritmo de búsqueda en un hilo separado, permitiendo que la interfaz gráfica
    no haga que el algoritmo se congele. Proporciona métodos para iniciar y detener la ejecución del algoritmo.
    """
    def __init__(self, algorithm_func, get_grid_func, on_step, interval=0.01):
        self.algorithm_func = algorithm_func
        self.get_grid_func = get_grid_func
        self.on_step = on_step
        self.interval = interval
        self.thread = None
        self.stop_event = threading.Event()

    def start(self, *args, **kwargs):
        """
        Inicia la ejecución del algoritmo en un hilo separado.
        """
        if self.thread and self.thread.is_alive():
            return

        self.stop_event.clear()
        self.thread = threading.Thread(target=self.run_algorithm, args=args, kwargs=kwargs, daemon=True)
        self.thread.start()

    def stop(self, timeout: float = 0.5):
        """
        Detiene la ejecución del algoritmo.
        """
        self.stop_event.set()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=timeout)

    def run_algorithm(self, *args, **kwargs):
        """
        Ejecuta el algoritmo de búsqueda.
        """
        try:
            self.algorithm_func(*args, on_step=self.on_step, should_stop=self.stop_event.is_set, **kwargs)
        except TypeError:
            self.algorithm_func(*args, on_step=self.on_step, **kwargs)