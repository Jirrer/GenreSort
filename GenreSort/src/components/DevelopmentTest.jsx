import React, { useState } from "react";
const API_URL = import.meta.env.VITE_API_URL;

const DevelopmentTest = () => {
    const [status, setStatus] = useState("");

    const sendPing = async () => {
      try {
        const response = await fetch(`${API_URL}/pingServer`);
        const data = await response.json();
        console.log(data);
      } catch (error) {
        console.error("Error:", error);
      }
    };

  return (
    <div className='devTest'>
      <h1>Dev Test</h1>
      <button
        className="PlaylistInputButton"
        onClick={sendPing}>
        ping server
      </button>
      <p className="SubmissionReport">{status}</p>
    </div>
  )
}

export default DevelopmentTest