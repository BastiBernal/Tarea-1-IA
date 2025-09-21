from random import randint

from utils import get_test_maze, get_test_maze_10x10, valid_move
'''
Crear arreglos de listas aleatorios que representen los caminos a tomar 
'''

def path1(s, columns) -> list:
    """
    Crea un camino a partir de la lista de filas a visitar.
    Comienza en la misma fila que la entrada y avanza por columnas.
    """
    path = []
    current_row = s[0]
    for col in range(columns):
        target_row = s[col]
        # Move vertically to target_row
        while current_row < target_row:
            path.append((current_row, col))
            current_row += 1
        while current_row > target_row:
            path.append((current_row, col))
            current_row -= 1
        path.append((current_row, col))
    return path

def path2(s, columns) -> list:
    """
    Similar a path1, pero puede tener otra lógica de inicio si lo necesitas.
    """
    path = []
    current_row = s[0]
    for col in range(columns):
        target_row = s[col]
        while current_row < target_row:
            path.append((current_row, col))
            current_row += 1
        while current_row > target_row:
            path.append((current_row, col))
            current_row -= 1
        path.append((current_row, col))
    return path

def is_valid(maze, point_1, point_2):
    rows = len(maze)
    cols = len(maze[0])
    r2, c2 = point_2
    # Check bounds
    if not (0 <= r2 < rows and 0 <= c2 < cols):
        return False
    # Check if destination is not a wall (assuming 1=wall, 0=open)
    if maze[r2][c2] == 1:
        return False
    # Check if move is adjacent (no jumps)
    dr = abs(point_2[0] - point_1[0])
    dc = abs(point_2[1] - point_1[1])

    if dr + dc != 1:
        return False
    return True

    allowed_moves = valid_move(maze, point_1)
    move = (point_2[0] - point_1[0], point_2[1] - point_1[1])

    if move in allowed_moves:
        return True
    else:
        return False
    
def create_path(population, maze, columns) -> None:
    """
    Creates a path based on the direction bit, and assigns
    the values of parameters i.e., invalid steps, path length
    and number of turns to that genotype based on that path.
    """

    for individual in population:
        t = 0
        for k in range(columns - 1):
            if individual.genes[k] != individual.genes[k + 1]:
                t += 1

        individual.num_turns = t

        if individual.direction:
            path = path1(individual.genes, columns)
            count = 0
            for j in range(len(path) - 1):
                if not is_valid(maze, path[j], path[j + 1]):
                    count += 1
            individual.invalid_steps = count
            individual.path_length = len(path)
            individual.path = path
            # Visualize the path
           
        else:
            path = path2(individual.genes, columns)
            count = 0
            for j in range(len(path) - 1):
                if not is_valid(maze, path[j], path[j + 1]):
                    count += 1
            individual.invalid_steps = count
            individual.path_length = len(path)
            individual.path = path
            # Visualize the path


class Individual:
    
    def __init__(self):
        self.genes = []
        self.path = []
        self.path_length = 0
        self.direction = 0        # en que direccion se expande el camino, 0 -> horizontal, 1 -> vertical
        self.fitness = 0          # que tan apto es el individuo
        self.invalid_steps = 0
        self.num_turns = 0

    def print_info(self):
        print(f"Genes: {self.genes}")
        print(f"Direction: {self.direction}")
        print(f"Fitness: {self.fitness}")
        print(f"Invalid steps: {self.invalid_steps}")
        print(f"Path length: {self.path_length}")
        print(f"Num turns: {self.num_turns}")
        print(f"Path: {self.path}")


class Genetic_Algorithm:

    def __init__(self, maze, start, goal, population_size=1000, mutation_rate = 1, minimum_fitness=0):
        # info laberinto
        self.maze = maze
        self.columns = len(maze[0])
        self.rows = len(maze)
        self.start = start                                 # posicion de inicio
        self.goal = goal                                   # arreglo de salidas posibles
        self.trap_goals = []                               # salidas falsas encontradas
        
        # Variables para el algoritmo
        self.population_size = population_size
        self.minimum_fitness = minimum_fitness
        self.population = self.generate_population()
        self.minimum_fitness
        self.mutation_rate = mutation_rate


    def generate_population(self):

        population = []
        for _ in range(self.population_size):
            individual = Individual()
            individual.genes.append(self.start[0])                         # Empezar en el inicio
            for _ in range(self.columns - 2):
                individual.genes.append(randint(0, self.rows - 1))          # Añadir filas aleatorias
        
            individual.genes.append(self.goal[0])                          # Terminar con la ultima fila
            individual.direction = randint(0, 1)               
            population.append(individual)                              # agregar individuo a la poblacion

        return population

    def crossover(self):
        '''
        Mezclar los genes de un cuarto de la poblacion con otro cuarto en un punto aleatorio, los mejores individuos. 
        Generan dos decendientes que son asignados a la segunda mitad de la población.
        '''
        offset = self.population_size // 2

        for i in range(0, offset, 2):
            crossover_pt = randint(1, self.columns - 2)
            self.population[i + offset].genes = (
                self.population[i].genes[:crossover_pt] + self.population[i + 1].genes[crossover_pt:]
            )
            try:
                self.population[i + offset + 1].genes = (
                    self.population[i + 1].genes[:crossover_pt] + self.population[i].genes[crossover_pt:]
                )
            except:
                pass

    def mutation(self):
        ''' 
        Mutar individuo 'mutation_rate' de por medio. 
        Tomar una fila aleatoria y mutarla. Tambien mutar direccion.
        '''
        for i in range(0, self.population_size, self.mutation_rate):
            self.population[i].genes[randint(1, self.columns-2)] = randint(0, self.rows-1)
            self.population[i].direction = randint(0, 1)

    def select_individuals(self):
        '''
        Ordenar poblacion de menor a mayor segun su fitness
        '''
        self.population.sort(key=lambda ind: ind.fitness, reverse=True)

    def fitness_func(self):
        """
        Calcular fitness de individuos con las variables pasos invalidos, largo del camino 
        y numero de vueltas tomadas, con los pesos 2, 2 y 3 respectivamente. Tiene un 
        rango de 0 a 300.
        """
    
        wl, wt, wf = 2,2,3                                                        # pesos de las variables

        Smax = max(ind.invalid_steps for ind in self.population)
        Smin = min(ind.invalid_steps for ind in self.population)

        Lmax = max(ind.path_length for ind in self.population)
        Lmin = min(ind.path_length for ind in self.population)

        Tmax = max(ind.num_turns for ind in self.population)
        Tmin = min(ind.num_turns for ind in self.population)

        for individual in self.population:

            individual.fitness = 0

            S = individual.invalid_steps
            T = individual.num_turns
            L = individual.path_length

            ff = 1 - ((S - Smin) / (Smax - Smin)) if Smax != Smin else 1
            fl = 1 - ((L - Lmin) / (Lmax - Lmin)) if Lmax != Lmin else 1
            ft = 1 - ((T - Tmin) / (Tmax - Tmin)) if Tmax != Tmin else 1

            f = ((float)(100 * wf * ff) * ((wl * fl) + (wt * ft))) / (wl + wt)
            individual.fitness = f
        

    def execute_GA(self, cant_generations=3000, on_step=None, should_stop=None):
        
        self.generate_population()

        for i in range(cant_generations):
            print('Generacion', i)
            create_path(self.population, self.maze, self.columns)
            self.fitness_func()
            self.select_individuals()

            if on_step:
                on_step([], [], self.population[0].path.copy())

            if i % 100 == 0:
                self.population[0].print_info()
        
            for individual in self.population:
                
                # si un camino llega a la meta sin cruzar ninguna pared, se retorna el camino.
                if individual.invalid_steps == 0 and individual.fitness >= self.minimum_fitness:       

                    self.population[0].print_info()
                    if on_step:
                        on_step([], [], individual.path.copy())            
                    return individual.path  


            self.crossover()
            self.mutation()
        
        '''
        si no se encuentra el camino en las generaciones permitidas, 
        se retorna None.
        '''
        return None


def genetic_algorithm(maze, start, goal, on_step=None, should_stop=None):
    ga = Genetic_Algorithm(maze, start, goal, population_size=500)
    path_solution = ga.execute_GA(cant_generations=3000, on_step=on_step)
    return path_solution


if __name__ == "__main__":
    MAZE = get_test_maze_10x10()
    ga = Genetic_Algorithm(MAZE, (0,0), (4,4))
    path = ga.execute_GA()
    if path:
        print('camino encontrado')
    else: 
        print('Camino no encontrado')
