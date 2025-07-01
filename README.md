# EMOS Configurator

Tool for configuring EMOS cameras via hotspot or wired setup.

## Setup

1. Clone this repository.
2. (Optional) Create and activate a Python virtual environment.
3. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the FastAPI App

Launch the server with `uvicorn`:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000` in your browser to open the configurator.

Visit `http://192.168.10.1:8000` to access the web interface. Each camera can be
assigned a codec and multicast port via the form and the settings are saved
through the FastAPI backend.

An **ARP Scan** button on the page lists devices on `eth0` whose MAC address
starts with `DC:36:43`. Use this to quickly discover connected EMOS cameras.

This project provides a minimal web interface for configuring EMOS cameras on a Raspberry Pi. The service can run in hotspot mode or over an existing wired connection.

## Installation

Follow these steps to set up the configurator:

1. **Installation mode** – connect the device to the internet via `eth0` and run:

   ```bash
   sudo ./scripts/install.sh
   ```

   The script installs required packages and marks the system for business mode on the next reboot.

2. **Business mode** – after the reboot, connect to Wi‑Fi network `Spindle_EMOS_Config` and open [http://192.168.10.1:8000](http://192.168.10.1:8000). The ethernet interface is now used only to configure EMOS cameras and for ARP scans.

## Example API usage

The FastAPI app exposes a small REST API. The root endpoint is useful for a quick health check:

```bash
curl http://192.168.10.1:8000/
```

Response:

```json
{"msg": "ok"}
```

## Hotspot and camera configuration

Power on the Raspberry Pi and connect to the hotspot mentioned above, then browse to [http://192.168.10.1:8000](http://192.168.10.1:8000). Follow the steps in the [user guide](userguide.md) to configure each camera.


## License

This project is licensed under the [MIT License](LICENSE).



