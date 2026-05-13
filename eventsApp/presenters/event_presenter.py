from eventsApp.interactors.presenter_interfaces.event_presenter_interface import EventPresenterInterface

class EventPresenter(EventPresenterInterface):
    def create_event_success_response(self, eventId):
        return{
            "message": 'Event Created Successfully',
            "id": eventId
        }
    def organizer_not_found(self):
        return {
            "message": "No Organizer with mentioned Id"
        }
    def invalid_data(self):
        return {
            "message": "Please ensure all the required fields are passed with proper values"
        }
    def invalid_event(self):
        return {
            "message": "Event not found"
        }
    def no_access(self):
        return {
            "message": "User has no permission for event creation, organizer only can create"
        }
    def no_permission(self):
        return {
            "message": "User doesn't have permission to access the details"
        }

    def get_event_details_success_response(self, eventDetailsDto):
        return {
            'id': eventDetailsDto.id,
            'event_title': eventDetailsDto.event_title,
            'description': eventDetailsDto.description,
            'start_date': eventDetailsDto.start_date,
            'end_date': eventDetailsDto.end_date,
            'venue': eventDetailsDto.venue,
            'maximum_attendees': eventDetailsDto.maximum_attendees,
            'organizer_details': [
                {
                    'organizer_id': organizer.organizer_id,
                    'organizer_email':organizer.organizer_email,
                    'organizer_name': organizer.organizer_name,
                } for organizer in eventDetailsDto.organizer_details
            ],
            'attendee_details': [
                {
                    'attendee_id': attendee.attendee_id,
                    'attendee_email':attendee.attendee_email,
                    'attendee_name':attendee.attendee_name
                 } for attendee in eventDetailsDto.attendee_details
            ],
            'booking_cancelled_users': [
                {
                    'attendee_id': attendee.attendee_id,
                    'attendee_email':attendee.attendee_email,
                    'attendee_name':attendee.attendee_name
                 } for attendee in eventDetailsDto.booking_cancelled_users
            ],
            'booking_pending_users':[
                {
                    'attendee_id': attendee.attendee_id,
                    'attendee_email':attendee.attendee_email,
                    'attendee_name':attendee.attendee_name
                 } for attendee in eventDetailsDto.booking_pending_users
            ],
        
            'ticket_details': [
                {
                    'ticket_price': ticket.ticket_price
                } for ticket in eventDetailsDto.ticket_details
            ],
            'total_bookings_count': eventDetailsDto.total_bookings_count,
            'cancelled_bookings_count': eventDetailsDto.cancelled_bookings_count,
            'pending_bookings_count': eventDetailsDto.pending_bookings_count,
            'available_seats': eventDetailsDto.available_seats
        }
