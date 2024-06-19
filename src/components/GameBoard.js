import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Select from 'react-select';

const GameBoard = () => {
    const [games, setGames] = useState([]);
    const [selectedGame, setSelectedGame] = useState(null);
    const [suggestions, setSuggestions] = useState([]);

    useEffect(() => {
        const fetchGames = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/games', {
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                setGames(response.data);
            } catch (error) {
                console.error('Error fetching games:', error);
            }
        };

        fetchGames();
    }, []);

    const handleInputChange = (inputValue) => {
        const filteredSuggestions = games.filter(game =>
            game.title.toLowerCase().includes(inputValue.toLowerCase())
        ).slice(0, 5);
        setSuggestions(filteredSuggestions.map(game => ({ value: game.title, label: game.title })));
    };

    const handleGameSelect = (selectedOption) => {
        setSelectedGame(selectedOption);
    };

    const handleSubmit = async () => {
        if (!selectedGame) return;

        try {
            const response = await axios.post('http://localhost:5000/guess', {
                title: selectedGame.value,
            });
            console.log('Response:', response.data);
        } catch (error) {
            console.error('Error submitting guess:', error);
        }
    };

    return (
        <div>
            <Select
                value={selectedGame}
                onChange={handleGameSelect}
                onInputChange={handleInputChange}
                options={suggestions}
                placeholder="Start typing a game title..."
            />
            <button onClick={handleSubmit}>Submit</button>
        </div>
    );
};

export default GameBoard;
