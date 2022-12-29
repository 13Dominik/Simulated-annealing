import unittest
import src.sa_algorithm as sa
import src.data_structures as ds
import src.exceptions as ex


class TestInitSolution(unittest.TestCase):
    def test_init_no_stations_at_start(self):
        c = ds.Car(50, 15, 0, 30)
        s1 = ds.Station("A", 0, 10, 201)
        s2 = ds.Station("B", 0, 10, 202)
        self.assertRaises(ex.NoStationsError, sa.init_solution, c, 300, 20, [s1, s2])

    def test_init_no_station_step1(self):
        c = ds.Car(50, 15, 0, 30)
        s1 = ds.Station("A", 0, 10, 100)
        s2 = ds.Station("B", 0, 10, 500)
        self.assertRaises(ex.NoStationsError, sa.init_solution, c, 600, 20, [s1, s2])

    def test_init_no_station_step2(self):
        c = ds.Car(50, 15, 0, 30)
        s1 = ds.Station("A", 0, 10, 100)
        s2 = ds.Station("B", 0, 10, 200)
        s3 = ds.Station("C", 0, 10, 700)
        self.assertRaises(ex.NoStationsError, sa.init_solution, c, 700, 20, [s1, s2, s3])


if __name__ == '__main__':
    unittest.main()
