import React from 'react'
import './Navbar.css'

const Navbar = () => {
  return (
    <div>
      <header className="navbar">
        <div className="logo">
          {/* Your logo image */}
          <img src="logo.png" alt="Logo" />
        </div>
        <nav className="nav-menu">
          <ul>
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
            {/* Add more menu items here */}
          </ul>
        </nav>
      </header>
    </div>
  )
}

export default Navbar
