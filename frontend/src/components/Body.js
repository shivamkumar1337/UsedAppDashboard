import Graph from "./Graph";
import Table from "./Table";
import React, { useEffect, useState } from "react";
import DatePicker from "react-datepicker";
import { format } from "date-fns";
import "react-datepicker/dist/react-datepicker.css";
import GraphLine from "./GraphLine";
import { useNavigate } from "react-router-dom";
const Body = (processes) => {
  const navigate = useNavigate();
  const handleAppSelection = async (app_id) => {
    navigate(`/detail/${app_id}`);
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

      <div style={{ width: "50%", height: "400px", overflowY: "auto" }}>
        {/* <h3>Table</h3> */}
        <Table data={processes} onRowClick={handleAppSelection} />
      </div>
    </div>
  );
};

export default Body;
