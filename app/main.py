from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import json
from pathlib import Path

from . import occ_wrapper
from . import network

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

CONFIG_DIR = Path("config")
CONFIG_DIR.mkdir(exist_ok=True)

CAMERAS = [1, 2, 3, 4]


def load_settings(camera_id: int):
    """Load settings for a camera or return defaults."""
    path = CONFIG_DIR / f"camera_{camera_id}.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {"codec": "MJPEG", "port": 5000}


def save_settings(camera_id: int, codec: str, port: int):
    """Persist settings for a camera."""
    path = CONFIG_DIR / f"camera_{camera_id}.json"
    with open(path, "w") as f:
        json.dump({"codec": codec, "port": port}, f)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the configuration page with current settings."""
    camera_settings = {cid: load_settings(cid) for cid in CAMERAS}
    return templates.TemplateResponse(
        "index.html", {"request": request, "cameras": camera_settings}
    )


@app.post("/settings/{camera_id}")
async def save_camera_settings(
    camera_id: int, codec: str = Form(...), port: int = Form(...)
):
    """Save settings submitted from the form and redirect back to index."""
    save_settings(camera_id, codec, port)
    return RedirectResponse(url="/", status_code=303)


@app.post("/arp_scan", response_class=HTMLResponse)
async def arp_scan(request: Request):
    """Run an ARP scan and display the results on the index page."""
    scan_results = network.find_emos_cameras()
    camera_settings = {cid: load_settings(cid) for cid in CAMERAS}
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "cameras": camera_settings,
            "scan_results": scan_results,
        },
    )


@app.get("/camera/{parameter}")
def get_camera_parameter(parameter: str):
    try:
        return occ_wrapper.read_parameter(parameter)
    except occ_wrapper.OCCError as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/camera/{parameter}")
def set_camera_parameter(parameter: str, value: str):
    try:
        return occ_wrapper.set_parameter(parameter, value)
    except occ_wrapper.OCCError as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/health")
def health():
    """Simple health check endpoint."""
    return {"msg": "ok"}
