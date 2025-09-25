import React, { useState } from "react";

const DevelopmentTest = () => {
    const [status, setStatus] = useState("");

    const sendPing = async () => {
        try {
            const response = await fetch('/pingServer');
            const data = await response.json();
            setStatus(data.status);

            if (data.status == 'success') {
                setStatus("Successfully pinged server")
            }
        } catch (error) {
        console.error("Error pinging server:", error);
        setStatus("Error pinging server");
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