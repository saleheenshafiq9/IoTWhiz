import React from 'react';
import '../Home/Home.css';

const DownloadFile = () => {
  return (
    <div> {/* Create a container */}
      <a
        id="button"
        type="button"
        href="./out.pdf"
        download="out.pdf"
        className='custom-file-upload'
        style={{
          textDecoration: "none"
        }}
      >
        Download Current Report
      </a>
    </div>
  );
};

export default DownloadFile;
