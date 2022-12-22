from data_structures import Solution, Car, Station
from typing import List
import matplotlib.pyplot as plt


def any_station_too_far(max_dist: int, solution: Solution) -> bool:
    """
    :param max_dist: Max distance which we can travel
    :param solution: list of stations to check
    :return: Returns True if at least one of stations exceeds max distance and False if no
    """
    for station_amount in solution:
        if station_amount[0].extra_route > max_dist:
            return True
    return False


def fuel_amount_in_limit(solution: Solution) -> bool:
    """
    :param solution: Vector of stations and amount of fuel
    :return: Returns True if every refueling is in range: tank_capacity / 2 < refueling < tank_capacity
    """
    for station_amount in solution:
        if station_amount[1] > solution.car.tank_capacity or station_amount[1] < (solution.car.tank_capacity / 2):
            return False
    return True


def list_of_possible_station(car: Car, station_list: List[Station]):
    """
    :param car: instance of Car class
    :param station_list: List of every available station of our road
    :return: List of available station to tank at particular part of algorithm
    """
    # Computing how far can we arrive with current level of fuel
    curr_range = car.curr_fuel_level / car.ave_fuel_consumption * 100
    # Computing List of available station at particular part. We cannot turn back at our road
    # and we have to arrive station with fuel at tank
    return [station for station in station_list if station.road_position > car.curr_position and
            (station.road_position - car.curr_position + station.extra_route) < curr_range]


def is_station_too_far(car: Car, new_station: Station, next_station: Station) -> bool:
    """
    Function to check if we can arrive from new chose station at sa_algorithm.new_solution()
    to next station in solution. If  drop last station, set next_station as Station(0,0,0,end_of_route)
    :param car: instance of Car class
    :param new_station: New choosen station
    :param next_station: Next station in solution
    :return: true if station is too faar, else false
    """

    # TODO tutaj jest założone że jest tankowane full, w razie czego do zmiany
    fuel_level = car.tank_capacity - new_station.extra_route / 100 * car.ave_fuel_consumption

    curr_range = fuel_level / car.ave_fuel_consumption * 100
    if curr_range > next_station.road_position - new_station.road_position + next_station.extra_route and next_station.road_position > new_station.road_position:
        return False

    return True


def plot_score(lst: List[float], iter: int) -> None:
    """
    Function to plot solution value trough iteration
    :param lst: Lst of particular solution value
    :param iter: Nuber of iteration
    :return:
    """
    plt.style.use('ggplot')
    plt.plot(range(iter), lst)
    plt.xlabel('Iteracja')
    plt.ylabel('Funkcja celu')
    plt.title('Wartość funkcji celu w poszczególnych iteracjach')
    plt.show()
    return None