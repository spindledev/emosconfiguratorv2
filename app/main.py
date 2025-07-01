from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import json
import subprocess
from pathlib import Path

from . import occ_wrapper
from . import network


from . import version
app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

CONFIG_DIR = Path("config")
CONFIG_DIR.mkdir(exist_ok=True)


BOOT_MODE_FILE = Path("/etc/emos/boot_mode")


def get_connected_cameras():
    """Return a list of detected camera identifiers."""
    try:
        return occ_wrapper.list_cameras()
    except occ_wrapper.OCCError:
        return []


def load_settings(camera_id: str):
    """Load settings for a camera or return defaults."""
    path = CONFIG_DIR / f"camera_{camera_id}.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {"codec": "MJPEG", "port": 5000}


def save_settings(camera_id: str, codec: str, port: int):
    """Persist settings for a camera."""
    path = CONFIG_DIR / f"camera_{camera_id}.json"
    with open(path, "w") as f:
        json.dump({"codec": codec, "port": port}, f)


def switch_to_business_mode():
    """Write 'business' to the boot mode file and start hotspot services."""
    try:
        subprocess.run(
            ["sudo", "sh", "-c", f"echo business > {BOOT_MODE_FILE}"],
            check=True,
        )
    except subprocess.CalledProcessError:
        pass
    subprocess.run(["sudo", "systemctl", "start", "hostapd"], check=False)
    subprocess.run(["sudo", "systemctl", "start", "dnsmasq"], check=False)
    network.set_eth0_static()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the configuration page with current settings."""
    cameras = get_connected_cameras()
    camera_settings = {cid: load_settings(cid) for cid in cameras}
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "cameras": camera_settings,
            "eth0_static": network.eth0_is_static(),
        },
    )


@app.post("/settings/{camera_id}")
async def save_camera_settings(
    camera_id: str, codec: str = Form(...), port: int = Form(...)
):
    """Save settings submitted from the form and redirect back to index."""
    save_settings(camera_id, codec, port)
    return RedirectResponse(url="/", status_code=303)


@app.get("/sniffer", response_class=HTMLResponse)
async def sniffer_page(request: Request):
    return templates.TemplateResponse(
        "sniffer.html",
        {"request": request, "results": [], "subnet": ""},
    )


@app.post("/sniffer", response_class=HTMLResponse)
async def run_sniffer(request: Request):
    results = network.sniff_emos_cameras(interface="eth0")
    subnet = network.subnet_from_ip(results[0]["ip"]) if results else ""
    return templates.TemplateResponse(
        "sniffer.html",
        {"request": request, "results": results, "subnet": subnet},
    )


@app.post("/apply_subnet")
async def apply_subnet(subnet: str = Form(...)):
    network.set_eth0_subnet(subnet)
    return RedirectResponse(url="/", status_code=303)


@app.post("/business")
async def switch_business():
    """Switch the device into business mode and redirect to the index."""
    switch_to_business_mode()
    return RedirectResponse(url="/", status_code=303)


@app.post("/dhcp")
async def switch_dhcp():
    """Configure ``eth0`` via DHCP and redirect to the index."""
    network.set_eth0_dhcp()
    return RedirectResponse(url="/", status_code=303)


@app.get("/eth0_subnet")
def eth0_subnet():
    """Return the IPv4 subnet of eth0."""
    return {"subnet": network.get_subnet("eth0")}


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


@app.get("/version")
def show_version():
    """Return local and remote version information."""
    local_v = version.get_local_version()
    remote_v = version.get_remote_version()
    return {
        "local_version": local_v,
        "remote_version": remote_v,
        "update_available": version.update_available(local_v)
    }


@app.get("/health")
def health():
    """Simple health check endpoint."""
    return {"msg": "ok"}
