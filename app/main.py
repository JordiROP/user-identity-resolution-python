from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.models.input.interaction import UpdateInteraction, CollectInteraction

app = FastAPI(title="Contentsquare interview Python")


@app.get("/ping")
def ping():
    return JSONResponse(
        content={"status": "OK"},
        status_code= 200,
        media_type="application/json"
    )


@app.post("/collect")
def collect(interaction: CollectInteraction):
    return JSONResponse(
        content={"status": "OK"},
        status_code= 200,
        media_type="application/json"
    )


@app.post("/update")
def update(interaction: UpdateInteraction):
    return JSONResponse(
        content={"status": "OK"},
        status_code= 200,
        media_type="application/json"
    )

@app.get("/metrics")
def metrics():
    return JSONResponse(
        content={"status": "OK"},
        status_code= 200,
        media_type="application/json"
    )