import './App.css';
import { Routes, Route } from 'react-router-dom';
import Home from './Components/Home/Home';
import Navbar from './Components/Navbar/Navbar';
import Analysis from './Components/Analysis/Analysis';

function App() {
  return (
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path='/analysis' element={<Analysis />} />
        </Routes>
        {/* Add more routes for other components */}
      </div>
  );
}

export default App;
