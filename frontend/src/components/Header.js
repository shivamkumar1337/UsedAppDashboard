const Header = () => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        width: window.innerWidth,
      }}
    >
      <text style={{ fontSize: 40, padding: 10, backgroundColor: "#BFCFE7", width:"100%", color:"#3D3B40"}}>
        APP USAGE DASHBOARD
      </text>
      <text style={{alignSelf:"flex-start",justifySelf:"flex-start",padding: 10, fontSize:20}}>Welcome, Shivam San</text>
    </div>
  );
};

export default Header;
