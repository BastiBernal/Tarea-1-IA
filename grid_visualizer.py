import numpy as np
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage

def maze_to_image(maze):
    color_map = np.array([
        [255, 255, 255],  # 0: empty space
        [0, 0, 0],        # 1: wall
        [50, 170, 50],    # 2: path in solution
        [80, 200, 210],   # 3: explored
        [255, 0, 0],      # 4: start
        [35, 255, 0],     # 5: goal
        [18, 110, 130]    # 6: frontier
    ], dtype=np.uint8)
    img = color_map[maze]
    return QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format.Format_RGB888).copy()

class MazeWidget(QLabel):
    def __init__(self, grid):
        super().__init__()
        self.grid = grid
        self.update_image()

    def set_grid(self, new_grid):
        self.grid = new_grid
        self.update_image()

    def update_image(self):
        img = maze_to_image(self.grid)
        self.setPixmap(QPixmap.fromImage(img).scaled(self.width(), self.height()))

    def resizeEvent(self, event):
        self.update_image()

class MainWindow(QWidget):
    def __init__(self, maze, get_grid_func):
        super().__init__()
        self.setWindowTitle("Laberinto")
        self.maze_widget = MazeWidget(maze)
        self.maze_widget.setMinimumSize(600, 400)
        layout = QVBoxLayout()
        layout.addWidget(self.maze_widget)
        self.setLayout(layout)

        self.get_grid_func = get_grid_func

        # Temporizador de refresco visual
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_view)
        self.refresh_timer.start(50)

    def refresh_view(self):
        self.maze_widget.set_grid(self.get_grid_func())