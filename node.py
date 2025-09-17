class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

class AStarNode(Node):
    def __init__(self, position, parent=None):
        super().__init__(position, parent)
        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic cost to goal
        self.f = 0  # Total cost

    def __lt__(self, other):
        return self.f < other.f
