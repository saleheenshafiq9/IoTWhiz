import React, { useState, useEffect } from 'react';

const PermissionCounts = () => {
  const [permissionCounts, setPermissionCounts] = useState({});

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch('http://localhost:8000/permission-counts'); // Replace with your FastAPI server address
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setPermissionCounts(data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const renderStats = () => {
    if (!permissionCounts) {
      return <p>Loading...</p>;
    }
    const { t_statistic, p_value, verdict, distribution_path } = permissionCounts;

    return (
      <div className="permission-container">
        <h3>Permission Analysis</h3>
        <p>T-statistic: {t_statistic}</p>
        <p>P-value: {p_value}</p>
        <p>Verdict: {verdict}</p>
        <img src={distribution_path} alt="Permission Frequency Distribution" />
      </div>
    );
    }

  return (
    <div className="comparison-container">
      {renderStats()}
    </div>
  );
};

export default PermissionCounts;