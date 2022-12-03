import unittest
from .. import data_structures as ds
from utils import any_station_too_far, fuel_amount_in_limit


class TestSolution(unittest.TestCase):
    def test_solution_value_1(self):
        c = ds.Car(0, 0)
        s1 = ds.Station("A", 10, 0, 0)
        s2 = ds.Station("B", 20, 0, 0)
        solution = ds.Solution(c)

        solution.add_station((s1, 10))
        solution.add_station((s2, 20))
        self.assertEqual(solution.solution_value(), 500)

    def test_solution_value_2(self):
        c = ds.Car(0, 0)
        s1 = ds.Station("A", 11, 0, 0)
        s2 = ds.Station("B", 22, 0, 0)
        solution = ds.Solution(c)

        solution.add_station((s1, 10))
        solution.add_station((s2, 20))
        self.assertEqual(solution.solution_value(), 550)


if __name__ == '__main__':
    unittest.main()
