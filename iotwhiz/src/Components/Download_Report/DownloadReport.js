import React, { useState } from 'react';
import axios from 'axios';
import '../Home/Home.css';

const DownloadReport = () => {
  const [generated, setGenerated] = useState(false);
  const [loading, setLoading] = useState(false); // New state for loading indicator

  const handleGenerate = async () => {
    setLoading(true); // Set loading to true when request starts
    try {
      const response = await axios.get('http://localhost:8000/generate-pdf');

      if (response.status === 200) {
        setGenerated(true);
      } else {
        console.error('Failed to generate PDF');
      }
    } catch (error) {
      console.error('Error occurred:', error);
    } finally {
      setLoading(false); // Set loading to false when request completes (whether success or error)
    }
  };

  return (
    <div>
      <button className="custom-file-upload" onClick={handleGenerate} disabled={loading}>
        {loading ? 'Generating...' : 'Generate Report'}
      </button>
      {loading && <div className="spinner"></div>}
      {generated && <p>PDF generated!</p>}
    </div>
  );
};

export default DownloadReport;
