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

