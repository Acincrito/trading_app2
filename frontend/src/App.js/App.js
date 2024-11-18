// frontend/src/App.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';
import RobotsPage from './pages/RobotsPage';

const App = () => {
  const [message, setMessage] = useState('');

  // Verifica o status da API ao carregar o aplicativo
  useEffect(() => {
    axios.get('/api/trading/status')
      .then(response => setMessage(response.data.message))
      .catch(error => setMessage('Erro ao conectar com a API'));
  }, []);

  return (
    <Router>
      <div className="App">
        <h1>Status da API</h1>
        <p>{message}</p>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/robots" element={<RobotsPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
