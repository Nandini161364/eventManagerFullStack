class BookingPresenter:
    def booking_success(self, bookingId):
        return {
            "message": "Booking Successful",
            "id": bookingId
        }

    def invalid_data(self):
        return {
            "message": "Event Id or Attendee Id can't be empty"
        }
    
    def invalid_event(self):
        return {
            "message": "Event details are not valid"
        }
    
    def invalid_attendee(self):
        return {
            "message": "Attendee details are not valid"
        }
    def seats_full(self):
        return {
            "message": "Your booking is waitlisted as Tickets are already full"
        }
    def already_booked(self):
        return {
            "message": "Already Registered for the Event"
        }
    def booking_cancelled(self):
        return {
            "message": "Booking got Cancelled Successfully"
        }
    def invalid_booking(self):
        return {
            "message": "Invalid Booking Id"
        }