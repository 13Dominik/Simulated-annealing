from typing import List, Tuple


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
        self.fuel_level_at_steps = [self.curr_fuel_level]

    def move_car(self, station_amount: Tuple[Station, int]):
        """
        Method which update car position, and current fuel level
        :param station_amount: Station where we will tank, and amount of fuel we will tank
        :return:
        """
        station, fuel_amount = station_amount

        # Computing how much fuel will we have when we arrive station
        self.curr_fuel_level = self.curr_fuel_level - (station.road_position - self.curr_position + station.extra_route) / 100 * self.ave_fuel_consumption
        # Adding fuel which we tank
        self.curr_fuel_level += fuel_amount
        # Computing how much will we have when we back at road from station
        self.curr_fuel_level = self.curr_fuel_level - station.extra_route / 100 * self.ave_fuel_consumption
        self.curr_position = station.road_position
        self.fuel_level_at_steps.append(self.curr_fuel_level)


class Solution:

    def __init__(self, car: Car, solution=None):
        """
        :param vector: Vector of stations and amount of petrol we should buy, for instance:
        [(A, 10), (B, 21), (C, 234)], if None it will be a empty list and we can add
        """
        self.solution = solution
        self.car = car
        self.penalty_function = 0

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

        Add new station and amount of petrol bought eg. ("A1", 20) and  update car info
        :param station_amount:
        :return:
        """
        #TODO pasuje jeszcze dodać do postaci rozwiązania(lub inaczej to zapisać) informacje o ilości paliwa po zatankowaniu
        # i wróceniu na trase. Wtedy Jak mamy stacje A -> B -> C i wyrzucimy B, to przsuwamy car na A, i możemy mu ustawić dzięki
        # temu car.curr_fuel_level. car.curr_position ustawaimy mu wtedy jako B.road_position.

        self.__solution.append(station_amount)
        # Updating information about car
        self.car.move_car(station_amount)
        # Updating penalty function, if we tank less than half of tank capacity
        if station_amount[1] < self.car.tank_capacity / 2:
            #TODO Tutaj można pomyśleć nad wzorem, i trzeba pamiętać że jak wyrzucamy jakąś stację
            # z rozwiązania to trzeba zmniejszyć funkcję kary - odejmiemy tylko od self.penalty_function
            # drugą wartość z krotki którą wyrzucamy, zgodnie z poniższym wzorem

            # The less we tank at once time, the more we punish
            self.penalty_function += (self.car.tank_capacity / 2 - station_amount[1]) * 0.5


    def solution_value(self) -> float:
        return sum([station[0].price * station[1] for station in self.solution]) + self.penalty_function

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
