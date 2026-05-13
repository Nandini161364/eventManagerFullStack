import {Link} from 'react-router-dom'

import './index.css'

const NotFound = () => (
  <main className="not-found-page">
    <section className="not-found-content">
      <p className="not-found-code">404</p>
      <h1>No route found</h1>
      <p className="not-found-message">
        The page you are trying to open does not exist.
      </p>
      <Link className="not-found-link" to="/register" replace>
        Go to Register
      </Link>
    </section>
  </main>
)

export default NotFound
