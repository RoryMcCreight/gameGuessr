import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import GameBoard from './components/GameBoard';
import Scoreboard from './components/Scoreboard';
import Footer from './components/Footer';
import './App.css';
import storeGames from './storeGames';

function App() {
  const sampleGuesses = [
    { gameName: 'Super Mario Bros', correct: true },
    { gameName: 'The Legend of Zelda', correct: false }
  ];

  useEffect(() => {
    // Call storeGames to fetch and store game data in Firestore
    storeGames();
  }, []);

  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={
            <>
              <GameBoard />
              <Scoreboard score={100} guesses={sampleGuesses} />
            </>
          } />
          <Route path="/about" element={<div>About Page</div>} />
          <Route path="/settings" element={<div>Settings Page</div>} />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
