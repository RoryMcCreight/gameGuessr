import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import GameBoard from './components/GameBoard';
import Hint from './components/Hint';
import InputForm from './components/InputForm';
import Scoreboard from './components/Scoreboard';
import './App.css'; // Assuming you have some CSS for the App

const App = () => (
  <Router>
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<GameBoard />} />
        <Route path="/hint" element={<Hint />} />
        <Route path="/input" element={<InputForm />} />
        <Route path="/scoreboard" element={<Scoreboard />} />
        {/* Add more routes as needed */}
      </Routes>
      <Footer />
    </div>
  </Router>
);

export default App;
