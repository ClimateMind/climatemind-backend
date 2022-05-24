class CustomError(Exception):
    status_code = 500

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message


class UnauthorizedError(CustomError):
    status_code = 401


class InvalidUsageError(CustomError):
    status_code = 400


class DatabaseError(CustomError):
    pass


class OntologyError(CustomError):
    pass


class ForbiddenError(CustomError):
    status_code = 403


class NotInDatabaseError(CustomError):
    status_code = 404


class AlreadyExistsError(CustomError):
    status_code = 409
