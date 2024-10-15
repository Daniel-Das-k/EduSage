import React from 'react';

const CheckList = () => {
  return (
    <div style={{ width: '100%', height: '100vh', overflow: 'hidden',background:"#333" }}>
      <iframe
        src="https://goblin.tools" // Replace with the URL you want to embed
        style={{ border: 'none', width: "100%",height:"100vh",margin:"0rem 0" }}
        title="Embedded Website"
        allowFullScreen
      />
    </div>
  );
};

export default CheckList;
