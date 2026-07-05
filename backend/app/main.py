from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.predict import router as predict_router
from app.routes.alerts  import router as alerts_router
from app.database import init_db

app = FastAPI(title="NIDS/AI", version="1.0.0",
              description="AI-powered Network Intrusion Detection System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    try:
        init_db()
        print("[NIDS] Database initialized")
    except Exception as e:
        print(f"[NIDS] DB init failed (PostgreSQL not running?) — {e}")

app.include_router(predict_router, prefix="/api")
app.include_router(alerts_router,  prefix="/api")

@app.get("/")
def root():
    return {"project": "NIDS/AI", "status": "running", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"api": "ok"}
