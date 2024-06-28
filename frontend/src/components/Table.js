import React from "react";

const Table = ({ data }) => {
  return (
    <div>
      {/* <button onClick={() => console.log(data)}>console</button> */}
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th style={{ border: "1px solid", padding: 8 }}>App Name</th>
            <th style={{ border: "1px solid", padding: 8 }}>Opening Time</th>
            <th style={{ border: "1px solid", padding: 8 }}>Closing Time</th>
            <th style={{ border: "1px solid", padding: 8 }}>Duration</th>
          </tr>
        </thead>
        <tbody>
          {data && data.processes.length > 0 ? (
            data.processes.map((app, index) => (
              <tr key={index}>
                <td style={{ border: "1px solid", padding: 6 }}>
                  {app.app_name}
                </td>
                <td style={{ border: "1px solid", padding: 6 }}>
                  {app.first_start_time_japan}
                </td>
                <td style={{ border: "1px solid", padding: 6 }}>
                  {app.final_end_time_japan}
                </td>
                <td style={{ border: "1px solid", padding: 6 }}>
                  {app.duration}
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td
                colSpan="4"
                style={{ border: "1px solid", padding: 6, textAlign: "center" }}
              >
                No data available
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default Table;
