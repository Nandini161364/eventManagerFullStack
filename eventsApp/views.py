# from oauth2_provider.contrib.rest_framework import OAuth2Authentication
# from oauth2_provider.decorators import protected_resource

import sentry_sdk
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes

from rest_framework.decorators import api_view
from rest_framework.response import Response


from eventsApp.adaptors.dtos import CreateEventDTO, CreateUserDTO, CreateBookingDto, CancelBookingDto, FeedbackDto

from eventsApp.storages.event_storage import EventStorage
from eventsApp.storages.user_storage import UserStorage
from eventsApp.storages.booking_storage import BookingStorage
from eventsApp.storages.feedback_storage import FeedbackStorage

from eventsApp.presenters.event_presenter import EventPresenter
from eventsApp.presenters.user_presenter import UserPresenter
from eventsApp.presenters.booking_presenter import BookingPresenter
from eventsApp.presenters.feedback_presenter import FeedbackPresenter

from eventsApp.interactors.create_event_interactor import CreateEventInteractor
from eventsApp.interactors.user_interactor import CreateUserInteractor
from eventsApp.interactors.booking_interactor import BookingInteractor
from eventsApp.interactors.get_event_details_interactor import GetEventDetailsInteractor
from eventsApp.interactors.feedback_interactor import FeedBackInteractor

from eventsApp.exceptions.exceptions import OrganizerNotFoundException, InvalidDataException, UserAlreadyExitsException, EventDoesnotExistException, AttendeeDoesnotExist, TicketsNotAvailableException, AlreadyBookedException, InvalidBookingIdException, EventNotFoundException, InvalidBookingException, UserCannotCreateEventException, UserCannotAccessEventException

from django.contrib.auth import get_user_model
from eventsApp.models import Booking, Event, Ticket
User = get_user_model()


def serialize_event(event, user):
    user_booking = Booking.objects.filter(event=event, attendee=user).first()

    ticket = event.tickets.first()

    return {
        "id": event.id,
        "event_title": event.event_title,
        "description": event.description,
        "start_date": event.start_date,
        "end_date": event.end_date,
        "venue": event.venue,
        "is_paid": event.is_paid,
        "maximum_attendees": event.maximum_attendees,
        "available_seats": event.maximum_attendees - event.bookings.filter(booking_status='booked').count(),
        "ticket_price": ticket.price if ticket else 0,
        "organizer_name": event.organizer.username,
        "booking_id": user_booking.id if user_booking else None,
        "booking_status": user_booking.booking_status if user_booking else None,
    }


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user

    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "phone_number": user.phone_number,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_events(request):
    user = request.user

    if user.role == 'organizer':
        events = Event.objects.filter(organizer=user).select_related('organizer').prefetch_related('tickets', 'bookings').order_by('-start_date')
        booked_events = Event.objects.filter(bookings__attendee=user).select_related('organizer').prefetch_related('tickets', 'bookings').distinct().order_by('-start_date')

        return Response({
            "events": [serialize_event(event, user) for event in events],
            "booked_events": [serialize_event(event, user) for event in booked_events],
        })
    else:
        events = Event.objects.filter(is_active=True).select_related('organizer').prefetch_related('tickets', 'bookings').order_by('start_date')

    return Response({
        "events": [serialize_event(event, user) for event in events],
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event(request):
    try:
        event_title = request.data.get("event_title")
        description = request.data.get("description")
        organizer = request.user
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")
        venue = request.data.get("venue")
        is_paid = request.data.get("is_paid")
        maximum_attendees = request.data.get("maximum_attendees")
        ticket_price = request.data.get("ticket_price")

        eventDto = CreateEventDTO(
            event_title,description,organizer.id,start_date,end_date,venue,is_paid,maximum_attendees, ticket_price = ticket_price
        )

        interactor = CreateEventInteractor(storage=EventStorage(), presenter=EventPresenter())
        response = interactor.create_event(eventDto)


        return Response(response, 200)
    
    except OrganizerNotFoundException as e:
        return Response(EventPresenter().organizer_not_found(), status=400)
    except InvalidDataException as e:
        return Response(EventPresenter().invalid_data(), status=400)
    except UserCannotCreateEventException as e:
        return Response(EventPresenter().no_access(), status=403)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        role = request.data.get("role")
        phone_number = request.data.get("phone_number")

        user = CreateUserDTO(
            username=username,
            password=password,
            email=email,
            role=role,
            phone_number=phone_number
        )
        interactor = CreateUserInteractor(storage=UserStorage(), presenter=UserPresenter())
        response = interactor.create_user(user)

        return Response(response, 200)

    except UserAlreadyExitsException as e:
        return Response(UserPresenter().invalid_mail(str(e)), 400)
    except InvalidDataException as e:
        return Response(UserPresenter().invalid_data(), 400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def event_booking(request):
    try:
        event_id = request.data.get('event_id')
        attendee_id = request.user.id

        bookingDto = CreateBookingDto(
            event_id,
            attendee_id
        )
        interactor = BookingInteractor(storage=BookingStorage(), presenter=BookingPresenter())

        response = interactor.create_booking(bookingDto)

        return Response(response, 200)

    except InvalidDataException as e:
        return Response(BookingPresenter().invalid_data(), 400)
    except AlreadyBookedException as e:
        return Response(BookingPresenter().already_booked(), 400)
    except EventDoesnotExistException as e:
        return Response(BookingPresenter().invalid_event(), 400)
    except AttendeeDoesnotExist as e:
        return Response(BookingPresenter().invalid_attendee(), 400)
    except TicketsNotAvailableException as e:
        sentry_sdk.capture_exception(e)
        return Response(BookingPresenter().seats_full(), 400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_booking(request):
    try:
        booking_id = request.data.get("booking_id")
        event_id = request.data.get("event_id")
        attendee_id = request.user.id
        cancelBookingDto = CancelBookingDto(booking_id, attendee_id, event_id)

        interactor = BookingInteractor(storage=BookingStorage(), presenter=BookingPresenter())
        response = interactor.cancel_booking(cancelBookingDto)

        return Response(response, 200)
    except AttendeeDoesnotExist as e:
        return Response(BookingPresenter().invalid_attendee(), 400)
    except InvalidDataException as e:
        return Response(BookingPresenter().invalid_data(), 400)
    except InvalidBookingIdException as e:
        return Response(BookingPresenter().invalid_booking(), 400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_event_details(request, event_id):
    try:
        user_id = request.user.id
        interactor = GetEventDetailsInteractor(storage=EventStorage(), presenter = EventPresenter())

        response = interactor.get_event_details(event_id, user_id)

        return Response(response, 200)
    except EventNotFoundException as e:
        return Response(EventPresenter().invalid_event(), 400)
    except UserCannotAccessEventException as e:
        return Response(EventPresenter().no_permission(), 403)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def give_feedback(request):
    try:
        rating = request.data.get('rating')
        comment = request.data.get('comment')
        event_id = request.data.get('event_id')
        attendee_id = request.user.id

        feedbackDto = FeedbackDto(
            rating, comment, event_id, attendee_id
        )

        interactor = FeedBackInteractor(storage=FeedbackStorage(), presenter=FeedbackPresenter())

        response = interactor.create_feedback(feedbackDto)

        return Response(response, 200)
    except InvalidDataException as e:
        return Response(FeedbackPresenter().invalid_data(), 400)
    except EventNotFoundException as e:
        return Response(FeedbackPresenter().invalid_event(), 400)
    except AttendeeDoesnotExist as e:
        return Response(FeedbackPresenter().invalid_user(), 400)
    except InvalidBookingException as e:
        return Response(FeedbackPresenter().invalid_booking(), 400)

@api_view(['POST'])
def make_superuser(request):

    email = request.data.get("email")

    user = User.objects.get(email=email)

    user.is_staff = True
    user.is_superuser = True
    user.save()

    return Response({
        "message": "User promoted successfully"
    })
        
