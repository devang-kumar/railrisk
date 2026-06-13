from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from pipeline import RailRiskPipeline
import json
import os

app = FastAPI(title="RailRisk API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = RailRiskPipeline()

class Shipment(BaseModel):
    id: str
    cargo_type: str
    destination: str
    delay_time_hours: float
    urgency_level: str
    dependency_type: str
    downstream_impact: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "RailRisk API is running"}

@app.post("/api/predict")
async def predict_risk(shipment: Shipment):
    try:
        report = pipeline.run(shipment.model_dump())
        return report.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/predict-batch")
async def predict_batch(shipments: List[Shipment]):
    try:
        reports = pipeline.run_batch([s.model_dump() for s in shipments])
        return [r.to_dict() for r in reports]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/shipments")
async def get_sample_shipments():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'freight_dataset.json')
    with open(data_path, 'r') as f:
        return json.load(f)

class ActionRequest(BaseModel):
    shipment_id: str
    human_status: str

action_status_store: dict = {}

@app.post("/api/action-status")
async def update_action_status(request: ActionRequest):
    action_status_store[request.shipment_id] = request.human_status
    return {"shipment_id": request.shipment_id, "human_status": request.human_status}

@app.get("/api/action-status/{shipment_id}")
async def get_action_status(shipment_id: str):
    return {"shipment_id": shipment_id, "human_status": action_status_store.get(shipment_id, "Pending")}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
