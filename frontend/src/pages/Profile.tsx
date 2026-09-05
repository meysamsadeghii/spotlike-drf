import React, { useEffect, useState } from 'react'
import api from '../api'

export default function Profile(){
  const [profile,setProfile] = useState<any>(null)

  useEffect(()=>{ fetchProfile() },[])
  const fetchProfile = async ()=>{
    try{
      const res = await api.get('/auth/profile/')
      setProfile(res.data)
    }catch(err){ console.error(err) }
  }

  if(!profile) return <div className="container">Loading...</div>
  return (
    <div className="container">
      <h2>Profile</h2>
      <div className="card">
        <div>Username: {profile.username}</div>
        <div>Email: {profile.email}</div>
        <div>Name: {profile.first_name} {profile.last_name}</div>
      </div>
    </div>
  )
}
