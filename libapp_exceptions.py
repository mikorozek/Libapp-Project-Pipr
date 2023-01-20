class AvailableBookReservationError(Exception):
    """
    An exception class for indicating that a book is already available
    for reservation. This exception should be raised when a user attempts
    to reserve a book that is already available for renting.
    :param message: str, appropriate message that should be displayed
        to the user
    """
    def __init__(self, message):
        super().__init__(message)


class InvalidLoginError(Exception):
    """
    An exception class for indicating an invalid login attempt. This
    exception should be raised when a user attempts to log in with
    login that is not in library database.
    :param message: str, appropriate message that should be displayed
        to the user
    """
    def __init__(self, message):
        super().__init__(message)


class UnavailableBookError(Exception):
    """
    An exception class for indicating attempt of renting unavailable
    book. This exception should be raised when user tries to borrow
    book which has already been borrowed by user or somebody else.
    :param message: str, appropriate message that should be displayed
        to the user
    """
    def __init__(self, message):
        super().__init__(message)


class DoubleReservationError(Exception):
    """
    An exception class for indicating attempt of reserving already booked
    book. This exception should be raised when user tries to reserve book
    which he has already made reservation for.
    :param message: str, appropriate message that should be displayed
        to the user
    """
    def __init__(self, message):
        super().__init__(message)


class RentedBookReservationError(Exception):
    """
    An exception class for indicating attempt of reserving already borrowed
    book. This exception should be raised when user tries to reserve book
    which he has already borrowed.
    :param message: str, appropriate message that should be displayed
        to the user
    """
    def __init__(self, message):
        super().__init__(message)


class NoRenewalsError(Exception):
    """
    An exception class for indicating attempt of renewing renting that has no
    renewals left. This exception should be raised when user tries to renew
    renting that is not available to renew.
    :param message: str, appropriate message that should be displayed
        to the user
    """
    def __init__(self, message):
        super().__init__(message)


class InvalidDateSelectionError(Exception):
    """
    An exception class for indicating attempt of selecting day on calendar
    when user made no rentings. This exception should be raised when user
    clicks on calendar dat that is not highlighted.
    :param message: str, appropriate message that should be displayed
        to the user
    """
    def __init__(self, message):
        super().__init__(message)


class EmptyLineError(Exception):
    """
    An exception class for indicating attemption of adding element with empty
    line. This exception should be raised when user for example wants to add
    book to library with empty Title line.
    :param message: str, appropriate message that should be displayed
        to the user
    """
    def __init__(self, message):
        super().__init__(message)
