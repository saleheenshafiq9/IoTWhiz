import './App.css';
import { Routes, Route } from 'react-router-dom';
import Home from './Components/Home/Home';
import Navbar from './Components/Navbar/Navbar';
import Analysis from './Components/Analysis/Analysis';
import Download from './Components/Download_Report/Download';
import PermissionStats from './Components/Comparison/PermissionStats';

function App() {
  return (
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path='/analysis' element={<Analysis />} />
          <Route path='/comparison' element={<Download />} />
          <Route path='/permissions' element={<PermissionStats />} />
        </Routes>
        {/* Add more routes for other components */}
      </div>
  );
}

export default App;
