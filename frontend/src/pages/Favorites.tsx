import React, { useEffect, useState } from 'react'
import api from '../api'

export default function Favorites(){
  const [favs,setFavs] = useState<any[]>([])
  useEffect(()=>{ fetch() },[])
  const fetch = async ()=>{
    try{ const res = await api.get('/favorites/'); setFavs(res.data.results || res.data) }catch(err){ console.error(err) }
  }
  const remove = async (id:number)=>{
    try{ await api.delete(`/favorites/${id}/`); fetch() }catch(err){ console.error(err) }
  }
  return (
    <div className="container">
      <h2>Favorites</h2>
      {favs.map(f => (
        <div className="card" key={f.id}>
          <div>{f.track.title} — {f.track.album?.title}</div>
          <button onClick={()=>remove(f.id)}>Remove</button>
        </div>
      ))}
    </div>
  )
}
