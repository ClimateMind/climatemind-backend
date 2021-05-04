class CustomError(Exception):

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message


class UnauthorizedError(CustomError):
    status_code = 401


class InvalidUsageError(CustomError):
    status_code = 400


class DatabaseError(CustomError):
    status_code = 500


class AlreadyExistsError(CustomError):
    status_code = 409
