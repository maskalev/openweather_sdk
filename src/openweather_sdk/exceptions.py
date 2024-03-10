class ClientBaseException(Exception):
    pass


class ClientAlreadyExistsException(ClientBaseException):
    def __init__(self):
        super().__init__("Client already exists")


class ClientDoesntExistException(ClientBaseException):
    def __init__(self):
        super().__init__("Client doesn't exist")


class BadResponseException(ClientBaseException):
    def __init__(self, code, message):
        super().__init__(f"Code: {code}, message: {message}")


class InvalidLocationException(ClientBaseException):
    def __init__(self):
        super().__init__("Invalid location")


class AttributeValidationException(ClientBaseException):
    def __init__(self, name, values):
        super().__init__(f"{name} must be one of {', '.join(values)}")


class UnexpectedException(ClientBaseException):
    def __init__(self, message):
        super().__init__(f"Unexpected error! Error: {message}")
