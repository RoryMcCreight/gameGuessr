// src/storeGames.js

import { db } from './firebase';
import { collection, addDoc } from "firebase/firestore";
import fetchGames from './fetchGames';

const storeGames = async () => {
  const games = await fetchGames();
  const gamesCollection = collection(db, "games");

  games.forEach(async (game) => {
    await addDoc(gamesCollection, {
      name: game.name,
      releaseDate: game.released,
      genre: game.genres.map(g => g.name),
      averageLength: game.playtime,
      publisher: game.publishers.map(p => p.name),
      averageUserRating: game.rating,
    });
  });
};

export default storeGames;
