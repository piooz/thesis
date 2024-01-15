import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import logo from './logo.svg';
import './App.css';
import Home from "./pages/Home"

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route index element={<Home />} />
                <Route path="/home" element={<Home />} />
                <Route path="/effects" element={<Home />} />
                <Route path="/analyze" element={<Home />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
