from math import ceil
from random import randint, random, choice
from numpy import sqrt, hypot
import sys 
'''
Crear arreglos de listas aleatorios que representen los caminos a tomar 
'''

def is_valid(maze, srt_point, dst_point):

    rows = len(maze)
    cols = len(maze[0])
    r2, c2 = dst_point

    # Ver que el pto 2 este dentro de la grilla
    if not (0 <= r2 < rows and 0 <= c2 < cols):
        return False
    
    # Chequear si dst_point es pared
    if maze[r2][c2] == 1:
        return False
    
    # Chequear que sean ptos adyacentes
    dr = abs(dst_point[0] - srt_point[0])
    dc = abs(dst_point[1] - srt_point[1])

    if dr + dc != 1:
        return False
    
    return True

    
def create_path(population, maze, start) -> None:
    """
    Creates a path based on the direction bit, and assigns
    the values of parameters i.e., invalid steps, path length
    and number of turns to that genotype based on that path.
    """

    for individual in population:

        '''
        Calcular el camino a partir de la secuencia de movimientos.
        '''
        path = [start]
        invalid_count = 0

        row = start[0]
        col = start[1]

        for move in individual.genes:

            if move == 'U':
                col -= 1
            elif move == 'D':
                col += 1
            elif move == 'L':
                row -= 1
            elif move == 'R':
                row += 1
          
            # aumentar la cantidad de pasos invalidos cada vez que cruza una pared
            if not is_valid(maze, path[-1], (row, col)):
                invalid_count += 1

            # añadir punto a camino
            path.append((row, col))


        individual.path = path
        individual.path_length = len(path)
        individual.invalid_steps = invalid_count
           

class Individual:
    
    def __init__(self, genes):
        self.genes = genes           # string de movimientos. 
        self.path = []            # arreglo de coordenadas del camino.
        self.path_length = 0
        self.fitness = 0          # que tan apto es el individuo
        self.invalid_steps = 0    # cant. de veces que atraviesa paredes

    def print_info(self, show_path=False):
        print(f"Genes: {self.genes}")
        print(f"Fitness: {self.fitness}")
        print(f"Invalid steps: {self.invalid_steps}")
        print(f"Path length: {self.path_length}")

        if show_path:
            print(f"Path: {self.path}")


class Genetic_Algorithm:

    def __init__(self, maze, start, goal, population_size=1000, mutation_rate = 1, minimum_fitness=0):
        # info laberinto
        self.maze = maze
        self.columns = len(maze[0])
        self.rows = len(maze)
        self.start = start                                 # posicion de inicio
        self.goal = goal                                   # arreglo de salidas posibles

        # Variables para el algoritmo
        self.population_size = population_size
        self.minimum_fitness = minimum_fitness
        self.population = self.generate_population()
        self.minimum_fitness
        self.mutation_rate = mutation_rate

    def generate_population(self):
        '''
        Generar arreglo de movimientos (genoma) para cada individuo.
        U -> arriba      L -> izquierda
        D -> abajo       R -> derecha
        '''

        population = []
        moves = ['U', 'D', 'R', 'L']
        
        for _ in range(self.population_size):
            
            genes = ""

            # generar genes hasta llegar a la meta
            for _ in range(ceil((self.columns + self.rows)*1.5)):
                genes += choice(moves)
    
            # Movimientos necesarios para llegar a la meta
            v_diff = self.goal[0] - self.start[0]
            h_diff = self.goal[1] - self.start[1]

            # Añadir movimientos faltantes para llegar a la meta
            while genes.count('U') - genes.count('D') < v_diff:
                position = randint(0, len(genes))
                genes = genes[:position] + 'U' + genes[position:]

            while genes.count('U') - genes.count('D') > v_diff:
                position = randint(0, len(genes))
                genes = genes[:position] + 'D' + genes[position:]

            while genes.count('R') - genes.count('L') < h_diff:
                position = randint(0, len(genes))
                genes = genes[:position] + 'R' + genes[position:]

            while genes.count('R') - genes.count('L') > h_diff:
                position = randint(0, len(genes))
                genes = genes[:position] + 'L' + genes[position:]

            # agregar individio a poblacion
            population.append(Individual(genes))

        return population

    def crossover(self):
        '''
        Mezclar los genes de un cuarto de la poblacion con otro cuarto en un punto aleatorio, los mejores individuos. 
        Generan dos decendientes que son asignados a la segunda mitad de la población.
        
        NO SE REAJUSTA PARA QUE LLEGUE A LA META.
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

        moves = ['U', 'D', 'R', 'L']

        for i in range(0, self.population_size, self.mutation_rate):
            genes = self.population[i].genes

            m = randint(0, len(genes) - 1)  
            mutated_gene = choice(moves)

            # Reemplazar movimiento en la posicion m
            genes = genes[:m] + mutated_gene + genes[m+1:]
            self.population[i].genes = genes


    def select_individuals(self):
        '''
        Ordenar poblacion de menor a mayor segun su fitness
        '''
        self.population.sort(key=lambda ind: ind.fitness, reverse=True)

    def fitness_func(self):
        """
        Calcular fitness de individuos con las variables pasos invalidos, largo del camino 
        y distancia a la meta, con los pesos 3, 2 y 2 respectivamente.
        """
    
        wl, wd, wf = 1,2,2    # pesos de las variables

        Smax = max(ind.invalid_steps for ind in self.population)
        Smin = min(ind.invalid_steps for ind in self.population)

        Lmax = max(ind.path_length for ind in self.population) 
        Lmin = min(ind.path_length for ind in self.population)


        for individual in self.population:
            final_row = individual.path[-1][0]
            final_col = individual.path[-1][1]

            # distancia de punto final del camino a la meta.
            d_goal = abs(self.goal[0] - final_row) + abs(self.goal[1] - final_col)
            individual.fitness = 0

            S = individual.invalid_steps
            L = individual.path_length

            # normalizacion inversa de pasos invalidos
            ff = 1 - ((S - Smin) / (Smax - Smin)) if Smax != Smin else 1

            # normalizacion inversa de largo del camino
            fl = 1 - ((L - Lmin) / (Lmax - Lmin)) if Lmax != Lmin else 1
            
            # Mientras menos distancia mejor
            fd = 1 - d_goal / abs(self.columns + self.rows)

            f = ((float)(100 * wf * ff) * ((wl * fl) + (wd * fd))) / (wl + wd)
            individual.fitness = f
        

    def execute_GA(self, cant_generations=3000, on_step=None, should_stop=None):
        
        self.generate_population()

        for i in range(cant_generations):
            create_path(self.population, self.maze, self.start)
            self.fitness_func()
            self.select_individuals()

            if on_step:
                on_step([], [], self.population[0].path.copy())

            if i % 100 == 0:
                sys.stdout.write('\033[F\033[K') 
                print('Generacion', i)
                self.population[0].print_info()
                print ('------------------------------')
                print()
        
            for individual in self.population:
                
                # si un camino llega a la meta sin cruzar ninguna pared, se retorna el camino.
                if individual.invalid_steps == 0 and individual.path[-1] == self.goal:       
                   
                    print(f'\033[92mGeneracion {i}\033[0m')  # Green
                    print('\033[93mIndividuo exitoso:\033[0m')  # Yellow
                    individual.print_info()
                    print('\033[90m------------------------------\033[0m')
                    print()

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

    if path_solution: 
        print('\n\033[92m##########################\033[0m')  # Green
        print('\033[94mCamino encontrado:\033[0m', path_solution)  # Blue
    else: 
        print('\033[91mCamino no encontrado.\033[0m')  # Red

    return path_solution
