import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale } from 'chart.js';
ChartJS.register(
    BarElement,
    CategoryScale,
    LinearScale
  );
  
const Graph = ({ data }) => {
    const labels = data.processes.map(app => app.app_name);
    const durations = data.processes.map(app => app.duration_minutes);
  
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