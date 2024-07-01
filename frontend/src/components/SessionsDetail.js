import React, { useState,useEffect } from "react";
import SubHeadingDetail from "./SubheadingDetail";
import Detail from "./Detail";
import { useParams } from "react-router-dom";
const SessionsDetail = () => {
  const [processes, setProcesses] = useState([]);

  const { app_id } = useParams();
  const [appData, setAppData] = useState(null);

  useEffect(() => {
    const fetchAppData = async () => {
        try {
            const response = await fetch(`http://localhost:5000/sessions/${app_id}`);
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
            setAppData(finalData);
            // navigate(`/detail/${app_id}`);
            console.log(appData)
            // console.log(selectedAppData)
          } catch (error) {
            console.log(error);
          }
    };

    fetchAppData();
  }, [app_id]);

  if (!appData) {
    return <div>Loading...</div>;
  }
  return (
    <div>
      <SubHeadingDetail setProcesses={setProcesses} processes={processes} />
      {appData.sessions && <Detail appData={appData}/>}
      {/* <button onClick={()=>console.log(appData)}>console</button> */}
    </div>
  );
};

export default SessionsDetail;
