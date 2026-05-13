import type {ChangeEvent, FormEvent} from 'react'
import type {
  CreateEventForm as CreateEventFormDetails,
  EventSummary,
  OrganizerTab,
} from '../../../types/home'
import CreateEventForm from '../CreateEventForm'
import EventCard from '../EventCard'

type OrganizerDashboardProps = {
  events: EventSummary[]
  bookedEvents: EventSummary[]
  organizerTab: OrganizerTab
  showCreateEvent: boolean
  eventForm: CreateEventFormDetails
  onChangeOrganizerTab: (tab: OrganizerTab) => void
  onToggleCreateEvent: () => void
  onChangeEventField: (
    event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => void
  onChangePaidStatus: (event: ChangeEvent<HTMLInputElement>) => void
  onCreateEvent: (event: FormEvent<HTMLFormElement>) => void
  onCancelCreateEvent: () => void
  onOpenEvent: (eventDetails: EventSummary) => void
}

const OrganizerDashboard = (props: OrganizerDashboardProps) => {
  const {
    events,
    bookedEvents,
    organizerTab,
    showCreateEvent,
    eventForm,
    onChangeOrganizerTab,
    onToggleCreateEvent,
    onChangeEventField,
    onChangePaidStatus,
    onCreateEvent,
    onCancelCreateEvent,
    onOpenEvent,
  } = props

  const visibleEvents = organizerTab === 'bookedEvents' ? bookedEvents : events

  return (
    <>
      <div className="dashboard-toolbar">
        <div>
          <h2>Organizer dashboard</h2>
          <p>Manage your events and your personal bookings.</p>
        </div>
        <button type="button" onClick={onToggleCreateEvent}>
          Create event
        </button>
      </div>
      <div className="tabs-list">
        <button
          className={organizerTab === 'myEvents' ? 'active-tab' : ''}
          type="button"
          onClick={() => onChangeOrganizerTab('myEvents')}
        >
          My events
        </button>
        <button
          className={organizerTab === 'bookedEvents' ? 'active-tab' : ''}
          type="button"
          onClick={() => onChangeOrganizerTab('bookedEvents')}
        >
          Booked events
        </button>
      </div>
      {showCreateEvent && (
        <CreateEventForm
          eventForm={eventForm}
          onCancelCreateEvent={onCancelCreateEvent}
          onChangeEventField={onChangeEventField}
          onChangePaidStatus={onChangePaidStatus}
          onCreateEvent={onCreateEvent}
        />
      )}
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

export default OrganizerDashboard
