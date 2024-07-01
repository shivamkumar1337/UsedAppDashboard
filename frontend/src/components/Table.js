import React from "react";

const Table = ({ data, onRowClick }) => {
  return (
    <div>
      <table style={tableStyle}>
        <thead>
          <tr>
            <th style={thStyle}>App Name</th>
            <th style={thStyle}>Opening Time</th>
            <th style={thStyle}>Closing Time</th>
            <th style={thStyle}>Duration</th>
          </tr>
        </thead>
        <tbody>
          {data && data.processes.length > 0 ? (
            data.processes.map((app, index) => (
              <tr
                key={index}
                style={trStyle}
                onClick={() => onRowClick(app.app_id)}
                onMouseOver={handleMouseOver}
                onMouseOut={handleMouseOut}
              >
                <td style={tdStyle}>{app.app_name}</td>
                <td style={tdStyle}>{app.first_start_time_japan}</td>
                <td style={tdStyle}>{app.final_end_time_japan}</td>
                <td style={tdStyle}>{app.duration}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="4" style={{ ...tdStyle, textAlign: "center" }}>
                No data available
              </td>
            </tr>
          )}
        </tbody>
      </table>
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

export default Table;
