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

    def __str__(self):
        return f"{self.name} {self.price}"

    def __repr__(self):
        return f"{self.name} {self.price}$"


class Solution:

    def __init__(self, car: Car, solution=None):
        """
        :param vector: Vector of stations and amout of petrol we should buy, for instance:
        [(A, 10), (B, 21), (C, 234)], if None it will be a empty list and we can add
        """
        self.solution = solution
        self.car = car

    @property
    def solution(self):
        return self.__solution

    @solution.setter
    def solution(self, value):
        if value is None:
            self.__solution = []
        else:
            self.__solution = value

    def add_station(self, station_amount: Tuple[Station, int]) -> None:
        """
        Add new station and amout of petrol bought eg. ("A1", 20)
        :param station_amount:
        :return:
        """
        self.__solution.append(station_amount)

    def solution_value(self) -> float:
        return sum([station[0].price * station[1] for station in self.solution])

    def __iter__(self):
        return iter(self.solution)

    def __gt__(self, other):
        return self.solution_value() > other.solution_value()

    def __ge__(self, other):
        return self.solution_value() >= other.solution_value()

    def __lt__(self, other):
        return self.solution_value() < other.solution_value()

    def __le__(self, other):
        return self.solution_value() <= other.solution_value()

    def __str__(self):
        return str(self.__solution)

    def __repr__(self):
        return str(self.__solution)
