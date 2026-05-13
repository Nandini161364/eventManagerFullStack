from eventsApp.interactors.presenter_interfaces.user_presenter_interface import UserPresenterInterface
from eventsApp.interactors.storage_interfaces.user_storage_interface import UserStorageInterface

from eventsApp.exceptions.exceptions import InvalidDataException, UserAlreadyExitsException


from eventsApp.utils.email_service import EmailService

class CreateUserInteractor:
    def __init__(self, storage: UserStorageInterface, presenter: UserPresenterInterface):
        self.storage = storage
        self.presenter = presenter
    
    def create_user(self, userDto):
        name = userDto.username.strip() if userDto.username else userDto.username
        email = userDto.email.strip().lower() if userDto.email else userDto.email
        password = userDto.password
        role = userDto.role.strip().lower() if userDto.role else userDto.role
        phone_number = userDto.phone_number.strip() if userDto.phone_number else userDto.phone_number

        userDto.username = name
        userDto.email = email
        userDto.role = role
        userDto.phone_number = phone_number

        if not (name and email and password and role and phone_number):
            raise InvalidDataException("Data can't be empty")
        if role not in ('organizer', 'attendee'):
            raise InvalidDataException("Role must be organizer or attendee")

        duplicate_fields = self.storage.get_existing_user_fields(name, email, phone_number)

        if duplicate_fields:
            raise UserAlreadyExitsException(
                f"User already exists with {', '.join(duplicate_fields)}"
            )
        
        response = self.storage.create_user(userDto)
        EmailService.send_registration_email(userDto)

        return self.presenter.create_user_success_response(response)
