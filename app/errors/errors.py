class CustomError(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.status_code = 500
        self.message = message


class UnauthorizedError(CustomError):
    self.status_code = 401


class InvalidUsageError(CustomError):
    self.status_code = 400


class DatabaseError(CustomError):
    self.status_code = 500


class AlreadyExistsError(CustomError):
    self.status_code = 409
