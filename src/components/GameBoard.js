// src/components/GameBoard.js

import React, { useState } from 'react';
import './GameBoard.css';

const categories = ["Year of Release", "Genre", "Average Length to Complete", "Publisher", "Average User Rating"];

const GameBoard = () => {
  const [guesses, setGuesses] = useState([]);
  const [currentGuess, setCurrentGuess] = useState("");

  const handleGuessSubmit = () => {
    // Add logic to handle guess submission
    const newGuess = { guess: currentGuess, categories: {} };
    categories.forEach(category => {
      // Logic to determine if the guess matches any category
      newGuess.categories[category] = Math.random() > 0.5; // Placeholder logic
    });
    setGuesses([...guesses, newGuess]);
    setCurrentGuess("");
  };

  return (
    <div className="game-board">
      <h1>Video Game Spotle</h1>
      <input
        type="text"
        value={currentGuess}
        onChange={(e) => setCurrentGuess(e.target.value)}
        placeholder="Enter your guess"
      />
      <button onClick={handleGuessSubmit}>Submit Guess</button>
      <div className="guesses">
        {guesses.map((guess, index) => (
          <div key={index} className="guess">
            <div className="guess-text">{guess.guess}</div>
            <div className="categories">
              {categories.map((category, idx) => (
                <div key={idx} className="category">
                  {category}: {guess.categories[category] ? "Match" : "No Match"}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default GameBoard;
