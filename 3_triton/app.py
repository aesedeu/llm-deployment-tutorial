from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import joblib
import uvicorn
import asyncio
import numpy as np

from infer_triton import InferenceLLMModule, InferenceLinearModel

inference_llm_module = InferenceLLMModule()
inference_linear_module = InferenceLinearModel()

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

app = FastAPI(
    lifespan=startup
)

@app.post("/classic")
async def classic(data: IncomeData):
    res = float(model.predict([[data.a, data.b, data.c]])[0])
    # await asyncio.sleep(1)
    return {"detail": res}


@app.post("/triton_classic_ml")
async def classic(
    payload: IncomeData,
    model_name: str = Query(..., description="Имя модели в Triton"),
    model_version: str = Query(..., description="Версия модели в Triton")
):
    result = await inference_linear_module.infer(
        np.array([payload.a, payload.b, payload.c]),
        model_name=model_name,
        model_version=model_version
    )

    return {"detail": result}


@app.post(
    "/triton_llm", description="Выполняет инференс текста через модель ruBERT в Triton."
)
async def predict(
    payload: TextInput,
    model_name: str = Query(..., description="Имя модели в Triton")
):
    """
    Выполнить инференс текста.

    Args:
        payload (TextInput): Ввод текста.
        model_name (str): Имя модели в Triton.

    Returns:
        dict: Эмбеддинг CLS токена (или другой выход, если нужно).
    """
    try:
        result = await inference_llm_module.infer_text(payload.text, model_name=model_name)

        return {"embedding": result["embedding"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        workers=-1
    )
