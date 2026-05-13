import pytest

from eventsApp.tests.factories import (
    BookingFactory,
    EventFactory,
    UserFactory
)

from eventsApp.adaptors.dtos import FeedbackDto
from eventsApp.models import Feedback

from eventsApp.interactors.feedback_interactor import FeedBackInteractor
from eventsApp.storages.feedback_storage import FeedbackStorage
from eventsApp.presenters.feedback_presenter import FeedbackPresenter

from eventsApp.exceptions.exceptions import (
    AttendeeDoesnotExist,
    EventNotFoundException,
    InvalidBookingException,
    InvalidDataException
)


@pytest.mark.django_db
class TestFeedback:

    def test_create_feedback_success(self):

        booking = BookingFactory(booking_status='booked')

        feedbackDto = FeedbackDto(
            rating=5,
            comment="Good event",
            event_id=booking.event.id,
            attendee_id=booking.attendee.id
        )

        interactor = FeedBackInteractor(
            storage=FeedbackStorage(),
            presenter=FeedbackPresenter()
        )

        response = interactor.create_feedback(feedbackDto)

        assert response["message"] == "Feedback given Successfully"
        assert "id" in response

    def test_create_feedback_with_invalid_user(self):

        event = EventFactory()

        feedbackDto = FeedbackDto(
            rating=5,
            comment="Good event",
            event_id=event.id,
            attendee_id=1000
        )

        interactor = FeedBackInteractor(
            storage=FeedbackStorage(),
            presenter=FeedbackPresenter()
        )

        with pytest.raises(AttendeeDoesnotExist):
            interactor.create_feedback(feedbackDto)

    def test_create_feedback_with_invalid_event(self):

        attendee = UserFactory(role='attendee')

        feedbackDto = FeedbackDto(
            rating=5,
            comment="Good event",
            event_id=1000,
            attendee_id=attendee.id
        )

        interactor = FeedBackInteractor(
            storage=FeedbackStorage(),
            presenter=FeedbackPresenter()
        )

        with pytest.raises(EventNotFoundException):
            interactor.create_feedback(feedbackDto)

    def test_create_feedback_with_invalid_data(self):

        booking = BookingFactory(booking_status='booked')

        feedbackDto = FeedbackDto(
            rating=None,
            comment="Good event",
            event_id=booking.event.id,
            attendee_id=booking.attendee.id
        )

        interactor = FeedBackInteractor(
            storage=FeedbackStorage(),
            presenter=FeedbackPresenter()
        )

        with pytest.raises(InvalidDataException):
            interactor.create_feedback(feedbackDto)

    def test_create_feedback_without_booking(self):

        attendee = UserFactory(role='attendee')
        event = EventFactory()

        feedbackDto = FeedbackDto(
            rating=5,
            comment="Good event",
            event_id=event.id,
            attendee_id=attendee.id
        )

        interactor = FeedBackInteractor(
            storage=FeedbackStorage(),
            presenter=FeedbackPresenter()
        )

        with pytest.raises(InvalidBookingException):
            interactor.create_feedback(feedbackDto)

    def test_create_feedback_updates_existing_feedback(self):

        booking = BookingFactory(booking_status='booked')
        existing_feedback = Feedback.objects.create(
            booking=booking,
            rating=3,
            comment="Average event"
        )

        feedbackDto = FeedbackDto(
            rating=5,
            comment="Good event",
            event_id=booking.event.id,
            attendee_id=booking.attendee.id
        )

        interactor = FeedBackInteractor(
            storage=FeedbackStorage(),
            presenter=FeedbackPresenter()
        )

        response = interactor.create_feedback(feedbackDto)

        existing_feedback.refresh_from_db()

        assert response["id"] == existing_feedback.id
        assert existing_feedback.rating == 5
        assert existing_feedback.comment == "Good event"

    def test_create_feedback_with_pending_booking(self):

        booking = BookingFactory(booking_status='pending')

        feedbackDto = FeedbackDto(
            rating=5,
            comment="Good event",
            event_id=booking.event.id,
            attendee_id=booking.attendee.id
        )

        interactor = FeedBackInteractor(
            storage=FeedbackStorage(),
            presenter=FeedbackPresenter()
        )

        with pytest.raises(InvalidBookingException):
            interactor.create_feedback(feedbackDto)
