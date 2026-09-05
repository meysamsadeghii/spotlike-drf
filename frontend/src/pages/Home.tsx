import React, { useEffect, useState } from 'react'
import api from '../api'
import Player from '../components/Player'

export default function Home(){
  const [tracks,setTracks] = useState<any[]>([])
  const [artists,setArtists] = useState<any[]>([])
  const [albums,setAlbums] = useState<any[]>([])
  const [now,setNow] = useState<string | null>(null)

  useEffect(()=>{ fetchData() },[])

  const fetchData = async ()=>{
    try{
      const [tRes,aRes,alRes] = await Promise.all([
        api.get('/tracks/'),
        api.get('/artists/'),
        api.get('/albums/'),
      ])
      setTracks(tRes.data.results || tRes.data)
      setArtists(aRes.data.results || aRes.data)
      setAlbums(alRes.data.results || alRes.data)
    }catch(err){ console.error(err) }
  }

  return (
    <div className="container">
      <h1>Browse</h1>
      <section>
        <h3>Tracks</h3>
        {tracks.map(t=> (
          <div className="card" key={t.id}>
            <strong>{t.title}</strong>
            <div>Album: {t.album}</div>
            <div>
              {t.audio_url && <button onClick={()=>setNow(t.audio_url)}>Play</button>}
            </div>
          </div>
        ))}
      </section>

      <section>
        <h3>Artists</h3>
        {artists.map(a=> (
          <div className="card" key={a.id}>{a.name}</div>
        ))}
      </section>

      <section>
        <h3>Albums</h3>
        {albums.map(a=> (
          <div className="card" key={a.id}>{a.title}</div>
        ))}
      </section>

      {now && <Player src={now} />}
    </div>
  )
}
