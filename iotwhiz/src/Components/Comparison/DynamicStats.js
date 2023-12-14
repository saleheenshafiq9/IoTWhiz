import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Comparison.css'; // Import the CSS file for the component

const DynamicStats = () => {
  const [statistics, setStatistics] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:8000/dynamic_stats', {
        headers: {
          'Content-Type': 'application/json',
        },
      }); // Replace with your FastAPI server address
      const data = response.data;
      setStatistics(data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const renderStats = () => {
    if (!statistics) {
      return <p>Loading...</p>;
    }

    return (
      <div className="statistics-container">
        <h2 className="title">Dynamic Class Loading Usage</h2>
        <div className="verdict">{statistics.Verdict}</div>
        <div className="list-container">
          <div className="iot">
            <h3 style={{ color: '#333' }}>For IoT Apps</h3>
            <ul>
              {statistics.IoT_Stats.split('\n').slice(1).map((line, index) => (
                <li key={index}>{line}</li>
              ))}
            </ul>
          </div>

          <div className="non-iot">
            <h3 style={{ color: '#333' }}>For Non-IoT Apps</h3>
            <ul>
              {statistics.Non_IoT_Stats.split('\n').slice(1).map((line, index) => (
                <li key={index}>{line}</li>
              ))}
            </ul>
          </div>
        </div>
        <img src="dynamic_histogram.png" alt="Histogram" />
      </div>
    );
  };

  return <div className="comparison-container">{renderStats()}</div>;
};

export default DynamicStats;
