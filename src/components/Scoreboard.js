import React from 'react';
import './Scoreboard.css';

function Scoreboard({ score, guesses }) {
  return (
    <div className="scoreboard">
      <h3>Score: {score}</h3>
      <ul>
        {guesses.map((guess, index) => (
          <li key={index} className={guess.correct ? 'correct' : 'incorrect'}>
            {guess.gameName} - {guess.correct ? 'Correct' : 'Incorrect'}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Scoreboard;
