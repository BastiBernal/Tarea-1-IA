from abc import ABC, abstractmethod
import numpy as np
import random

#Clase padre para distintas estrategias para generar laberintos
#Idea de patrón Strategy
#En un futuro se pueden implementar otro tipo de laberintos con algoritmo de Prim o Kruskal
class MazeGenerator:
    @abstractmethod
    def execute(self,size,n_walls,start, n_metas, metas, walls):
        pass

class DFSStrategy(MazeGenerator):
    """
    Clase generadora de laberintos mediante DFS común
    Probablemente la estrategia mas simple y genera laberintos sin ciclos en un principio
    """
    def execute(self,size,n_walls,start, n_metas, metas, walls):
        size +=2
        maze = np.ones((size,size),dtype=int)

        #Se pinta la frontera de un color especifico para diferenciar
        maze[0, :] = 6
        maze[-1, :] = 6
        maze[:, 0] = 6
        maze[:, -1] = 6
        maze[start] = 2

        walls[0] = list(zip(*np.where(maze == 1)))

        def vecinos(x,y):
            direcciones= [(2,0),(-2,0),(0,2),(0,-2)]
            for dx, dy in direcciones:
                vecino_x, vecino_y = x+dx, y+dy
                if 1 <= vecino_x < size - 1 and 1 <= vecino_y < size - 1:
                    yield vecino_x, vecino_y

        stack = [start]
        hoja = True
        #DFS mediante la matriz
        while stack and len(walls[0]) > n_walls:
            x,y = stack[-1]
            posibles = [(nx, ny) for nx, ny in vecinos(x, y) if maze[nx, ny] == 1]
            if posibles:
                hoja = True
                nx,ny = (random.choice(posibles))
                maze[(x + nx) // 2, (y + ny) // 2] = 0
                maze[nx, ny] = 0
                walls[0].remove((nx,ny))
                walls[0].remove(((x + nx) // 2, (y + ny) // 2))
                stack.append((nx, ny))
            else:
                #Si es el primer pop no consecutivo que se hace es el final de un camino
                #Se pone una meta aca para tener metas solo en callejones
                if hoja:
                    metas.append((x,y))
                    hoja = False
                stack.pop()

        #Se eliminan muros al azar hasta tener la cantidad solicitada
        while len(walls[0]) > n_walls:
            delete = random.choice(walls[0])
            walls[0].remove(delete)
            maze[delete] = 0

        #Se eliminan metas al azar hasta tener la cantidad solicitada
        while len(metas) > n_metas:
            metas.remove(random.choice(metas))

        #Retorna la matriz que representa el laberinto
        return maze


