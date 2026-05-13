class FeedbackPresenter:
    def create_feedback_response(self, feedbackId):
        return {
            "message": "Feedback given Successfully",
            "id": feedbackId
        }
    
    def invalid_user(self):
        return {
            "message": "Invalid User"
        }
    
    def invalid_event(self):
        return {
            "message": "Event not found"
        }
    
    def invalid_data(self):
        return{
            "message": "Rating or Comment can not be empty"
        }
    
    def invalid_booking(self):
        return {
            "message": "Invalid booking details"
        }