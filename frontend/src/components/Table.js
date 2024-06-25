const Table = ({ data }) => {
    return (
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ border: '1px solid ', padding: 8 }}>App Name</th>
            <th style={{ border: '1px solid ', padding: 8 }}>Opening Time</th>
            <th style={{ border: '1px solid ', padding: 8 }}>Closing Time</th>
            <th style={{ border: '1px solid ', padding: 8 }}>Duration</th>
          </tr>
        </thead>
        <tbody>
          {data.system_apps.map((app, index) => (
            <tr key={index}>
              <td style={{ border: '1px solid', padding: 6 }}>{app.app_name}</td>
              <td style={{ border: '1px solid', padding: 6 }}>{new Date(app.opening_time).toLocaleString()}</td>
              <td style={{ border: '1px solid', padding: 6 }}>{new Date(app.closing_time).toLocaleString()}</td>
              <td style={{ border: '1px solid', padding: 6 }}>{app.duration}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  export default Table;