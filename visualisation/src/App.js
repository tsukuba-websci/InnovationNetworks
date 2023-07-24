import React from 'react';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom'
import EmpiricalComparison1 from './components/EmpiricalComparison.js'
import SimulationComparison from './components/SimulationComparison.js';

function App() {
  return (
    <div className="App">
      <Router>
        <main style={{flexGrow: 1, maxWidth:"100%", maxHeight: "100%", overflow: "hidden"}}>
          <Routes>
            <Route path='/empirical' element={<EmpiricalComparison1 />} />
            <Route path='/simulation' element={<SimulationComparison />} />
          </Routes>
        </main>
      </Router>
    </div>
  );
}

export default App;
