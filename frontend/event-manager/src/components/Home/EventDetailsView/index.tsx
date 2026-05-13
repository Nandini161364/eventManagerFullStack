import eventImage from '../../../assets/hero.png'
import type {
  EventDetails,
  EventSummary,
  OrganizerTab,
  UserRole,
} from '../../../types/home'
import {formatDateTime, getPrice} from '../helpers'

type EventDetailsViewProps = {
  selectedEvent: EventSummary
  selectedEventDetails: EventDetails | null
  userRole: UserRole
  organizerTab: OrganizerTab
  showAttendees: boolean
  actionEventId: number | null
  onBackToEvents: () => void
  onToggleAttendees: () => void
  onBookEvent: (eventId: number) => void
  onCancelBooking: (eventDetails: EventSummary) => void
}

const EventDetailsView = (props: EventDetailsViewProps) => {
  const {
    selectedEvent,
    selectedEventDetails,
    userRole,
    organizerTab,
    showAttendees,
    actionEventId,
    onBackToEvents,
    onToggleAttendees,
    onBookEvent,
    onCancelBooking,
  } = props

  const attendeeCount = selectedEventDetails?.total_bookings_count ?? 0
  const seatsLeft =
    selectedEventDetails?.available_seats ?? selectedEvent.available_seats

  const isBookedEvent =
    selectedEvent.booking_status === 'booked' ||
    selectedEvent.booking_status === 'waitlisted' ||
    selectedEvent.booking_status === 'pending'

  const showBookingAction = userRole === 'attendee' || organizerTab === 'bookedEvents'
  const showAttendeeList = userRole === 'organizer' && organizerTab === 'myEvents'

  return (
    <section className="event-details">
      <img src={eventImage} alt="" className="event-banner" />
      <div className="event-details-grid">
        <div className="event-details-left">
          <button className="text-button" type="button" onClick={onBackToEvents}>
            Back to events
          </button>
          <h2>{selectedEvent.event_title}</h2>
          <p>{selectedEvent.description}</p>
          <dl className="details-list">
            <div>
              <dt>Venue</dt>
              <dd>{selectedEvent.venue}</dd>
            </div>
            <div>
              <dt>Starts</dt>
              <dd>{formatDateTime(selectedEvent.start_date)}</dd>
            </div>
            <div>
              <dt>Ends</dt>
              <dd>{formatDateTime(selectedEvent.end_date)}</dd>
            </div>
            <div>
              <dt>Price</dt>
              <dd>{getPrice(selectedEvent)}</dd>
            </div>
            {selectedEvent.booking_status !== null && (
              <div>
                <dt>Booking status</dt>
                <dd>{selectedEvent.booking_status}</dd>
              </div>
            )}
          </dl>
          {showBookingAction && (
            <div className="event-actions">
              {isBookedEvent ? (
                <button
                  className="secondary-button"
                  type="button"
                  disabled={actionEventId === selectedEvent.id}
                  onClick={() => onCancelBooking(selectedEvent)}
                >
                  Cancel event
                </button>
              ) : (
                <button
                  type="button"
                  disabled={actionEventId === selectedEvent.id}
                  onClick={() => onBookEvent(selectedEvent.id)}
                >
                  Book event
                </button>
              )}
            </div>
          )}
        </div>
        <aside className="event-details-right">
          <div>
            <span>Attendees</span>
            <strong>{attendeeCount}</strong>
          </div>
          <div>
            <span>Seats left</span>
            <strong>{seatsLeft}</strong>
          </div>
          {showAttendeeList && (
            <button className="text-button" type="button" onClick={onToggleAttendees}>
              See attendee list
            </button>
          )}
          {showAttendees && selectedEventDetails !== null && (
            <ul className="attendee-list">
              {selectedEventDetails.attendee_details.length === 0 ? (
                <li>No attendees to be shown</li>
              ) : (
                selectedEventDetails.attendee_details.map(attendee => (
                  <li key={attendee.attendee_id}>
                    <strong>{attendee.attendee_name}</strong>
                    <span>{attendee.attendee_email}</span>
                  </li>
                ))
              )}
            </ul>
          )}
        </aside>
      </div>
    </section>
  )
}

export default EventDetailsView
