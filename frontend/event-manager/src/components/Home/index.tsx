import {useEffect, useState, type ChangeEvent, type FormEvent} from 'react'
import {useNavigate} from 'react-router-dom'
import type {
  ApiMessage,
  CreateEventForm,
  CurrentUser,
  EventDetails,
  EventSummary,
  EventsResponse,
  EventTab,
  OrganizerTab,
} from '../../types/home'
import AttendeeDashboard from './AttendeeDashboard'
import EventDetailsView from './EventDetailsView'
import OrganizerDashboard from './OrganizerDashboard'
import './index.css'

const API_BASE_URL = 'http://127.0.0.1:8000'

const emptyEventForm: CreateEventForm = {
  event_title: '',
  description: '',
  start_date: '',
  end_date: '',
  venue: '',
  is_paid: false,
  maximum_attendees: '',
  ticket_price: '',
}

const getAuthHeaders = () => ({
  Authorization: `Bearer ${localStorage.getItem('accessToken') ?? ''}`,
  'Content-Type': 'application/json',
})

const Home = () => {
  const navigate = useNavigate()
  const [user, setUser] = useState<CurrentUser | null>(null)
  const [events, setEvents] = useState<EventSummary[]>([])
  const [bookedEvents, setBookedEvents] = useState<EventSummary[]>([])
  const [selectedEvent, setSelectedEvent] = useState<EventSummary | null>(null)
  const [selectedEventDetails, setSelectedEventDetails] = useState<EventDetails | null>(null)
  const [attendeeTab, setAttendeeTab] = useState<EventTab>('active')
  const [organizerTab, setOrganizerTab] = useState<OrganizerTab>('myEvents')
  const [showCreateEvent, setShowCreateEvent] = useState(false)
  const [showAttendees, setShowAttendees] = useState(false)
  const [eventForm, setEventForm] = useState<CreateEventForm>(emptyEventForm)
  const [isLoading, setIsLoading] = useState(true)
  const [actionEventId, setActionEventId] = useState<number | null>(null)
  const [message, setMessage] = useState('')
  const [errorMessage, setErrorMessage] = useState('')

  const loadHome = async () => {
    setIsLoading(true)
    setErrorMessage('')

    try {
      const [userResponse, eventsResponse] = await Promise.all([
        fetch(`${API_BASE_URL}/event/me/`, {headers: getAuthHeaders()}),
        fetch(`${API_BASE_URL}/event/events/`, {headers: getAuthHeaders()}),
      ])

      if (userResponse.status === 401 || eventsResponse.status === 401) {
        localStorage.removeItem('accessToken')
        localStorage.removeItem('refreshToken')
        navigate('/login', {replace: true})
        return
      }

      if (!userResponse.ok || !eventsResponse.ok) {
        setErrorMessage('Unable to load events right now.')
        return
      }

      const userData = (await userResponse.json()) as CurrentUser
      const eventsData = (await eventsResponse.json()) as EventsResponse

      setUser(userData)
      setEvents(eventsData.events)
      setBookedEvents(eventsData.booked_events ?? [])
    } catch {
      setErrorMessage('Unable to connect to the server.')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    void loadHome()
  }, [])

  const onLogout = () => {
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    navigate('/login', {replace: true})
  }

  const onBackToEvents = () => {
    setSelectedEvent(null)
    setSelectedEventDetails(null)
    setShowAttendees(false)
  }

  const onChangeAttendeeTab = (tab: EventTab) => {
    setAttendeeTab(tab)
    onBackToEvents()
  }

  const onChangeOrganizerTab = (tab: OrganizerTab) => {
    setOrganizerTab(tab)
    onBackToEvents()
  }

  const onChangeEventField = (
    event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    const {name, value} = event.target

    setEventForm(previousDetails => ({
      ...previousDetails,
      [name]: value,
    }))
  }

  const onChangePaidStatus = (event: ChangeEvent<HTMLInputElement>) => {
    setEventForm(previousDetails => ({
      ...previousDetails,
      is_paid: event.target.checked,
      ticket_price: event.target.checked ? previousDetails.ticket_price : '0',
    }))
  }

  const onCreateEvent = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setErrorMessage('')
    setMessage('')

    try {
      const response = await fetch(`${API_BASE_URL}/event/create/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({
          ...eventForm,
          maximum_attendees: Number(eventForm.maximum_attendees),
          ticket_price: eventForm.is_paid ? Number(eventForm.ticket_price) : 0,
        }),
      })
      const data = (await response.json()) as ApiMessage

      if (!response.ok) {
        setErrorMessage(data.message ?? 'Unable to create event.')
        return
      }

      setMessage(data.message ?? 'Event created successfully.')
      setEventForm(emptyEventForm)
      setShowCreateEvent(false)
      await loadHome()
    } catch {
      setErrorMessage('Unable to create event right now.')
    }
  }

  const onBookEvent = async (eventId: number) => {
    setActionEventId(eventId)
    setMessage('')
    setErrorMessage('')

    try {
      const response = await fetch(`${API_BASE_URL}/event/booking/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({event_id: eventId}),
      })
      const data = (await response.json()) as ApiMessage

      if (!response.ok && !data.message?.toLowerCase().includes('waitlisted')) {
        setErrorMessage(data.message ?? 'Unable to book this event.')
        return
      }

      setMessage(data.message ?? 'Event booked successfully.')
      onBackToEvents()
      await loadHome()
    } catch {
      setErrorMessage('Unable to book this event.')
    } finally {
      setActionEventId(null)
    }
  }

  const onCancelBooking = async (eventDetails: EventSummary) => {
    if (eventDetails.booking_id === null) {
      return
    }

    setActionEventId(eventDetails.id)
    setMessage('')
    setErrorMessage('')

    try {
      const response = await fetch(`${API_BASE_URL}/event/cancel-booking/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({
          booking_id: eventDetails.booking_id,
          event_id: eventDetails.id,
        }),
      })
      const data = (await response.json()) as ApiMessage

      if (!response.ok) {
        setErrorMessage(data.message ?? 'Unable to cancel this booking.')
        return
      }

      setMessage(data.message ?? 'Booking cancelled.')
      onBackToEvents()
      await loadHome()
    } catch {
      setErrorMessage('Unable to cancel this booking.')
    } finally {
      setActionEventId(null)
    }
  }

  const onOpenEvent = async (eventDetails: EventSummary) => {
    setSelectedEvent(eventDetails)
    setSelectedEventDetails(null)
    setShowAttendees(false)
    setErrorMessage('')

    if (user?.role !== 'organizer' || organizerTab !== 'myEvents') {
      return
    }

    setActionEventId(eventDetails.id)

    try {
      const response = await fetch(
        `${API_BASE_URL}/event/get-event/${eventDetails.id}/`,
        {headers: getAuthHeaders()},
      )

      if (!response.ok) {
        setErrorMessage('Unable to open event details.')
        return
      }

      const data = (await response.json()) as EventDetails
      setSelectedEventDetails(data)
    } catch {
      setErrorMessage('Unable to open event details.')
    } finally {
      setActionEventId(null)
    }
  }

  if (isLoading) {
    return <main className="home-page loading-state">Loading events...</main>
  }

  return (
    <main className="home-page">
      <header className="home-header">
        <div className="brand-area">
          <span className="brand-logo">EM</span>
          <h1>Event Manager</h1>
        </div>
        <div className="profile-area">
          <div>
            <span>{user?.role}</span>
            <p>{user?.username}</p>
          </div>
          <button className="secondary-button" type="button" onClick={onLogout}>
            Logout
          </button>
        </div>
      </header>

      <section className="dashboard-body">
        {message !== '' && <p className="success-message">{message}</p>}
        {errorMessage !== '' && <p className="error-message">{errorMessage}</p>}

        {selectedEvent === null && user?.role === 'organizer' && (
          <OrganizerDashboard
            bookedEvents={bookedEvents}
            eventForm={eventForm}
            events={events}
            organizerTab={organizerTab}
            showCreateEvent={showCreateEvent}
            onCancelCreateEvent={() => setShowCreateEvent(false)}
            onChangeEventField={onChangeEventField}
            onChangeOrganizerTab={onChangeOrganizerTab}
            onChangePaidStatus={onChangePaidStatus}
            onCreateEvent={onCreateEvent}
            onOpenEvent={eventDetails => void onOpenEvent(eventDetails)}
            onToggleCreateEvent={() =>
              setShowCreateEvent(previousValue => !previousValue)
            }
          />
        )}

        {selectedEvent === null && user?.role === 'attendee' && (
          <AttendeeDashboard
            attendeeTab={attendeeTab}
            events={events}
            onChangeAttendeeTab={onChangeAttendeeTab}
            onOpenEvent={eventDetails => void onOpenEvent(eventDetails)}
          />
        )}

        {selectedEvent !== null && user !== null && (
          <EventDetailsView
            actionEventId={actionEventId}
            organizerTab={organizerTab}
            selectedEvent={selectedEvent}
            selectedEventDetails={selectedEventDetails}
            showAttendees={showAttendees}
            userRole={user.role}
            onBackToEvents={onBackToEvents}
            onBookEvent={eventId => void onBookEvent(eventId)}
            onCancelBooking={eventDetails => void onCancelBooking(eventDetails)}
            onToggleAttendees={() =>
              setShowAttendees(previousValue => !previousValue)
            }
          />
        )}
      </section>
    </main>
  )
}

export default Home
