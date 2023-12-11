import React, { useState, useEffect } from 'react';
import './Comparison.css'; 
import Chart from 'chart.js/auto';
import PermissionCounts from './PermissionCounts';

const PermissionStats = () => {
  const [statistics, setStatistics] = useState(null);
  const [cooccurrences, setCooccurrences] = useState(null)

  useEffect(() => {
    fetch('http://localhost:8000/permission_cooccurrences')
      .then(response => response.json())
      .then(data => setCooccurrences(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  useEffect(() => {
    if (cooccurrences) {
      renderCharts();
    }
  });

  const renderCharts = () => {
    destroyChart('iotChart');
    destroyChart('nonIotChart');

    if (cooccurrences) {
      renderChart('iotChart', cooccurrences.iot_cooccurrences, 'Top 10 IoT Co-Occurrences');
      renderChart('nonIotChart', cooccurrences.non_iot_cooccurrences, 'Top 10 Non-IoT Co-Occurrences');
    }
  };

  const destroyChart = (chartId) => {
    const chartInstance = Chart.getChart(chartId);
    if (chartInstance) {
      chartInstance.destroy();
    }
  };
    const renderChart = (chartId, dataObject, title) => {
        const permissions = Object.entries(dataObject)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10)
        .map(([permission]) => permission);
      
      const counts = Object.entries(dataObject)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10)
        .map(([permission, count]) => count);

        const backgroundColors = chartId === 'iotChart'
        ? 'rgba(75,192,192,1)' // Use the same color for IoT
        : 'rgba(255,99,132,1)'; // Different color for non-IoT
  
      const chartData = {
        labels: permissions,
        datasets: [
          {
            label: 'Permission Counts',
            backgroundColor: backgroundColors,
            borderColor: 'rgba(0,0,0,1)',
            borderWidth: 1,
            hoverBackgroundColor: backgroundColors.replace(',1)', ',0.4)'),
            hoverBorderColor: 'rgba(0,0,0,1)',
            data: counts,
          },
        ],
      };
  
      const ctx = document.getElementById(chartId);
  
      if (ctx) {
        new Chart(ctx, {
          type: 'bar',
          data: chartData,
          options: {
            indexAxis: 'y',
            plugins: {
              title: {
                display: true,
                text: title,
              },
              legend: {
                display: true,
                position: 'right',
              },
            },
            scales: {
              y: {
                beginAtZero: true,
              },
              x: {
                labels: permissions, // Set the same labels for both charts
                min: 0, // Set the minimum value for the x-axis
                max: 140, // Set the maximum value for the x-axis
              },
            },
          },
        });
      }
    };

  useEffect(() => {
    fetch('http://localhost:8000/permission_stats')
      .then(response => response.json())
      .then(data => setStatistics(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  if (!statistics) return <p>Loading...</p>;

  // Extract data from statistics object
  const { permission_stats } = statistics;
  const { count, max, min, mean, std } = permission_stats;

  return (
    <>
    <div className="statistics-container" style={{ color: "#333" }}>
    <h1>Permission Stats</h1>

    <p>Count: {count.iot} (IoT) / {count["non-iot"]} (Non-IoT)</p>
    <p>Max: {max.iot} (IoT) / {max["non-iot"]} (Non-IoT)</p>
    <p>Mean: {mean.iot.toFixed(3)} (IoT) / {mean["non-iot"].toFixed(3)} (Non-IoT)</p>
    <p>Min: {min.iot} (IoT) / {min["non-iot"]} (Non-IoT)</p>
    <p>Std: {std.iot.toFixed(3)} (IoT) / {std["non-iot"].toFixed(3)} (Non-IoT)</p>
    </div>
    <div className="statistics-container" style={{ color: '#333' }}>
      <h2>Permission Co-Occurrences</h2>
      <div className="row">
        <div className="col-6">
          <h3>iot_cooccurrences</h3>
          <canvas id="iotChart" width="400" height="400"></canvas>
        </div>
        <div className="col-6">
          <h3>non_iot_cooccurrences</h3>
          <canvas id="nonIotChart" width="400" height="400"></canvas>
        </div>
      </div>
    </div>
    <div className='statistics-container'>
      <PermissionCounts />
    </div>
    </>
  );
};

export default PermissionStats;
