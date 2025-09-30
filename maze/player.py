from core.algorithm_runner import AlgorithmRunner
import time

class MazePlayer:

    def __init__(self, maze, strategy: AlgorithmRunner, life_turns=100, calculate_cost=1, on_game_over=None, on_victory=None):
        self.strategy = strategy
        self.maze = maze
        self.life_turns = life_turns
        self.calculate_cost = calculate_cost
        self.path = []
        self.on_game_over = on_game_over
        self.on_victory = on_victory

    def calcular_ruta(self):
        maze = self.maze
        start = self.maze.player
        goal = self.maze.getGoal(*start)
        self.strategy.run_algorithm(maze,start,goal)
        #self.strategy.thread.join()
        self.path = self.strategy.resultado


    def start_game(self):
        won = False

        while self.life_turns > 0:
            if not self.path:
                self.calcular_ruta()
                self.life_turns -= self.calculate_cost
                if self.path == []:
                    self.life_turns = self.life_turns - self.maze.frequenty_move + self.maze.turn_counter
                    self.maze.turns = 0
                    self.maze.mover_paredes()
            else:
                for pos in self.path:
                    self.life_turns -= 1
                    time.sleep(0.1)
                    if not self.maze.move(pos) and self.maze.player != pos:
                        self.path = []
                        break

                if self.path and not self.maze.evaluar_meta(self.maze.player):
                    self.path = []
                elif self.path:
                    won = True
                    break

        if won:
            print("Ganaste!")
            if callable(self.on_victory):
                try:
                    self.on_victory()
                except Exception:
                    pass
        else:
            print("Game over...")
            if callable(self.on_game_over):
                try:
                    self.on_game_over()
                except Exception:
                    pass

