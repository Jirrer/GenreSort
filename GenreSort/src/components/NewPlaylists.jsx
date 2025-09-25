import React, { useState } from "react";

const NewPlaylists = () => {
    const [input, setInput] = useState("");
    const [SubmissionReport, setReportMessage] = useState('');

    const sendPlaylist = async () => {
        try {
        const res = await fetch("/passinNewPlaylists", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: input })  
        });

        const data = await res.json();
        
        if (data.status == 'success') {
          window.open(data.auth_url, "_blank");
        } else{
          setReportMessage("Invalid Playlist Link")
        }
        } catch (err) {
        console.error(err);
        setReportMessage(`Eorr - ${err}`)
        }
    };

  return (
    <div className='newPlaylists'>
      <h1>New Playlists</h1>
      <p>
      Splits submitted playlist into a few (2 - 5) new playlists based 
      on the genre of the artists.
      </p>
      <input
          className="PlaylistInputBox"
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter Playlist Link"
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              sendPlaylist();
            }
          }}
        />
      <button
        className="PlaylistInputButton"
        onClick={sendPlaylist}>
        Generate New Playlists
      </button>
      <p className="SubmissionReport">{SubmissionReport}</p>
    </div>
  )
}

export default NewPlaylists