import React, { useEffect, useState } from "react";
import DatePicker from "react-datepicker";
import { format } from "date-fns";
import "react-datepicker/dist/react-datepicker.css";

const SubHeading = ({ setProcesses, processes }) => {
  const [fromDateTime, setFromDateTime] = useState(new Date());
  const [toDateTime, setToDateTime] = useState(new Date());
  const [visibleCustomDate, setVisibleCustomDate] = useState(false);
  const today = new Date();
  const formattedDate = format(today, "yyyy, EEEE, dd");
  useEffect(() => {
    fetchProcessesToday();
  }, []);

  const handleFromDateChange = (date) => {
    setFromDateTime(date);
    // Close date picker after selection
    // setVisibleCustomDate(false);
  };

  const handleToDateChange = (date) => {
    setToDateTime(date);
    // Close date picker after selection
    // setVisibleCustomDate(false);
  };

  const fetchProcesses = async () => {
    try {
      const response = await fetch("http://localhost:5000/aggregated_sessions");
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data = await response.json();
      const convertedData = data.map((item) => ({
        ...item,
        first_start_time_japan: new Date(
          item.first_start_time
        ).toLocaleString(),
        final_end_time_japan: new Date(item.final_end_time).toLocaleString(),
      }));
      setProcesses(convertedData);
    } catch (error) {
      console.log("Error fetching all time data:", error);
    }
  };

  const fetchProcessesToday = async () => {
    try {
      const response = await fetch(
        "http://localhost:5000/aggregated_sessions_today"
      );
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data = await response.json();
      const convertedData = data.map((item) => ({
        ...item,
        first_start_time_japan: new Date(
          item.first_start_time
        ).toLocaleString(),
        final_end_time_japan: new Date(item.final_end_time).toLocaleString(),
      }));
      setProcesses(convertedData);
    } catch (error) {
      console.log("Error fetching today's data:", error);
    }
  };

  const fetchProcessesCustom = async () => {
    try {
      const response = await fetch(
        `http://localhost:5000/aggregated_sessions_custom?start_date=${encodeURIComponent(
          fromDateTime.toISOString()
        )}&end_date=${encodeURIComponent(toDateTime.toISOString())}`
      );
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data = await response.json();
      const convertedData = data.map((item) => ({
        ...item,
        first_start_time_japan: new Date(
          item.first_start_time
        ).toLocaleString(),
        final_end_time_japan: new Date(item.final_end_time).toLocaleString(),
      }));
      setProcesses(convertedData);
      setVisibleCustomDate(false);
    } catch (error) {
      console.error("Error fetching session data:", error);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "10px 20px",
        backgroundColor: "#f0f0f0",
        borderRadius: "8px",
        boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
      }}
    >
      <div style={{ display: "flex", alignItems: "center" }}>
        <button
          style={{
            fontSize: "24px",
            backgroundColor: "transparent",
            border: "none",
            outline: "none",
            cursor: "pointer",
            color: "#333",
            marginRight: "20px",
          }}
          onClick={fetchProcessesToday}
          onMouseEnter={(e) => {
            e.target.style.color = "#4A249D";
          }}
          onMouseLeave={(e) => {
            e.target.style.color = "#333";
          }}
        >
          {formattedDate}
        </button>
        <button
          style={{
            padding: "10px 20px",
            borderRadius: "8px",
            backgroundColor: "#4A249D",
            color: "white",
            border: "none",
            outline: "none",
            cursor: "pointer",
            marginRight: "10px",
          }}
          onClick={fetchProcesses}
        >
          Show All Time Data
        </button>
      </div>

      <div style={{ display: "flex", alignItems: "center" }}>
        {visibleCustomDate ? (
          <div style={{ display: "flex", alignItems: "center" }}>
            <div style={{ marginRight: "20px" }}>
              <h3 style={{ marginBottom: "5px" }}>From</h3>
              <DatePicker
                selected={fromDateTime}
                onChange={handleFromDateChange}
                showTimeSelect
                dateFormat="yyyy-MM-dd HH:mm:ss"
                className="date-picker"
              />
            </div>
            <div style={{ marginRight: "20px" }}>
              <h3 style={{ marginBottom: "5px" }}>To</h3>
              <DatePicker
                selected={toDateTime}
                onChange={handleToDateChange}
                showTimeSelect
                dateFormat="yyyy-MM-dd HH:mm:ss"
                minDate={fromDateTime}
                className="date-picker"
              />
            </div>
            <button
              style={{
                padding: "10px 20px",
                borderRadius: "8px",
                backgroundColor: "#4A249D",
                color: "white",
                border: "none",
                outline: "none",
                cursor: "pointer",
                marginRight: "10px",
              }}
              onClick={fetchProcessesCustom}
            >
              Go
            </button>
          </div>
        ) : (
          <button
            style={{
              padding: "10px 20px",
              borderRadius: "8px",
              backgroundColor: "#4A249D",
              color: "white",
              border: "none",
              outline: "none",
              cursor: "pointer",
            }}
            onClick={() => setVisibleCustomDate(true)}
          >
            Select Custom Date
          </button>
        )}
      </div>
    </div>
  );
};

export default SubHeading;
