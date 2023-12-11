import './App.css';
import { Routes, Route } from 'react-router-dom';
import Home from './Components/Home/Home';
import Navbar from './Components/Navbar/Navbar';
import Analysis from './Components/Analysis/Analysis';
import Comparison from './Components/Comparison/Comparison';
import DynamicStats from './Components/Comparison/DynamicStats';
import PermissionStats from './Components/Comparison/PermissionStats';
import PermissionCounts from './Components/Comparison/PermissionCounts';

function App() {
  return (
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path='/analysis' element={<Analysis />} />
          <Route path='/comparison' element={<Comparison />} />
          <Route path='/dc' element={<DynamicStats />} />
          <Route path='/permissions' element={<PermissionStats />} />
          <Route path='/permissionsC' element={<PermissionCounts />} />
        </Routes>
        {/* Add more routes for other components */}
      </div>
  );
}

export default App;
