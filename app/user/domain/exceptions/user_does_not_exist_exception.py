class UserDoesNotExistException(Exception):
    """Base class for custom application exceptions."""

    def __init__(self):
        self.detail = "User does not exist"
