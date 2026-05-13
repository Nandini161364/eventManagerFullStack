from abc import ABC, abstractmethod


class UserPresenterInterface(ABC):
    @abstractmethod
    def create_user_success_response(self, personId):
        pass

    @abstractmethod
    def invalid_data(self):
        pass

    @abstractmethod
    def invalid_mail(self, message="User already exists"):
        pass
