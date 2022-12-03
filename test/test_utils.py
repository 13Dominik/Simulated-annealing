import unittest
from .. import data_structures as ds
from utils import any_station_too_far, fuel_amount_in_limit


class TestAny_station_too_far(unittest.TestCase):
    def test_station_too_far(self):
        c = ds.Car(0, 0)
        s1 = ds.Station("A", 10, 30, 0)
        s2 = ds.Station("B", 20, 40, 0)
        solution = ds.Solution(c)

        solution.add_station((s1, 10))
        solution.add_station((s2, 20))
        self.assertTrue(any_station_too_far(25, solution))

    def test_station_not_too_far(self):
        c = ds.Car(0, 0)
        s1 = ds.Station("A", 10, 30, 0)
        s2 = ds.Station("B", 20, 40, 0)
        solution = ds.Solution(c)

        solution.add_station((s1, 10))
        solution.add_station((s2, 20))
        self.assertFalse(any_station_too_far(45, solution))


class TestFuel_amount_in_limit(unittest.TestCase):
    def test_refueling_in_limit(self):
        c = ds.Car(30, 0)
        s1 = ds.Station("A", 10, 30, 0)
        s2 = ds.Station("B", 20, 40, 0)
        solution = ds.Solution(c)
        solution.add_station((s1, 15))
        solution.add_station((s2, 25))

        self.assertTrue(fuel_amount_in_limit(solution))

    def test_refueling_not_in_limit(self):
        c = ds.Car(20, 0)
        s1 = ds.Station("A", 10, 30, 0)
        s2 = ds.Station("B", 20, 40, 0)
        solution = ds.Solution(c)
        solution.add_station((s1, 15))
        solution.add_station((s2, 25))

        self.assertFalse(fuel_amount_in_limit(solution))


if __name__ == '__main__':
    unittest.main()
