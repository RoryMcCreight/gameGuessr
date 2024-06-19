import fetchGames from './fetchGames';

const storeGames = async () => {
  const games = await fetchGames();

  games.forEach(async (game) => {
    const gameData = {
      name: game.name,
      releaseDate: game.released,
      genre: game.genres.map(g => g.name),
      averageLength: game.playtime,
      publisher: game.publishers.map(p => p.name),
      averageUserRating: game.rating,
    };

    try {
      const response = await fetch('http://localhost:5000/api/games', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(gameData),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const result = await response.json();
      console.log('Game stored successfully:', result);
    } catch (error) {
      console.error('Error storing game:', error);
    }
  });
};

export default storeGames;
