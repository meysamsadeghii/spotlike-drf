import React, { useRef, useEffect } from 'react'

export default function Player({ src }: { src: string }){
  const ref = useRef<HTMLAudioElement | null>(null)
  useEffect(()=>{ if(ref.current){ ref.current.load(); ref.current.play().catch(()=>{}) } },[src])
  return (
    <div style={{position:'fixed',left:16,right:16,bottom:16,background:'#fff',padding:8,borderRadius:8}}>
      <audio controls ref={ref} style={{width:'100%'}}>
        <source src={src} />
        Your browser does not support the audio element.
      </audio>
    </div>
  )
}
