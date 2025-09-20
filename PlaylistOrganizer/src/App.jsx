import React, { useState } from "react";

function SendString() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  const sendString = async () => {
    try {
      const res = await fetch("/passInPlaylist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input })  // send the string
      });
      const data = await res.json();
      // backend returns { status: "..." }
      setResponse(data.status || JSON.stringify(data)); // show response from backend
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type something..."
      />
      <button onClick={sendString}>Send</button>
      {response && <p>Response: {response}</p>}
    </div>
  );
}

export default SendString;
