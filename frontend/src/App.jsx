import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadEvents = async () => {
    try {
      const response = await fetch(`${API_URL}/events`);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      setEvents(data);
      setError("");
    } catch (err) {
      console.error("API Error:", err);
      setError("Unable to connect to VMS backend");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEvents();

    const interval = setInterval(loadEvents, 3000);

    return () => clearInterval(interval);
  }, []);

  const intrusionCount = events.filter(
    (event) => event.event_type === "Intrusion"
  ).length;

  const averageConfidence =
    events.length > 0
      ? (
          (events.reduce(
            (sum, event) => sum + Number(event.confidence || 0),
            0
          ) /
            events.length) *
          100
        ).toFixed(0)
      : 0;

  return (
    <div className="app">

      {/* SIDEBAR */}
      <aside className="sidebar">
        <div className="logo">
          <div className="logo-icon">◉</div>
          <div>
            <h2>SMART VMS</h2>
            <span>Video Management System</span>
          </div>
        </div>

        <nav>
          <div className="nav-item active">
            <span>▦</span>
            Dashboard
          </div>

          <div className="nav-item">
            <span>▣</span>
            Live Cameras
          </div>

          <div className="nav-item">
            <span>◷</span>
            Recordings
          </div>

          <div className="nav-item">
            <span>⚠</span>
            Events
          </div>

          <div className="nav-item">
            <span>⚙</span>
            Settings
          </div>
        </nav>

        <div className="system-status">
          <div className="status-dot"></div>
          <div>
            <strong>System Online</strong>
            <small>All services operational</small>
          </div>
        </div>
      </aside>

      {/* MAIN */}
      <main className="main">

        {/* HEADER */}
        <header className="header">
          <div>
            <h1>Security Dashboard</h1>
            <p>Real-time surveillance monitoring</p>
          </div>

          <div className="header-right">
            <div className="live-status">
              <span></span>
              LIVE
            </div>

            <div className="operator">
              <div className="avatar">OP</div>
              <div>
                <strong>Operator</strong>
                <small>Control Room</small>
              </div>
            </div>
          </div>
        </header>

        {/* ERROR */}
        {error && (
          <div className="error-box">
            ⚠ {error}
          </div>
        )}

        {/* KPI CARDS */}
        <section className="stats">

          <div className="stat-card">
            <div className="stat-icon blue">▣</div>
            <div>
              <span>Camera Status</span>
              <h2>1 / 1</h2>
              <small className="success">● All cameras online</small>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon red">⚠</div>
            <div>
              <span>Intrusion Events</span>
              <h2>{intrusionCount}</h2>
              <small className="danger">● AI detected</small>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon orange">◉</div>
            <div>
              <span>AI Confidence</span>
              <h2>{averageConfidence}%</h2>
              <small>Average detection confidence</small>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon green">✓</div>
            <div>
              <span>System Health</span>
              <h2>100%</h2>
              <small className="success">● Operational</small>
            </div>
          </div>

        </section>

        {/* CONTENT GRID */}
        <section className="content-grid">

          {/* CAMERA */}
          <div className="panel camera-panel">
            <div className="panel-header">
              <div>
                <h3>Camera 01</h3>
                <span className="camera-online">● Online</span>
              </div>

              <button className="fullscreen-btn">⛶</button>
            </div>

            <div className="video-container">

              <video
                controls
                autoPlay
                muted
                loop
                src="/camera01.mp4"
              />

              <div className="camera-overlay">
                <span>CAM 01</span>
                <span>LIVE</span>
              </div>

            </div>

            <div className="video-info">
              <span>Resolution: 3840 × 2160</span>
              <span>FPS: 29.97</span>
              <span>AI Detection: ON</span>
            </div>
          </div>

          {/* ALERTS */}
          <div className="panel alerts-panel">

            <div className="panel-header">
              <div>
                <h3>Recent AI Detections</h3>
                <span>Latest security events</span>
              </div>

              <button onClick={loadEvents} className="refresh-btn">
                ↻
              </button>
            </div>

            <div className="events">

              {loading && (
                <div className="empty">
                  Loading events...
                </div>
              )}

              {!loading && events.length === 0 && (
                <div className="empty">
                  No detections found
                </div>
              )}

              {events.map((event) => (
                <div className="event" key={event.id}>

                  <div className="event-icon">
                    ⚠
                  </div>

                  <div className="event-info">
                    <strong>{event.event_type}</strong>

                    <span>
                      {event.camera_id} • {event.zone}
                    </span>

                    <small>
                      Timestamp: {Number(event.timestamp).toFixed(2)} sec
                    </small>
                  </div>

                  <div className="confidence">
                    {(Number(event.confidence) * 100).toFixed(0)}%
                  </div>

                </div>
              ))}

            </div>

          </div>

        </section>

        {/* EVENT TABLE */}
        <section className="panel event-table">

          <div className="panel-header">
            <div>
              <h3>Event History</h3>
              <span>AI detection records from database</span>
            </div>
          </div>

          <table>

            <thead>
              <tr>
                <th>ID</th>
                <th>Camera</th>
                <th>Event</th>
                <th>Zone</th>
                <th>Timestamp</th>
                <th>Confidence</th>
              </tr>
            </thead>

            <tbody>

              {events.map((event) => (
                <tr key={event.id}>

                  <td>#{event.id}</td>

                  <td>{event.camera_id}</td>

                  <td>
                    <span className="event-badge">
                      {event.event_type}
                    </span>
                  </td>

                  <td>{event.zone}</td>

                  <td>
                    {Number(event.timestamp).toFixed(2)} sec
                  </td>

                  <td>
                    <strong>
                      {(Number(event.confidence) * 100).toFixed(0)}%
                    </strong>
                  </td>

                </tr>
              ))}

            </tbody>

          </table>

        </section>

      </main>
    </div>
  );
}

export default App;