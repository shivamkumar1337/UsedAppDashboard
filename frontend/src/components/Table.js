import React from 'react';

const Table = ({ data }) => {
  return (
    <div>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ border: '1px solid', padding: 8 }}>App Name</th>
            <th style={{ border: '1px solid', padding: 8 }}>Opening Time</th>
            <th style={{ border: '1px solid', padding: 8 }}>Closing Time</th>
            <th style={{ border: '1px solid', padding: 8 }}>Duration</th>
          </tr>
        </thead>
        <tbody>
          {data && data.length > 0 ? (
            data.map((app, index) => (
              <tr key={index}>
                <td style={{ border: '1px solid', padding: 6 }}>{app.name}</td>
                <td style={{ border: '1px solid', padding: 6 }}>{app.create_time}</td>
                <td style={{ border: '1px solid', padding: 6 }}>{app.end_time}</td>
                <td style={{ border: '1px solid', padding: 6 }}>{app.runtime}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="4" style={{ border: '1px solid', padding: 6, textAlign: 'center' }}>
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