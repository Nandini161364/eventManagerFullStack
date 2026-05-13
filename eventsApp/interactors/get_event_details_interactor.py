from eventsApp.interactors.storage_interfaces.event_storage_interface import EventStorageInterface
from eventsApp.interactors.presenter_interfaces.event_presenter_interface import EventPresenterInterface

from eventsApp.exceptions.exceptions import EventNotFoundException, UserCannotAccessEventException

class GetEventDetailsInteractor:
    def __init__(self, storage:EventStorageInterface, presenter:EventPresenterInterface):
        self.storage = storage
        self.presenter = presenter

    def get_event_details(self, eventId, userId):
        is_valid_event = self.storage.is_valid_event(event_id=eventId)
        is_organizer = self.storage.is_organizer(eventId, userId)
        if not is_valid_event:
            raise EventNotFoundException("Invalid Event Details")
        if not is_organizer:
            raise UserCannotAccessEventException("no permission")
        
        eventDetailsDto = self.storage.get_event_details(eventId)
        return self.presenter.get_event_details_success_response(eventDetailsDto)
    