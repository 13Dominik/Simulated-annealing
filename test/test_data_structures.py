import unittest
import data_structures as ds


class TestSolution(unittest.TestCase):
    def test_solution_init(self):
        c = ds.Car(0, 0, 0, 0)
        s1 = ds.Station("A", 10, 0, 0)
        s2 = ds.Station("B", 20, 0, 0)
        sol1 = ds.Solution(c)
        sol1.add_station((s1, 10))
        sol1.add_station((s2, 20))

        sol2 = ds.Solution(c, [(s1, 10), (s2, 20)])
        self.assertEqual(sol1.solution, sol2.solution)

    def test_solution_value_1(self):
        c = ds.Car(0, 0, 0, 0)
        s1 = ds.Station("A", 10, 0, 0)
        s2 = ds.Station("B", 20, 0, 0)
        solution = ds.Solution(c)

        solution.add_station((s1, 10))
        solution.add_station((s2, 20))
        self.assertEqual(solution.solution_value(), 500)

    def test_solution_value_2(self):
        c = ds.Car(0, 0, 0, 0)
        s1 = ds.Station("A", 11, 0, 0)
        s2 = ds.Station("B", 22, 0, 0)
        solution = ds.Solution(c)

        solution.add_station((s1, 10))
        solution.add_station((s2, 20))
        self.assertEqual(solution.solution_value(), 550)

    def test_solution_gt(self):
        c = ds.Car(0, 0, 0, 0)
        s1 = ds.Station("A", 11, 0, 0)
        s2 = ds.Station("B", 22, 0, 0)

        solution1 = ds.Solution(c, [(s1, 10), (s2, 20)])
        solution2 = ds.Solution(c, [(s1, 20), (s2, 30)])
        self.assertTrue(solution2 > solution1)

    def test_solution_ge(self):
        c = ds.Car(0, 0, 0, 0)
        s1 = ds.Station("A", 10, 0, 0)
        s2 = ds.Station("B", 20, 0, 0)

        solution1 = ds.Solution(c)
        solution2 = ds.Solution(c)
        solution1.add_station((s1, 10))
        solution1.add_station((s2, 20))
        solution2.add_station((s1, 10))
        solution2.add_station((s2, 20))
        self.assertTrue(solution2 >= solution1)

    def test_solution_lt(self):
        c = ds.Car(0, 0, 0, 0)
        s1 = ds.Station("A", 11, 0, 0)
        s2 = ds.Station("B", 22, 0, 0)

        solution1 = ds.Solution(c)
        solution2 = ds.Solution(c)
        solution1.add_station((s1, 10))
        solution1.add_station((s2, 20))
        solution2.add_station((s1, 5))
        solution2.add_station((s2, 5))
        self.assertTrue(solution2 < solution1)

    def test_solution_le(self):
        c = ds.Car(0, 0, 0, 0)
        s1 = ds.Station("A", 10, 0, 0)
        s2 = ds.Station("B", 20, 0, 0)

        solution1 = ds.Solution(c, [(s1, 10), (s2, 20)])
        solution2 = ds.Solution(c, [(s1, 10), (s2, 20)])
        self.assertTrue(solution2 <= solution1)

    def test_solution_penalty_function(self):
        c = ds.Car(50, 10, 0, 40)
        s = ds.Solution(c)
        s1 = ds.Station("A", 10, 10, 100)
        s2 = ds.Station("B", 20, 20, 200)

        s.add_station((s1, 5))
        s.add_station((s2, 10))

        self.assertEqual(s.penalty_function, 17.5)


class TestCar(unittest.TestCase):
    def test_move_car_position(self):
        c = ds.Car(50, 10, 0, 40)
        s1 = ds.Station("A", 10, 5, 75)
        s2 = ds.Station("B", 20, 15, 200)

        c.move_car((s1, 3))
        c.move_car((s2, 5))
        self.assertEqual(c.curr_position, 200)

    def test_move_car_fuel_level(self):
        c = ds.Car(50, 10, 0, 40)
        s1 = ds.Station("A", 10, 10, 80)
        s2 = ds.Station("B", 20, 15, 250)

        c.move_car((s1, 10))
        c.move_car((s2, 10))
        self.assertEqual(c.curr_fuel_level, 30)


if __name__ == '__main__':
    unittest.main()
