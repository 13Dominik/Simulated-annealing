import random
import numpy as np
from typing import List, Tuple

from src.data_structures import Solution, Car, Station


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


def random_station_generator(station_amount: int, end_point: int, price_range: Tuple[int]) -> List[Station]:
    """
    Function which generate random data, and plot it
    :param station_amount: Amount of station to generate
    :param end_point: End of our road
    :param price_range: Range of random price at generated station
    :return:
    """
    station_list = []
    coord_list = []
    for i in range(station_amount):
        # Randomly generate coordinate
        x = np.round(random.uniform(0, end_point), 2)
        y = np.round(random.uniform(0, end_point), 2)
        # To function y = x
        a = 1
        b = 0

        # Suppose our road is function y = x -> then distance from point
        # to function is equal abs(Ax0 + By0 + C) / sqrt(A^2 + B^2)
        A = -a
        B = 1
        C = b
        extra_route = np.round(np.abs(A * x + B * y + C) / (np.sqrt(A ** 2 + B ** 2)), 2)
        # Having extra route, now compute Station.road_position its intersection of
        # perpendicular function to y=x, passer trough point (x,y)

        # slope of perpendicular function to y=x
        a_prim = -1 / a
        b_prim = y - a_prim * x
        road_position = np.round((b - b_prim) / (a_prim - a), 2)
        # road_position its first coordinate of our intersection and also
        # road.position of our station

        # Generating random price for current station
        price = np.round(random.uniform(price_range[0], price_range[1]), 2)
        station_list.append((Station(f'Station: {i}', price, extra_route, road_position)))
        coord_list.append((x, y))

    return station_list, coord_list


def get_cords_of_stations(all_stations: List[Station], solution: Solution, coord_list: List[Tuple[int]]) -> List[
    Tuple[float]]:
    """
    Function that returns coors of choosen stations from all stations
    :param all_stations: All possible stations in whole algorithm
    :param solution: Stations that we have chosen
    :param coord_list: All stations coords list
    :return: List of tuples of coordinates
    """
    cords = []
    for station in solution.get_stations():
        cords.append(coord_list[all_stations.index(station)])
    return cords
