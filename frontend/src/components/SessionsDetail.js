import React, { useState,useEffect } from "react";
import SubHeadingDetail from "./SubheadingDetail";
import Detail from "./Detail";
import { useParams } from "react-router-dom";
const SessionsDetail = () => {
  const [processes, setProcesses] = useState([]);

  const { app_id } = useParams();
  // const [appData, setAppData] = useState(null);

  if (!processes) {
    return <div>Loading...</div>;
  }
  return (
    <div>
      <SubHeadingDetail app_id={app_id} setProcesses={setProcesses}/>
      {processes.sessions && <Detail appData={processes}/>}
    </div>
  );
};

export default SessionsDetail;
