import {useEffect, useState, type ChangeEvent, type SubmitEvent} from 'react'
import {Link, useNavigate} from 'react-router-dom'

import {type Role} from '../../types/register'

import './index.css'

const Register = () => {
  const [username, setUserName] = useState<string>('')
  const [email, setEmail] = useState<string>('')
  const [password, setPassword] = useState<string>('')
  const [phoneNumber, setPhoneNumber] = useState<string>('')
  const [role, setRole] = useState<Role | ''>('')
  const [errMsg, setErrorMsg] = useState<string>('')
  const navigate = useNavigate()

  useEffect(() => {
    const accessToken = localStorage.getItem('accessToken')

    if (accessToken !== null) {
      navigate('/', {replace: true})
    }
  }, [navigate])

  const onUserNameGiven = (event: ChangeEvent<HTMLInputElement>) => {
    return setUserName(event.target.value)
  }

  const onEmailGiven = (event: ChangeEvent<HTMLInputElement>) => {
    return setEmail(event.target.value)
  }

  const onPasswordGiven = (event: ChangeEvent<HTMLInputElement>) => {
    return setPassword(event.target.value)
  }

  const onPhoneNumberGiven = (event: ChangeEvent<HTMLInputElement>) => {
    return setPhoneNumber(event.target.value)
  } 

  const onRoleGiven = (event: ChangeEvent<HTMLInputElement>) => {
    return setRole(event.target.value as Role)
  }

  const onFormSubmission = async (event: SubmitEvent<HTMLFormElement>) => {
    event.preventDefault()
    setErrorMsg('')
    const apiUrl = 'http://127.0.0.1:8000/event/user/'
    const userDetails = {
      username,
      password,
      email,
      phone_number: phoneNumber,
      role,
    }

    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userDetails),
    }

    try {
      const response = await fetch(apiUrl, options)
      const data = await response.json()
      if (response?.ok === true) {
        setErrorMsg('')
        console.log(data)
        navigate('/')
      } else {
        const message = data.message ?? data.detail ?? 'Registration failed'
        setErrorMsg(message)
        console.log('Registration failed')
      }
    } catch (error) {
      setErrorMsg('Unable to register right now. Please try again.')
      console.log('Error occurred during registration:', error)
    }
  }


  return(
    <section className="register-section">
      <div className="register-brand-panel">
        <p className="brand-mark">Event Manager</p>
        <h1>Create your account</h1>
        <p>
          Register as an organizer to create events, or join as an attendee to
          book and manage your event activity.
        </p>
      </div>

      <form className="registration-form" onSubmit={onFormSubmission}>
        <div className="form-header">
          <p>Register</p>
          <h2>Get started</h2>
        </div>

        <div className="field-group">
          <label htmlFor="username">UserName</label>
          <input
            type="text"
            id="username"
            placeholder="Enter your username"
            value={username}
            onChange={onUserNameGiven}
            required
          />
        </div>

        <div className="field-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            placeholder="Enter your email"
            value={email}
            onChange={onEmailGiven}
            required
          />
        </div>

        <div className="field-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            placeholder="Enter your password"
            value={password}
            onChange={onPasswordGiven}
            required
          />
        </div>

        <div className="field-group">
          <label htmlFor="phone">Phone Number</label>
          <input
            type="tel"
            id="phone"
            placeholder="Enter your 10 digit phone number"
            value={phoneNumber}
            onChange={onPhoneNumberGiven}
            required
          />
        </div>

        <div className="field-group">
          <p className="field-label">Role</p>
          <div className="role-options">
            <label
              className={`role-option ${role === 'organizer' ? 'active-role' : ''}`}
              htmlFor="organizer"
            >
              <input
                type="radio"
                id="organizer"
                name="role"
                value="organizer"
                checked={role === 'organizer'}
                onChange={onRoleGiven}
                required
              />
              <span>Organizer</span>
            </label>
            <label
              className={`role-option ${role === 'attendee' ? 'active-role' : ''}`}
              htmlFor="attendee"
            >
              <input
                type="radio"
                id="attendee"
                name="role"
                value="attendee"
                checked={role === 'attendee'}
                onChange={onRoleGiven}
              />
              <span>Attendee</span>
            </label>
          </div>
        </div>

        <button type="submit">Submit</button>
        {errMsg !== '' && <p className="error-message">{errMsg}</p>}
        <p className="auth-switch">
          Already have an account? Kindly <Link to="/login">login here</Link>.
        </p>
      </form>
    </section>
  )


}

export default Register
