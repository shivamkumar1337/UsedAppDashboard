import Graph from "./Graph";
import Table from "./Table";
import React, { useEffect, useState } from "react";

const tempData = [
    {
      name: "Calculator",
      create_time: "2024-06-25T08:30:00Z",
      end_time: "2024-06-25T08:45:00Z",
      runtime: "00:15:00",
    },
    {
      name: "Calendar",
      create_time: "2024-06-25T09:00:00Z",
      end_time: "2024-06-25T09:30:00Z",
      runtime: "00:30:00",
    },
    {
      name: "Settings",
      create_time: "2024-06-25T10:00:00Z",
      end_time: "2024-06-25T10:05:00Z",
      runtime: "00:05:00",
    },
    {
      name: "File Manager",
      create_time: "2024-06-25T11:15:00Z",
      end_time: "2024-06-25T11:45:00Z",
      runtime: "00:30:00",
    },
    {
      name: "Notes",
      create_time: "2024-06-25T12:00:00Z",
      end_time: "2024-06-25T12:10:00Z",
      runtime: "00:10:00",
    }
  ];

const Body = () => {
  const [processes, setProcesses] = useState([]);

  const fetchProcesses = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/processes");
      const data = await response.json();
      console.log(data);
      setProcesses(data);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#F8EDFF",
        flexDirection: "column",
        padding: 10,
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          width: "100%",
        }}
      >
        <text
          style={{
            padding: 10,
            fontSize: 20,
          }}
        >
          Welcome Shivam San !
        </text>
        <button
          style={{
            padding: 5,
            borderRadius: 8,
            backgroundColor: "#525CEB",
            color: "white",
          }}
          onClick={fetchProcesses}
        >
          Refresh
        </button>
      </div>
      <div
        style={{
          width: "100%",
        //   backgroundColor: "#BFCFE7",
          margin: 5,
          borderRadius: 8,
          padding: 5,
        }}
      >
        <h3>Table</h3>
        <Table data={processes} />
      </div>
      <div
        style={{
          width: "100%",
        //   backgroundColor: "#BFCFE7",
          margin: 5,
          borderRadius: 8,
        }}
      >
        <h3>Graph</h3>
        <Graph data={processes} />
      </div>
    </div>
  );
};

export default Body;
