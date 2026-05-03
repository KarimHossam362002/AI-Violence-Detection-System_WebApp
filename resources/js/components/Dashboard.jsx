import React, { useEffect, useRef, useState } from 'react';

export default function Dashboard({ initialCameras, initialIncidents, initialStats, latestUrl }) {
    const [cameras] = useState(initialCameras);
    const [incidents, setIncidents] = useState(initialIncidents);
    const [stats] = useState(initialStats);
    const [cameraState, setCameraState] = useState('Idle');
    const [cameraActive, setCameraActive] = useState(false);
    const [selectedService, setSelectedService] = useState('weapon');
    const [streamUrl, setStreamUrl] = useState(serviceStreamUrl('weapon'));
    const [externalStreamUrl, setExternalStreamUrl] = useState('');
    const [aiState, setAiState] = useState('Paused');
    const [mode, setMode] = useState('idle');
    const videoRef = useRef(null);
    const mediaStream = useRef(null);
    const liveStats = {
        critical: incidents.filter((incident) => incident.alert_level === 'critical').length || stats.critical || 0,
        high: incidents.filter((incident) => incident.alert_level === 'high').length || stats.high || 0,
        today: stats.today || incidents.length || 0,
        cameras: stats.cameras || cameras.length || 0,
    };

    useEffect(() => {
        if (!latestUrl) return undefined;

        const interval = window.setInterval(async () => {
            try {
                const response = await fetch(latestUrl, {
                    headers: { Accept: 'application/json' },
                });
                const data = await response.json();
                setIncidents(data.incidents || []);
            } catch (error) {
                // Keep the current incident table if a transient poll fails.
            }
        }, 5000);

        return () => window.clearInterval(interval);
    }, [latestUrl]);

    useEffect(() => () => stopWebcam(), []);

    async function startWebcam() {
        try {
            stopWebcam();
            setExternalStreamUrl('');

            mediaStream.current = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: false,
            });

            if (videoRef.current) {
                videoRef.current.srcObject = mediaStream.current;
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

    function stopWebcam() {
        if (mediaStream.current) {
            mediaStream.current.getTracks().forEach((track) => track.stop());
            mediaStream.current = null;
        }

        if (videoRef.current) {
            videoRef.current.srcObject = null;
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
        setExternalStreamUrl(streamUrl);
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
            const data = await response.json();
            setAiState(data.tracking ? 'Tracking' : 'Paused');
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
                    <span className="eyebrow">Live operations</span>
                    <h1>Detection Dashboard</h1>
                </div>
                <div className="header-actions">
                    <button className="secondary-button" type="button" onClick={startWebcam}>Start webcam</button>
                    <button className="ghost-button" type="button" onClick={stopCamera}>Stop</button>
                </div>
            </header>

            <section className="stat-grid">
                <StatCard label="Critical" value={liveStats.critical} tone="danger" />
                <StatCard label="High" value={liveStats.high} tone="warning" />
                <StatCard label="Today" value={liveStats.today} />
                <StatCard label="Cameras" value={liveStats.cameras} />
            </section>

            <section className="action-card-grid">
                <ActionCard
                    title="Live Webcam"
                    metric={`${serviceLabel(selectedService)} / ${aiState}`}
                    text="Pick weapon or violence detection, load the stream, then start analysis from the dashboard."
                    tone={cameraActive ? 'active' : ''}
                    action={<button className="secondary-button" type="button" onClick={startWebcam}>Start webcam</button>}
                />
                <ActionCard
                    title="Incident Archive"
                    metric={`${incidents.length} recent`}
                    text="Review detections posted by the AI service, including alert level, confidence, snapshots, and saved clips."
                    tone="incident"
                    action={<button className="ghost-button" type="button" onClick={() => document.getElementById('incidents')?.scrollIntoView({ behavior: 'smooth' })}>View incidents</button>}
                />
                <ActionCard
                    title="Camera Registry"
                    metric={`${cameras.length} cameras`}
                    text="Cameras are registered automatically the first time your Python service sends a detection event."
                    action={<button className="ghost-button" type="button" onClick={() => document.getElementById('cameras')?.scrollIntoView({ behavior: 'smooth' })}>View cameras</button>}
                />
                <ActionCard
                    title="System Health"
                    metric="Polling"
                    text="The dashboard refreshes incidents every five seconds. WebSockets can replace this later for instant alerts."
                    tone="system"
                    action={<a className="ghost-button" href="/up" target="_blank" rel="noreferrer">Check app</a>}
                />
            </section>

            <section className="dashboard-grid">
                <div className="panel camera-panel">
                    <div className="panel-header">
                        <div>
                            <h2>Camera Access</h2>
                            <p>Use browser webcam preview, or load one of the Python AI streams.</p>
                        </div>
                        <span className={`status-pill ${cameraActive ? 'online' : ''}`}>{cameraState}</span>
                    </div>

                    <div className="video-frame">
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

                <div className="panel" id="cameras">
                    <div className="panel-header">
                        <div>
                            <h2>Registered Cameras</h2>
                            <p>Cameras appear here automatically when Python posts incidents.</p>
                        </div>
                    </div>

                    <div className="camera-list">
                        {cameras.length ? cameras.map((camera) => (
                            <div className="camera-row" key={camera.id}>
                                <div>
                                    <strong>{camera.name}</strong>
                                    <small>{camera.district || 'No district'}</small>
                                </div>
                                <span className="status-pill">{camera.status}</span>
                            </div>
                        )) : <p className="empty-state">No cameras registered yet.</p>}
                    </div>
                </div>
            </section>

            <section className="panel incident-panel" id="incidents">
                <div className="panel-header">
                    <div>
                        <h2>Incidents</h2>
                        <p>Updated every five seconds while the dashboard is open.</p>
                    </div>
                </div>

                <div className="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Alert</th>
                                <th>Event</th>
                                <th>Camera</th>
                                <th>Confidence</th>
                                <th>Detected</th>
                                <th>Evidence</th>
                            </tr>
                        </thead>
                        <tbody>
                            {incidents.length ? incidents.map((incident) => (
                                <IncidentRow incident={incident} key={incident.id} />
                            )) : (
                                <tr>
                                    <td colSpan="6" className="empty-state">No incidents received yet.</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
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

function ActionCard({ title, metric, text, action, tone = '' }) {
    return (
        <div className={`action-card ${tone}`}>
            <div>
                <small>{title}</small>
                <strong>{metric}</strong>
                <p>{text}</p>
            </div>
            <div className="action-card-footer">
                {action}
            </div>
        </div>
    );
}

function StatCard({ label, value, tone = '' }) {
    return (
        <div className={`stat-card ${tone}`}>
            <small>{label}</small>
            <strong>{value}</strong>
        </div>
    );
}

function IncidentRow({ incident }) {
    const cameraId = incident.external_camera_id || incident.camera?.camera_id || 'Unknown';
    const district = incident.district || incident.camera?.district || 'No district';
    const confidence = incident.confidence === null || incident.confidence === undefined
        ? 'N/A'
        : `${(Number(incident.confidence) * 100).toFixed(1)}%`;
    const detectedAt = incident.detected_at || incident.created_at;

    return (
        <tr>
            <td><span className={`alert-badge ${incident.alert_level}`}>{incident.alert_level}</span></td>
            <td>
                <strong>{incident.event_type}</strong>
                <small>{incident.weapon_detected ? 'Weapon detected' : 'No weapon flag'}</small>
            </td>
            <td>
                <strong>{cameraId}</strong>
                <small>{district}</small>
            </td>
            <td>{confidence}</td>
            <td>{detectedAt ? new Date(detectedAt).toLocaleString() : 'N/A'}</td>
            <td className="evidence-links">
                {incident.snapshot_url && <a href={incident.snapshot_url} target="_blank" rel="noreferrer">Snapshot</a>}
                {incident.clip_path && <a href={incident.clip_path} target="_blank" rel="noreferrer">Clip</a>}
                {!incident.snapshot_url && !incident.clip_path && <span>N/A</span>}
            </td>
        </tr>
    );
}
