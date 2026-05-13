from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    ROLE_CHOICES = (
        ('organizer', 'Organizer'),
        ('attendee', 'Attendee'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, unique=True)

# Create your models here.
# class Person(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Organizer(models.Model):
#     person = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organizer')
#     organization_name = models.CharField(max_length=100)
#     organization_email = models.EmailField(unique=True)

#     def __str__(self):
#         return self.organization_name

    
class Event(models.Model):
    event_title = models.CharField(max_length=100)
    description = models.TextField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    venue = models.CharField(max_length=100)
    is_paid = models.BooleanField(default=False)
    maximum_attendees = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_full = models.BooleanField(default=False)

    def __str__(self):
        return self.event_title

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.event.event_title


class Booking(models.Model):
    booking_status = [
        ('pending', 'Pending'),
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('waitlisted','Waitlisted')
    ]

    attendee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    booking_status = models.CharField(max_length=100, choices=booking_status, default='pending')
    

    class Meta:
        unique_together = ('attendee', 'event')

    def __str__(self):
        return f"{self.attendee.username} - {self.event.event_title} - {self.ticket.price}"


class Feedback(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='feedbacks', null=True, blank=True)
    rating = models.IntegerField(default=0, choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    comment = models.TextField(blank=True, null=True)
    feedback_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.booking.attendee.username} - {self.booking.event.event_title} - {self.rating}" if self.booking else "No booking found"
    
# class Attendance(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance')
#     event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendance')
#     attended_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
#     class Meta:
#         unique_together = ('user', 'event')