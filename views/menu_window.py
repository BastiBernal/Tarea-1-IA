from PySide6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QFrame, QHBoxLayout, QLabel
from .constants import COLORES
from .toolbar import SimulationToolbar
from .screens import MazeSelectionScreen, AlgorithmSelectionScreen, GAParametersScreen, RunSimulationScreen

'''
Clase para dibujar la ventana de seleccion de parametros.
'''

class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()

        # diccionario para argumentos de la simulacion.
        self.simulation_args = { 
            'crazy_val': 0.005,
            'maze_size': 100,
            'algorithm': '',
            'wall_n': 4000,
            'goal_n': 5,
            'population_size': 350,
            'generation_n': 100,
            'individual_mutation_p': 0.80,
            'optimize': True
        }
        def _noop_start():
            pass
        self.start_simulation = _noop_start
        self.stage = 1
        self.setup_window()
        self.setup_callbacks()
        self.create_screens()
        
    def setup_window(self):
        # Inicializar ventana y estilos
        self.setWindowTitle("Laberinto")
        self.setMinimumSize(600, 400)
        self.apply_styling()
        self.setup_layout()
        
    def apply_styling(self):
        """Apply CSS styling to the window"""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #{COLORES.deep_blue};
                color: white;
            }}
            QPushButton {{
                background-color: #{COLORES.dark_blue};
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 12px;
                border-radius: 4px;
                outline: none;
            }}
            QPushButton:hover {{
                background-color: #{COLORES.dark_green};
            }}
            QPushButton:pressed {{
                background-color: #002a4a;
            }}
            QPushButton:focus {{
                outline: none;
                border: none;
            }}
            QLabel {{
                color: white;
            }}
            QSlider {{
                outline: none;
            }}
            QSlider:focus {{
                outline: none;
            }}
        """)
        
    def setup_layout(self):
        """Setup the main layout structure"""
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.toolbar = SimulationToolbar(self.simulation_args)
        self.toolbar.update_toolbar()
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_widget.setLayout(self.content_layout)
        
        self.main_layout.addWidget(self.toolbar)
        self.main_layout.addWidget(self.content_widget)

        button = QPushButton("Iniciar Simulacion")
        button.clicked.connect(lambda: self.change_screen(1))
        self.content_layout.addWidget(button)

        self.setLayout(self.main_layout)
        
    def setup_callbacks(self):
        """Setup callback dictionary for screens"""
        self.callbacks = {
            'change_screen': self.change_screen,
            'save_parameter': self.save_parameter,
            'update_walls': self.update_walls,
            'update_goals': self.update_goals,
            'update_population': self.update_population,
            'update_generations': self.update_generations,
            'update_mutation': self.update_mutation,
            'run_simulation': self.run_simulation,
            'update_crazy_value': self.update_crazy_value
        }
        
    def create_screens(self):
        """Create screen instances"""
        self.maze_screen = MazeSelectionScreen(self.content_layout, self.simulation_args, self.callbacks)
        self.algorithm_screen = AlgorithmSelectionScreen(self.content_layout, self.callbacks)
        self.ga_screen = GAParametersScreen(self.content_layout, self.simulation_args, self.callbacks)
        self.run_screen = RunSimulationScreen(self.content_layout, self.simulation_args, self.callbacks)

    def save_parameter(self, key, val, screen=None):
        if key in ['generation_n', 'goal_n', 'population_size']: 
            val = int(val)
        self.simulation_args[key] = val
        self.toolbar.update_toolbar()
        

    def change_screen(self, screen):
        if screen == None:
            return
        
        self.stage = screen
        self.clear_layout()

        if screen == 0:

            # dibujar el inicio
            button = QPushButton("Iniciar Simulacion")       
            button.clicked.connect(lambda: self.change_screen(1))
            self.content_layout.addWidget(button)

        elif screen == 1:
            self.maze_screen.show()
        elif screen == 2:
            self.algorithm_screen.show()
        elif screen == 3:
            if self.simulation_args['algorithm'] == 'GA':
                self.ga_screen.show()
            else:
                self.run_screen.show()
        elif screen == 4:
            self.run_screen.show()

    def clear_layout(self):
        """Clear current layout"""
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # Update methods
    def update_walls(self, value):
        if hasattr(self.maze_screen, 'walls_label'):
            self.maze_screen.walls_label.setText(f'Número de Muros: {value}')
        self.save_parameter('wall_n', value)

    def update_goals(self, value):
        if hasattr(self.maze_screen, 'goals_label'):
            self.maze_screen.goals_label.setText(f'Número de Metas: {value}')
        self.save_parameter('goal_n', value)

    def update_crazy_value(self, value):
        if hasattr(self.maze_screen, 'crazy_label'):
            self.maze_screen.crazy_label.setText(f'Cantidad de Movimiento de los Muros: {value}')
        self.save_parameter('crazy_val', value / 1000)

    def update_population(self, value):
        if hasattr(self.ga_screen, 'pop_label'):
            self.ga_screen.pop_label.setText(f'Tamaño de la Población: {value}')
        self.save_parameter('population_size', value)

    def update_mutation(self, value):
        if hasattr(self.ga_screen, 'indv_mut_label'):
            self.ga_screen.indv_mut_label.setText(f'Probabilidad de Mutar Individuos: {value / 100}')
        self.save_parameter('individual_mutation_p', value / 100)

    def update_generations(self, value):
        if hasattr(self.ga_screen, 'gen_label'):
            self.ga_screen.gen_label.setText(f'Cantidad de Generaciones: {value}')
        self.save_parameter('generation_n', value)


    def run_simulation(self):
        # Iniciar simulacion
        if callable(self.start_simulation):
            self.start_simulation()
        else:
            print("Error: Simulacion empezada antes de ser configurada.")