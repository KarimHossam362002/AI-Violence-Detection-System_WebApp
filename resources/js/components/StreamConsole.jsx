import React, { useEffect, useRef, useState } from 'react';

export default function StreamConsole({ initialCameras = [] }) {
    const [cameraState, setCameraState] = useState('Idle');
    const [cameraActive, setCameraActive] = useState(false);
    const [selectedService, setSelectedService] = useState('weapon');
    const [streamUrl, setStreamUrl] = useState(serviceStreamUrl('weapon'));
    const [externalStreamUrl, setExternalStreamUrl] = useState('');
    const [aiState, setAiState] = useState('Paused');
    const [mode, setMode] = useState('idle');

    const videoRef = useRef(null);
    const mediaStream = useRef(null);

    useEffect(() => {
        return () => stopWebcam();
    }, []);

    function stopWebcam() {
        if (mediaStream.current) {
            mediaStream.current.getTracks().forEach((track) => track.stop());
            mediaStream.current = null;
        }

        if (videoRef.current) {
            videoRef.current.srcObject = null;
        }
    }

    async function startWebcam() {
        try {
            stopWebcam();
            setExternalStreamUrl('');

            const stream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: false,
            });

            mediaStream.current = stream;

            if (videoRef.current) {
                videoRef.current.srcObject = stream;
            }

            setMode('webcam');
            setCameraState('Webcam active');
            setCameraActive(true);
        } catch (error) {
            setMode('idle');
            setCameraState('Camera blocked');
            setCameraActive(false);
        }
    }

    function stopCamera() {
        stopWebcam();
        setExternalStreamUrl('');
        setMode('idle');
        setCameraState('Idle');
        setCameraActive(false);
    }

    function loadPythonStream() {
        if (!streamUrl) return;

        stopWebcam();
        setExternalStreamUrl(`${streamUrl}${streamUrl.includes('?') ? '&' : '?'}t=${Date.now()}`);
        setMode('stream');
        setCameraState('Stream active');
        setCameraActive(true);
    }

    async function toggleAiTracking(shouldStart) {
        const endpoint = pythonServiceEndpoint(shouldStart ? 'start' : 'stop');

        if (!endpoint) {
            setAiState('Missing stream URL');
            return;
        }

        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { Accept: 'application/json' },
            });

            if (response.ok) {
                const data = await response.json();
                setAiState(data.tracking ? 'Tracking' : 'Paused');
            } else {
                setAiState('Service error');
            }
        } catch (error) {
            setAiState('Service offline');
        }
    }

    function pythonServiceEndpoint(path) {
        try {
            const url = new URL(streamUrl);
            return `${url.origin}/${path}`;
        } catch (error) {
            return '';
        }
    }

    return (
        <>
            <header className="page-header">
                <div>
                    <span className="eyebrow">Live monitoring</span>
                    <h1>Camera Stream</h1>
                    <p className="page-subtitle">Operate browser webcam preview or connect to the Python AI streams.</p>
                </div>
                <div className="header-actions">
                    <button className="secondary-button" type="button" onClick={startWebcam}>Start webcam</button>
                    <button className="ghost-button" type="button" onClick={stopCamera}>Stop</button>
                    <button className="theme-icon-button" type="button" data-theme-toggle aria-label="Switch to dark mode">
                        <svg className="theme-icon theme-icon-dark" viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M21 14.5A8.5 8.5 0 0 1 9.5 3 7 7 0 1 0 21 14.5Z" />
                        </svg>
                        <svg className="theme-icon theme-icon-light" viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M12 4V2m0 20v-2m8-8h2M2 12h2m13.66-5.66 1.41-1.41M4.93 19.07l1.41-1.41m0-11.32L4.93 4.93m14.14 14.14-1.41-1.41" />
                            <circle cx="12" cy="12" r="4" />
                        </svg>
                    </button>
                </div>
            </header>

            <section className="dashboard-grid stream-page-grid">
                <div className="panel camera-panel">
                    <div className="panel-header">
                        <div>
                            <h2>Stream Console</h2>
                            <p>Select a model service, load its MJPEG stream, then start or stop inference.</p>
                        </div>
                        <span className={`status-pill ${cameraActive ? 'online' : ''}`}>{cameraState}</span>
                    </div>

                    <div className="video-frame large-video-frame">
                        {mode === 'webcam' && <video ref={videoRef} autoPlay muted playsInline />}
                        {mode === 'stream' && <img src={externalStreamUrl} alt="Python stream preview" />}
                        {mode === 'idle' && <span>No camera feed active</span>}
                    </div>

                    <div className="stream-controls">
                        <select
                            value={selectedService}
                            onChange={(event) => {
                                const service = event.target.value;
                                setSelectedService(service);
                                setStreamUrl(serviceStreamUrl(service));
                                setExternalStreamUrl('');
                                setMode('idle');
                                setCameraState('Idle');
                                setCameraActive(false);
                                setAiState('Paused');
                            }}
                        >
                            <option value="weapon">Weapon detection</option>
                            <option value="violence">Violence detection</option>
                        </select>
                        <input
                            type="url"
                            value={streamUrl}
                            onChange={(event) => setStreamUrl(event.target.value)}
                            placeholder="http://127.0.0.1:5000/stream"
                        />
                        <button className="secondary-button" type="button" onClick={loadPythonStream}>Load stream</button>
                        <button className="primary-button" type="button" onClick={() => toggleAiTracking(true)}>Start AI</button>
                        <button className="ghost-button" type="button" onClick={() => toggleAiTracking(false)}>Stop AI</button>
                    </div>
                </div>

                <aside className="panel stream-side-panel">
                    <div className="panel-header">
                        <div>
                            <h2>Service State</h2>
                            <p>Current stream configuration.</p>
                        </div>
                    </div>
                    <div className="detail-list">
                        <div><span>Selected model</span><strong>{serviceLabel(selectedService)}</strong></div>
                        <div><span>AI status</span><strong>{aiState}</strong></div>
                        <div><span>Registered cameras</span><strong>{initialCameras.length}</strong></div>
                    </div>
                </aside>
            </section>
        </>
    );
}

function serviceStreamUrl(service) {
    return service === 'violence'
        ? 'http://127.0.0.1:5001/stream'
        : 'http://127.0.0.1:5000/stream';
}

function serviceLabel(service) {
    return service === 'violence' ? 'Violence AI' : 'Weapon AI';
}
