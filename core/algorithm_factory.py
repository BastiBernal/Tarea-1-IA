from typing import Any, Callable, List, Optional, Tuple
from algorithms.genetic_algorithm import Genetic_Algorithm
from algorithms.a_star import a_star
from algorithms.iddfs import iddfs

def make_ga_algorithm(
    *,
    population_size: int = 500,
    generation_n: int = 500,
    individual_mutation_p: float = 0.80,
    p_gene_mutation: float = 0.06,
    minimum_fitness: float = 0.0,
    optimize: bool = False,
    experimental: bool = False,
) -> Callable[[Any, Tuple[int, int], Tuple[int, int], Optional[Callable], Optional[Callable]], Optional[List[Tuple[int, int]]]]:
    """
    Retorna una función que ejecuta el algoritmo genético con los parámetros especificados.
    """

    def _algo(maze, start, goal, optimizer=optimize, on_step=None, should_stop=None):
        ga = Genetic_Algorithm(
            maze,
            start,
            goal,
            population_size=population_size,
            individual_mutation_p=individual_mutation_p,
            p_gene_mutation=p_gene_mutation,
            minimum_fitness=int(minimum_fitness),
        )
        return ga.run(generation_n=generation_n, optimize=optimizer, on_step=on_step, should_stop=should_stop,experimental=experimental)

    return _algo

def make_a_star_algorithm() -> Callable[[Any, Tuple[int, int], Tuple[int, int], Optional[Callable], Optional[Callable]], Optional[List[Tuple[int, int]]]]:
    """
    Retorna una función que ejecuta el algoritmo A*.
    (De momento no es necesario, pero sirve para mantener la consistencia)
    """
    return a_star

def make_iddfs_algorithm() -> Callable[[Any, Tuple[int, int], Tuple[int, int], Optional[Callable], Optional[Callable]], Optional[List[Tuple[int, int]]]]:
    """
    Retorna una función que ejecuta el algoritmo IDDFS.
    """
    def _algo(maze, start, goal, on_step=None, should_stop=None):
        return iddfs(maze, start, goal, max_depth=50, on_step=on_step, should_stop=should_stop)

    return _algo