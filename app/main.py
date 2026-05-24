from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.models.input.interaction import UpdateInteraction, CollectInteraction
from app.jobs.collection import process_collect as

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
    process_collect(interaction)
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