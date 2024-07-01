import React from "react";
import { format } from "date-fns";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Detail = ({ appData }) => {
//   const sessionData = appData.sessions.map((session) => ({
//     start_time: new Date(session.start_time).getTime(),
//     end_time: new Date(session.end_time).getTime(),
//     duration: (new Date(session.end_time) - new Date(session.start_time)) / 1000, // duration in seconds
//   }));

  const aggregatedData = [];
  let accumulatedDuration = 0;

  appData.sessions.forEach((session) => {
    accumulatedDuration += session.duration;
    aggregatedData.push({
      time: format(new Date(session.end_time), 'yyyy-MM-dd HH:mm:ss'),
      total_duration: accumulatedDuration / 3600, // Convert to hours
    });
  });

  return (
    <div style={{ padding: 20, display: "flex", flexDirection: "row" }}>
      <div style={{ width: "50%" }}>
        <h1>{appData.app_name}</h1>
        <p>Total Duration: {appData.total_duration}</p>
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
      </div>

      <div style={{ width: "50%", height: "400px", overflowY: "auto" }}>
        <button onClick={()=>console.log(appData)}>console</button>
        <table style={tableStyle}>
          <thead>
            <tr>
              <th style={thStyle}>Start Time</th>
              <th style={thStyle}>End Time</th>
              <th style={thStyle}>Duration</th>
            </tr>
          </thead>
          <tbody>
            {appData.sessions.length > 0 ? (
              appData.sessions.map((session, index) => (
                <tr
                  key={index}
                  style={trStyle}
                  onMouseOver={handleMouseOver}
                  onMouseOut={handleMouseOut}
                >
                  <td style={tdStyle}>{session.start_time}</td>
                  <td style={tdStyle}>{session.end_time}</td>
                  <td style={tdStyle}>{session.duration}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="3" style={{ ...tdStyle, textAlign: "center" }}>
                  No data available
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

const tableStyle = {
  width: "100%",
  borderCollapse: "collapse",
  boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
};

const thStyle = {
  border: "1px solid #ddd",
  padding: 12,
  backgroundColor: "#4A249D",
  color: "white",
  textAlign: "left",
  fontWeight: "bold",
};

const tdStyle = {
  border: "1px solid #ddd",
  padding: 10,
  color: "#333",
};

const trStyle = {
  cursor: "pointer",
};

const handleMouseOver = (e) => {
  e.currentTarget.style.backgroundColor = "#f1f1f1";
};

const handleMouseOut = (e) => {
  e.currentTarget.style.backgroundColor = "";
};

export default Detail;
