from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import json
from pathlib import Path

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

CONFIG_DIR = Path("config")
CONFIG_DIR.mkdir(exist_ok=True)

# Example list of cameras that can be configured
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
async def save_camera_settings(camera_id: int, codec: str = Form(...), port: int = Form(...)):
    """Save settings submitted from the form and redirect back to index."""
    save_settings(camera_id, codec, port)
    return RedirectResponse(url="/", status_code=303)
