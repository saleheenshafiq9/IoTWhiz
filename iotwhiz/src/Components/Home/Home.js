import React, {useState,useEffect,useRef} from 'react'
import Modal from 'react-modal';
import './Home.css'
import Analysis from '../Analysis/Analysis';
import CountAnalysis from '../Analysis/CountAnalysis';
import ReflectionAnalysis from '../Analysis/ReflectionAnalysis';
import DatabaseStorage from '../Analysis/DatabaseStorage';

const Home = () => {
  const [showOptions, setShowOptions] = useState(false);
  const dropdownRef = useRef(null);
  const apkInputRef = useRef(null);
  const [showModal, setShowModal] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [sha256, setSha256] = useState('');
  const [downloading, setDownloading] = useState(false); // New state for download status
  const [downloadSuccess, setDownloadSuccess] = useState(false); // New state for download success message
  const [decompilationSuccessful, setDecompilationSuccessful] = useState(false);
  const [uploadAPK, setUploadAPK] = useState(false);
  const [decompileAPK, setDecompileAPK] = useState(false);
  const [genericAnalysis, setGenericAnalysis] = useState(null)
  const [lineAnalysis, setLineAnalysis] = useState(null)
  const [databaseAnalysis, setDatabaseAnalysis] = useState(null)
  const [reflectionAnalysis, setReflectionAnalysis] = useState(null)
  const [layoutAnalysis, setLayoutAnalysis] = useState(null)
  const [uploadProject, setUploadProject] = useState(false)

    const handleFolderUpload = (event) => {
        setUploadProject(true);
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
                setGenericAnalysis(data);
            })
            .catch(error => {
                console.error('Error:', error);
                // Handle errors
            });

            fetch('http://localhost:8000/loc-class-method/', {
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
                setLineAnalysis(data);
            })
            .catch(error => {
                console.error('Error:', error);
                // Handle errors
            });

            fetch('http://localhost:8000/reflection/', {
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
                setReflectionAnalysis(data);
            })
            .catch(error => {
                console.error('Error:', error);
                // Handle errors
            });

            fetch('http://localhost:8000/database-storage/', {
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
                  setDatabaseAnalysis(data);
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
                  setLayoutAnalysis(data)
                  setUploadProject(false);
              })
              .catch(error => {
                  console.error('Error:', error);
                  // Handle errors
                  setUploadProject(false);
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
        // console.log(data)
        setDownloading(true); // Start download, set state to true
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
            setDownloading(false); // End download, set state to false after receiving the response
            setDownloadSuccess(true); // Show 'Download Successful!' message
            setTimeout(() => {
              setDownloadSuccess(false); // Hide 'Download Successful!' after a certain duration
            }, 3000); // Hide after 3 seconds (adjust as needed)
          })
          .catch(error => {
            console.error('Error:', error);
            // Handle errors
            setDownloading(false); // End download, set state to false in case of an error
          });
      };
      
      const handleGetSourceCode = () => {
        // Logic for getting source code using apiKey and sha256 values
        setDownloading(true); // Start download, set state to true
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
            setDownloading(false); // End download, set state to false after receiving the response
            setDownloadSuccess(true); // Show 'Download Successful!' message
            setTimeout(() => {
              setDownloadSuccess(false);
              setTimeout(() => {
                setDecompilationSuccessful(true);
                setTimeout(() => {
                  setDecompilationSuccessful(false); // Reset to false after 3 seconds
                }, 3000); 
              }, 3000);
            }, 3000); // Hide after 3 seconds (adjust as needed)
          })
          .catch(error => {
            console.error('Error:', error);
            // Handle errors
            setDownloading(false); // End download, set state to false in case of an error
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
          setUploadAPK(true);
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
              setUploadAPK(false);
              // Handle the response from the backend
              setDecompileAPK(true); // Show 'Download Successful!' message
                setTimeout(() => {
                  setDecompileAPK(false); 
                }, 3000); // Hide after 3 seconds (adjust as needed)
            })
            .catch(error => {
              console.error('Error:', error);
              // Handle errors
              setUploadAPK(false);
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
    <>
    {!genericAnalysis && !layoutAnalysis && !lineAnalysis &&
    <div className='content'>
    <img src='./city.png' alt='city' width='350px' style={{ marginTop: '40px' }} />
    <h1 style={{
      marginTop: "40px",
      marginBottom: "40px"
    }}>
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
        {uploadAPK && <p style={{
          marginTop: "40px"
        }}>Uploading & Decompiling...</p>} {/* Show 'Downloading...' if downloading */}
        {decompileAPK && <p style={{
          color: '#C3EB78',
          marginTop: "40px"
        }}>Decompilation Successful!</p>} {/* Show 'Download Successful!' message */}
        {uploadProject && <p style={{
          marginTop: "40px"
        }}>Decompiling...</p>} {/* Show 'Downloading...' if downloading */}

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
        {downloading && <p>Downloading...</p>} {/* Show 'Downloading...' if downloading */}
        {downloadSuccess && <p style={{
          color: '#C3EB78'
        }}>Download Successful!</p>} {/* Show 'Download Successful!' message */}
        {decompilationSuccessful && <p style={{
          color: '#C3EB78'
        }}>Decompilation Successful!</p>} {/* Show 'Download Successful!' message */}
      </Modal>
  </div>
    }

  {genericAnalysis && layoutAnalysis && lineAnalysis && databaseAnalysis && reflectionAnalysis && (
    <div>
      <div className='row'>
        <div className='col-3'>
          <Analysis genericAnalysis={genericAnalysis} layoutAnalysis={layoutAnalysis} />
        </div>
        <div className='col-3'>
          <ReflectionAnalysis lineAnalysis={reflectionAnalysis} />
        </div>
        <div className='col-3'>
          <DatabaseStorage dataAnalysis={databaseAnalysis} />
        </div>
        <div className='col-3'>
          <CountAnalysis lineAnalysis={lineAnalysis} />
        </div>
      </div>
    </div>
    )}
    </>
    )
}

export default Home
