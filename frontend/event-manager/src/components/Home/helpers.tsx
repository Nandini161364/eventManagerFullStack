import type {EventSummary} from '../../types/home'

export const formatDateTime = (value: string) =>
  new Intl.DateTimeFormat('en-IN', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value))

export const getPrice = (eventDetails: EventSummary) => {
  if (!eventDetails.is_paid) {
    return 'Free'
  }

  return `Rs. ${eventDetails.ticket_price}`
}

export const renderStatus = (eventDetails: EventSummary) => {
  if (eventDetails.booking_status === null) {
    return <span className="status-pill open">Open</span>
  }

  return (
    <span className={`status-pill ${eventDetails.booking_status}`}>
      {eventDetails.booking_status}
    </span>
  )
}
