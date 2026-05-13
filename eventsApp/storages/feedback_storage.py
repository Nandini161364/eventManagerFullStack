from eventsApp.models import Event, Feedback, Booking, User

class FeedbackStorage:
    def is_valid_event(self, eventId):
        try:
            return Event.objects.get(id=eventId)
        except Event.DoesNotExist:
            return None 
    def is_valid_user(self, attendeeId):
        try:
            return User.objects.get(id=attendeeId)
        except User.DoesNotExist:
            return None
            
    def get_booking(self, feedbackDto):
        attendeeId = feedbackDto.attendee_id
        eventId = feedbackDto.event_id
        try:
            return Booking.objects.get(attendee__id=attendeeId, event__id = eventId, booking_status='booked')
        except Booking.DoesNotExist:
            return None
    
    def is_feedback_already_given(self, feedbackDto):
        attendeeId = feedbackDto.attendee_id
        eventId = feedbackDto.event_id
        return Feedback.objects.filter(booking__attendee__id=attendeeId, booking__event__id = eventId).exists()
        
        
    def create_feedback(self, feedbackDto):
        comment = feedbackDto.comment
        rating = feedbackDto.rating
        booking = self.get_booking(feedbackDto)

        newFeedback = Feedback.objects.create(
            rating=rating, comment=comment, booking=booking
        ) 
        
        return newFeedback.id
    def update_feedback(self, feedbackDto):
        attendeeId = feedbackDto.attendee_id
        eventId = feedbackDto.event_id
        comment = feedbackDto.comment
        rating = feedbackDto.rating

        existingFeedback = Feedback.objects.get(booking__attendee__id=attendeeId, booking__event__id = eventId)

        existingFeedback.rating = rating
        existingFeedback.comment = comment
        existingFeedback.save()
        
        return existingFeedback.id
