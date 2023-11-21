import React, {useState,useEffect,useRef} from 'react'
import Modal from 'react-modal';
import './Home.css'

const Home = () => {
  const [showOptions, setShowOptions] = useState(false);
  const dropdownRef = useRef(null);
  const apkInputRef = useRef(null);
  const [showModal, setShowModal] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [sha256, setSha256] = useState('');

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
          setShowModal(true);
        }
        setShowOptions(false); // Hide the dropdown after selecting an option
      };

      const handleModalClose = () => {
        setShowModal(false);
        // Optionally, reset API key and SHA256 state values
        setApiKey('');
        setSha256('');
      };

      const handleDownloadAPK = () => {
        // Logic for downloading APK using apiKey and sha256 values
        const data = { api_key: apiKey, sha256: sha256 };
        console.log(data)
        fetch('http://localhost:8000/receive-api-key-sha256/', {
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
      };
      
      const handleGetSourceCode = () => {
        // Logic for getting source code using apiKey and sha256 values
        const data = { api_key: apiKey, sha256: sha256 };
      
        fetch('http://localhost:8000/receive-api-key-sha256-get-source-code/', {
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
      };
      
      const handleModalSubmit = (choice) => {
        // Logic for handling the modal form submission
        console.log('API Key:', apiKey);
        console.log('SHA256 Code:', sha256);
        // Perform actions with the entered data
        if (choice === 'download') {
          handleDownloadAPK();
        } else if (choice === 'get_source_code') {
          handleGetSourceCode();
        }
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
      <Modal isOpen={showModal} onRequestClose={handleModalClose} className="modal" overlayClassName="overlay">
        <header>
        <button className="close-btn" onClick={handleModalClose}>
          <span aria-hidden="true">×</span>
        </button>
        </header>
        <img src='download.png' alt='download' width='70px' style={{
          marginBottom:'20px'
        }}/>
        <h2 style={{
          marginBottom: '40px'
        }}>Download from AndroZoo</h2>
        <div className="modal-inputs">
          <input
            type="text"
            placeholder="Your API Key"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            className="custom-input"
          />
          <input
            type="text"
            placeholder="SHA256 Code"
            value={sha256}
            onChange={(e) => setSha256(e.target.value)}
            className="custom-input"
          />
        </div>
        <div className="modal-buttons" style={{
          marginBottom: '20px'
        }}>
          <button onClick={() => handleModalSubmit('download')} className="custom-file-upload">
            Download APK
          </button>
          <button onClick={() => handleModalSubmit('get_source_code')} className="custom-file-upload">
            Get Source Code
          </button>
        </div>
      </Modal>
  </div>
  )
}

export default Home
