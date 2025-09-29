import numpy as np
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QSlider, QFrame, QHBoxLayout
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer, Slot, Qt, Signal
from PySide6.QtGui import QImage
from views.dead_screen import DeadScreen

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
    7: agente actual
    8: aventurero
    """
    color_map = np.array([
        [255, 255, 255],
        [0, 0, 0],
        [0, 255, 200],
        [80, 200, 210],
        [255, 170, 50],
        [35, 255, 0],
        [18, 110, 130],
        [255, 0, 0],
        [200, 100, 0]  
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
    trigger_dead = Signal()
    def __init__(self, maze, get_grid_func):
        super().__init__()
        self.setWindowTitle("Laberinto")
        # Contenido principal
        self.maze_widget = MazeWidget(maze)
        self.maze_widget.setMinimumSize(600, 400)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(self.maze_widget)

        # Overlay simple como hijo del MainWindow
        self._dead_screen_widget = DeadScreen(self)
        self._dead_screen_widget.hide()
        self._dead_screen_widget.setGeometry(self.rect())

        self.get_grid_func = get_grid_func

        self.trigger_dead.connect(self.show_dead_screen)

        # Temporizador de refresco visual
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_view)
        self.refresh_timer.start(50)  # 20 fps

    @Slot()
    def show_dead_screen(self) -> None:
        """Muestra la pantalla de muerte cubriendo el laberinto en esta misma ventana."""
        self._dead_screen_widget.setGeometry(self.rect())
        self._dead_screen_widget.show()
        self._dead_screen_widget.raise_()

    def hide_dead_screen(self) -> None:
        """Vuelve a mostrar el laberinto (oculta la pantalla de muerte)."""
        self._dead_screen_widget.hide()

    def refresh_view(self):
        """
        Actualiza la vista del laberinto.
        """
        self.maze_widget.set_grid(self.get_grid_func())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._dead_screen_widget and self._dead_screen_widget.isVisible():
            self._dead_screen_widget.setGeometry(self.rect())

