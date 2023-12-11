import React from 'react'
import { Link } from 'react-router-dom';
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
          <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/about">About</Link>
            </li>
            <li>
              <Link to="/permissionsC">Result</Link>
            </li>
          </ul>
        </nav>
      </header>
    </div>
  )
}

export default Navbar
