from unittest.mock import patch

import pytest

from eventsApp.tests.factories import (
    BookingFactory,
    UserFactory,
    EventFactory
)

from eventsApp.adaptors.dtos import CreateBookingDto
from eventsApp.adaptors.dtos import CancelBookingDto
from eventsApp.models import Booking

from eventsApp.interactors.booking_interactor import BookingInteractor
from eventsApp.storages.booking_storage import BookingStorage
from eventsApp.presenters.booking_presenter import BookingPresenter

from eventsApp.exceptions.exceptions import (
    InvalidDataException,
    EventDoesnotExistException,
    AttendeeDoesnotExist,
    TicketsNotAvailableException,
    AlreadyBookedException,
    InvalidBookingIdException
)


@pytest.mark.django_db
class TestCreateBooking:

    @patch('eventsApp.interactors.booking_interactor.EmailService.send_booking_confirmation')
    def test_create_booking_success(self, mock_send_email):

        attendee = UserFactory(role='attendee')

        event = EventFactory()

        bookingDto = CreateBookingDto(
            attendee_id=attendee.id,
            event_id=event.id
        )

        interactor = BookingInteractor(
            storage=BookingStorage(),
            presenter=BookingPresenter()
        )

        response = interactor.create_booking(
            bookingDto
        )

        assert response["message"] == "Booking Successful"
        assert "id" in response
        mock_send_email.assert_called_once()
    def test_create_booking_with_invalid_user(self):
        event = EventFactory()

        bookingDto = CreateBookingDto(
            attendee_id=100,
            event_id=event.id
        )

        interactor = BookingInteractor(
            storage=BookingStorage(),
            presenter=BookingPresenter()
        )

        with pytest.raises(AttendeeDoesnotExist):
            interactor.create_booking(bookingDto)
    def test_create_booking_with_invalid_event(self):
        user = UserFactory()
        event = EventFactory()

        bookingDto = CreateBookingDto(
            attendee_id=user.id,
            event_id=100
        )

        interactor = BookingInteractor(
            storage=BookingStorage(),
            presenter=BookingPresenter()
        )

        with pytest.raises(EventDoesnotExistException):
            interactor.create_booking(bookingDto)
    @patch('eventsApp.interactors.booking_interactor.EmailService.send_booking_confirmation')
    def test_create_booking_for_same_event(self, mock_send_email):
        user = UserFactory()
        event = EventFactory()

        bookingDto = CreateBookingDto(
            attendee_id=user.id,
            event_id=event.id
        )

        interactor = BookingInteractor(
            storage=BookingStorage(),
            presenter=BookingPresenter()
        )

        interactor.create_booking(
            bookingDto
        )

        with pytest.raises(AlreadyBookedException):
            interactor.create_booking(bookingDto)

    @patch('eventsApp.interactors.booking_interactor.EmailService.send_booking_confirmation')
    def test_tickets_full(self, mock_send_email):
        event = EventFactory(maximum_attendees=1)

        user1 = UserFactory(role='attendee')
        user2 = UserFactory(role='attendee')

        interactor = BookingInteractor(BookingStorage(), BookingPresenter())

        bookingDto1 = CreateBookingDto(
            attendee_id=user1.id,
            event_id=event.id
        )
        interactor.create_booking(bookingDto1)

        bookingDto2 = CreateBookingDto(
            attendee_id=user2.id,
            event_id=event.id
        )

        with pytest.raises(TicketsNotAvailableException):
            interactor.create_booking(bookingDto2)

        assert Booking.objects.filter(
            event=event,
            attendee=user2,
            booking_status='waitlisted'
        ).exists()

    @patch('eventsApp.interactors.booking_interactor.EmailService.send_booking_confirmation')
    def test_cancelled_booking_gets_booked_again(self, mock_send_email):
        booking = BookingFactory(booking_status='cancelled')

        bookingDto = CreateBookingDto(
            attendee_id=booking.attendee.id,
            event_id=booking.event.id
        )

        interactor = BookingInteractor(
            storage=BookingStorage(),
            presenter=BookingPresenter()
        )

        response = interactor.create_booking(bookingDto)

        booking.refresh_from_db()

        assert response["message"] == "Booking Successful"
        assert booking.booking_status == 'booked'

    def test_cancel_booking_success(self):
        booking = BookingFactory(booking_status='booked')

        cancelBookingDto = CancelBookingDto(
            booking_id=booking.id,
            attendee_id=booking.attendee.id,
            event_id=booking.event.id
        )

        interactor = BookingInteractor(
            storage=BookingStorage(),
            presenter=BookingPresenter()
        )

        response = interactor.cancel_booking(cancelBookingDto)

        booking.refresh_from_db()

        assert response["message"] == "Booking got Cancelled Successfully"
        assert booking.booking_status == 'cancelled'

    def test_cancel_booking_with_invalid_booking_id(self):
        attendee = UserFactory(role='attendee')
        event = EventFactory()

        cancelBookingDto = CancelBookingDto(
            booking_id=1000,
            attendee_id=attendee.id,
            event_id=event.id
        )

        interactor = BookingInteractor(
            storage=BookingStorage(),
            presenter=BookingPresenter()
        )

        with pytest.raises(InvalidBookingIdException):
            interactor.cancel_booking(cancelBookingDto)

    def test_cancel_booking_with_invalid_attendee(self):
        booking = BookingFactory(booking_status='booked')

        cancelBookingDto = CancelBookingDto(
            booking_id=booking.id,
            attendee_id=1000,
            event_id=booking.event.id
        )

        interactor = BookingInteractor(
            storage=BookingStorage(),
            presenter=BookingPresenter()
        )

        with pytest.raises(AttendeeDoesnotExist):
            interactor.cancel_booking(cancelBookingDto)

    def test_cancel_booking_promotes_first_waitlisted_user(self):
        event = EventFactory(maximum_attendees=1)
        booked_booking = BookingFactory(event=event, booking_status='booked')
        waitlisted_booking = BookingFactory(event=event, booking_status='waitlisted')

        cancelBookingDto = CancelBookingDto(
            booking_id=booked_booking.id,
            attendee_id=booked_booking.attendee.id,
            event_id=event.id
        )

        interactor = BookingInteractor(
            storage=BookingStorage(),
            presenter=BookingPresenter()
        )

        interactor.cancel_booking(cancelBookingDto)

        booked_booking.refresh_from_db()
        waitlisted_booking.refresh_from_db()

        assert booked_booking.booking_status == 'cancelled'
        assert waitlisted_booking.booking_status == 'booked'
