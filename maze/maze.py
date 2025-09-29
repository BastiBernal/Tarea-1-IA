import sys
from core.callback import make_get_grid_func
from core.shared import SharedState
from utils.utils import valid_move
import random
from maze.maze_generators import *
from views.grid_visualizer import MainWindow
import sys
import os
import pickle

class Maze:

    def __init__(self, size, n_walls, n_goals ,strategy, crazy_value = 0.05, start = (1,1), frequenty_move = 15):
        """
        Args:
            size : tamaño del laberinto.
            n_walls: Cantidad de murallas
            n_goal : Cantidad de metas .
            strategy (MazeGenerator): Clase para generar el laberinto
            crazy_value (float del 0 al 1): Probabilidad de que las paredes se muevan
            start (tupla) : Posición inicial del jugador
            frequenty_move (int): Cantidad de turnos en las que las murallas se van moviendo
        """
        self.crazy_value = crazy_value
        walls_container = [[]]
        self.goals = []
        self.start = start
        self.maze = strategy.execute(size, n_walls, start, n_goals, self.goals, walls_container)
        self.walls = [tuple(w) for w in walls_container[0]]
        self.real_goal = random.choice(self.goals)
        self.player = self.start
        self.turn_counter = 0
        self.frequenty_move = frequenty_move

        for meta in self.goals:
            self.maze[meta] = 0

    def mover_paredes(self):
        crazy_value = self.crazy_value*100
        for i in range(len(self.walls)):
            moves = valid_move(self.maze, self.walls[i])
            if self.walls[i][0] == 0 or self.walls[i][1]  == 0:
                continue
            if moves:
                if random.randint(0,100) < crazy_value:
                    move = random.choice(moves)
                    if self.isGoal(move) or move == self.player:
                        continue
                    self.maze[self.walls[i]] = 0
                    self.walls[i] = move
                    self.maze[self.walls[i]] = 1

    def getGoal(self,x =  None,y = None):
        if x is None:
            x = self.start[0]
        if y is None:
            y = self.start[1]
        min = self.goals[0]
        val = self.get_distance(x,y,self.goals[0][0],self.goals[0][1])
        for i in range (1,len(self.goals)):
            new = self.get_distance(x,y,self.goals[i][0],self.goals[i][1])
            if val > new:
                val = new
                min= self.goals[i]
        return min

    def get_distance(self,x1,y1, x2,y2 ):
        return abs(x1 - x2) + abs(y1 - y2)

    def evaluar_meta(self, goal):
        if goal == self.real_goal:
            return True
        try:
            self.goals.remove(goal)
        finally:
            return False

    def move(self, pos ):
        self.turn_counter += 1
        if self.turn_counter == self.frequenty_move:
            self.mover_paredes()
            self.turn_counter = 0
        if pos in valid_move(self.maze, self.player):
            self.maze[self.player] = 0
            self.player = pos
            self.maze[self.player] = 8
            return True
        return False

    def isGoal(self,pos):
        return pos in self.goals

def save_maze(name,maze ,subfolder = None):
    carpeta = 'laberintos'

    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    if subfolder:
        if not os.path.exists(f'{carpeta}/{subfolder}'):
            os.makedirs(f'{carpeta}/{subfolder}')
        with open(f'{carpeta}/{subfolder}/{name}.pkl', 'wb') as f:
            pickle.dump(maze,f)
        return

    with open(f'{carpeta}/{name}.pkl', 'wb') as f:
        pickle.dump(maze, f)


def load_maze(file):
    if not os.path.exists(file):
        return
    with open(file, 'rb') as archivo:
        maze = pickle.load(archivo)
    return maze


if __name__ == "__main__":
    maze = Maze(50, 800, 5, DFSStrategy(), crazy_value=0.05, start=(1, 1))
    save_maze('maze',maze)
    maze = Maze(100, 800, 5, DFSStrategy(), crazy_value=0.05, start=(1, 1))
    maze = load_maze('laberintos/maze.pkl')
    print(maze.maze.shape[0])