# NIDS/AI — AI-Powered Network Intrusion Detection System

An end-to-end Network Intrusion Detection System combining a Random Forest classifier trained on CICIDS2017 with a live packet-capture pipeline, a FastAPI backend, a PostgreSQL alert store, and a real-time React dashboard — fully containerized with Docker Compose.

Originally scoped as a two-person project (ML engineer + infrastructure engineer), built solo end to end.

## Architecture

```
Live traffic (NFStream) --> feature_mapper.py --> FastAPI /api/predict --> PostgreSQL
                                                          |
                                                          v
                                                  WebSocket /api/ws/alerts
                                                          |
                                                          v
                                                  React dashboard (live feed)
```

## Results at a glance

- **Model:** Random Forest, 100 trees, `class_weight="balanced"`
- **Macro F1:** 0.90 on a held-out 20% stratified test set (565,559 flows)
- Outperformed both XGBoost (0.89 macro F1) and a Keras neural network (0.37 macro F1) — trees clearly beat deep learning on this flat tabular data
- **Key finding:** the model relies heavily on `Destination Port` as a feature (highest Gini importance), which causes it to miss PortScan/brute-force attacks in live testing when the attack targets a port not seen during training. See `NIDS_Final_Evaluation_Report.docx` for the full writeup, including the live-traffic generalization gap.

Full methodology, per-class metrics, benchmark comparison, and limitations are documented in **`NIDS_Final_Evaluation_Report.docx`**.

## Project structure

```
nids-ai/
├── backend/           FastAPI app (prediction endpoint, alerts, WebSocket, live capture)
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models/
│   │   └── routes/
│   ├── feature_mapper.py     Maps NFStream flows to the 78-feature model input
│   ├── live_capture.py       NFStream-based live packet capture
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/          React (Vite) live SOC-style dashboard
│   └── Dockerfile
├── ml/
│   ├── 01_load_merge.py .. 07_neural_network.py   Pipeline scripts, run in order
│   ├── data/          CICIDS2017 CSVs (not committed — see setup below)
│   └── models/        Trained models (not committed — see setup below)
├── docker-compose.yml
└── NIDS_Final_Evaluation_Report.docx
```

## Setup

### 1. Get the dataset

Download **CICIDS2017** from Kaggle:
[kaggle.com/datasets/sweety18/cicids2017-full-modified-all-8-files](https://www.kaggle.com/datasets/sweety18/cicids2017-full-modified-all-8-files)

Place the CSV(s) under `ml/data/`, then run the pipeline in order to reproduce cleaning, imbalance experiments, and model training:

```bash
cd ml
python3 -m venv venv && source venv/bin/activate
pip install -r ../backend/requirements.txt pandas scikit-learn xgboost tensorflow matplotlib

python3 01_load_merge.py          # merge + clean raw CSVs -> data/merged_clean.csv
python3 03_class_imbalance.py     # compares SMOTE / undersampling / class weights
python3 04_random_forest.py       # trains production model -> models/best_model.joblib
python3 05_xgboost.py             # trains comparison model
python3 07_neural_network.py      # trains comparison model
```

This produces `ml/models/best_model.joblib`, `feature_names.joblib`, `label_encoder.joblib`, and `scaler.joblib` — all required by the backend and excluded from Git via `.gitignore` due to size.

### 2. Run the full stack with Docker Compose

```bash
docker compose up --build
```

This starts three services:
| Service | Port | Description |
|---|---|---|
| `postgres` | 5432 | Alert storage |
| `backend` | 8000 | FastAPI — `/api/predict`, `/api/alerts`, `/api/alerts/stats`, `/api/ws/alerts` |
| `frontend` | 5173 | React dashboard |

Open **http://localhost:5173** for the live dashboard, or **http://localhost:8000/docs** for the interactive API docs.

### 3. Feed it live traffic (optional)

The backend's `live_capture.py` uses NFStream to capture real packets and extract the 78 CICIDS2017-compatible features from your network interface. Requires running with elevated privileges outside the container, or granting `NET_RAW`/`NET_ADMIN` capabilities to the backend container.

## Known limitations

The model generalizes very well within the statistical envelope of CICIDS2017 (0.90 macro F1, in line with published benchmarks) but was found during live-traffic testing to misclassify attacks that don't match training-data patterns closely enough — most notably PortScan and brute-force attempts on ports not seen during training. Full details, root-cause analysis, and proposed fixes are in Section 9 of the evaluation report.

## Tech stack

**ML:** scikit-learn (Random Forest), XGBoost, TensorFlow/Keras, pandas
**Backend:** FastAPI, SQLAlchemy, PostgreSQL, WebSockets, NFStream
**Frontend:** React, Vite
**Infra:** Docker, Docker Compose
