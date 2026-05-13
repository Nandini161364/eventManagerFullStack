from eventsApp.adaptors.dtos import CreateEventDTO
from abc import ABC, abstractmethod


class EventStorageInterface(ABC):
    @abstractmethod
    def create_event(self, event_dto: CreateEventDTO):
        pass
    @abstractmethod
    def get_organizer(self, organizerId: int):
        pass
    @abstractmethod
    def create_ticket(self, event_id: int, price: float):
        pass
    @abstractmethod
    def get_event_details(self, event_id:int):
        pass

    @abstractmethod
    def is_valid_event(self, event_id:int):
        pass
    
    @abstractmethod
    def is_organizer(self, event_id:int, user_id: int):
        pass