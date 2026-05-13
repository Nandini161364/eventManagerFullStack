from django.contrib import admin
from eventsApp.models import User, Event, Ticket, Feedback, Booking
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'phone_number')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('role',)
    
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'organizer', 'start_date', 'end_date', 'venue', 'is_paid', 'maximum_attendees')

    fieldsets = (
        (None, {
            'fields': ('event_title', 'organizer', 'start_date', 'end_date', 'venue', 'is_paid', 'maximum_attendees')
        }),
        ('Advanced', {
            'fields': ('description',),
        }),
    )
    list_filter = ('organizer', 'start_date', 'end_date', 'is_paid')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
    search_fields = ('event_title', 'organizer__username', 'venue')
    list_per_page = 10
    list_max_show_all = 100
    list_editable = ('is_paid', 'maximum_attendees', 'start_date', 'end_date', 'venue')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('event', 'price')
   

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('booking', 'rating', 'comment', 'feedback_date')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('attendee', 'event', 'booking_date', 'booking_status')
    

admin.site.register(User, UserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Booking, BookingAdmin)
