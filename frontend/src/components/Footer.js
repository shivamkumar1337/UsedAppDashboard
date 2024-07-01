import React from 'react';

const Footer = () => {
  return (
    <footer
      style={{
        backgroundColor: '#4A249D',
        padding: '20px',
        textAlign: 'center',
        marginTop: '20px',
        position: 'fixed',
        bottom: 0,
        left: 0,
        width: '100%',
      }}
    >
      <p style={{ margin: 0 , color:"#f1f1f1"}}>
        &copy; {new Date().getFullYear()} Made by Shivam Kumar. All rights reserved.
      </p>
    </footer>
  );
};

export default Footer;
