class Node:
    """
    Clase que representa un nodo.
    """
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

class AStarNode(Node):
    """
    Clase que representa un nodo específico del algoritmo A*.
    """
    def __init__(self, position, parent=None):
        super().__init__(position, parent)
        self.g = 0  # Coste que va desde el inicio hasta el nodo actual
        self.h = 0  # Coste heurístico hasta el objetivo
        self.f = 0  # Coste total

    def __lt__(self, other):
        return self.f < other.f
