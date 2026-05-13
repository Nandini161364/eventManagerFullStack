import type {EventSummary} from '../../../types/home'
import {formatDateTime, getPrice, renderStatus} from '../helpers'

type EventCardProps = {
  eventDetails: EventSummary
  onOpenEvent: (eventDetails: EventSummary) => void
}

const EventCard = (props: EventCardProps) => {
  const {eventDetails, onOpenEvent} = props

  return (
    <article className="event-card" onClick={() => onOpenEvent(eventDetails)}>
      <div className="event-card-header">
        <div>
          <h3>{eventDetails.event_title}</h3>
          <p>{eventDetails.venue}</p>
        </div>
        {renderStatus(eventDetails)}
      </div>
      <p className="event-description">{eventDetails.description}</p>
      <dl className="event-meta">
        <div>
          <dt>Starts</dt>
          <dd>{formatDateTime(eventDetails.start_date)}</dd>
        </div>
        <div>
          <dt>Seats left</dt>
          <dd>{eventDetails.available_seats}</dd>
        </div>
        <div>
          <dt>Price</dt>
          <dd>{getPrice(eventDetails)}</dd>
        </div>
      </dl>
    </article>
  )
}

export default EventCard
