import React, { useState } from "react";

const DevelopmentTest = () => {
    const [input, setInput] = useState("");
    const [ServerResponse, setResponse] = useState('');

    const sendPing = async () => {
        try {
        const res = await fetch("/pingServer", {});

        const data = await res.json();
        setResponse(data)
        } catch (err) {
        console.error(err);
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
      <p className="SubmissionReport">{ServerResponse}</p>
    </div>
  )
}

export default DevelopmentTest