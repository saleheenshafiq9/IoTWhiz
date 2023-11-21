import React, {useState,useEffect,useRef} from 'react'
import './Home.css'

const Home = () => {
  const [showOptions, setShowOptions] = useState(false);
  const dropdownRef = useRef(null);
  const apkInputRef = useRef(null);

    const handleFolderUpload = (event) => {
        const folderPath = event.target.files[0].webkitRelativePath.split('/')[0];
        console.log(folderPath); // Displays the first part of the folder path
        fetch('http://localhost:8000/upload-folder/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ folder_path: folderPath }),
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                // Handle the response from the backend
            })
            .catch(error => {
                console.error('Error:', error);
                // Handle errors
            });

            fetch('http://localhost:8000/analyze-layout/', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({ folder_path: folderPath }),
              })
              .then(response => response.json())
              .then(data => {
                  console.log(data);
                  // Handle the response from the backend
              })
              .catch(error => {
                  console.error('Error:', error);
                  // Handle errors
              });
      };

      const handleDecompileAPK = (option) => {
        if (option === 'upload') {
          apkInputRef.current.click(); // Trigger file selection dialog for APK
        } else if (option === 'download') {
          // Logic for downloading from AndroZoo
        }
        setShowOptions(false); // Hide the dropdown after selecting an option
      };

      const handleAPKFileUpload = (event) => {
        const apkFile = event.target.files[0];
        if (apkFile) {
          const data = { file_name: apkFile.name };
      
          fetch('http://localhost:8000/upload-apk/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
          })
            .then(response => response.json())
            .then(data => {
              console.log('Response from backend:', data);
              // Handle the response from the backend
            })
            .catch(error => {
              console.error('Error:', error);
              // Handle errors
            });
        }
      };

      const handleClickOutside = (event) => {
        if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
          setShowOptions(false);
        }
      };

      useEffect(() => {
        if (showOptions) {
          document.addEventListener('click', handleClickOutside);
        } else {
          document.removeEventListener('click', handleClickOutside);
        }
    
        return () => {
          document.removeEventListener('click', handleClickOutside);
        };
      }, [showOptions]);
      
  return (
    <div className='content'>
    <img src='./city.png' alt='city' width='350px' style={{ marginTop: '40px' }} />
    <h1>
      IoTWhiz
    </h1>
    <p className='tool-summary'>
      <span>A Comprehensive Analysis Tool for IoT and Non-IoT Android Apps.</span><br />
      <span>Discover distinctive characteristics using API usage, permissions, UI layouts, code size, and more.</span><br />
      <span>Visualizations unveil app differences, guiding efficient development choices.</span>
    </p>
    <div className="button-container">
      <div className="dropdown" ref={dropdownRef}>
        <label className="dropdown-btn" onClick={() => setShowOptions(!showOptions)}>Decompile APK</label>
        {showOptions && (
          <div className="dropdown-content">
            <span onClick={() => handleDecompileAPK('upload')}>Upload APK</span>
            <span onClick={() => handleDecompileAPK('download')}>Download from AndroZoo</span>
          </div>
        )}
      </div>
      <label htmlFor="folder-upload" className="custom-file-upload">
        Upload Project Folder
      </label>
      <input
        id="folder-upload"
        type="file"
        webkitdirectory=""
        onChange={handleFolderUpload}
        style={{ display: 'none' }}
      />
    </div>
          <label htmlFor="apk-upload" className="custom-file-upload" style={{ display: 'none' }}>
            Select APK File
          </label>
          <input
            id="apk-upload"
            type="file"
            accept=".apk"
            ref={apkInputRef}
            onChange={handleAPKFileUpload}
            style={{ display: 'none' }}
          />
  </div>
  )
}

export default Home
