import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { format } from 'date-fns';

const Detail = () => {
  const { app_id } = useParams();
  const [appData, setAppData] = useState(null);

  useEffect(() => {
    const fetchAppData = async () => {
      try {
        const response = await fetch(`http://localhost:5000/sessions/${app_id}`);
        const data = await response.json();
        setAppData(data);
      } catch (error) {
        console.error("Error fetching app data:", error);
      }
    };

    fetchAppData();
  }, [app_id]);

  if (!appData) {
    return <div>Loading...</div>;
  }

  // Prepare data for the chart
  const sessionData = appData.sessions.map((session) => ({
    start_time: new Date(session.start_time).getTime(),
    end_time: new Date(session.end_time).getTime(),
    duration: (new Date(session.end_time) - new Date(session.start_time)) / 1000, // duration in seconds
  }));

  const aggregatedData = [];
  let accumulatedDuration = 0;

  sessionData.forEach((session) => {
    accumulatedDuration += session.duration;
    aggregatedData.push({
      time: format(new Date(session.end_time), 'yyyy-MM-dd HH:mm:ss'),
      total_duration: accumulatedDuration / 3600, // Convert to hours
    });
  });

  return (
    <div style={{ padding: 20 }}>
      <h1>{appData.app_name}</h1>
      <p>Total Duration: {appData.total_duration}</p>
      <h2>Sessions</h2>
      <ul>
        {appData.sessions.map((session, index) => (
          <li key={index}>
            Start: {session.start_time}, End: {session.end_time}
          </li>
        ))}
      </ul>

      <h2>Session Durations</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart
          data={aggregatedData}
          margin={{
            top: 10,
            right: 30,
            left: 0,
            bottom: 0,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis label={{ value: 'Total Duration (hours)', angle: -90, position: 'insideLeft' }} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="total_duration" stroke="#8884d8" activeDot={{ r: 8 }} />
        </LineChart>
      </ResponsiveContainer>
      
      <button onClick={() => console.log(appData)}>console</button>
    </div>
  );
};

export default Detail;
