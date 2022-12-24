class NoStationsError(Exception):
    def __init__(self, message, position):
        super().__init__(message)
        self.message = message
        self.position = position

    def __str__(self):
        return f"No stations to go from {self.position}"
