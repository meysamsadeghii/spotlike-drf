import React from 'react'
import { Link, useNavigate } from 'react-router-dom'

export default function Nav(){
  const navigate = useNavigate()
  const token = localStorage.getItem('access_token')
  const logout = () => { localStorage.removeItem('access_token'); localStorage.removeItem('refresh_token'); navigate('/login') }
  return (
    <nav>
      <div className="container" style={{display:'flex',alignItems:'center',justifyContent:'space-between'}}>
        <div>
          <Link to="/">Spotlike</Link>
          <Link to="/favorites" style={{marginLeft:12}}>Favorites</Link>
          <Link to="/profile" style={{marginLeft:12}}>Profile</Link>
        </div>
        <div>
          {token ? (
            <button onClick={logout}>Logout</button>
          ) : (
            <>
              <Link to="/login">Login</Link>
              <Link to="/register" style={{marginLeft:8}}>Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}
