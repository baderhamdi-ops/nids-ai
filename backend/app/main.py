from fastapi import FastAPI
from app.routes.predict import router as predict_router

app = FastAPI(title="NIDS API", version="1.0.0")
app.include_router(predict_router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "NIDS API is running"}
