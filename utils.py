from data_structures import Solution, Car, Station
from typing import List


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
    remain_distance = car.curr_fuel_level / car.ave_fuel_consumption * 100
    # Computing List of available station at particular part. We cannot turn back at our road
    # and we have to arrive station with fuel at tank
    return [station for station in station_list if station.road_position > car.curr_position and
            (station.road_position - car.curr_position + station.extra_route) < remain_distance]

