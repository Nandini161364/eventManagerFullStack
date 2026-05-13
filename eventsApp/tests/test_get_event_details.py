import pytest

from eventsApp.tests.factories import (
    BookingFactory,
    EventFactory,
    UserFactory
)

from eventsApp.interactors.get_event_details_interactor import GetEventDetailsInteractor
from eventsApp.storages.event_storage import EventStorage
from eventsApp.presenters.event_presenter import EventPresenter

from eventsApp.exceptions.exceptions import EventNotFoundException, UserCannotAccessEventException


@pytest.mark.django_db
class TestGetEventDetails:

    def test_get_event_details_success(self):

        organizer = UserFactory(role='organizer')
        event = EventFactory(
            organizer=organizer,
            event_title="Standup",
            venue="Gachibowli",
            maximum_attendees=100
        )
        booked_booking = BookingFactory(
            event=event,
            booking_status='booked'
        )
        cancelled_booking = BookingFactory(
            event=event,
            booking_status='cancelled'
        )
        pending_booking = BookingFactory(
            event=event,
            booking_status='pending'
        )

        interactor = GetEventDetailsInteractor(
            storage=EventStorage(),
            presenter=EventPresenter()
        )

        response = interactor.get_event_details(event.id, organizer.id)

        assert response["id"] == event.id
        assert response["event_title"] == "Standup"
        assert response["venue"] == "Gachibowli"
        assert response["maximum_attendees"] == 100
        assert response["organizer_details"][0]["organizer_id"] == organizer.id
        assert response["attendee_details"][0]["attendee_id"] == booked_booking.attendee.id
        assert response["booking_cancelled_users"][0]["attendee_id"] == cancelled_booking.attendee.id
        assert response["booking_pending_users"][0]["attendee_id"] == pending_booking.attendee.id
        assert response["ticket_details"][0]["ticket_price"] == event.tickets.first().price
        assert response["total_bookings_count"] == 1
        assert response["cancelled_bookings_count"] == 1
        assert response["pending_bookings_count"] == 1
        assert response["available_seats"] == 99

    def test_get_event_details_with_no_bookings(self):
        organizer = UserFactory(role='organizer')
        event = EventFactory(
            organizer=organizer,
            maximum_attendees=100
        )

        interactor = GetEventDetailsInteractor(
            storage=EventStorage(),
            presenter=EventPresenter()
        )

        response = interactor.get_event_details(event.id, organizer.id)

        assert response["attendee_details"] == []
        assert response["booking_cancelled_users"] == []
        assert response["booking_pending_users"] == []
        assert response["total_bookings_count"] == 0
        assert response["cancelled_bookings_count"] == 0
        assert response["pending_bookings_count"] == 0
        assert response["available_seats"] == 100

    def test_get_event_details_does_not_include_waitlisted_bookings(self):
        organizer = UserFactory(role='organizer')
        event = EventFactory(
            organizer=organizer,
            maximum_attendees=100
        )
        BookingFactory(
            event=event,
            booking_status='waitlisted'
        )

        interactor = GetEventDetailsInteractor(
            storage=EventStorage(),
            presenter=EventPresenter()
        )

        response = interactor.get_event_details(event.id, organizer.id)

        assert response["attendee_details"] == []
        assert response["booking_cancelled_users"] == []
        assert response["booking_pending_users"] == []
        assert response["total_bookings_count"] == 0
        assert response["available_seats"] == 100

    def test_get_event_details_with_invalid_event(self):

        interactor = GetEventDetailsInteractor(
            storage=EventStorage(),
            presenter=EventPresenter()
        )

        with pytest.raises(EventNotFoundException):
            interactor.get_event_details(1000, 1)

    def test_get_event_details_with_non_organizer(self):
        organizer = UserFactory(role='organizer')
        attendee = UserFactory(role='attendee')
        event = EventFactory(organizer=organizer)

        interactor = GetEventDetailsInteractor(
            storage=EventStorage(),
            presenter=EventPresenter()
        )

        with pytest.raises(UserCannotAccessEventException):
            interactor.get_event_details(event.id, attendee.id)
