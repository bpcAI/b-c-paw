from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from auth import validate_serial
from logic import predict, undo, reset
import sqlite3

app = FastAPI()

class SerialRequest(BaseModel):
    serial: str

class PredictRequest(BaseModel):
    code: str  # 4碼或6碼

@app.post("/validate_serial")
def validate(req: SerialRequest):
    token = validate_serial(req.serial)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid serial")
    return {"session_token": token}

@app.post("/predict")
def predict_api(req: PredictRequest):
    return predict(req.code)

@app.post("/undo")
def undo_api():
    return undo()

@app.post("/reset")
def reset_api():
    return reset()

@app.get("/meta")
def meta():
    return {"version": "1.0.0", "status": "ok"}
