class InvalidCredentialsException(Exception):
    """Base class for custom application exceptions."""

    def __init__(self):
        self.detail = "Invalid credentials"
