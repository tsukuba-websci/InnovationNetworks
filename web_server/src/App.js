import React from 'react';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom'
import EmpiricalComparison from './components/EmpiricalComparison.js';
import InnovationComparison from './components/InnovationComparison.js';
import SimulationComparison from './components/SimulationComparison.js';
import Timeline from './components/Timeline.js';

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
          </Routes>
        </main>
      </Router>
    </div>
  );
}

export default App;
