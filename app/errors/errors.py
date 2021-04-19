class CustomError(Exception):
    status_code = 500

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message


class InvalidUsageError(CustomError):
    status_code = 400


class DatabaseError(CustomError):
    status_code = 500


class AlreadyExistsError(CustomError):
    status_code = 409
