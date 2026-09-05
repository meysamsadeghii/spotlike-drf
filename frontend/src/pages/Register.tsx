import React, { useState } from 'react'
import api from '../api'
import { useNavigate } from 'react-router-dom'

export default function Register(){
  const [username,setUsername] = useState('')
  const [email,setEmail] = useState('')
  const [password,setPassword] = useState('')
  const [error,setError] = useState('')
  const navigate = useNavigate()

  const submit = async (e: React.FormEvent) =>{
    e.preventDefault()
    try{
      await api.post('/auth/register/', { username, email, password })
      navigate('/login')
    }catch(err:any){ setError('Registration failed') }
  }

  return (
    <div className="container" style={{maxWidth:400}}>
      <h2>Register</h2>
      <form onSubmit={submit} className="card">
        {error && <div style={{color:'red'}}>{error}</div>}
        <div>
          <label>Username</label>
          <input value={username} onChange={e=>setUsername(e.target.value)} />
        </div>
        <div>
          <label>Email</label>
          <input value={email} onChange={e=>setEmail(e.target.value)} />
        </div>
        <div>
          <label>Password</label>
          <input type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        </div>
        <div style={{marginTop:8}}>
          <button type="submit">Register</button>
        </div>
      </form>
    </div>
  )
}
