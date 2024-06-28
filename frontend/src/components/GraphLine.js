import React from "react";
import { Line } from "react-chartjs-2";

const GraphLine = ({ data }) => {
  // Extract labels (process names) and data points (durations)
  const labels = data.map((item) => item.name);
  const durations = data.map((item) => item.duration);

  // Chart.js data object format
  const chartData = {
    labels: labels,
    datasets: [
      {
        label: "Process Durations (minutes)",
        data: durations,
        fill: false,
        borderColor: "rgb(75, 192, 192)",
        tension: 0.1,
      },
    ],
  };

  // Chart.js options
  const chartOptions = {
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: "Duration (minutes)",
        },
      },
    },
  };

  return (
    <div>
      <Line data={chartData} options={chartOptions} />
    </div>
  );
};

export default GraphLine;
