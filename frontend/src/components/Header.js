import React from "react";

const Header = () => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row",
        backgroundColor: "#4A249D",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "10px 20px",
      }}
    ><div style={{display: "flex",
      flexDirection: "row",}}>

      <img
          src="/logo.jpg"
          alt="Avatar"
          style={{ width: "50px", height: "50px",borderRadius:8,   marginRight:20}}
          />
      <h3
        style={{
          fontSize: 40,
          color: "#F9E2AF",
          margin: 0,
        }}
        >
        APP USAGE DASHBOARD
      </h3>
        </div>
      <div style={{ display: "flex", alignItems: "center" }}>
        <h3 style={{ fontSize: 20, color: "#f1f1f1", marginRight: "20px" }}>
          Welcome Shivam San!
        </h3>
        <img
          src="/avatar.jpg"
          alt="Avatar"
          style={{ width: "50px", height: "50px", borderRadius: "50%" }}
        />
      </div>
    </div>
  );
};

export default Header;
