import factory
from datetime import timedelta

from eventsApp.models import User, Booking, Event, Ticket


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Sequence(lambda n: f"user{n}@example.com")

    role = factory.Iterator([
        'organizer',
        'attendee'
    ])

    phone_number = factory.Sequence(
        lambda n: f"98765432{n:02}"
    )

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        password = extracted if extracted else "password123"
        obj.set_password(password)
        if create:
            obj.save()


class TicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ticket

    price = factory.Faker(
        'pydecimal',
        left_digits=4,
        right_digits=2,
        positive=True
    )


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    event_title = factory.Sequence(
        lambda n: f"event{n}"
    )

    description = factory.Faker('text')

    organizer = factory.SubFactory(
        UserFactory,
        role='organizer'
    )

    start_date = factory.Faker(
        'future_datetime'
    )

    end_date = factory.LazyAttribute(
        lambda obj: obj.start_date + timedelta(hours=2)
    )

    venue = factory.Sequence(
        lambda n: f"venue{n}"
    )

    is_paid = factory.Faker('boolean')

    maximum_attendees = factory.Faker(
        'random_int',
        min=1,
        max=100
    )

    # ticket = factory.RelatedFactory(
    #     TicketFactory,
    #     factory_related_name='event'
    # )
    @factory.post_generation
    def ensure_ticket(self, create, extracted, **kwargs):
        if create:
            TicketFactory.create(event=self)


class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking

    attendee = factory.SubFactory(
        UserFactory,
        role='attendee'
    )

    event = factory.SubFactory(EventFactory)

    ticket = factory.LazyAttribute(
        lambda obj: obj.event.tickets.first()
    )

    booking_status = factory.Iterator([
        'booked',
        'pending',
        'cancelled'
    ])