import os
import numpy as np
import joblib
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.models.alert import get_severity
from app.database import SessionLocal
from app.models.alert import Alert
from app.routes.alerts import broadcast
from datetime import datetime

router = APIRouter()

# Load model once at startup
_MODEL_PATH = os.getenv("MODEL_PATH", "/home/b4der/nids-ai/ml/models/best_model.joblib")
_FEAT_PATH  = os.getenv("FEAT_PATH",  "/home/b4der/nids-ai/ml/models/feature_names.joblib")

try:
    _model    = joblib.load(_MODEL_PATH)
    _features = joblib.load(_FEAT_PATH)
    print(f"[NIDS] Model loaded ({len(_features)} features)")
except Exception as e:
    _model    = None
    _features = None
    print(f"[NIDS] WARNING: model not loaded — {e}")

class NetworkFeatures(BaseModel):
    features: List[float]
    src_ip:   Optional[str] = None
    dst_ip:   Optional[str] = None
    dst_port: Optional[int] = None
    protocol: Optional[str] = None

class PredictionResponse(BaseModel):
    prediction:  str
    confidence:  float
    is_attack:   bool
    severity:    str
    attack_type: Optional[str]
    alert_id:    Optional[int]

@router.post("/predict", response_model=PredictionResponse)
async def predict(data: NetworkFeatures):
    if _model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    if len(data.features) != 78:
        raise HTTPException(status_code=422, detail=f"Expected 78 features, got {len(data.features)}")

    X          = np.array(data.features).reshape(1, -1)
    label      = _model.predict(X)[0]
    proba      = _model.predict_proba(X)[0]
    confidence = float(np.max(proba))
    is_attack  = label != "BENIGN"
    severity   = get_severity(label) if is_attack else "NONE"

    alert_id = None
    if is_attack:
        db = SessionLocal()
        try:
            alert = Alert(
                label=label, confidence=confidence,
                is_attack=True, severity=severity,
                src_ip=data.src_ip, dst_ip=data.dst_ip,
                dst_port=data.dst_port, protocol=data.protocol,
                created_at=datetime.utcnow(),
            )
            db.add(alert)
            db.commit()
            db.refresh(alert)
            alert_id = alert.id
            await broadcast({
                "id": alert_id, "label": label, "severity": severity,
                "confidence": round(confidence, 4), "src_ip": data.src_ip,
                "dst_ip": data.dst_ip, "dst_port": data.dst_port,
            })
        finally:
            db.close()

    return PredictionResponse(
        prediction=label, confidence=round(confidence, 4),
        is_attack=is_attack, severity=severity,
        attack_type=label if is_attack else None,
        alert_id=alert_id,
    )
