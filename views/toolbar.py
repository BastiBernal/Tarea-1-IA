from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel
from PySide6.QtCore import Qt

class SimulationToolbar(QFrame):
    def __init__(self, simulation_args):
        super().__init__()
        self.simulation_args = simulation_args
        self.setup_toolbar()
        
    def setup_toolbar(self):
        """Create toolbar with simulation parameters"""
        self.setFrameStyle(QFrame.StyledPanel)
        self.setStyleSheet("""
            QFrame {                  
                background-color: #548691 ;
                border-bottom: 1px solid #c0c0c0;
                padding: 5px;
                min-height: 10px;
                max-height: 20px;
            }
            QLabel {
                font-size: 10px;
                padding: 1px;
                margin: 1px;
                color: #fff;
            }
        """)

        self.setMaximumHeight(30)
        self.setMinimumHeight(30)
        
        self.toolbar_layout = QHBoxLayout()
        self.toolbar_layout.setSpacing(8)
        self.toolbar_layout.setContentsMargins(10, 5, 10, 5)
        
        # Create labels
        self.create_labels()
        self.add_labels_to_layout()
        self.setLayout(self.toolbar_layout)
        
    def create_labels(self):
        """Create all toolbar labels"""
        self.toolbar_algorithm = QLabel("Algoritmo: -")
        self.toolbar_algorithm.setAlignment(Qt.AlignCenter)
        
        self.toolbar_walls = QLabel(f"Muros: {self.simulation_args['wall_n']}")
        self.toolbar_walls.setAlignment(Qt.AlignCenter)
        
        self.toolbar_goals = QLabel(f"Metas: {self.simulation_args['goal_n']}")
        self.toolbar_goals.setAlignment(Qt.AlignCenter)
        
        self.toolbar_population = QLabel(f"Población: {self.simulation_args['population_size']}")
        self.toolbar_population.setAlignment(Qt.AlignCenter)
        
        self.toolbar_generations = QLabel(f"Generaciones: {self.simulation_args['generation_n']}")
        self.toolbar_generations.setAlignment(Qt.AlignCenter)
        
        self.toolbar_mutation = QLabel(f"Mutación: {self.simulation_args['individual_mutation_p']}")
        self.toolbar_mutation.setAlignment(Qt.AlignCenter)
        
    def add_labels_to_layout(self):
        """Add labels and separators to layout"""
        separators = [QLabel("|") for _ in range(5)]
        for sep in separators:
            sep.setAlignment(Qt.AlignCenter)
        
        widgets = [
            self.toolbar_algorithm, separators[0],
            self.toolbar_walls, separators[1],
            self.toolbar_goals, separators[2],
            self.toolbar_population, separators[3],
            self.toolbar_generations, separators[4],
            self.toolbar_mutation
        ]
        
        for widget in widgets:
            self.toolbar_layout.addWidget(widget)
        self.toolbar_layout.addStretch()

    def update_toolbar(self):
        """Update toolbar with current simulation arguments"""
        algorithm_text = self.simulation_args['algorithm'] if self.simulation_args['algorithm'] else '-'
        self.toolbar_algorithm.setText(f"Algoritmo: {algorithm_text}")
        self.toolbar_walls.setText(f"Muros: {self.simulation_args['wall_n']}")
        self.toolbar_goals.setText(f"Metas: {self.simulation_args['goal_n']}")

        if self.simulation_args['algorithm'] == 'GA':
            self.toolbar_population.setText(f"Población: {self.simulation_args['population_size']}")
            self.toolbar_generations.setText(f"Generaciones: {self.simulation_args['generation_n']}")
            self.toolbar_mutation.setText(f"Mutación: {self.simulation_args['individual_mutation_p']:.2f}")
        else: 
            self.toolbar_population.setText("Población: -")
            self.toolbar_generations.setText("Generaciones: -")
            self.toolbar_mutation.setText("Mutación: -")
