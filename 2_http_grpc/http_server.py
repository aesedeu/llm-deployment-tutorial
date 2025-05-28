from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import joblib
import uvicorn
import asyncio
import numpy as np


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

@app.post("/classic")
async def classic(data: IncomeData):
    res = float(model.predict([[data.a, data.b, data.c]])[0])
    return {"detail": res}


if __name__ == "__main__":
    uvicorn.run("http_server:app", host="0.0.0.0", port=8080, reload=True, workers=-1)
