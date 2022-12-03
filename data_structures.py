from typing import List, Tuple


class Car:
    def __init__(self, tank_capacity: int, ave_fuel_consumption: float):
        self.tank_capacity = tank_capacity
        self.ave_fuel_consumption = ave_fuel_consumption


class Station:
    def __init__(self, name: str, price: float, extra_route: float, road_position: float):
        """
        :param name: Station id
        :param price: Petrol price
        :param extra_route: The road we must add visit station
        :param road_position: Position on road, (when we can consider this station)
        :return: None
        """
        self.name = name
        self.price = price
        self.extra_route = extra_route
        self.road_position = road_position


class Solution:

    def __init__(self, car: Car):
        """
        :param solution: Vector of stations and amout of petrol we should buy, for instance:
        [(A, 10), (B, 21), (C, 234)]
        """
        self.solution = []
        self.car = car

    def add_station(self, station_amount: Tuple[Station, int]):
        self.solution.append(station_amount)

    def solution_value(self):
        return sum([station[0].price * station[1] for station in self.solution])

    def __iter__(self):
        return iter(self.solution)
