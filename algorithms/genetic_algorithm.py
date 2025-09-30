from math import ceil
from random import randint, random, choice
from numpy import exp, sqrt, hypot
import sys

from utils.utils import eliminar_ciclos

'''
Calcula si es que un punto en el laberinto es una interseccion. La meta cuenta como intersección.
'''
def intersection_point(maze, point, goal) -> bool:
    '''
    (0, 1), (0, -1),       # Derecha, Izquierda
    (1, 0), (-1, 0)        # Abajo, Arriba
    
    '''
    # si el punto esta fuera de la grilla, no es punto de interseccion. 
    x, y = point
    if not (0 <= x < maze.shape[0] and 0 <= y < maze.shape[1]):
        return False

    W = maze[x][y - 1] == 1 if y > 0 else True  # Borde izquierdo = pared
    E = maze[x][y + 1] == 1 if y < maze.shape[1] - 1 else True  # Borde derecho = pared
    N = maze[x - 1][y] == 1 if x > 0 else True  # Borde superior = pared
    S = maze[x + 1][y] == 1 if x < maze.shape[0] - 1 else True  # Borde inferior = pared
   
   
    # la meta real es un pto de interseccion; admitir una o varias metas (coordenadas)
    if isinstance(goal, (list, set)):
        if point in goal:
            return True
    elif point == goal:
        return True
    
    # si es un pasillo no es punto de interseccion
    elif (W and E and (not N and not S)) or (N and S and (not E and not W)):
        return False

    # el resto de combinaciones se cuentan como punto de interseccion
    return True


'''
Representa un individuo de la poblacion del algoritmo genetico.
'''

class Individual:
    
    def __init__(self, chromosome):
        self.chromosome = chromosome           # string de movimientos. 
        self.path = []            # arreglo de coordenadas del camino.
        self.path_length = 0
        self.fitness = 0          # que tan apto es el individuo
        self.invalid_steps = 0    # cant. de veces que atraviesa paredes
        self.loops = 0            # cant de veces que pasa por el mismo lugar

    def print_info(self, show_path=False, show_chromosome=False):
        
        print(f"\033[96mFitness:\033[0m {self.fitness:.3f}")
        print(f"\033[96mPasos Invalidos:\033[0m {self.invalid_steps}")
        print(f"\033[96mLargo del Camino:\033[0m {self.path_length}")

        if show_chromosome: 
            print(f"\033[96mCromosoma:\033[0m {self.chromosome}")
        if show_path:
            print(f"\033[91mPath: {self.path}\033[0m")


'''
Clase para encontrar salidas de un laberinto con un algoritmo genetico.
'''
class Genetic_Algorithm:

    def __init__(self, maze, start, goal, population_size=1000, individual_mutation_p=0.80, p_gene_mutation=0.06, minimum_fitness=0):
        # info laberinto
        self.maze = maze
        self.columns = len(maze.maze[0])
        self.rows = len(maze.maze)
        self.start = start                                 # posicion de inicio
        self.goal = goal                                   # arreglo de salidas posibles

        # Variables para el algoritmo
        self.population_size = population_size
        self.minimum_fitness = minimum_fitness
        self.population = self.generate_population()
        self.minimum_fitness = minimum_fitness
        self.individual_mutation_p = individual_mutation_p       # probabilidad de mutar un individuo
        self.p_gene_mutation = p_gene_mutation                   # probabilidad de mutar un gen 

        self.min_path = -1
        self.max_path = -1

        


    def adjust_chromosome(self, chromosome, flexibility_factor=0.3):
        """
        Ajusta genes con más flexibilidad para permitir rodeos y retrocesos.
        """
        # Movimientos necesarios para llegar a la meta
        v_diff = self.goal[0] - self.start[0]
        h_diff = self.goal[1] - self.start[1]
        
        # Permitir movimientos extra para rodeos (factor de flexibilidad)
        min_moves_needed = abs(v_diff) + abs(h_diff)
        extra_moves = int(min_moves_needed * flexibility_factor)
        
        # Contar movimientos actuales
        current_v_net = chromosome.count('U') - chromosome.count('D')
        current_h_net = chromosome.count('R') - chromosome.count('L')
        
        # Solo ajustar si estamos MUY lejos del balance necesario
        v_tolerance = abs(v_diff) + extra_moves
        h_tolerance = abs(h_diff) + extra_moves
        
        # Ajustar movimientos verticales solo si excede la tolerancia
        while current_v_net < v_diff - v_tolerance:
            position = randint(0, len(chromosome))
            chromosome = chromosome[:position] + 'U' + chromosome[position:]
            current_v_net += 1
            
        while current_v_net > v_diff + v_tolerance:
            position = randint(0, len(chromosome))
            chromosome = chromosome[:position] + 'D' + chromosome[position:]
            current_v_net -= 1
        
        # Ajustar movimientos horizontales solo si excede la tolerancia
        while current_h_net < h_diff - h_tolerance:
            position = randint(0, len(chromosome))
            chromosome = chromosome[:position] + 'R' + chromosome[position:]
            current_h_net += 1
            
        while current_h_net > h_diff + h_tolerance:
            position = randint(0, len(chromosome))
            chromosome = chromosome[:position] + 'L' + chromosome[position:]
            current_h_net -= 1

        return chromosome

    '''
    Funcion para generar los individuos de la poblacion con genes aleatorios.
    '''
    def generate_population(self):
        '''
        Generar arreglo de movimientos (genoma) para cada individuo.
        U -> arriba      L -> izquierda
        D -> abajo       R -> derecha
        '''

        population = []
        moves = ['U', 'D', 'R', 'L']

        # Distancia mínima 
        min_distance = sqrt(abs(self.goal[0] - self.start[0]) + abs(self.goal[1] - self.start[1])) * ((self.columns+self.rows)/10)
        
        for i in range(self.population_size):
            # Variar la longitud de los genes según diferentes estrategias
            if i < self.population_size * 0.3:  # 30% rutas cortas
                gene_length = int(min_distance)
            elif i < self.population_size * 0.7:  # 40% rutas medianas
                gene_length = int(min_distance * 1.5)
            else:  # 30% rutas largas (para rodeos complejos)
                gene_length = int(min_distance * 2.0)
            
            chromosome = ""
            for _ in range(gene_length):
                chromosome += choice(moves)

            # Aplicar ajuste flexible
            chromosome = self.adjust_chromosome(chromosome, flexibility_factor=0.4)
            
            population.append(Individual(chromosome))

        return population
    
    '''
    Genera el camino a partir de los genes del individuo. 
    '''
    def create_path(self, individual, maze, start, goal, on_step=None) :

        '''
        Calcular el camino a partir de la secuencia de movimientos.
        '''
        tuple_goal = isinstance(self.goal, (list, set))
        goal_index = None # 


        path    = [self.start] 
        visited = {self.start} 

        invalid_count = 0
        loop_count = 0

        current_pos = self.start      
        # mover agente 
        for move in individual.chromosome:

            # avanzar hasta llegar a una interseccion.
            while(True):

                new_row, new_col = current_pos
                
                if move == 'U':
                    new_row -= 1
                elif move == 'D':
                    new_row += 1
                elif move == 'L':
                    new_col -= 1
                elif move == 'R':
                    new_col += 1
                
                new_pos = (new_row, new_col)

                # Ver que el pto 2 este dentro de la grilla
                if not (0 <= new_row < maze.shape[0] and 0 <= new_col < maze.shape[1]):
                    invalid_count += 1
                    break
                
                # si el siguiente punto no es espacio libre
                if maze[new_row][new_col] != 0 and maze[new_row][new_col] != 5:
                    invalid_count += 1
                    break

                # guardar nueva posicion
                current_pos = new_pos

                # Verificar si es un loop
                if current_pos in visited:
                    loop_count += 1
          
                # añadir punto al camino
                path.append(current_pos)
                visited.add(current_pos)

                # dejar de crear el camino si se encuentra una meta.
                if tuple_goal:
                    if current_pos in self.goal:
                        goal_index = len(path) - 1
                        break
                else:
                    if self.maze.maze[current_pos] == 5:
                        self.goal = current_pos
                        goal_index = len(path) - 1
                        break

                # si llega a una interseccion o esquina pasa al siguiente movimiento
                if intersection_point(maze, new_pos, goal) == True:
                    break
            
            # dejar de crear camino si se llega a meta
            if goal_index:
                break
        
        individual.path = path
        individual.path_length = len(path)
        individual.invalid_steps = invalid_count
        individual.loops = loop_count


        if self.min_path == -1 or individual.path_length < self.min_path:
            self.min_path = individual.path_length
        elif self.max_path == -1  or  individual.path_length > self.max_path:
            self.max_path = individual.path_length

        return goal_index

        

    def verify_goal(self, individual, goal_index, on_step=None, experimental = False, gen = None):
        
        # revisar si algun individuo ha llegado a la meta
        
        # goal_index = None
        # if isinstance(self.goal, (list, set)):
        #     # Primera aparición de cualquier meta
        #     for idx, pos in enumerate(individual.path):
        #         if pos in self.goal:
        #             goal_index = idx
        #             return
        # else:
            
        #     if self.maze.maze[pos] == 5:
        #         self.goal = pos
        #         goal_index = individual.path.index(pos)
        #         return

        if goal_index is not None:
            if not experimental or self.maze.evaluar_meta(individual.path[goal_index]):
                
                print('\033[93mIndividuo exitoso:\033[0m')  # Yellow
                individual.print_info(show_path=False)
                print('\033[90m------------------------------\033[0m')
                print()

                if on_step:
                    try:
                        on_step(set(), set(), individual.path[:goal_index + 1].copy())
                    except Exception as e:
                        print(f"Error in final on_step callback: {e}")

                # Cortar el camino en el punto donde encuentra la meta.
                return eliminar_ciclos(individual.path[:goal_index + 1])
            else:
                print(self.goal)
                self.goal = self.maze.getGoal()
                print(self.goal)

        


    '''
    Funcion para mezclar los genes de un cuarto de la poblacion con otro cuarto en un punto aleatorio, los mejores individuos. 
    Generan dos decendientes que son asignados a la segunda mitad de la población.
    '''
    def crossover(self):
        offset = self.population_size // 2

        for i in range(0, offset, 2):

            parent_1 = self.population[i]
            parent_2 = self.population[i + 1]

            crossover_pt = randint(0, min(parent_1.path_length, parent_2.path_length) - 1)

            chromosome_1 = (
                parent_1.chromosome[:crossover_pt] + parent_2.chromosome[crossover_pt:]
            )

            # mutar cromosoma calculado
            self.population[i + offset].chromosome = self.mutation(chromosome_1) 


            # usar un try en caso de que los genes no sean multiplos de 4.
            try:
                chromosome_2 = (
                    parent_2.chromosome[:crossover_pt] + parent_1.chromosome[crossover_pt:]
                )

                self.population[i + offset + 1].chromosome = self.mutation(chromosome_2) 

            except:
                pass
                
            # mutar a los padres e hijos excluyendo el mejor 5%

            if i >= self.population_size * 0.05:
                parent_1.chromosome = self.mutation(parent_1.chromosome)
                parent_2.chromosome = self.mutation(parent_2.chromosome)

    ''' 
    Funcion para mutar individuo con cierta probabilidad. 
    '''
    def mutation(self, chromosome) -> str:

        moves = ['U', 'D', 'R', 'L']

        # individual_mutation_p  -> probabilidad de mutacion del individuo
        # p_gene_mutation -> probabilidad de mutacion de cada gen
        
        chrom = chromosome  
        if random() <= self.individual_mutation_p:
            
            for m in range(len(chromosome)):
                if random() <= self.p_gene_mutation: 
                    # Reemplazar movimiento en la posicion m
                    chrom = chrom[:m] + choice(moves) + chrom[m+1:]

        return chrom

    """
    Función para calcular que tan bien adaptado esta el individuo.
    """
    def fitness_func(self):
       
        # Pesos
        w_is = 0.38      # Penalización por pasos inválidos
        w_d = 0.35      # Distancia a la meta (reducido)
        w_l = -0.15       # Longitud del camino
        w_prog = 0.15   # Progreso máximo alcanzado 
        w_loop = 0.4    # Progreso máximo alcanzado 
       
        # Distancia Manhattan total posible
        d_tot = abs(self.goal[0] - self.start[0]) + abs(self.goal[1] - self.start[1])

        # Obtener rangos para normalización 
        path_lengths = [ind.path_length for ind in self.population]

        Lmax = self.max_path
        Lmin = self.min_path

        for ind in self.population:
            final_pos = ind.path[-1]
            d_goal = abs(self.goal[0] - final_pos[0]) + abs(self.goal[1] - final_pos[1]) # manhattan distance
            d_goal = sqrt((self.goal[0] - final_pos[0])**2 + abs(self.goal[1] - final_pos[1])**2) # euclidian distance
            
            # Cantidad de pasos inválidos (penalización exponencial suavizada)
            f_is = 1.0 / (1.0 + ind.invalid_steps)  

            # Cantidad de loops (penalización exponencial)
            f_loop = 1.0 / (1.0 + ind.loops)  
            
            # Distancia a la meta (más crítico cerca de la meta)
            if d_goal == 0:  # Ha llegado a la meta
                f_d = 1.0
            else:
                # Penalización exponencial para distancias grandes
                f_d = exp(-d_goal / max(d_tot, 1))
            
            # Longitud del camino (normalización mejorada)
            if Lmax > Lmin:
                f_l = 1.0 - ((ind.path_length - Lmin) / (Lmax - Lmin))
            else:
                f_l = 1.0

            # Progreso máximo alcanzado durante el recorrido
            best_distance_in_path = min(
                abs(self.goal[0] - pos[0]) + abs(self.goal[1] - pos[1])
                for pos in ind.path
            )

            f_prog = 1.0 - (best_distance_in_path / max(d_tot, 1))
            
           
            # Bonificación especial si llega a la meta con 0 pasos invalidos
            goal_bonus = 0
            if d_goal == 0 and ind.invalid_steps == 0:
                goal_bonus = 5.0  
            
            # Fitness final combinado
            ind.fitness = (w_is * f_is + 
                      w_d * f_d + 
                      w_l * f_l + 
                      w_loop * f_loop +
                      w_prog * f_prog +
                      goal_bonus) * 100



    '''
    Funcion para ejecutar el algoritmo.
    '''        
    def run(self, generation_n=3000, optimize=False, on_step=None, should_stop=None, experimental=False):
        
        for i in range(generation_n):

            if should_stop and should_stop():
                if optimize:
                    for ind in self.population:
                        goal_index = self.create_path(ind, self.maze.maze, self.start, self.goal)
                        if goal_index is not None:
                            if not experimental or self.maze.evaluar_meta(ind.path[goal_index]):
                                return eliminar_ciclos(ind.path[:goal_index + 1])
                
                return []

            # revisar el camino del individuo
            for ind in self.population:
                goal_index = self.create_path(ind, self.maze.maze, self.start, self.goal)

                if optimize == False:
                    path = self.verify_goal(ind, goal_index, on_step=on_step, experimental=experimental,gen= i)
                   
                    if path :
                        print("Camino encontrado.")
                        return path
                    
                if goal_index is not None and (not experimental or self.maze.evaluar_meta(ind.path[goal_index])):
                
                    print('\033[93mIndividuo exitoso:\033[0m')  # Yellow
                    ind.print_info(show_path=False)
                    print('\033[90m------------------------------\033[0m')
                    print()

                    if on_step:
                        try:
                            on_step(set(), set(), ind.path[:goal_index + 1].copy())
                        except Exception as e:
                            print(f"Error en ultima llamada de on_step: {e}")

                    # Si no estamos optimizando, retornar inmediatamente
                    if not optimize:
                        print("Camino encontrado.")
                        return eliminar_ciclos(ind.path[:goal_index + 1])
                   
                
                elif goal_index is not None:
                    print(self.goal)
                    self.goal = self.maze.getGoal()
                    # print(self.goal)
                
                        
            else:
                print(self.goal)
                self.goal = self.maze.getGoal()
                print(self.goal)

            # calcular su fitness
            self.fitness_func()
            
            # seleccionar mejores individuos segun fitness dejandolos al inicio de la lista
            self.population.sort(key=lambda ind: ind.fitness, reverse=True)

            # graficar e imprimir info del mejor individuo
            if on_step:
                last = self.population[0].path[-1]
                on_step([], [last], self.population[0].path[:-1].copy())

            if i % 10 == 0:

                print('Generacion', i)
                self.population[0].print_info()
                print('Largo Cromosoma:', len(self.population[0].chromosome))
                print ('------------------------------')
            
            

            # cruzar y mutar los individuos para la siguiente generacion

            self.crossover() # se llama a mutacion dentro
           
        
        '''
        si no se encuentra el camino en las generaciones permitidas, 
        se retorna None.
        '''
        if optimize:
            # Buscar la mejor solución encontrada
            for ind in self.population:
                goal_index = self.create_path(ind, self.maze.maze, self.start, self.goal)
                if goal_index is not None:
                    if not experimental or self.maze.evaluar_meta(ind.path[goal_index]):
                        return eliminar_ciclos(ind.path[:goal_index + 1])
        
        return []
    



'''
Funcion wrapper para llamar al algoritmo.
'''
def genetic_algorithm(
        maze, 
        start, 
        goal, 
        population_size=500, 
        generation_n=500, 
        individual_mutation_p=0.80, 
        optimize=False,
        on_step=None, 
        should_stop=None
        ) -> list:
    
    

    ga = Genetic_Algorithm(maze, start, goal, population_size=population_size, individual_mutation_p=individual_mutation_p)
    path_solution = ga.run(generation_n=generation_n, optimize=optimize, on_step=on_step, should_stop=should_stop)

    if not path_solution: 
        print('\033[91mCamino no encontrado.\033[0m')  # Red
        print('Mejor Individuo:', ga.population[0].chromosome)

    return path_solution or []
