import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import Detail from "./components/Detail";
// import Home from "./Home";
// import Detail from "./Detail";

const App = () => {
  return (
    <div style={{paddingBottom:'40px'}}>
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/detail/:app_id" element={<Detail/>} />
        <Route path="*" element={<Home />} />
      </Routes>
    </Router>
    </div>
  );
};

export default App;
