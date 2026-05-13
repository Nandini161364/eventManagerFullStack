export type UserRole = 'attendee' | 'organizer'

export type CurrentUser = {
  id: number
  username: string
  email: string
  role: UserRole
  phone_number: string
}

export type BookingStatus = 'booked' | 'pending' | 'cancelled' | 'waitlisted'

export type EventSummary = {
  id: number
  event_title: string
  description: string
  start_date: string
  end_date: string
  venue: string
  is_paid: boolean
  maximum_attendees: number
  available_seats: number
  ticket_price: string | number
  organizer_name: string
  booking_id: number | null
  booking_status: BookingStatus | null
}

export type EventsResponse = {
  events: EventSummary[]
  booked_events?: EventSummary[]
}

export type EventTab = 'active' | 'booked' | 'cancelled' | 'waitlisted'

export type OrganizerTab = 'myEvents' | 'bookedEvents'

export type CreateEventForm = {
  event_title: string
  description: string
  start_date: string
  end_date: string
  venue: string
  is_paid: boolean
  maximum_attendees: string
  ticket_price: string
}

export type AttendeeDetails = {
  attendee_id: number
  attendee_email: string
  attendee_name: string
}

export type EventDetails = EventSummary & {
  attendee_details: AttendeeDetails[]
  booking_pending_users: AttendeeDetails[]
  booking_cancelled_users: AttendeeDetails[]
  total_bookings_count: number
  pending_bookings_count: number
  cancelled_bookings_count: number
}

export type ApiMessage = {
  message?: string
  id?: number
}
