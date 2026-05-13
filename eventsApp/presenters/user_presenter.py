class UserPresenter:
    def create_user_success_response(self, userId):
        return {
            "message": "User created Successfully",
            "id": userId
        }
    def invalid_data(self):
        return {
            "message": "Please ensure all the required fields are passed with proper values"
        }
    def invalid_mail(self, message="User already exists"):
        return {
            "message": message
        }
