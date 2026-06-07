from fastapi import APIRouter

router = APIRouter()

@router.post("/predict")
def predict(features: dict):
    # Placeholder — real model integrated in Week 2
    return {
        "prediction": "BENIGN",
        "confidence": 0.99,
        "message": "Model not yet integrated"
    }
