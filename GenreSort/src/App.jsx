import React, { act, useState } from "react";
import './App.css';
import NewPlaylists from "./components/newPlaylists";
import Temp from "./components/Temp";
import HomePage from "./components/HomePage";
import DevelopmentTest from "./components/DevelopmentTest"

function App() {
  const [active, setActive] = useState('HomePage');

  return (
    <>
      <div className="topBar">
        <button onClick={() => setActive('NewPlaylists')}>New Playlists</button>
        <button onClick={() => setActive('DevelopmentTest')}>Dev Test</button>
        <button onClick={() => setActive('Temp')}>Temp</button>
        <button onClick={() => setActive('Temp')}>Temp</button>

      </div>
      <div className="screenContent">
        {active === 'HomePage' && <HomePage />}
        {active === 'NewPlaylists' && <NewPlaylists/>}
        {active === 'DevelopmentTest' && <DevelopmentTest />}
        {active === 'Temp' && <Temp/>}
      </div>
    </>
  );
}

export default App;
