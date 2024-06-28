import Graph from "./Graph";
import Table from "./Table";
import React, { useEffect, useState } from "react";
import DatePicker from "react-datepicker";
import { format } from "date-fns";
import "react-datepicker/dist/react-datepicker.css";

const SubHeading = ({ setProcesses,processes }) => {
  const [fromDateTime, setFromDateTime] = useState(new Date());
  const [toDateTime, setToDateTime] = useState(new Date());

  useEffect(()=>{fetchProcesses()},[])
  const handlefromDateChange = (date) => {
    const newDate = new Date(date.target.value);
    setFromDateTime(newDate);
  };
  const handleToDateChange = (date) => {
    const newDate = new Date(date.target.value);
    setToDateTime(newDate);
  };

  const fetchProcesses = async () => {
    try {
      const response = await fetch("http://localhost:5000/aggregated_sessions");
      const data = await response.json();
      const convertedData = data.map((item) => {
        return {
          ...item,
          first_start_time_japan: new Date(item[1]).toLocaleString(),
          final_end_time_japan: new Date(item[2]).toLocaleString(),
        };
      });
      setProcesses(convertedData);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "flex-end",
        // width: "100%",
        alignItems: "center",
        paddingTop:10
      }}
    >
      <h3
        style={{
          padding: 10,
          fontSize: 20,
        //   position: "absolute",
        //   left: 0,
        width:"20%"
        }}
      >
        Welcome Shivam San !
      </h3>
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          justifyContent: "space-between",
          width: "80%",
        //   border:1,
          borderRadius:8,
          borderColor:"#525CEB"
        }}
      >
        <div>
          <h3>Search</h3>
          <input type="text" />
        </div>
        {/* <div
            style={{
              display: "flex",
              flexDirection: "row",
              justifyContent: "center",
              alignItems: "center",
            }}
          > */}
        <div>
          <h3>From</h3>
          <input
            type="datetime-local"
            value={format(fromDateTime, "yyyy-MM-dd'T'HH:mm:ss")}
            onChange={handlefromDateChange}
          />
        </div>
        <div>
          <h3>To</h3>
          <input
            type="datetime-local"
            value={format(toDateTime, "yyyy-MM-dd'T'HH:mm:ss")}
            onChange={handleToDateChange}
          />
        </div>
        <button
          style={{
            padding: 10,
            borderRadius: 8,
            backgroundColor: "#525CEB",
            color: "white",
            height:"100%",
            margin: 10,
          }}
          onClick={fetchProcesses}
        >
          Get Data
        </button>
        {/* </div> */}
      </div>
     </div>
  );
};

export default SubHeading;
