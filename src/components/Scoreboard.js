import React, { useState, useEffect } from 'react';

const Scoreboard = () => {
  const [scores, setScores] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/games')
      .then(response => response.json())
      .then(data => setScores(data))
      .catch(error => console.error('Error fetching scores:', error));
  }, []);

  if (!scores.length) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Scoreboard</h1>
      <ul>
        {scores.map((score, index) => (
          <li key={index}>{score.name}: {score.points}</li>
        ))}
      </ul>
    </div>
  );
};

export default Scoreboard;
