import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Profile from './pages/Profile'
import Favorites from './pages/Favorites'
import Nav from './components/Nav'

export default function App(){
  return (
    <div>
      <Nav />
      <main style={{padding: '1rem'}}>
        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/login" element={<Login/>} />
          <Route path="/register" element={<Register/>} />
          <Route path="/profile" element={<Profile/>} />
          <Route path="/favorites" element={<Favorites/>} />
        </Routes>
      </main>
    </div>
  )
}
