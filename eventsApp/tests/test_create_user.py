from unittest.mock import patch

import pytest

from eventsApp.adaptors.dtos import CreateUserDTO
from eventsApp.exceptions.exceptions import InvalidDataException, UserAlreadyExitsException
from eventsApp.interactors.user_interactor import CreateUserInteractor
from eventsApp.presenters.user_presenter import UserPresenter
from eventsApp.storages.user_storage import UserStorage
from eventsApp.tests.factories import UserFactory


@pytest.mark.django_db
class TestCreateUser:

    @patch('eventsApp.interactors.user_interactor.EmailService.send_registration_email')
    def test_create_user_success(self, mock_send_email):
        userDto = CreateUserDTO(
            username='new_user',
            email='NEW_USER@EXAMPLE.COM',
            password='password123',
            phone_number='9876543210',
            role='ATTENDEE'
        )

        interactor = CreateUserInteractor(
            storage=UserStorage(),
            presenter=UserPresenter()
        )

        response = interactor.create_user(userDto)

        assert response["message"] == "User created Successfully"
        assert "id" in response
        assert userDto.email == 'new_user@example.com'
        assert userDto.role == 'attendee'
        mock_send_email.assert_called_once_with(userDto)

    def test_create_user_with_empty_data(self):
        userDto = CreateUserDTO(
            username='',
            email='user@example.com',
            password='password123',
            phone_number='9876543210',
            role='attendee'
        )

        interactor = CreateUserInteractor(
            storage=UserStorage(),
            presenter=UserPresenter()
        )

        with pytest.raises(InvalidDataException):
            interactor.create_user(userDto)

    def test_create_user_with_invalid_role(self):
        userDto = CreateUserDTO(
            username='new_user',
            email='user@example.com',
            password='password123',
            phone_number='9876543210',
            role='admin'
        )

        interactor = CreateUserInteractor(
            storage=UserStorage(),
            presenter=UserPresenter()
        )

        with pytest.raises(InvalidDataException):
            interactor.create_user(userDto)

    def test_create_user_with_duplicate_username(self):
        existing_user = UserFactory(username='existing_user')

        userDto = CreateUserDTO(
            username=existing_user.username,
            email='new_email@example.com',
            password='password123',
            phone_number='9876543210',
            role='attendee'
        )

        interactor = CreateUserInteractor(
            storage=UserStorage(),
            presenter=UserPresenter()
        )

        with pytest.raises(UserAlreadyExitsException) as exception:
            interactor.create_user(userDto)

        assert str(exception.value) == "User already exists with username"

    def test_create_user_with_duplicate_email(self):
        existing_user = UserFactory(email='existing@example.com')

        userDto = CreateUserDTO(
            username='new_user',
            email=existing_user.email.upper(),
            password='password123',
            phone_number='9876543210',
            role='attendee'
        )

        interactor = CreateUserInteractor(
            storage=UserStorage(),
            presenter=UserPresenter()
        )

        with pytest.raises(UserAlreadyExitsException) as exception:
            interactor.create_user(userDto)

        assert str(exception.value) == "User already exists with email"

    def test_create_user_with_duplicate_phone_number(self):
        existing_user = UserFactory(phone_number='9876543210')

        userDto = CreateUserDTO(
            username='new_user',
            email='new_email@example.com',
            password='password123',
            phone_number=existing_user.phone_number,
            role='attendee'
        )

        interactor = CreateUserInteractor(
            storage=UserStorage(),
            presenter=UserPresenter()
        )

        with pytest.raises(UserAlreadyExitsException) as exception:
            interactor.create_user(userDto)

        assert str(exception.value) == "User already exists with phone_number"

    def test_create_user_with_multiple_duplicate_fields(self):
        existing_user = UserFactory(
            username='existing_user',
            email='existing@example.com',
            phone_number='9876543210'
        )

        userDto = CreateUserDTO(
            username=existing_user.username,
            email=existing_user.email,
            password='password123',
            phone_number=existing_user.phone_number,
            role='attendee'
        )

        interactor = CreateUserInteractor(
            storage=UserStorage(),
            presenter=UserPresenter()
        )

        with pytest.raises(UserAlreadyExitsException) as exception:
            interactor.create_user(userDto)

        assert str(exception.value) == "User already exists with email, phone_number, username"
