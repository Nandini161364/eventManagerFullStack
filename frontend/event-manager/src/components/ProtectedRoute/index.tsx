import type { ProtectedRouteProps } from "../../types/protectedRoute"
import {Navigate} from 'react-router-dom'


const ProtectedRoute = ({children}: ProtectedRouteProps) => {
  const accessToken = localStorage.getItem('accessToken')

  if (accessToken === null) {
    return <Navigate to="/login" replace />
  }

  return children
}

export default ProtectedRoute