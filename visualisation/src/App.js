import React from 'react';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom'
import Comparison from './components/Comparison.js'

function App() {
  return (
    <div className="App">
      <Router>
        <main style={{flexGrow: 1, maxWidth:"100%", maxHeight: "100%", overflow: "hidden"}}>
          <Routes>
            <Route path='/' element={<Comparison />} />
          </Routes>
        </main>
      </Router>
    </div>
  );
}

export default App;
