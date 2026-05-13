from eventsApp.models import User
from django.db.models import Q
from django.db import IntegrityError
from eventsApp.exceptions.exceptions import UserAlreadyExitsException


class UserStorage:
    def create_user(self, userDto):
        username = userDto.username
        email = userDto.email
        password = userDto.password
        phone_number = userDto.phone_number
        role = userDto.role

        try:
            response = User.objects.create_user(username=username, email=email, password=password, role=role, phone_number=phone_number)
        except IntegrityError:
            raise UserAlreadyExitsException("User already exists")

        return response.id

    def get_existing_user_fields(self, username, email, phone_number):
        existing_users = User.objects.filter(
            Q(username=username) | Q(email=email) | Q(phone_number=phone_number)
        ).only('username', 'email', 'phone_number')

        duplicate_fields = set()
        for user in existing_users:
            if user.username == username:
                duplicate_fields.add('username')
            if user.email == email:
                duplicate_fields.add('email')
            if user.phone_number == phone_number:
                duplicate_fields.add('phone_number')

        return sorted(duplicate_fields)
