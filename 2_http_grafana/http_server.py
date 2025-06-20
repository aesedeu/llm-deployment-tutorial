from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import joblib
import uvicorn
import asyncio
import numpy as np
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter


@asynccontextmanager
async def startup(app: FastAPI):
    global model
    model = joblib.load("model.joblib")
    yield


class IncomeData(BaseModel):
    a: float
    b: float
    c: float


class TextInput(BaseModel):
    text: str


app = FastAPI(lifespan=startup)

Instrumentator().instrument(app).expose(app)

# Custom Prometheus Counter for /classic
classic_counter = Counter(
    'classic_requests_total',
    'Total number of requests to the /classic endpoint'
)

@app.post("/classic")
async def classic(data: IncomeData):
    classic_counter.inc()
    res = float(model.predict([[data.a, data.b, data.c]])[0])
    return {"detail": res}


if __name__ == "__main__":
    uvicorn.run("http_server:app", host="0.0.0.0", port=8080, reload=True, workers=-1)
