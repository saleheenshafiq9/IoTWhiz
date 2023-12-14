import React from 'react'
import DownloadReport from './DownloadReport'
import DownloadFile from './DownloadFile'
import '../Home/Home.css'
import { Link } from 'react-router-dom'

const Download = () => {
  return (
    <>
<div style={{ textAlign: "center", marginTop: "50px" }}>
  <img
    src='./iot.jpg'
    alt='hh'
    width="600px"
    style={{
      borderRadius: "50%", /* Sets a semi-circle shape */
      width: "600px", /* Set the width */
      objectFit: "cover", /* Ensures the image covers the semi-circle shape */
      marginLeft: "10px"
    }}
  />
</div>

    <div className="center-container">
        <DownloadReport />
    </div>
    <div className='center-container'>
        <DownloadFile />
    </div>
    <br></br>
    <div className='center-container'>
        <Link to='/permissions' style={{
        marginTop: "15px",
        color: "#fff"
    }}>Find Top 10 Permission Co-occurrences</Link>
    </div>
    </>
  )
}

export default Download
