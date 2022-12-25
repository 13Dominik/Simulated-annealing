class WrongDataFormatError(Exception):
    """
    Raised when txt file with Car, Stations and end_point have a wrong format or missing data
    """
    pass


class NoStationsError(Exception):
    """
    Raised when we cannot find a station that we can get to from current position.
    """

    def __init__(self, message, position):
        super().__init__(message)
        self.message = message
        self.position = position

    def __str__(self):
        return f"No stations to go from {self.position}"
