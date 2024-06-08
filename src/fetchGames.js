// src/fetchGames.js

const fetchGames = async () => {
    const response = await fetch('https://api.rawg.io/api/games?key=YOUR_RAWG_API_KEY');
    const data = await response.json();
    return data.results;
  };
  
  export default fetchGames;
  