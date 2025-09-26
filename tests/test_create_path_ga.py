import pytest
from algorithms.genetic_algorithm import Individual, create_path, intersection_point
import numpy as np
MAZE = np.array([
    [0, 0, 0, 0, 1, 0, 1, 1, 0, 0],
    [1, 0, 1, 1, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 1, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 1, 1, 0, 0],
    [0, 1, 1, 0, 1, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 1, 1, 1, 0, 1, 0],
    [1, 1, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 1, 1, 1, 0]
])


def test_invalid_steps():
    
    chromosome_ans = [
        ('RDRDRDLDDDRDRURD', 0),
        ('LUDRRUDRL', 6),
        ('LLLLLUUUU', 9)
    ]

    population = []
    for crom in chromosome_ans:
        population.append(Individual(crom[0]))


    create_path(population=population, maze=MAZE, start=(0,0), goal=(9,9))

    for i in range(len(population)):
        assert population[i].invalid_steps == chromosome_ans[i][1]

def test_intersection_point():

    assert intersection_point(MAZE, (8,7), (9,9)) == False # pasillo
    assert intersection_point(MAZE, (2,2), (9,9)) == True # esquina
    assert intersection_point(MAZE, (5,2), (9,9)) == True # 3 direcciones
    assert intersection_point(MAZE, (9,9), (9,9)) == True # meta
    assert intersection_point(MAZE, (2,0), (9,9)) == True # sin salida
    

def test_create_path():
    GENES =  'RDRDRDLDDDRDRURD'
    population = [Individual(GENES)]
    create_path(population=population, maze=MAZE, start=(0,0), goal=(9,9))

    assert population[0].path == [(0,0), (0,1), (1,1), (2,1), (2, 2), (3,2), (3,3), (4,3), (5,3), (5,2), (6, 2), (7, 2), (8, 2), (8, 3), (9, 3), (9, 4), (9, 5), (8,5), (8, 6), (8, 7), (8, 8), (8, 9), (9, 9)]