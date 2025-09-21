import React, { useState } from "react";
import './App.css';
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
        {active === 'NewPlaylists' && <NewPlaylists/>}
        {active === 'Temp' && <Temp/>}
      </div>
    </>
  );
}

export default App;
