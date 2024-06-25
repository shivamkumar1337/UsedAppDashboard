import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale } from 'chart.js';
ChartJS.register(
    BarElement,
    CategoryScale,
    LinearScale
  );
  
const Graph = ({ data }) => {
    const labels = data.system_apps.map(app => app.app_name);
    const durations = data.system_apps.map(app => {
      const [hours, minutes, seconds] = app.duration.split(':').map(Number);
      return hours * 60 + minutes + seconds / 60; // Convert duration to minutes
    });
  
    const chartData = {
      labels: labels,
      datasets: [{
        label: 'Duration (minutes)',
        data: durations,
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }]
    };
  
    return <Bar data={chartData} />;
  };

  export default Graph;