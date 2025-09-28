from PySide6.QtWidgets import QLabel, QPushButton, QSlider
from PySide6.QtCore import Qt
from .constants import WALL_N, COLORES

class MazeSelectionScreen:
    def __init__(self, layout, simulation_args, callbacks):
        self.layout = layout
        self.simulation_args = simulation_args
        self.callbacks = callbacks
        
    def show(self):
        self.walls_label = QLabel(f'Número de Muros: {self.simulation_args["wall_n"]}')
        self.layout.addWidget(self.walls_label)

        self.wall_buttons = []
        for wall_count in WALL_N:
            btn = QPushButton(f"{wall_count} muros")
            btn.clicked.connect(lambda checked, count=wall_count: self.callbacks['update_walls'](count))
            self.wall_buttons.append(btn)
            self.layout.addWidget(btn)

        self.goals_label = QLabel(f'Número de Metas: {self.simulation_args["goal_n"]}')
        self.layout.addWidget(self.goals_label)

        self.sld_goals = QSlider(Qt.Horizontal)
        self.sld_goals.setMinimum(1)
        self.sld_goals.setMaximum(100)
        self.sld_goals.setValue(self.simulation_args['goal_n'])
        self.sld_goals.valueChanged.connect(self.callbacks['update_goals'])
        self.layout.addWidget(self.sld_goals)
        
        self.crazy_label = QLabel(f'Cantidad de Movimiento de los Muros: {self.simulation_args["crazy_val"] * 1000}')
        self.layout.addWidget(self.crazy_label)

        self.sld_crazy_val = QSlider(Qt.Horizontal)
        self.sld_crazy_val.setMinimum(0)
        self.sld_crazy_val.setMaximum(10)
        self.sld_crazy_val.setValue(self.simulation_args['crazy_val'])
        self.sld_crazy_val.valueChanged.connect(self.callbacks['update_crazy_value'])
        self.layout.addWidget(self.sld_crazy_val)

        btn_next = QPushButton('Continuar')
        btn_next.clicked.connect(lambda: self.callbacks['change_screen'](2))
        self.layout.addWidget(btn_next)

class AlgorithmSelectionScreen:
    def __init__(self, layout, callbacks):
        self.layout = layout
        self.callbacks = callbacks
        
    def show(self):
        algorithms = [
            ('A*', 'A*'),
            ('Genetic Algorithm', 'GA'),
            ('Iterative Depth DFS', 'IDDFS')
        ]
        
        for name, code in algorithms:
            btn = QPushButton(name)

            if code == 'GA':
                btn.clicked.connect(lambda checked, c=code: (
                    self.callbacks['save_parameter']('algorithm', c),
                    self.callbacks['change_screen'](3)
                ))

            else: 
                btn.clicked.connect(lambda checked, c=code: (
                    self.callbacks['save_parameter']('algorithm', c),
                    self.callbacks['change_screen'](4)
                ))

            self.layout.addWidget(btn)

        btn_back = QPushButton('Volver')
        btn_back.clicked.connect(lambda: self.callbacks['change_screen'](1))
        self.layout.addWidget(btn_back)

class GAParametersScreen:
    def __init__(self, layout, simulation_args, callbacks):
        self.layout = layout
        self.simulation_args = simulation_args
        self.callbacks = callbacks
        
    def show(self):
        # Population size
        self.pop_label = QLabel(f'Tamaño de la Población: {self.simulation_args["population_size"]}')
        self.population = QSlider(Qt.Horizontal)
        self.population.setMaximum(3000)
        self.population.setMinimum(100)
        self.population.setValue(self.simulation_args['population_size'])
        self.population.valueChanged.connect(self.callbacks['update_population'])

        self.layout.addWidget(self.pop_label)
        self.layout.addWidget(self.population)

        # Generations
        self.gen_label = QLabel(f'Cantidad de Generaciones: {self.simulation_args["generation_n"]}')
        self.generations = QSlider(Qt.Horizontal)
        self.generations.setMinimum(0)
        self.generations.setMaximum(3000)
        self.generations.setValue(self.simulation_args['generation_n'])
        self.generations.valueChanged.connect(self.callbacks['update_generations'])

        # Mutation probability
        self.indv_mut_label = QLabel(f'Probabilidad de Mutar Individuos: {self.simulation_args["individual_mutation_p"]}')
        self.indv_mutation = QSlider(Qt.Horizontal)
        self.indv_mutation.setMinimum(0)
        self.indv_mutation.setMaximum(100)
        self.indv_mutation.setValue(int(self.simulation_args['individual_mutation_p'] * 100))
        self.indv_mutation.valueChanged.connect(self.callbacks['update_mutation'])

        self.layout.addWidget(self.indv_mut_label)
        self.layout.addWidget(self.indv_mutation)
        self.layout.addWidget(self.gen_label)
        self.layout.addWidget(self.generations)

        # Navigation buttons
        btn_done = QPushButton('Continuar')
        btn_back = QPushButton('Volver')
        btn_back.clicked.connect(lambda: self.callbacks['change_screen'](2))
        btn_done.clicked.connect(lambda: self.callbacks['change_screen'](4))

        self.layout.addWidget(btn_done)
        self.layout.addWidget(btn_back)

class RunSimulationScreen:
    def __init__(self, layout, simulation_args, callbacks):
        self.layout = layout
        self.simulation_args = simulation_args
        self.callbacks = callbacks
        
    def show(self):
        summary_label = QLabel("Configuración de la Simulación:")
        summary_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        self.layout.addWidget(summary_label)
        
        if self.simulation_args['algorithm'] == 'GA':
            config_text = f"""
            Algoritmo: {self.simulation_args['algorithm']}
            Muros: {self.simulation_args['wall_n']}
            Movimiento Muros: {int(self.simulation_args['crazy_val'] * 1000)}
            Metas: {self.simulation_args['goal_n']}
            Población: {self.simulation_args['population_size']}
            Generaciones: {self.simulation_args['generation_n']}
            Mutación: {self.simulation_args['individual_mutation_p']}
            """
        else:
            config_text = f"""
            Algoritmo: {self.simulation_args['algorithm']}
            Movimiento Muros: {int(self.simulation_args['crazy_val'] * 1000)}
            Muros: {self.simulation_args['wall_n']}
            Metas: {self.simulation_args['goal_n']}
            """
        
        config_label = QLabel(config_text)
        config_label.setStyleSheet("margin: 10px; padding: 10px; background-color: rgba(255,255,255,0.1); border-radius: 5px;")
        self.layout.addWidget(config_label)
        
        btn_run = QPushButton('Ejecutar Simulación')
        btn_run.setStyleSheet(f"""
            QPushButton {{
                background-color: #{COLORES.dark_green};
                font-size: 14px;
                font-weight: bold;
                padding: 12px 24px;
                margin: 20px;
            }}
        """)
        btn_run.clicked.connect(self.callbacks['run_simulation'])
        self.layout.addWidget(btn_run)
        
        btn_back = QPushButton('Volver')

        if self.simulation_args['algorithm'] == 'GA':
            btn_back.clicked.connect(lambda: self.callbacks['change_screen'](3))
        else:
            btn_back.clicked.connect(lambda: self.callbacks['change_screen'](2))
            
        self.layout.addWidget(btn_back)

