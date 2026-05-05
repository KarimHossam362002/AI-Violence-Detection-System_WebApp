import './bootstrap';
import React from 'react';
import { createRoot } from 'react-dom/client';
import StreamConsole from './components/StreamConsole.jsx';

const streamRoot = document.getElementById('stream-root');

if (streamRoot) {
    createRoot(streamRoot).render(React.createElement(StreamConsole, {
        initialCameras: JSON.parse(streamRoot.dataset.cameras || '[]'),
    }));
}
