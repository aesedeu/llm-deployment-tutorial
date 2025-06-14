# server.py (FastAPI + WebSocket + gRPC)
import grpc
import asyncio
from fastapi import FastAPI, WebSocket
from proto import generation_pb2, generation_pb2_grpc

app = FastAPI()

@app.websocket("/ws")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()

    prompt = await websocket.receive_text()

    # подключение к vLLM gRPC
    channel = grpc.aio.insecure_channel("localhost:50051")
    stub = generation_pb2_grpc.GenerationServiceStub(channel)

    request = generation_pb2.GenerationRequest(
        prompt=prompt,
        max_tokens=128,
        temperature=0.9,
        stream=True
    )

    async for response in stub.Generate(request):
        token_text = response.text  # или .token, если возвращает int
        await websocket.send_text(token_text)

    await websocket.close()
