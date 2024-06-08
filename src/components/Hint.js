import React from 'react';
import './Hint.css';

function Hint({ category, hint }) {
  return (
    <div className="hint">
      <h4>{category}</h4>
      <p>{hint}</p>
    </div>
  );
}

export default Hint;
