import random
from math import exp
from typing import Callable, List

from utils import list_of_possible_station
from data_structures import Solution, Station, Car


def init_solution(car: Car, end_point: int, stations: List[Station]) -> Solution:
    """
    :param car: Car that we are traveling
    :param end_point: Point (int coordinate) which represents end of route
    :param stations: List of stations
    :return: Solution (random)
    """
    solution = Solution(car)
    #     car position + (fuel we have in tank) - reserve < end_point
    while car.curr_position + car.curr_fuel_level / car.ave_fuel_consumption * 100 - 10 < end_point:
        stations_in_step = list_of_possible_station(car, stations)
        station = random.choice(stations_in_step)
        amount = car.move_car(station)
        solution.add_station((station, amount))
    # TODO: Uzupełnić o to jak dużo nam zostało paliwa i jak to wliczać w solution
    return solution

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
    :param T: Temperature parametr
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
c1 = Car(200, 10, 0, 50)
s1 = Station("A", 3, 20, 200)
s2 = Station("B", 3.5, 25, 190)
s3 = Station("C", 4, 15, 210)
s4 = Station("D", 4, 30, 650)
s5 = Station("E", 4, 40, 750)
stations = [s1, s2, s3, s4, s5]


sol = init_solution(c1, 2500, stations)
print(sol)
