import React, { useState } from "react";
import SubHeading from "./SubHeading";
import Body from "./Body";

const Home = () => {
  const [processes, setProcesses] = useState([]);

  const handleRowClick = (appId) => {
    window.location.href = `/detail/${appId}`;
  };

  return (
    <div>
      <SubHeading setProcesses={setProcesses} processes={processes} />
      <Body processes={processes} onRowClick={handleRowClick} />
    </div>
  );
};

export default Home;
