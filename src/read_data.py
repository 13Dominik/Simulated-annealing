from typing import List, Tuple

from src.data_structures import Car, Station
from src.exceptions import WrongDataFormatError


def validate_txt_data(path) -> None:
    """
    Function to check if txt file with data have a correct format
    :param path: Path to file that should be validated
    :return: None if file format is correct
    """
    with open(path, "r") as file:
        lines = file.readlines()
    # Validating first line that should contain car parameters
    try:
        car_line = lines[0].split()
        assert len(car_line) == 4
        for param in car_line:
            assert param.isnumeric()
            assert float(param) >= 0
    except:
        raise WrongDataFormatError("Wrong data format in line 1 (car line)")

    # Validating blank lines
    try:
        assert lines[1].isspace()
        assert lines[3].isspace()
    except:
        raise WrongDataFormatError("Line 2 and 4 should be empty!")

    # Validating end point
    try:
        end_point_line = lines[2].strip()
        assert end_point_line.isnumeric()  # checking if end of route is int and positive
        assert int(end_point_line) > 0
    except:
        raise WrongDataFormatError("Wrong end point")

    # Validating stations
    # To hold on current line to inform user which line is potentially wrong
    current_line = 4  # to inform user we use numeration from 1
    for station_line in lines[4:]:
        current_line += 1
        try:
            station_line = station_line.split()
            assert len(station_line) == 4  # line should have 4 values
            for i in range(1, 4):
                assert station_line[i].isnumeric()  # checking if all is numeric and no negative
                assert int(station_line[i]) >= 0
        except:
            raise WrongDataFormatError(f"Wrong station format in line: {current_line}")


def read_txt(path) -> Tuple[List[Station], int, Car]:
    """
    Read Car, end Point and stations from txt file. File should look like an example_data.txt
    :param path: Path to file containing all the data
    :return: List of stations, end_point, car
    """
    # Validate file
    validate_txt_data(path)

    with open(path, 'r') as file:
        lines = file.readlines()
    car_string = lines[0].split()
    car = Car(int(car_string[0]), float(car_string[1]), float(car_string[2]), float(car_string[3]))

    end_point = int(lines[2])

    station_list = []
    for station_line in lines[4:]:
        station_line = station_line.split()
        station = Station(station_line[0], float(station_line[1]), float(station_line[2]), float(station_line[3]))
        station_list.append(station)
    return station_list, end_point, car
