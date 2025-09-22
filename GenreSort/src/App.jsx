import React, { useState } from "react";
import './App.css';
import ParticleBackground from "./components/ParticleBackground";
import NewPlaylists from "./components/newPlaylists";
import Temp from "./components/Temp";

function App() {
  const [active, setActive] = useState('');

  return (
    <>
      <div className="topBar">
        <button onClick={() => setActive('NewPlaylists')}>New Playlists</button>
        <button onClick={() => setActive('Temp')}>Temp</button>
        <button onClick={() => setActive('Temp')}>Temp</button>
        <button onClick={() => setActive('Temp')}>Temp</button>

      </div>
      <div className="screenContent">
        <ParticleBackground />
        {active === 'NewPlaylists' && <NewPlaylists/>}
        {active === 'Temp' && <Temp/>}
      </div>
    </>
  );
}

export default App;
