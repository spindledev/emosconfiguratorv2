from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    """Return a simple health check response."""
    return {"msg": "ok"}
