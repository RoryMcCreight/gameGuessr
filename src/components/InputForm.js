import React, { useState } from 'react';
import './InputForm.css';

function InputForm({ onSubmit }) {
  const [guess, setGuess] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (guess.trim() === '') {
      alert("Please enter a guess!");
      return;
    }
    onSubmit(guess);
    setGuess(''); // Reset input after submit
  };

  return (
    <form className="input-form" onSubmit={handleSubmit}>
      <input
        type="text"
        value={guess}
        onChange={(e) => setGuess(e.target.value)}
        placeholder="Enter your guess here"
      />
      <button type="submit">Submit</button>
    </form>
  );
}

export default InputForm;
