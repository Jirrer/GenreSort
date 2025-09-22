import React, { useState } from "react";
import ParticleBackground from "./ParticleBackground";

const NewPlaylists = () => {
    const [input, setInput] = useState("");

    const sendPlaylist = async () => {
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
        className="PlaylistInputBox"
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Enter Playlist Link"
      />
      <button
        className="PlaylistInputButton"
        onClick={sendPlaylist}>
        Generate New Playlists
      </button>
    </div>
  )
}

export default NewPlaylists