import Graph from "./Graph";
import Table from "./Table";
import React, { useEffect, useState } from "react";
import DatePicker from "react-datepicker";
import { format } from "date-fns";
import "react-datepicker/dist/react-datepicker.css";
import GraphLine from "./GraphLine";
import { useNavigate } from "react-router-dom";
const Body = (processes) => {
  const [selectedAppData, setSelectedAppData] = useState(null);
  const navigate = useNavigate();
  const handleAppSelection = async (app_id) => {
    try {
      const response = await fetch(`http://localhost:5000/sessions/${app_id}`);
      const data = await response.json();
      console.log(data)
      const convertedData = data.sessions.map((item) => {
        return {
          ...item,
          start_time: new Date(item.start_time).toLocaleString(),
          end_time: new Date(item.end_time).toLocaleString(),
        };
      });
      setSelectedAppData(convertedData);
      navigate(`/detail/${app_id}`);
      console.log(selectedAppData)
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
        // backgroundColor: "#F8EDFF",
        flexDirection: "row",
        padding: 10,
      }}
    >
      {/* <button onClick={()=>handleAppSelection(1)}>button</button> */}
      <div
        style={{
          width: "50%",
          //   backgroundColor: "#BFCFE7",
          margin: 5,
          borderRadius: 8,
        }}
      >
        {/* <h3>Graph</h3> */}
        <Graph data={processes} />
      </div>
      
      <div
        style={{
          width: "50%",
          //   backgroundColor: "#BFCFE7",
          margin: 5,
          borderRadius: 8,
          padding: 5,
        }}
      >
        {/* <h3>Table</h3> */}
        <Table data={processes} onRowClick={handleAppSelection}/>
      </div>
      
    </div>
  );
};

export default Body;
