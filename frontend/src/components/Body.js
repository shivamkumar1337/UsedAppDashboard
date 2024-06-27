import Graph from "./Graph";
import Table from "./Table";
import React, { useEffect, useState } from "react";
import DatePicker from "react-datepicker";
import { format } from "date-fns";
import "react-datepicker/dist/react-datepicker.css";
const tempData = [
    {
      name: "Calculator",
      start_time: "2024-06-25T08:30:00Z",
      end_time: "2024-06-25T08:45:00Z",
      runtime: "00:15:00",
    },
    {
      name: "Calendar",
      start_time: "2024-06-25T09:00:00Z",
      end_time: "2024-06-25T09:30:00Z",
      runtime: "00:30:00",
    },
    {
      name: "Settings",
      start_time: "2024-06-25T10:00:00Z",
      end_time: "2024-06-25T10:05:00Z",
      runtime: "00:05:00",
    },
    {
      name: "File Manager",
      start_time: "2024-06-25T11:15:00Z",
      end_time: "2024-06-25T11:45:00Z",
      runtime: "00:30:00",
    },
    {
      name: "Notes",
      start_time: "2024-06-25T12:00:00Z",
      end_time: "2024-06-25T12:10:00Z",
      runtime: "00:10:00",
    },
  ];

const Body = (processes) => {

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
