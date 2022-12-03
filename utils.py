from data_structures import Solution


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
