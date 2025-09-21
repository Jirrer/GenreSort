import React, { useState } from "react";

const NewPlaylists = () => {
    const [input, setInput] = useState("");
    const [response, setResponse] = useState("");

    const sendString = async () => {
        try {
        const res = await fetch("/passInPlaylist", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: input })  
        });
        const data = await res.json();
        setResponse(data.status || JSON.stringify(data)); 
        } catch (err) {
        console.error(err);
        }
    };

  return (
    <div className='newPlaylists'>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter Playlist Link"
        />
        <button onClick={sendString}>Send</button>
        {response && <p>Response: {response}</p>}
    </div>
  )
}

export default NewPlaylists