from eventsApp.models import Event, User, Ticket, Booking
from django.db.models import Q

class BookingStorage:
    def get_event_by_id(self, event_id):
        try:
            return Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return None
    def get_attendee_by_id(self, attendee_id):
        try:
            return User.objects.get(id=attendee_id)
        except User.DoesNotExist:
            return None
    
    def seats_available(self, event_id):
        event = self.get_event_by_id(event_id)
        if not event:
            return None
        maximum_seats =  event.maximum_attendees
        current_seats_count = Booking.objects.filter(event_id=event_id, booking_status = "booked").count()

        if current_seats_count< maximum_seats:
            return True
        else:

            return False
    
    def is_already_booked(self, bookingDto):
        try:
            return Booking.objects.filter(
                event_id = bookingDto.event_id,
                attendee_id = bookingDto.attendee_id,
                booking_status = 'booked'
            ).exists()
        except Booking.DoesNotExist:
            return None
        
    def is_pending_or_cancelled_booking_exists(self, bookingDto):
        try:
            return Booking.objects.filter(
                Q(booking_status = 'pending') | Q(booking_status = 'cancelled'),
                event_id = bookingDto.event_id,
                attendee_id = bookingDto.attendee_id
            ).exists()
        except Booking.DoesNotExist:
            return None

    def create_booking(self, bookingDto, bookingStatus):
        self.bookingDto = bookingDto
        event_id = bookingDto.event_id
        attendee_id = bookingDto.attendee_id
        ticket = Ticket.objects.get(event_id=event_id)

        response = Booking.objects.create(
            attendee_id = attendee_id,
            event_id = event_id,
            booking_status = bookingStatus,
            ticket=ticket
        )

        return response.id
    
    def update_booking(self, bookingDto):
        event_id = bookingDto.event_id
        attendee_id = bookingDto.attendee_id
        try:
            existing_booking = Booking.objects.get(Q(event_id= event_id), Q(attendee_id=attendee_id))
        except Booking.DoesNotExist:
            return None

        existing_booking.booking_status = 'booked'
        existing_booking.save()
        return existing_booking.id

        
    def get_booking_details_by_id(self, booking_id):
        try:
            return Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return None
                
    def cancel_booking(self, bookingDto):
        booking_id = bookingDto.booking_id
        attendee_id = bookingDto.attendee_id
        event_id = bookingDto.event_id
        try:
            existing_booking = Booking.objects.get(Q(id=booking_id), Q(attendee_id=attendee_id))
        except Booking.DoesNotExist:
            return None

        if existing_booking.booking_status == 'cancelled':
            print("Already Cancelled")
            return False

        existing_booking.booking_status = 'cancelled'
        existing_booking.save()
        
        first_waitlisted_user = Booking.objects.filter(event_id=event_id, booking_status='waitlisted').order_by('booking_date').first()
        
        if first_waitlisted_user:
            first_waitlisted_user.booking_status = 'booked'
            first_waitlisted_user.save()

        return True
