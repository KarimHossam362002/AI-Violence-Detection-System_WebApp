import './bootstrap';
import React from 'react';
import { createRoot } from 'react-dom/client';
import Dashboard from './components/Dashboard.jsx';

const dashboardRoot = document.getElementById('dashboard-root');

if (dashboardRoot) {
    createRoot(dashboardRoot).render(React.createElement(Dashboard, {
        initialCameras: JSON.parse(dashboardRoot.dataset.cameras || '[]'),
        initialIncidents: JSON.parse(dashboardRoot.dataset.incidents || '[]'),
        initialStats: JSON.parse(dashboardRoot.dataset.stats || '{}'),
        latestUrl: JSON.parse(dashboardRoot.dataset.latestUrl || '""'),
    }));
}
