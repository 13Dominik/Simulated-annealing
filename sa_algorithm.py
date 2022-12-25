import random
from math import exp
from typing import Callable, List, Tuple
from copy import deepcopy
from utils import list_of_possible_station, is_station_too_far, random_station_generator, get_cords_of_stations
from data_structures import Solution, Station, Car
from visualization import *
from exceptions import NoStationsError


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

        if len(stations_in_step) == 0:
            if len(solution) > 0:
                last_position = solution.get_station(len(solution) - 1)
                raise NoStationsError("There is no station we can get!", last_position.road_position)
            else:
                raise NoStationsError("There is no station we can get!", 0)

        station = random.choice(stations_in_step)
        amount = car.move_car(station)
        solution.add_station((station, round(amount, 2)))
    # TODO: Uzupełnić o to jak dużo nam zostało paliwa i jak to wliczać w solution
    return solution


def new_solution(solution: Solution, car: Car, stations: List[Station], end_point: int = 2500) -> Tuple[Solution, Car]:
    # TODO: jeszcze trzeba dorzucic warunek o tym ile maksymalnie mozna zjechac z trasy
    # To już prosto - dodamy to w warunku w 2 funkcjach z utils
    """
    Funtion to create new solution
    :param solution: of current instance Solution in algorithm
    :param car: current instance Car in algorithm
    :param stations: List of stations
    :param end_point: End of our road
    :return:
    """
    #TODO: tutaj pewnie bedziemy musieli pomyslec nad zmiana generowania nowego rozwiazania prosze panstwa
    # Creating copy of instance - we do not know if we will accept this solution
    car_copy = deepcopy(car)
    solution_copy = deepcopy(solution)
    solution_copy.car = car_copy

    # Chosing index of station to drop
    station_to_drop = random.randint(0, len(solution_copy) - 1)

    # transport car to station before station to drop - or beginning of road if drop first station
    car_copy.curr_position = solution_copy.get_station_position(station_to_drop - 1)
    # Setting fuel_level to proper at particular step
    car_copy.curr_fuel_level = car_copy.get_fuel_level_at_step(station_to_drop)
    station_in_step = list_of_possible_station(car_copy, stations)

    # While we have potential station to chose
    while station_in_step:
        # randomly chose station from list of available station
        new_station = station_in_step.pop(random.randint(0, len(station_in_step) - 1))
        # Setting next station after new choosen station
        if station_to_drop == len(solution_copy) - 1:
            # If we dropped last station, 'next_station' is end of road
            next_station = Station('xyz', 0, 0, end_point)
        else:
            # else  next station is next station in solution.__solution
            next_station = solution_copy.get_station(station_to_drop + 1)

        # Checking if new chosen station is not too far to next station in solution
        if not is_station_too_far(car_copy, new_station, next_station):

            # Adding station to solution and update structure
            solution_copy.remove_station(station_to_drop)
            amount = car_copy.move_car(new_station, station_to_drop=station_to_drop)
            solution_copy.add_station((new_station, round(amount, 2)), station_to_drop)

            # We have to update amount of fuel at next station
            if station_to_drop == len(solution_copy) - 1:
                # If we dropped last station - nothing to update
                pass

            else:
                # Updating information about next station in solution
                solution_copy.remove_station(station_to_drop + 1)
                amount = car_copy.move_car(next_station, station_to_drop=station_to_drop + 1)
                solution_copy.add_station((next_station, round(amount, 2)), station_to_drop + 1)

            return solution_copy, car_copy

    # If list of potential station to choose end return not modificated instance
    return solution, car


def simulated_annealing(new_solution: Callable, init_solution: Solution, stations: List[Station], end_point: int,
                        T: int, alfa: float, iter_max: int = 10000) -> Tuple[Solution, List[float], int, int]:
    """
    :param new_solution: Function that returns new solution to compare
    :param init_solution: First solution
    :param stations: List of Stations at road
    :param end_point: End of our road
    :param T: Temperature parametr
    :param alfa: Parameter to reduce T
    :param iter_max: Maximum number of iterations (needed in stop condition)
    :return: Solution
    """
    solution = init_solution
    # save the best global solution
    best_solution = solution
    car = init_solution.car
    #TODO tutaj to best_car bedzie mozna wyjebac - bardziej bylo w celach testu
    best_car = car
    iterations = 0
    swap_worse_counter = 0
    lst_of_scores = []

    while iterations < iter_max and T > 0.1:

        solution_prim, car_prim = new_solution(solution, car, stations, end_point)
        if solution_prim < solution:  # if new solution is better
            solution = solution_prim
            car = car_prim
        else:
            delta = solution_prim - solution
            r = random.uniform(0, 1)
            if r > exp(-delta / T):
                solution = solution_prim
                car = car_prim
                # Updating counter
                swap_worse_counter += 1
            else:
                solution = solution
                car = car

        # Condition to upgrade best solution - we can latter lose it
        if solution < best_solution:
            best_solution = solution
            best_car = car

        # Updating list of value at every iter
        lst_of_scores.append(solution.solution_value())
        iterations += 1
        T = alfa * T
    return best_solution, lst_of_scores, iterations, swap_worse_counter


# Wszystko ponizej tylko do testu
c1 = Car(150, 10, 0, 50)
s1 = Station('A', 1, 10, 150)
s2 = Station("C", 3, 20, 200)
s3 = Station("B", 3.5, 25, 190)
s4 = Station("D", 4, 15, 210)
s5 = Station("E", 4, 30, 650)
s6 = Station("F", 4, 40, 750)
s7 = Station('G', 1, 10, 1000)
s8 = Station('H', 1, 15, 1150)
s9 = Station('I', 0.5, 20, 1200)
s10 = Station('J', 2, 15, 1500)
stations = [s1, s2, s3, s4, s5, s6, s7, s8]

# stations_lst, cord_list = random_station_generator(200, 5000, (2, 10))
# plot_random_stations(5000, cord_list)
# sol = init_solution(c1, 5000, stations_lst)
# print(sol)
# print(sol.penalty_function)
#
# final_solution, lst, iter_number, count = simulated_annealing(new_solution, sol, stations_lst, 5400, 0.9, 0.999,
#                                                               iter_max=1009)
# print(final_solution.get_stations())
#
# print(get_cords_of_stations(stations_lst, final_solution, cord_list))
# coords = get_cords_of_stations(stations_lst, final_solution, cord_list)
#
#
#
# #print(final_solution[0])
# #print(final_solution.get_station(0))
# #plot_solution(5000, coords, final_solution)
# print(final_solution.penalty_function)
#
# plot_score(lst, iter_number)
