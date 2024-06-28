import Graph from "./Graph";
import Table from "./Table";
import React, { useEffect, useState } from "react";
import DatePicker from "react-datepicker";
import { format } from "date-fns";
import "react-datepicker/dist/react-datepicker.css";
import GraphLine from "./GraphLine";

const Body = (processes) => {

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#F8EDFF",
        flexDirection: "row",
        padding: 10,
      }}
    >
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
        <Table data={processes} />
      </div>
      
    </div>
  );
};

export default Body;
