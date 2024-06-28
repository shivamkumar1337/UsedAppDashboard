import { useState } from "react";
import Body from "./components/Body";
import Header from "./components/Header";
import SubHeading from "./components/SubHeading";


function App() {
  const [processes, setProcesses] = useState([]);

  return (
    <div className="App">
      <Header/>
      <SubHeading setProcesses={setProcesses} processes={processes}/>
      <Body processes={processes}/>
    </div>
  );
}

export default App;
