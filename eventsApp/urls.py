from django.urls import path
from .views import create_event, register_user, event_booking, cancel_booking, get_event_details, give_feedback, make_superuser, current_user, list_events

urlpatterns = [
    path('create/', create_event, name='create_event'),
    path('user/', register_user, name='register'),
    path('me/', current_user, name='current_user'),
    path('events/', list_events, name='list_events'),
    path('booking/', event_booking, name='booking'),
    path('cancel-booking/', cancel_booking, name='cancel_booking'),
    path('get-event/<int:event_id>/',get_event_details, name='get_event_details'),
    path('feedback/', give_feedback, name='give_feedback'),
    path("make-superuser/", make_superuser, name='superuser')
]
