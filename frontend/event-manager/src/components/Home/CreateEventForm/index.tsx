import type {ChangeEvent, FormEvent} from 'react'
import type {CreateEventForm as CreateEventFormDetails} from '../../../types/home'

type CreateEventFormProps = {
  eventForm: CreateEventFormDetails
  onChangeEventField: (
    event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => void
  onChangePaidStatus: (event: ChangeEvent<HTMLInputElement>) => void
  onCreateEvent: (event: FormEvent<HTMLFormElement>) => void
  onCancelCreateEvent: () => void
}

const CreateEventForm = (props: CreateEventFormProps) => {
  const {
    eventForm,
    onChangeEventField,
    onChangePaidStatus,
    onCreateEvent,
    onCancelCreateEvent,
  } = props

  return (
    <form className="create-event-form" onSubmit={onCreateEvent}>
      <div className="form-row two-columns">
        <label htmlFor="event_title">
          Event title
          <input
            id="event_title"
            name="event_title"
            type="text"
            value={eventForm.event_title}
            onChange={onChangeEventField}
            required
          />
        </label>
        <label htmlFor="venue">
          Venue
          <input
            id="venue"
            name="venue"
            type="text"
            value={eventForm.venue}
            onChange={onChangeEventField}
            required
          />
        </label>
      </div>
      <label htmlFor="description">
        Description
        <textarea
          id="description"
          name="description"
          value={eventForm.description}
          onChange={onChangeEventField}
          required
        />
      </label>
      <div className="form-row two-columns">
        <label htmlFor="start_date">
          Start date
          <input
            id="start_date"
            name="start_date"
            type="datetime-local"
            value={eventForm.start_date}
            onChange={onChangeEventField}
            required
          />
        </label>
        <label htmlFor="end_date">
          End date
          <input
            id="end_date"
            name="end_date"
            type="datetime-local"
            value={eventForm.end_date}
            onChange={onChangeEventField}
            required
          />
        </label>
      </div>
      <div className="form-row two-columns">
        <label htmlFor="maximum_attendees">
          Maximum attendees
          <input
            id="maximum_attendees"
            name="maximum_attendees"
            type="number"
            min="1"
            value={eventForm.maximum_attendees}
            onChange={onChangeEventField}
            required
          />
        </label>
        <label htmlFor="ticket_price">
          Ticket price
          <input
            id="ticket_price"
            name="ticket_price"
            type="number"
            min="0"
            value={eventForm.ticket_price}
            onChange={onChangeEventField}
            disabled={!eventForm.is_paid}
          />
        </label>
      </div>
      <label className="checkbox-field" htmlFor="is_paid">
        <input
          id="is_paid"
          type="checkbox"
          checked={eventForm.is_paid}
          onChange={onChangePaidStatus}
        />
        Paid event
      </label>
      <div className="form-actions">
        <button type="submit">Create event</button>
        <button
          className="secondary-button"
          type="button"
          onClick={onCancelCreateEvent}
        >
          Cancel
        </button>
      </div>
    </form>
  )
}

export default CreateEventForm
