import random
from math import exp
from data_structures import Solution, Station, Car
from typing import Callable


def init_solution() -> Solution:
    pass


def new_solution() -> Solution:
    pass
    # Wszystko ponizej jest tylko w celu testu, wiec trzeba usunac
    # c1 = Car(10, 20, 0, 0)
    # s1 = Station("A", 10, 0, 0)
    # s2 = Station("B", 20, 0, 0)
    ##s3 = Station("C", 30, 0, 0)
    # return Solution(c1, [(s1, 5), (s2, 222), (s3, 30)])


def simulated_annealing(new_solution: Callable, init_solution: Solution, T: int,
                        alfa: float, iter_max: int = 10000) -> Solution:
    """
    :param new_solution: Function that returns new solution to compare
    :param init_solution: First solution
    :param T: Temperature parametr #TODO: Tu sie trzeba zastanowic jak to ustawic
    :param alfa: Parameter to reduce T
    :param iter_max: Maximum number of iterations (needed in stop condition)
    :return: Solution
    """
    solution = init_solution
    iterations = 0
    while iterations < iter_max and T > 0.1:
        solution_prim = new_solution()
        if solution_prim < solution:  # if new solution is better
            solution = solution_prim
        else:
            delta = solution_prim - solution
            r = random.uniform(0, 1)
            if r > exp(-delta / T):
                solution = solution_prim
            else:
                solution = solution
        iterations += 1
        T = alfa * T
    return solution

# Wszystko ponizej tylko do testu
# c1 = Car(10, 20, 0, 0)
# s1 = Station("A", 10, 0, 0)
# s2 = Station("B", 20, 0, 0)
# s3 = Station("C", 30, 0, 0)
# print(simulated_annealing(new_solution, Solution(c1, [(s1, 10), (s2, 20), (s3, 30)]), 200, 0.95))
#
# print(new_solution())
# print(Solution(c1, [(s1, 5), (s2, 20), (s3, 30)]))
