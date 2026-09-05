import React, { useState } from 'react'
import api from '../api'
import { useNavigate } from 'react-router-dom'

export default function Login(){
  const [username,setUsername] = useState('')
  const [password,setPassword] = useState('')
  const [error,setError] = useState('')
  const navigate = useNavigate()

  const submit = async (e: React.FormEvent) =>{
    e.preventDefault()
    try{
      const res = await api.post('/auth/token/', { username, password })
      localStorage.setItem('access_token', res.data.access)
      localStorage.setItem('refresh_token', res.data.refresh)
      navigate('/')
    }catch(err:any){ setError('Login failed') }
  }

  return (
    <div className="container" style={{maxWidth:400}}>
      <h2>Login</h2>
      <form onSubmit={submit} className="card">
        {error && <div style={{color:'red'}}>{error}</div>}
        <div>
          <label>Username</label>
          <input value={username} onChange={e=>setUsername(e.target.value)} />
        </div>
        <div>
          <label>Password</label>
          <input type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        </div>
        <div style={{marginTop:8}}>
          <button type="submit">Login</button>
        </div>
      </form>
    </div>
  )
}
