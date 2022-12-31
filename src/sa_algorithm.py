import random
from math import exp
from typing import Callable, List, Tuple
from copy import deepcopy

from src.utils import list_of_possible_station, is_station_too_far, random_station_generator, get_cords_of_stations, compute_fuel_before_tank
from src.data_structures import Solution, Station, Car
from src.visualization import *
from src.exceptions import NoStationsError


def init_solution(car: Car, end_point: int, max_dist: float, stations: List[Station]) -> Solution:
    """
    :param car: Car that we are traveling
    :param end_point: Point (int coordinate) which represents end of route
    :param max_dist: Max distance we can drive down from road
    :param stations: List of stations
    :return: Solution (random)
    """
    solution = Solution(car)
    #     car position + (fuel we have in tank) - reserve < end_point
    while car.curr_position + car.curr_fuel_level / car.ave_fuel_consumption * 100 - 10 < end_point:
        stations_in_step = list_of_possible_station(car, max_dist, stations)

        if len(stations_in_step) == 0:
            if len(solution) > 0:
                last_position = solution.get_station(len(solution) - 1)
                raise NoStationsError("There is no station we can get!", last_position.road_position)
            else:
                raise NoStationsError("There is no station we can get!", 0)

        station = random.choice(stations_in_step)
        amount = car.move_car(station)
        solution.add_station((station, round(amount, 2)))
    # Updating left fuel at end of road
    solution.update_left_fuel(end_point)

    return solution


def change_station(solution: Solution, car: Car, stations: List[Station], end_point: int, max_dist: float) -> Tuple[Solution, Car]:

    """
    Funtion to create new solution by exchange random station
    :param solution: current instance Solution in algorithm
    :param car: current instance Car in algorithm
    :param stations: List of stations
    :param end_point: End of our road
    :param max_dist: Max distance we can drive down from road
    :return:
    """

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
    station_in_step = list_of_possible_station(car_copy, max_dist, stations)

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


def mix_values(solution: Solution, car: Car, end_point: int) -> Tuple[Solution, Car]:
    """
    Function to mix amount of fuel tanked at stations
    :param solution: current instance Solution in algorithm
    :param car: Instance of Car in our road
    :param end_point: End of our road
    :return:
    """
    # Getting full solution, list of station and fuel amount
    solution_lst = solution.get_solution()
    for index, value in enumerate(solution_lst):

        # Tuple unpacking
        station, amount = value
        # Getting station before current
        last_station = solution_lst[index - 1][0]
        # Getting next station - if current is last create next station as end of road
        try:
            next_station = solution_lst[index + 1][0]
        except IndexError:
            next_station = Station('xyz', 0, 0, end_point)

        # Handling with last station if current station is first
        if index == 0:
            last_station = Station('xyz', 0, 0, 0)

        # Computing how many km we have to ride from current station to next station
        distance_to_ride = next_station.road_position - station.road_position + next_station.extra_route + station.extra_route

        # Amount of fuel we will use from current station to next and add some reserve
        fuel_to_use = distance_to_ride / 100 * car.ave_fuel_consumption + 2

        # Computing how much fuel we had when we reached current station
        fuel_before_tank = compute_fuel_before_tank(station, last_station, index, car)

        # Computing max amount of fuel we can tank
        max_fuel_to_tank = car.tank_capacity - fuel_before_tank

        # Computing min amount of fuel we should tank to reach next station
        min_fuel_to_tank = max(0, fuel_to_use - fuel_before_tank)

        new_amount = round(random.uniform(min_fuel_to_tank, max_fuel_to_tank), 2)

        # Updating information about fuel at step
        car.fuel_level_at_steps[index + 1] = round(fuel_before_tank + new_amount - station.extra_route / 100 * car.ave_fuel_consumption, 2)

        # Updating data in solution. Its easier in that way cause pen function will be update too
        solution.remove_station(index)
        solution.add_station((station, new_amount), index)

    # Update left fuel. Not necessary in changing_station cause mix values is always used
    solution.update_left_fuel(end_point)

    return solution, car


def new_solution(solution: Solution, car: Car, stations: List[Station], end_point: int, P: float, max_dist: float) -> Tuple[Solution, Car]:
    """
    Function which deal with choosing apropiate aproach to update our solution - mix fuel values or changing station
    :param solution: current instance Solution in algorithm
    :param car: Instance of Car in our road
    :param stations: List of stations
    :param end_point: End of our road
    :param P: Propability of chosing changing station aproach - P=0.7 means that we have 70% chance to use changing
    station way
    :param max_dist: Max distance we can drive down from road
    :return:
    """

    # Working at copy its more safe for us
    solution_copy = deepcopy(solution)
    car_copy = deepcopy(car)
    # Choosing way of update solution
    if P > random.uniform(0, 1):
        # Updating station list and mix values
        solution_copy, car_copy = change_station(solution_copy, car_copy, stations, end_point, max_dist)
        return mix_values(solution_copy, car_copy, end_point)

    else:
        # Only mix values
        return mix_values(solution_copy, car_copy,  end_point)


def simulated_annealing(new_solution: Callable, init_solution: Solution, stations: List[Station], end_point: int, max_dist: float, P: float,
                        T: int, alfa: float, iter_max: int = 10000) -> Tuple[Solution, List[float], int, int]:
    """
    :param new_solution: Function that returns new solution to compare
    :param init_solution: First solution
    :param stations: List of Stations at road
    :param end_point: End of our road
    :param max_dist: Max distance we can drive down from road
    :param P: Propability of chosing changing station aproach - P=0.7 means that we have 70% chance to use changing
    :param T: Temperature parametr
    :param alfa: Parameter to reduce T
    :param iter_max: Maximum number of iterations (needed in stop condition)
    :return: Solution
    """
    solution = init_solution
    # save the best global solution
    best_solution = solution
    car = init_solution.car
    iterations = 0
    swap_worse_counter = 0
    lst_of_scores = []

    while iterations < iter_max and T > 0.1:

        solution_prim, car_prim = new_solution(solution, car, stations, end_point, P, max_dist)
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


        # Updating list of value at every iter
        lst_of_scores.append(solution.solution_value())
        iterations += 1
        T = alfa * T
    return best_solution, lst_of_scores, iterations, swap_worse_counter


# Wszystko ponizej tylko do testu
# c1 = Car(150, 10, 0, 50)
# s1 = Station('A', 1, 10, 150)
# s2 = Station("C", 3, 20, 200)
# s3 = Station("B", 3.5, 25, 190)
# s4 = Station("D", 4, 15, 210)
# s5 = Station("E", 4, 30, 650)
# s6 = Station("F", 4, 40, 750)
# s7 = Station('G', 1, 10, 1000)
# s8 = Station('H', 1, 15, 1250)
# s9 = Station('I', 0.5, 20, 1200)
# s10 = Station('J', 2, 15, 1500)
# stations = [s1, s2, s3, s4, s5, s6, s7, s8]
#
# end_point = 2500
# max_dist = 30
# sol = init_solution(c1, end_point, max_dist, stations)
# print(sol)
# final_solution, lst, iter_number, count = simulated_annealing(new_solution, sol, stations, end_point,max_dist, 0.8 , 0.9, 0.999,
#                                                                    iter_max=1009)
# print(final_solution)
# print(final_solution.penalty_function)
# print(final_solution.left_fuel)

# P_lst = [0,0.1,0.3,0.5,0.7,0.9,1]
# val_lst = []
#
#
#
# station_lst, cord_lst = random_station_generator(500,end_point,(2,10))
# sol = init_solution(c1, end_point, max_dist, station_lst)
# final_solution, lst, iter_number, count = simulated_annealing(new_solution, sol, station_lst, end_point, max_dist, 0.8 , 0.9, 0.999,
#                                                               iter_max=1009)
# print(sol)
# print(final_solution)
# print(final_solution.left_fuel)
# plot_random_stations(end_point,cord_lst)
# plot_score(lst, iter_number)



# for elem in P_lst:
#     final_solution, lst, iter_number, count = simulated_annealing(new_solution, sol, station_lst, end_point, max_dist, elem , 0.9, 0.999,
#                                                               iter_max=1009)
#     val_lst.append(final_solution.solution_value())
#
# print(val_lst)



# stations_lst, cord_list = random_station_generator(200, 5000, (2, 10))
# plot_random_stations(5000, cord_list)
# sol = init_solution(c1, 5000, stations_lst)
# print(sol)
# print(sol.penalty_function)
#

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
