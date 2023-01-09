from typing import List, Tuple
import numpy as np


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
        return f"{self.name} {self.price}$"

    def __repr__(self):
        return f"{self.name} {self.price}$"

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price


class Car:
    def __init__(self, tank_capacity: int, ave_fuel_consumption: float, curr_position: float, curr_fuel_level: float):
        """
        :param tank_capacity: Tank capacity
        :param ave_fuel_consumption: Average fuel consumption
        :param curr_position: Current position of car at road
        :param curr_fuel_level: Current amount of fuel in tank
        :return: None
        """
        self.tank_capacity = tank_capacity
        self.ave_fuel_consumption = ave_fuel_consumption
        self.curr_position = curr_position
        self.curr_fuel_level = curr_fuel_level
        self.start_fuel_level = self.curr_fuel_level
        # Contains fuel level in tank at every route stage (station position)
        self.fuel_level_at_steps = [self.curr_fuel_level]

    def get_fuel_level_at_step(self, index):
        return self.fuel_level_at_steps[index]

    def move_car(self, station: Station, station_to_drop: int = None) -> float:
        """
        Method which update car position, current fuel level, and fuel level at steps
        :param station: Station where we will tank, we are tanking as much as possible
        :param station_to_drop: index to update at fuel_level_at_steps - !important - fist station in solution its 1 index here
        :return: Amount of fuel we are tanking on this particular station
        """

        # Computing how much fuel will we have when we arrive station
        current_lack = self.tank_capacity - self.curr_fuel_level  # current space in tank
        fuel_we_will_use = (
                                   station.road_position - self.curr_position + station.extra_route) / 100 * self.ave_fuel_consumption
        # current_lack + amount of fuel we will use to get in to the station
        amount_to_tank = fuel_we_will_use + current_lack

        # Tanking as much as possible (tank must be full)
        self.curr_fuel_level = self.tank_capacity  # tank max
        # Computing how much will we have when we back at road from station
        self.curr_fuel_level = self.curr_fuel_level - station.extra_route / 100 * self.ave_fuel_consumption
        self.curr_position = station.road_position

        # Checking if it is init solution or not
        if station_to_drop is None:
            # If init - we do not have pop element form curr_fuel_level
            self.fuel_level_at_steps.append(self.curr_fuel_level)
            return amount_to_tank
        else:
            # If not, we have to pop and insert new value
            self.fuel_level_at_steps.pop(station_to_drop + 1)
            self.fuel_level_at_steps.insert(station_to_drop + 1, self.curr_fuel_level)
        return amount_to_tank

    def __eq__(self, other):
        return self.tank_capacity == other.tank_capacity and self.ave_fuel_consumption == other.ave_fuel_consumption


class Solution:
    """
    We try to minimize cost of travelling (minimize solution)
    Value of solution is computed according to the rule:
    Sum of money spent on every station + penalty function - (+) cost of surplus (minus) of fuel

    Penalty function - is added when we refuel when we have more than half of capacity of tank.
    Surplus - When at the end (end_point) of route we have more fuel than at start (0 position)
    Minus - When at the end (end_point) we have less fuel than at start (0 position)
    Cost of surplus (minus) - is average price of fuel at stations that we tanked
    """

    def __init__(self, car: Car, solution=None):
        """
        :param solution: Vector of stations and amount of petrol we should buy, for instance:
        [(A, 10), (B, 21), (C, 234)], if None it will be an empty list and we can add
        """
        self.solution = solution
        self.car = car
        self.penalty_function = []
        # Fuel at endpoint
        self.left_fuel = None
        # Difference between fuel at end_point and at start
        self.fuel_difference = None

    @property
    def solution(self):
        return self.__solution

    @solution.setter
    def solution(self, value):
        if value is None:
            self.__solution = []
        else:
            self.__solution = value

    def add_station(self, station_amount: Tuple[Station, float], insert_index: int = None) -> None:
        """
        Add new station and amount of petrol bought eg. ("A1", 20)
        :param station_amount:
        :param insert_index: Index where insert new station - If None, insert at end
        :return:
        """

        if insert_index is None:
            insert_index = len(self.solution)
        self.solution.insert(insert_index, station_amount)
        # Updating penalty function, if we tank less than half of tank capacity
        if station_amount[1] < self.car.tank_capacity / 2:
            # The less we tank at once time, the more we punish
            self.penalty_function.insert(insert_index, round(self.car.tank_capacity / 2 - station_amount[1] * 0.5, 2))
        else:
            self.penalty_function.insert(insert_index, 0)

    def remove_station(self, station_index: int):
        """
        Method to remove station from solution and penalty_function
        :param station_index: Index of station to remove
        :return:
        """
        self.solution.pop(station_index)
        self.penalty_function.pop(station_index)

    def solution_value(self) -> float:
        # Computing solution value included fuel_difference

        # computing weighted average
        fuel_prices = [elem[0].price for elem in self.solution]
        fuel_amount = [elem[1] for elem in self.solution]
        mean_price = 0
        for i in range(len(fuel_amount)):
            mean_price += fuel_amount[i] * fuel_prices[i]
        mean_price = (mean_price / sum(fuel_amount))

        return round(sum([station[0].price * station[1] for station in self.solution]) + sum(
            self.penalty_function) - mean_price * self.fuel_difference, 2)

    def get_penalty(self) -> float:
        """ Returns sum of all penalties """
        return sum(self.penalty_function)

    def get_cost_of_solution(self) -> float:
        """ Returns cost of fuel (without penalty function!!!) """
        return sum([elem[0].price * elem[1] for elem in self.solution])

    def get_station_position(self, station_index):
        """
        Method to return station position from index
        :param station_index: Station index
        :return:
        """
        if station_index == -1:
            return 0
        return self.solution[station_index][0].road_position

    def get_station(self, station_index):
        """
        Method to return station from index
        :param station_index:
        :return:
        """
        return self.solution[station_index][0]

    def get_stations(self):
        return [elem[0] for elem in self.solution]

    def get_solution(self):
        return self.solution

    def update_left_fuel(self, endpoint: int) -> None:
        """
        Method to update left_fuel parameter and fuel_difference
        :param endpoint: End of our road
        :return:
        """
        # Grabbing last station
        last_station = self.get_station(-1)
        # Computing left distance and fuel to use
        distance_to_ride = endpoint - last_station.road_position
        fuel_to_use = distance_to_ride / 100 * self.car.ave_fuel_consumption

        # Left fuel is fuel after last tank minus fuel to use and fuel at beginning
        self.left_fuel = round(self.car.get_fuel_level_at_step(-1) - fuel_to_use, 2)
        self.fuel_difference = round(self.left_fuel - self.car.start_fuel_level, 2)

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
        return str(self.__solution) + str(self.solution_value())

    def __repr__(self):
        return str(self.__solution) + str(self.solution_value())

    def __sub__(self, other):
        return self.solution_value() - other.solution_value()

    def __len__(self):
        return len(self.solution)
