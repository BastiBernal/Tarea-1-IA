import sys

from numpy.random import randint

from core.callback import make_get_grid_func
from core.shared import SharedState
from utils.utils import valid_move
import random
from maze_generators import *
from views.grid_visualizer import MainWindow
import sys

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtGui import QImage, QPixmap

class Maze:

    def __init__(self, size, n_walls, n_goals ,strategy, crazy_value = 0.05, start = (1,1)):
        self.crazy_value = crazy_value
        self.walls = [[]]
        self.goals = []
        self.start = start
        self.maze = strategy.execute(size, n_walls,start ,n_goals, self.goals, self.walls)
        self.walls = self.walls[0]
        self.real_goal = random.choice(self.goals)

    def mover_paredes(self):
        crazy_value = self.crazy_value*100
        for i in range(len(self.walls)):
            moves = valid_move(self.maze, self.walls[i])
            if self.walls[i][0] == 0 or self.walls[i][1]  == 0:
                continue
            if moves:
                if random.randint(0,100) < crazy_value:
                    move = random.choice(moves)
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



if __name__ == "__main__":
    app = QApplication(sys.argv)

    # matriz de ejemplo
    maze = Maze(30,10,30,DFSStrategy(),crazy_value = 0.5, start = (6,6))
    print(maze.walls)
    print(maze.goals)
    matriz = maze.maze
    print(maze.getGoal())

    m = make_get_grid_func(maze.maze, SharedState(),maze.start,maze.goals)
    ventana = MainWindow(matriz,m )
    ventana.show()
    sys.exit(app.exec())
