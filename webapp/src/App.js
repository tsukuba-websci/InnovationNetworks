import React from 'react';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom'
import EmpiricalComparison from './components/EmpiricalComparison.js';
import InnovationComparison from './components/InnovationComparison.js';
import SimulationComparison from './components/SimulationComparison.js';
import Timeline from './components/Timeline.js';
import BestWorst from './components/BestWorst.js';
import BestNCTF from './components/BestNCTF.js'
import BestTTF from './components/BestTTF.js'

function App() {
  return (
    <div className="App">
      <Router>
        <main style={{flexGrow: 1, maxWidth:"100%", maxHeight: "100%", overflow: "hidden"}}>
          <Routes>
            <Route path='/empirical' element={<EmpiricalComparison />} />
            <Route path='/simulation' element={<SimulationComparison />} />
            <Route path='/timeline' element={<Timeline />} />
            <Route path='/innovation' element={<InnovationComparison />} />
            <Route path='/best-worst' element={<BestWorst />} />
            <Route path='/best-nctf' element={<BestNCTF />} />
            <Route path='/best-ttf' element={<BestTTF />} />
          </Routes>
        </main>
      </Router>
    </div>
  );
}

export default App;
