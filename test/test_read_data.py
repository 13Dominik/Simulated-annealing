import unittest
import os

from src.read_data import validate_txt_data, read_txt
from src.exceptions import WrongDataFormatError
from src.data_structures import Car, Station


# It is needed because of test_data directory
if os.getcwd().endswith("test"):
    pass
else:
    os.chdir('test')


class TestValidateTxtData(unittest.TestCase):
    def test_wrong_car1(self):
        """Tank capacity is a string."""
        self.assertRaises(WrongDataFormatError, validate_txt_data, 'test_data/wrong_car_data1.txt')

    def test_wrong_car2(self):
        """One value is missing."""
        self.assertRaises(WrongDataFormatError, validate_txt_data, 'test_data/wrong_car_data2.txt')

    def test_wrong_blank_lines(self):
        """There is no blank line."""
        self.assertRaises(WrongDataFormatError, validate_txt_data, 'test_data/wrong_blank_lines.txt')

    def test_wrong_stations1(self):
        """There are no stations."""
        self.assertRaises(WrongDataFormatError, validate_txt_data, 'test_data/wrong_stations1.txt')

    def test_wrong_stations2(self):
        """Empty line between stations."""
        self.assertRaises(WrongDataFormatError, validate_txt_data, 'test_data/wrong_stations2.txt')

    def test_wrong_stations3(self):
        """Station with wrong argument"""
        self.assertRaises(WrongDataFormatError, validate_txt_data, 'test_data/wrong_stations3.txt')

    def test_wrong_stations4(self):
        """Station with missing argument"""
        self.assertRaises(WrongDataFormatError, validate_txt_data, 'test_data/wrong_stations4.txt')


class TestReadTxt(unittest.TestCase):
    def test_read_data1(self):
        c = Car(50, 10, 0, 20)
        s1 = Station("a", 10, 0, 200)
        s2 = Station("b", 20, 12, 1300)
        end_point = 1500
        self.assertEqual(([s1, s2], end_point, c), read_txt('test_data/example_data1.txt'))

    def test_read_data2(self):
        c = Car(30, 5, 0, 20)
        s1 = Station("AA", 30, 20, 300)
        s2 = Station("BB", 4, 0, 400)
        s3 = Station("CC", 12, 0, 500)
        end_point = 500
        self.assertEqual(([s1, s2, s3], end_point, c), read_txt('test_data/example_data2.txt'))


if __name__ == '__main__':
    unittest.main()
