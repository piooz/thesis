import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import Home from "./pages/Home"
import Analyze from "./pages/Analyze"
import Effects from "./pages/Effects"
import History from "./pages/History"
import Layout from './components/Layout';

function App() {
    return (
        <Layout>
            <Router>
                <Routes>
                    <Route index element={<Home />} />
                    <Route path="/home" element={<Home />} />
                    <Route path="/effects" element={<Effects />} />
                    <Route path="/analyze" element={<Analyze />} />
                    <Route path="/history" element={<History />} />
                </Routes>
            </Router>
        </Layout>
    );
}

export default App;
