from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Literal

app = FastAPI()

# Simple in-memory camera configuration store
cameras: Dict[int, dict] = {
    1: {"id": 1, "codec": "MJPEG", "multicast_port": 5000},
    2: {"id": 2, "codec": "H264", "multicast_port": 5001},
}

class CameraConfig(BaseModel):
    codec: Literal["MJPEG", "H264"]
    multicast_port: int = Field(..., ge=1024, le=65535)

class Camera(CameraConfig):
    id: int

@app.get("/")
def read_root():
    return {"msg": "ok"}

@app.get("/cameras", response_model=List[Camera])
def list_cameras():
    return list(cameras.values())

@app.get("/cameras/{camera_id}", response_model=Camera)
def get_camera(camera_id: int):
    if camera_id not in cameras:
        raise HTTPException(status_code=404, detail="Camera not found")
    return cameras[camera_id]

@app.put("/cameras/{camera_id}/settings", response_model=Camera)
def update_camera_settings(camera_id: int, config: CameraConfig):
    if camera_id not in cameras:
        raise HTTPException(status_code=404, detail="Camera not found")
    cameras[camera_id].update(config.dict())
    return cameras[camera_id]
