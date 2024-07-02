import React, { useEffect, useState } from "react";
import DatePicker from "react-datepicker";
import { format } from "date-fns";
import "react-datepicker/dist/react-datepicker.css";

const SubHeadingDetail = ({ setProcesses, app_id }) => {
  const [fromDateTime, setFromDateTime] = useState(new Date());
  const [toDateTime, setToDateTime] = useState(new Date());
  const [visibleCustomDate, setVisibleCustomDate] = useState(false);

  useEffect(() => {
    fetchProcessesToday();
  }, []);

  // useEffect(() => {
  //   fetchAppData();
  // }, [app_id]);

//   const fetchAppData = async () => {
//     try {
//         const response = await fetch(`http://localhost:5000/sessions/${app_id}`);
//         const data = await response.json();
//         // console.log(data)
//         const convertedData = data.sessions.map((item) => {
//           return {
//             ...item,
//             start_time: new Date(item.start_time).toLocaleString(),
//             end_time: new Date(item.end_time).toLocaleString(),
//             duration: item.duration
//           };
//         });
//         const finalData = {app_id:data.app_id,app_name:data.app_name,total_duration:data.total_duration,sessions:convertedData}
//         setProcesses(finalData);
//         // navigate(`/detail/${app_id}`);
//         // console.log(appData)
//         // console.log(selectedAppData)
//       } catch (error) {
//         console.log(error);
//       }
// };

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
        const response = await fetch(`http://localhost:5000/sessions/${app_id}`);
        const data = await response.json();
        // console.log(data)
        const convertedData = data.sessions.map((item) => {
          return {
            ...item,
            start_time: new Date(item.start_time).toLocaleString(),
            end_time: new Date(item.end_time).toLocaleString(),
            duration: item.duration
          };
        });
        const finalData = {app_id:data.app_id,app_name:data.app_name,total_duration:data.total_duration,sessions:convertedData}
        setProcesses(finalData);
        // navigate(`/detail/${app_id}`);
        // console.log(appData)
        // console.log(selectedAppData)
      } catch (error) {
        console.log(error);
      }
  };

  const fetchProcessesToday = async () => {
    try {
      const response = await fetch(`http://localhost:5000/sessions_today/${app_id}`);
      const data = await response.json();
      // console.log(data)
      const convertedData = data.sessions.map((item) => {
        return {
          ...item,
          start_time: new Date(item.start_time).toLocaleString(),
          end_time: new Date(item.end_time).toLocaleString(),
          duration: item.duration
        };
      });
      const finalData = {app_id:data.app_id,app_name:data.app_name,total_duration:data.total_duration,sessions:convertedData}
      setProcesses(finalData);
      // navigate(`/detail/${app_id}`);
      // console.log(appData)
      // console.log(selectedAppData)
    } catch (error) {
      console.log(error);
    }
  };

  const fetchProcessesCustom = async () => {
    try {
      const response = await fetch(
        `http://localhost:5000/sessions_custom/${app_id}?start_date=${encodeURIComponent(
          fromDateTime.toISOString()
        )}&end_date=${encodeURIComponent(toDateTime.toISOString())}`
      );
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data = await response.json();
      const convertedData = data.sessions.map((item) => {
        return {
          ...item,
          start_time: new Date(item.start_time).toLocaleString(),
          end_time: new Date(item.end_time).toLocaleString(),
          duration: item.duration
        };
      });
      const finalData = {app_id:data.app_id,app_name:data.app_name,total_duration:data.total_duration,sessions:convertedData}
      setProcesses(finalData);
      setVisibleCustomDate(false);
    } catch (error) {
      console.error("Error fetching session data:", error);
    }
  };
  const [currentDate, setCurrentDate] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentDate(new Date());
    }, 1000);

    return () => clearInterval(timer); // Clear interval on component unmount
  }, []);

  const formattedDate = format(currentDate, "yyyy, EEEE, dd");
  const formattedTime = format(currentDate, "HH:mm:ss");
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
            display: "flex",
            flexDirection: "row",
            alignItems: "center",
            justifyContent: "center",
          }}
          onClick={fetchProcessesToday}
          onMouseEnter={(e) => {
            e.target.style.color = "#4A249D";
          }}
          onMouseLeave={(e) => {
            e.target.style.color = "#333";
          }}
        >
          <h3>{formattedDate}</h3>, {formattedTime}
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
          <>
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
          </>
        )}
      </div>
    </div>
  );
};

export default SubHeadingDetail;
