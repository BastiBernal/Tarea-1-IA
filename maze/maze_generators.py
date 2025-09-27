from abc import ABC, abstractmethod
import numpy as np
import random


class MazeGenerator:
    @abstractmethod
    def execute(self):
        pass

class DFSStrategy(MazeGenerator):
    def execute(self,size,n_walls,start, n_metas, metas, walls):
        maze = np.ones((size,size),dtype=int)
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
                if hoja:
                    metas.append((x,y))
                    hoja = False
                stack.pop()


        while len(walls[0]) > n_walls:
            delete = random.choice(walls[0])
            walls[0].remove(delete)
            maze[delete] = 0

        while len(metas) > n_metas:
            metas.remove(random.choice(metas))

        #libres = list(zip(*np.where(maze == 0)))
        #for i in range(n_metas):
            #x,y = random.choice(libres)
            #maze[x,y] = 3
            #metas.append((x,y))

        return maze


