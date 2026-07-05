import json
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.database import SessionLocal
from app.models.alert import Alert

router = APIRouter()

# All connected dashboard clients
_clients: list = []

async def broadcast(alert: dict):
    dead = []
    for ws in _clients:
        try:
            await ws.send_text(json.dumps(alert))
        except Exception:
            dead.append(ws)
    for ws in dead:
        _clients.remove(ws)

@router.websocket("/ws/alerts")
async def ws_alerts(websocket: WebSocket):
    await websocket.accept()
    _clients.append(websocket)
    try:
        while True:
            await asyncio.sleep(20)
            await websocket.send_text(json.dumps({"type": "ping"}))
    except WebSocketDisconnect:
        if websocket in _clients:
            _clients.remove(websocket)

@router.get("/alerts")
def list_alerts(limit: int = 50):
    db = SessionLocal()
    try:
        rows = db.query(Alert).order_by(Alert.created_at.desc()).limit(limit).all()
        return [
            {
                "id":         r.id,
                "label":      r.label,
                "severity":   r.severity,
                "confidence": r.confidence,
                "is_attack":  r.is_attack,
                "src_ip":     r.src_ip,
                "dst_ip":     r.dst_ip,
                "dst_port":   r.dst_port,
                "created_at": str(r.created_at),
            }
            for r in rows
        ]
    finally:
        db.close()

@router.get("/alerts/stats")
def alert_stats():
    db = SessionLocal()
    try:
        total    = db.query(Alert).count()
        high     = db.query(Alert).filter(Alert.severity == "HIGH").count()
        medium   = db.query(Alert).filter(Alert.severity == "MEDIUM").count()
        low      = db.query(Alert).filter(Alert.severity == "LOW").count()
        return {"total": total, "HIGH": high, "MEDIUM": medium, "LOW": low}
    finally:
        db.close()
