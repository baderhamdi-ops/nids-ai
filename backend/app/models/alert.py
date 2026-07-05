from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

SEVERITY_MAP = {
    "HIGH":   {"DDoS","DoS Hulk","DoS GoldenEye","DoS slowloris","DoS Slowhttptest","Heartbleed","Infiltration"},
    "MEDIUM": {"Bot","FTP-Patator","SSH-Patator","PortScan"},
}

def get_severity(label: str) -> str:
    for sev, labels in SEVERITY_MAP.items():
        if label in labels:
            return sev
    return "LOW"

class Alert(Base):
    __tablename__ = "alerts"
    id          = Column(Integer,  primary_key=True, index=True)
    label       = Column(String,   nullable=False)
    confidence  = Column(Float,    nullable=False)
    is_attack   = Column(Boolean,  nullable=False)
    severity    = Column(String,   nullable=False)
    src_ip      = Column(String,   nullable=True)
    dst_ip      = Column(String,   nullable=True)
    dst_port    = Column(Integer,  nullable=True)
    protocol    = Column(String,   nullable=True)
    created_at  = Column(DateTime, default=datetime.utcnow)
