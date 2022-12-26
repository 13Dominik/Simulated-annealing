import unittest
import src.data_structures as ds


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

    def test_solution_len(self):
        c = ds.Car(0, 0, 0, 0)
        s1 = ds.Station("A", 10, 0, 0)
        s2 = ds.Station("B", 20, 0, 0)

        solution1 = ds.Solution(c, [(s1, 10), (s2, 20)])
        self.assertEqual(len(solution1), 2)

    def test_solution_penalty_function(self):
        c = ds.Car(50, 10, 0, 40)
        s = ds.Solution(c)
        s1 = ds.Station("A", 10, 10, 100)
        s2 = ds.Station("B", 20, 20, 200)

        s.add_station((s1, 5))
        s.add_station((s2, 10))

        self.assertEqual(s.penalty_function, [22.5, 20])

    def test_solution_penalty_function2(self):
        c = ds.Car(50, 10, 0, 40)
        s = ds.Solution(c)
        s1 = ds.Station("A", 10, 10, 100)
        s2 = ds.Station("B", 20, 20, 200)

        s.add_station((s1, 5))
        s.add_station((s2, 10))

        self.assertEqual(s.get_penalty(), 42.5)

    def test_solution_remove(self):
        c = ds.Car(50, 10, 0, 40)
        s = ds.Solution(c)
        s1 = ds.Station("A", 10, 10, 100)
        s2 = ds.Station("B", 20, 20, 200)
        s3 = ds.Station("C", 30, 30, 300)

        s.add_station((s1, 5))
        s.add_station((s2, 10))
        s.add_station((s3, 29))
        s.remove_station(1)
        self.assertEqual(len(s), 2)

    def test_get_station_position(self):
        c = ds.Car(50, 10, 0, 40)
        s = ds.Solution(c)
        s1 = ds.Station("A", 10, 10, 100)
        s.add_station((s1, 20))
        self.assertEqual(s.get_station_position(0), 100)

    def test_get_station(self):
        c = ds.Car(50, 10, 0, 40)
        s = ds.Solution(c)
        s1 = ds.Station("A", 10, 10, 100)
        s.add_station((s1, 20))
        self.assertEqual(s.get_station(0), s1)

    def test_get_stations(self):
        c = ds.Car(50, 10, 0, 40)
        s = ds.Solution(c)
        s1 = ds.Station("A", 10, 10, 100)
        s2 = ds.Station("Z", 30, 40, 50)
        s.add_station((s1, 20))
        s.add_station((s2, 300))
        self.assertEqual(s.get_stations(), [s1, s2])


class TestCar(unittest.TestCase):
    def test_move_car_position(self):
        c = ds.Car(50, 10, 0, 40)
        s1 = ds.Station("A", 10, 5, 75)
        s2 = ds.Station("B", 20, 15, 200)

        c.move_car(s1)
        c.move_car(s2)
        self.assertEqual(c.curr_position, 200)

    def test_move_car_fuel_level(self):
        c = ds.Car(50, 10, 0, 40)
        s1 = ds.Station("A", 10, 10, 80)

        c.move_car(s1)
        self.assertEqual(c.curr_fuel_level, 49)

    def test_move_car_fuel_level2(self):
        c = ds.Car(50, 15, 0, 40)
        s1 = ds.Station("A", 10, 30, 80)

        c.move_car(s1)
        self.assertEqual(c.curr_fuel_level, 45.5)


class TestStation(unittest.TestCase):
    def test_equal(self):
        s1 = ds.Station("A", 30, 30, 40)
        s2 = ds.Station("A", 30, 30, 40)
        self.assertEqual(s1, s2)


if __name__ == '__main__':
    unittest.main()
