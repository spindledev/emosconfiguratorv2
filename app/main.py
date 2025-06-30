from fastapi import FastAPI, HTTPException

from . import occ_wrapper

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "ok"}


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
@app.get('/')
def read_root(): return {'msg': 'ok'}

