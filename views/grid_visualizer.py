import numpy as np
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage

def maze_to_image(maze):
    """
    Convierte una matriz a una imagen usando un código de colores predefinido.
    0: espacio libre
    1: pared
    2: camino de la solución actual
    3: cuadro explorado
    4: inicio
    5: meta
    6: frontera
    """
    color_map = np.array([
        [230, 240, 252],  
        [47, 56, 66],     
        [38, 237, 214],   
        [80, 200, 210],   
        [255, 69, 69],    
        [75, 227, 101],   
        [18, 110, 130]      
    ], dtype=np.uint8)
    img = color_map[maze]
    return QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format.Format_RGB888).copy()

class MazeWidget(QLabel):
    """
    Widget para mostrar el laberinto como una imagen.
    """
    def __init__(self, grid):
        super().__init__()
        self.grid = grid
        self.update_image()

    def set_grid(self, new_grid):
        """
        Actualiza la cuadrícula del widget.
        """
        self.grid = new_grid
        self.update_image()

    def update_image(self):
        """
        Actualiza la imagen mostrada en el widget.
        """
        img = maze_to_image(self.grid)
        self.setPixmap(QPixmap.fromImage(img).scaled(self.width(), self.height()))

    def resizeEvent(self, event):
        """
        Maneja el evento de cambio de tamaño del widget.
        """
        super().resizeEvent(event)
        self.update_image()

class MainWindow(QWidget):
    """
    Ventana principal que contiene el widget del laberinto y maneja la actualización periódica de la vista.
    """
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
        self.refresh_timer.start(50)  # 20 fps

    def refresh_view(self):
        """
        Actualiza la vista del laberinto.
        """
        self.maze_widget.set_grid(self.get_grid_func())