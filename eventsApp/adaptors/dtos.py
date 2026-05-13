from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class CreateEventDTO:
    event_title: str
    description: str
    organizer: int
    start_date: datetime
    end_date: datetime
    venue: str
    is_paid: bool
    maximum_attendees: int
    ticket_price: float

@dataclass
class CreateUserDTO:
    username: str
    email: str
    password: str
    phone_number: str
    role: str

@dataclass
class CreateBookingDto:
    event_id: int
    attendee_id: int

@dataclass
class CancelBookingDto:
    booking_id: int
    attendee_id: int
    event_id: int

@dataclass
class OrganizerDetailsDto:
    organizer_name: str
    organizer_email:str
    organizer_id: int

@dataclass
class AttendeeDetailsDto:
    attendee_id: int
    attendee_name: str
    attendee_email: str

@dataclass
class TicketDetailsDto:
    ticket_price: float

@dataclass
class EventDetailsDto:
    id: int
    event_title: str
    description: str
    start_date: datetime
    end_date: datetime
    venue: str
    maximum_attendees: int
    organizer_details: List[OrganizerDetailsDto]
    attendee_details: List[AttendeeDetailsDto]
    booking_cancelled_users: List[AttendeeDetailsDto]
    booking_pending_users: List[AttendeeDetailsDto]
    ticket_details: List[TicketDetailsDto]
    total_bookings_count: int
    cancelled_bookings_count: int
    pending_bookings_count: int
    available_seats: int

@dataclass
class FeedbackDto:
    rating: int
    comment: str
    event_id: int
    attendee_id: int
