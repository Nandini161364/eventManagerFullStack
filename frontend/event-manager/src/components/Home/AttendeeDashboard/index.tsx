import type {EventSummary, EventTab} from '../../../types/home'
import EventCard from '../EventCard'

type AttendeeDashboardProps = {
  events: EventSummary[]
  attendeeTab: EventTab
  onChangeAttendeeTab: (tab: EventTab) => void
  onOpenEvent: (eventDetails: EventSummary) => void
}

const AttendeeDashboard = (props: AttendeeDashboardProps) => {
  const {events, attendeeTab, onChangeAttendeeTab, onOpenEvent} = props

  const visibleEvents =
    attendeeTab === 'active'
      ? events.filter(eventDetails => eventDetails.booking_status === null)
      : events.filter(eventDetails => eventDetails.booking_status === attendeeTab)

  return (
    <>
      <div className="dashboard-toolbar">
        <div>
          <h2>Explore events</h2>
          <p>Book, cancel, and track your event status.</p>
        </div>
      </div>
      <div className="tabs-list">
        <button
          className={attendeeTab === 'active' ? 'active-tab' : ''}
          type="button"
          onClick={() => onChangeAttendeeTab('active')}
        >
          Active events
        </button>
        <button
          className={attendeeTab === 'booked' ? 'active-tab' : ''}
          type="button"
          onClick={() => onChangeAttendeeTab('booked')}
        >
          Booked events
        </button>
        <button
          className={attendeeTab === 'cancelled' ? 'active-tab' : ''}
          type="button"
          onClick={() => onChangeAttendeeTab('cancelled')}
        >
          Cancelled events
        </button>
        <button
          className={attendeeTab === 'waitlisted' ? 'active-tab' : ''}
          type="button"
          onClick={() => onChangeAttendeeTab('waitlisted')}
        >
          Waitlisted events
        </button>
      </div>
      {visibleEvents.length === 0 ? (
        <p className="empty-state">No events to be shown</p>
      ) : (
        <section className="events-grid">
          {visibleEvents.map(eventDetails => (
            <EventCard
              eventDetails={eventDetails}
              key={eventDetails.id}
              onOpenEvent={onOpenEvent}
            />
          ))}
        </section>
      )}
    </>
  )
}

export default AttendeeDashboard
