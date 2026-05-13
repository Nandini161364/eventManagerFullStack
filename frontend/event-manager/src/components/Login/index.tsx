import {useState, type SubmitEvent} from 'react'
import {useNavigate} from 'react-router-dom'
import './index.css'
import type {LoginErrorResponse, LoginResponse} from '../../types/login'

const API_BASE_URL = 'http://127.0.0.1:8000/api/token/'

const Login = () => {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [errorMessage, setErrorMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const onSubmitLogin = async (event: SubmitEvent) => {
    event.preventDefault()
    setErrorMessage('')
    setIsLoading(true)

    try {
      const response = await fetch(API_BASE_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          password,
        }),
      })

      const data = (await response.json()) as LoginResponse & LoginErrorResponse

      if (!response.ok) {
        setErrorMessage(data.message ?? 'Invalid username or password')
        return
      }

      localStorage.setItem('accessToken', data.access)
      localStorage.setItem('refreshToken', data.refresh)
      navigate('/', {replace: true})
    } catch {
      setErrorMessage('Unable to login. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <section className="login-section">
      <div className="brand-panel">
        <p className="brand-mark">Event Manager</p>
        <h1>Run every event with calm control.</h1>
        <p className="brand-copy">
          Plan, publish, book, and manage attendee activity from one focused
          workspace.
        </p>
      </div>
      <form className="login-form" onSubmit={onSubmitLogin}>
        <div className="form-header">
          <p className="form-kicker">Sign in</p>
          <h2>Welcome back</h2>
        </div>

        <div className="field-group">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={event => setUsername(event.target.value)}
            placeholder="Enter username"
            required
          />
        </div>

        <div className="field-group">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={event => setPassword(event.target.value)}
            placeholder="Enter password"
            required
          />
        </div>

        {errorMessage !== '' && <p className="error-message">{errorMessage}</p>}

        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Logging in...' : 'Login'}
        </button>
      </form>
    </section>
  )
}

export default Login
