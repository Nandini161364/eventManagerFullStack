class OrganizerNotFoundException(Exception):
    pass

class InvalidDataException(Exception):
    pass

class UserAlreadyExitsException(Exception):
    pass

class EventDoesnotExistException(Exception):
    pass

class AttendeeDoesnotExist(Exception):
    pass

class TicketsNotAvailableException(Exception):
    pass

class AlreadyBookedException(Exception):
    pass

class InvalidBookingIdException(Exception):
    pass

class EventNotFoundException(Exception):
    pass

class InvalidBookingException(Exception):
    pass

class UserCannotCreateEventException(Exception):
    pass
class UserCannotAccessEventException(Exception):
    pass