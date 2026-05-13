from abc import ABC, abstractmethod
from eventsApp.adaptors.dtos import CreateBookingDto, CancelBookingDto

class BookingStorageInterface(ABC):
    @abstractmethod
    def get_attendee_by_id(self, attendee_id:int):
        pass
    @abstractmethod
    def get_event_by_id(self, event_id:int):
        pass

    @abstractmethod
    def create_booking(self, bookingDto:CreateBookingDto, booking_status:str):
        pass

    @abstractmethod
    def seats_available(self, event_id:int):
        pass

    @abstractmethod
    def is_already_booked(self, bookingDto:CreateBookingDto):
        pass

    @abstractmethod
    def get_booking_details_by_id(self, booking_id:int):
        pass

    @abstractmethod
    def cancel_booking(self, bookingDto:CancelBookingDto):
        pass
    @abstractmethod
    def is_pending_or_cancelled_booking_exists(self, bookingDto: CreateBookingDto):
        pass

    @abstractmethod
    def update_booking(self, bookingDto:CreateBookingDto):
        pass