import { useState, useEffect, useRef, useCallback } from "react";
import "./App.css";

const API = "http://localhost:8000/api";
const WS = "ws://localhost:8000/api/ws/alerts";
const MAX_FEED = 60;

function timeAgo(iso) {
  const s = Math.floor((Date.now() - new Date(iso + "Z")) / 1000);
  if (s < 5) return "now";
  if (s < 60) return `${s}s ago`;
  return `${Math.floor(s / 60)}m ago`;
}

export default function App() {
  const [feed, setFeed] = useState([]);
  const [stats, setStats] = useState({ total: 0, HIGH: 0, MEDIUM: 0, LOW: 0 });
  const [connected, setConnected] = useState(false);
  const wsRef = useRef(null);

  const refreshStats = useCallback(() => {
    fetch(`${API}/alerts/stats`).then(r => r.json()).then(setStats).catch(() => {});
  }, []);

  useEffect(() => {
    fetch(`${API}/alerts?limit=${MAX_FEED}`)
      .then(r => r.json())
      .then(rows => setFeed(rows.map(r => ({ ...r, live: false }))));
    refreshStats();

    function connect() {
      const ws = new WebSocket(WS);
      wsRef.current = ws;
      ws.onopen = () => setConnected(true);
      ws.onclose = () => { setConnected(false); setTimeout(connect, 2000); };
      ws.onerror = () => ws.close();
      ws.onmessage = (evt) => {
        const msg = JSON.parse(evt.data);
        if (msg.type === "ping") return;
        setFeed(prev => {
          if (prev.some(a => a.id === msg.id)) return prev; // dedupe StrictMode double-connect
          return [{ ...msg, live: true, created_at: new Date().toISOString().slice(0, -1) },
                  ...prev].slice(0, MAX_FEED);
        });
        refreshStats();
      };
    }
    connect();
    return () => wsRef.current?.close();
  }, [refreshStats]);

  const sevClass = (s) => (s === "HIGH" ? "sev-high" : s === "MEDIUM" ? "sev-med" : s === "LOW" ? "sev-low" : "sev-none");

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark" data-live={connected} />
          <span className="brand-name">NIDS<span className="brand-ai">/AI</span></span>
        </div>
        <div className={`link-state ${connected ? "up" : "down"}`}>
          {connected ? "LIVE — wlan0" : "RECONNECTING…"}
        </div>
      </header>

      <section className="stat-row">
        <div className="stat">
          <span className="stat-label">Total Alerts</span>
          <span className="stat-value">{stats.total}</span>
        </div>
        <div className="stat stat-high">
          <span className="stat-label">High</span>
          <span className="stat-value">{stats.HIGH}</span>
        </div>
        <div className="stat stat-med">
          <span className="stat-label">Medium</span>
          <span className="stat-value">{stats.MEDIUM}</span>
        </div>
        <div className="stat stat-low">
          <span className="stat-label">Low</span>
          <span className="stat-value">{stats.LOW}</span>
        </div>
      </section>

      <section className="feed-panel">
        <div className="feed-head">
          <span>LIVE FLOW ALERTS</span>
          <span className="feed-count">{feed.length} shown</span>
        </div>
        <div className="feed">
          {feed.length === 0 && (
            <div className="feed-empty">No alerts yet — watching wlan0.</div>
          )}
          {feed.map((a, i) => (
            <div key={`${a.id}-${i}`} className={`feed-row ${sevClass(a.severity)} ${a.live ? "flash" : ""}`}>
              <span className="feed-time">{timeAgo(a.created_at)}</span>
              <span className="feed-sev">{a.severity}</span>
              <span className="feed-label">{a.label}</span>
              <span className="feed-route">{a.src_ip} → {a.dst_ip}:{a.dst_port}</span>
              <span className="feed-conf">{Math.round((a.confidence ?? 0) * 100)}%</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
