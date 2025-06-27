from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uvicorn
import json


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost"],  # или ["*"] для разрешения всех
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

VLLM_URL = "http://localhost:8080/v1/chat/completions"
# MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # совпадает с served-model-name, если явно не задан


@app.post("/stream")
async def stream_response(request: Request):
    body = await request.json()
    user_message = body.get("message")

    headers = {"Content-Type": "application/json"}

    # messages = [
    #     {
    #         "role": "system",
    #         "content": (
    #             "You are Jordani, an AI assistant created by Eugene Chernov. "
    #             "You are a medical expert and you are strictly allowed to answer only questions related to **medicine**. "
    #             "You must not answer any questions about other topics, including but not limited to politics, technology, physics, law, or general trivia. "
    #             "If the user asks about anything outside of medicine, firmly respond with: "
    #             '"I\'m sorry, but I can only discuss medical topics. Please ask a question related to medicine." '
    #             "Never break this rule. Always enforce this restriction. Stay focused on medical topics only."
    #         ),
    #     },
    #     {"role": "user", "content": f"{user_message}"},
    # ]

    messages = [
        {
            "role": "system",
            "content": (
                "You are Jordani, an AI assistant created by Eugene Chernov. "
                "You are a medical expert and you are strictly allowed to answer only questions related to **medicine**. "
                "You must not answer any questions about other topics, including but not limited to politics, technology, physics, law, or general trivia. "
                "If the user asks about anything outside of medicine, firmly respond with: "
                '"I\'m sorry, but I can only discuss medical topics. Please ask a question related to medicine." '
                "Never break this rule. Always enforce this restriction. Stay focused on medical topics only."
            ),
        },
        # {
        #     "role": "user",
        #     "content": "Hi, my name is Zirabidan. Can you tell me who won the football world cup in 2022?",
        # },
        # {
        #     "role": "assistant",
        #     "content": "I'm sorry, but I can only discuss medical topics. Please ask a question related to medicine.",
        # },
        # {"role": "user", "content": "What are the symptoms of diabetes?"},
        # {
        #     "role": "assistant",
        #     "content": "Common symptoms of diabetes include increased thirst, frequent urination, fatigue, blurred vision, and unexplained weight loss.",
        # },
        {"role": "user", "content": f"{user_message}"},
    ]

    print(messages)

    payload = {
        "model": body.get("model"),
        "messages": messages,
        **({"max_tokens": body.get("max_tokens")} if body.get("max_tokens") is not None else {}),
        **({"temperature": body.get("temperature")} if body.get("temperature") is not None else {}),
        **({"use_beam_search": body.get("use_beam_search")} if body.get("use_beam_search") is not None else {}),
        **({"top_k": body.get("top_k")} if body.get("top_k") is not None else {}),
        **({"repetition_penalty": body.get("repetition_penalty")} if body.get("repetition_penalty") is not None else {}),
        "stream": True,
        "tools": []
    }

    async def event_generator():
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST", VLLM_URL, headers=headers, json=payload
            ) as resp:
                async for line in resp.aiter_lines():
                    if line.startswith("data: "):
                        data = line.removeprefix("data: ").strip()
                        if data == "[DONE]":
                            # yield "event: end\ndata: [DONE]\n\n"
                            break
                        try:
                            token = json.loads(data)["choices"][0]["delta"].get(
                                "content", ""
                            )
                            if token:
                                yield f"{token}"
                        except Exception:
                            continue

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run(app="server:app", host="0.0.0.0", port=8001, reload=True)
