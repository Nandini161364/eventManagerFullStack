from eventsApp.interactors.storage_interfaces.event_storage_interface import EventStorageInterface
from eventsApp.interactors.presenter_interfaces.event_presenter_interface import EventPresenterInterface

from eventsApp.exceptions.exceptions import OrganizerNotFoundException, InvalidDataException, UserCannotCreateEventException

class CreateEventInteractor:
    def __init__(self, storage:EventStorageInterface, presenter: EventPresenterInterface):
        self.storage = storage
        self.presenter = presenter

    def create_event(self, eventDto):
        event_title = eventDto.event_title
        description = eventDto.description
        organizer = eventDto.organizer
        is_paid = eventDto.is_paid
        start_date = eventDto.start_date
        end_date = eventDto.end_date
        maximum_attendees = eventDto.maximum_attendees
        venue = eventDto.venue
        ticket_price = eventDto.ticket_price

        organizer = self.storage.get_organizer(organizer)

        if not organizer:
            raise OrganizerNotFoundException("Organizer is not found")
        if organizer.role != 'organizer':
            raise UserCannotCreateEventException('Only organizer can create the event')
        if not (event_title and description and start_date and organizer and end_date and venue and maximum_attendees):
            raise InvalidDataException("Data can't be empty")
        if ticket_price is None:
            raise InvalidDataException("Data can't be empty")
        if is_paid is None:
            raise InvalidDataException("Data can't be empty")
        
        newEvent = self.storage.create_event(eventDto)
        self.storage.create_ticket(
            event_id=newEvent,
            price=eventDto.ticket_price
        )

        return self.presenter.create_event_success_response(newEvent)
        
