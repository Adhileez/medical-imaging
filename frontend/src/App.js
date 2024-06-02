import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import UploadPage from './UploadPage';
import Login from './Login';
import Register from './Register';
import DisplayPage from './DisplayPage';
import './App.css';

function App() {
  const isAuthenticated = () => {
    const token = localStorage.getItem('token');
    return token != null;
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/upload" element={isAuthenticated() ? <UploadPage /> : <Navigate to="/login" />} />
        <Route path="/display/:filename" element={isAuthenticated() ? <DisplayPage /> : <Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;



