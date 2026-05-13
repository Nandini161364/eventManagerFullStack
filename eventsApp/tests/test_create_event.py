import pytest

from eventsApp.tests.factories import UserFactory
from eventsApp.adaptors.dtos import CreateEventDTO

from eventsApp.interactors.create_event_interactor import CreateEventInteractor
from eventsApp.storages.event_storage import EventStorage
from eventsApp.presenters.event_presenter import EventPresenter

from eventsApp.exceptions.exceptions import (
    InvalidDataException,
    OrganizerNotFoundException,
    UserCannotCreateEventException
)


@pytest.mark.django_db
class TestCreateEvent:

    def test_create_event_success(self):

        organizer = UserFactory(role='organizer')

        eventDto = CreateEventDTO(
            event_title="Standup",
            description="Testing",
            organizer=organizer.id,
            start_date="2026-05-10T10:00:00Z",
            end_date="2026-05-10T13:00:00Z",
            venue="Gachibowli",
            is_paid=False,
            maximum_attendees=100,
            ticket_price=0.0
        )

        interactor = CreateEventInteractor(
            storage=EventStorage(),
            presenter=EventPresenter()
        )

        response = interactor.create_event(eventDto)

        assert response["message"] == "Event Created Successfully"
        assert "id" in response


    def test_create_event_with_invalid_data(self):

        organizer = UserFactory(role='organizer')

        eventDto = CreateEventDTO(
            event_title="",
            description="Testing",
            organizer=organizer.id,
            start_date="2026-05-10T10:00:00Z",
            end_date="2026-05-10T13:00:00Z",
            venue="Gachibowli",
            is_paid=True,
            maximum_attendees=100,
            ticket_price=1000.0
        )

        interactor = CreateEventInteractor(
            storage=EventStorage(),
            presenter=EventPresenter()
        )

        with pytest.raises(InvalidDataException):
            interactor.create_event(eventDto)


    def test_create_event_with_invalid_organizer(self):

        eventDto = CreateEventDTO(
            event_title="Invalid Organizer",
            description="Testing",
            organizer=1000,
            start_date="2026-05-10T10:00:00Z",
            end_date="2026-05-10T13:00:00Z",
            venue="Gachibowli",
            is_paid=True,
            maximum_attendees=100,
            ticket_price=1000.0
        )

        interactor = CreateEventInteractor(
            storage=EventStorage(),
            presenter=EventPresenter()
        )

        with pytest.raises(OrganizerNotFoundException):
            interactor.create_event(eventDto)

    def test_attendee_cannot_create_event(self):

        attendee = UserFactory(role='attendee')

        eventDto = CreateEventDTO(
            event_title="Invalid Organizer",
            description="Testing",
            organizer=attendee.id,
            start_date="2026-05-10T10:00:00Z",
            end_date="2026-05-10T13:00:00Z",
            venue="Gachibowli",
            is_paid=True,
            maximum_attendees=100,
            ticket_price=1000.0
        )

        interactor = CreateEventInteractor(
            storage=EventStorage(),
            presenter=EventPresenter()
        )

        with pytest.raises(UserCannotCreateEventException):
            interactor.create_event(eventDto)

    def test_create_event_with_ticket_price_none(self):

        organizer = UserFactory(role='organizer')

        eventDto = CreateEventDTO(
            event_title="Standup",
            description="Testing",
            organizer=organizer.id,
            start_date="2026-05-10T10:00:00Z",
            end_date="2026-05-10T13:00:00Z",
            venue="Gachibowli",
            is_paid=True,
            maximum_attendees=100,
            ticket_price=None
        )

        interactor = CreateEventInteractor(
            storage=EventStorage(),
            presenter=EventPresenter()
        )

        with pytest.raises(InvalidDataException):
            interactor.create_event(eventDto)

    def test_create_event_with_is_paid_none(self):

        organizer = UserFactory(role='organizer')

        eventDto = CreateEventDTO(
            event_title="Standup",
            description="Testing",
            organizer=organizer.id,
            start_date="2026-05-10T10:00:00Z",
            end_date="2026-05-10T13:00:00Z",
            venue="Gachibowli",
            is_paid=None,
            maximum_attendees=100,
            ticket_price=1000.0
        )

        interactor = CreateEventInteractor(
            storage=EventStorage(),
            presenter=EventPresenter()
        )

        with pytest.raises(InvalidDataException):
            interactor.create_event(eventDto)
