import unittest
import data_structures as ds
from utils import any_station_too_far, fuel_amount_in_limit, list_of_possible_station, get_cords_of_stations, \
    is_station_too_far


class TestAny_station_too_far(unittest.TestCase):
    def test_station_too_far(self):
        c = ds.Car(0, 0, 0, 0)
        s1 = ds.Station("A", 10, 30, 0)
        s2 = ds.Station("B", 20, 40, 0)
        solution = ds.Solution(c)

        solution.add_station((s1, 10))
        solution.add_station((s2, 20))
        self.assertTrue(any_station_too_far(25, solution))

    def test_station_not_too_far(self):
        c = ds.Car(0, 0, 0, 0)
        s1 = ds.Station("A", 10, 30, 0)
        s2 = ds.Station("B", 20, 40, 0)
        solution = ds.Solution(c)

        solution.add_station((s1, 10))
        solution.add_station((s2, 20))
        self.assertFalse(any_station_too_far(45, solution))


class TestFuel_amount_in_limit(unittest.TestCase):
    def test_refueling_in_limit(self):
        c = ds.Car(30, 0, 0, 0)
        s1 = ds.Station("A", 10, 30, 0)
        s2 = ds.Station("B", 20, 40, 0)
        solution = ds.Solution(c)
        solution.add_station((s1, 15))
        solution.add_station((s2, 25))

        self.assertTrue(fuel_amount_in_limit(solution))

    def test_refueling_not_in_limit(self):
        c = ds.Car(20, 0, 0, 0)
        s1 = ds.Station("A", 10, 30, 0)
        s2 = ds.Station("B", 20, 40, 0)
        solution = ds.Solution(c)
        solution.add_station((s1, 15))
        solution.add_station((s2, 25))

        self.assertFalse(fuel_amount_in_limit(solution))


class TestListOfStation(unittest.TestCase):
    def setUp(self) -> None:
        self.c = ds.Car(50, 10, 10, 50)
        self.s1 = ds.Station("A", 10, 10, 5)
        self.s2 = ds.Station("B", 20, 20, 100)
        self.s3 = ds.Station("C", 15, 7, 350)
        self.s4 = ds.Station("D", 25, 5, 500)
        self.s5 = ds.Station("E", 10, 20, 500)
        self.s6 = ds.Station("F", 15, 10, 600)

    def test_list_of_station(self):
        self.assertEqual([self.s2, self.s3, self.s4],
                         list_of_possible_station(self.c, [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6]))


class TestGetCordsOfStations(unittest.TestCase):
    def setUp(self) -> None:
        self.c = ds.Car(50, 10, 10, 50)
        self.s1 = ds.Station("A", 10, 10, 5)
        self.s2 = ds.Station("B", 20, 20, 100)
        self.s3 = ds.Station("C", 15, 7, 350)
        self.s4 = ds.Station("D", 25, 5, 500)
        self.s5 = ds.Station("E", 10, 20, 500)
        self.s6 = ds.Station("F", 15, 10, 600)

    def test_get_cords_of_stations1(self):
        cords = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]
        all_stations = [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6]
        solution = ds.Solution(self.c, [(self.s1, 10), (self.s3, 3), (self.s4, 20)])
        self.assertEqual([(1, 1), (3, 3), (4, 4)], get_cords_of_stations(all_stations, solution, cords))

    def test_get_cords_of_stations2(self):
        cords = [(10, 10), (20, 20), (30, 30), (40, 40), (50, 50), (60, 60)]
        all_stations = [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6]
        solution = ds.Solution(self.c, [(self.s1, 10), (self.s5, 20)])
        self.assertEqual([(10, 10), (50, 50)], get_cords_of_stations(all_stations, solution, cords))


class TestIsStationTooFar(unittest.TestCase):
    def test_is_station_too_far_true(self):
        c = ds.Car(30, 20, 50, 10)
        next = ds.Station("next", 10, 50, 350)
        new = ds.Station("new", 20, 100, 50)
        self.assertTrue(is_station_too_far(c, new, next))

    def test_is_station_too_far_False(self):
        c = ds.Car(91, 20, 50, 65)
        next = ds.Station("next", 10, 50, 350)
        new = ds.Station("new", 20, 100, 50)
        self.assertFalse(is_station_too_far(c, new, next))


if __name__ == '__main__':
    unittest.main()
