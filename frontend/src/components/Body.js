import Graph from "./Graph";
import Table from "./Table";
import React, { useEffect, useState } from "react";
import DatePicker from "react-datepicker"
import 'react-datepicker/dist/react-datepicker.css';
const tempData = {
  system_apps: [
    {
      app_name: "Calculator",
      opening_time: "2024-06-25T08:30:00Z",
      closing_time: "2024-06-25T08:45:00Z",
      duration: "00:15:00",
    },
    {
      app_name: "Calendar",
      opening_time: "2024-06-25T09:00:00Z",
      closing_time: "2024-06-25T09:30:00Z",
      duration: "00:30:00",
    },
    {
      app_name: "Settings",
      opening_time: "2024-06-25T10:00:00Z",
      closing_time: "2024-06-25T10:05:00Z",
      duration: "00:05:00",
    },
    {
      app_name: "File Manager",
      opening_time: "2024-06-25T11:15:00Z",
      closing_time: "2024-06-25T11:45:00Z",
      duration: "00:30:00",
    },
    {
      app_name: "Notes",
      opening_time: "2024-06-25T12:00:00Z",
      closing_time: "2024-06-25T12:10:00Z",
      duration: "00:10:00",
    },
  ],
};

const Body = () => {
  const [processes, setProcesses] = useState([]);
  const [fromDate, setFromDate] = useState(new Date());
  const [toDate, setToDate] = useState(new Date());

  const handlefromDateChange = (date) => {
    setFromDate(date);
  }
  const handleToDateChange = (date) => {
    setToDate(date);
  }
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
          justifyContent: "center",
          width: "100%",
          alignItems:"center"
          
        }}
      >
        <h3
          style={{
            padding: 10,
            fontSize: 20,
            position:"absolute",
            left:0
          }}
        >
          Welcome Shivam San !
        </h3>
        <div style={{display:"flex",flexDirection:"row", justifyContent:"space-between", width:"40%"}}>
          <div>

        <h3>From</h3>
        <DatePicker
        style={{padding:10}}
        
        selected={fromDate}
        onChange={handlefromDateChange}
        dateFormat="yyyy/MM/dd"
        />
        </div>
        <div>

        <h3>To</h3>
        <DatePicker
        style={{padding:10}}
        selected={toDate}
        onChange={handleToDateChange}
        dateFormat="yyyy/MM/dd"
        />
        </div>
        </div>
        <button
          style={{
            padding: 5,
            borderRadius: 8,
            backgroundColor: "#525CEB",
            color: "white",
            position:"absolute",
            right:0,
            margin:10
          }}
          onClick={fetchProcesses}
        >
          Get Data
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
        <Table data={tempData} />
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
        <Graph data={tempData} />
      </div>
    </div>
  );
};

export default Body;
