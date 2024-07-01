import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale } from 'chart.js';
import React from 'react';

ChartJS.register(
    BarElement,
    CategoryScale,
    LinearScale
);

const parseDuration = (duration) => {
    const [hours, minutes, seconds] = duration.split(':').map(Number);
    return hours + minutes / 60 + seconds / 3600; // Convert duration to hours
};

const Graph = ({ data }) => {
    const labels = data.processes.map(app => app.app_name);
    const durations = data.processes.map(app => parseDuration(app.duration));
  
    const chartData = {
      labels: labels,
      datasets: [{
        label: 'Duration (hours)',
        data: durations,
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }]
    };
  
    return <Bar data={chartData} />;
};

export default Graph;
