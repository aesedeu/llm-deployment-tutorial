### 10 Run vLLM /v1/chat/completions with SSE FastAPI  (`10_vllm_sse_fastapi/`)
```bash
# tinyllama
python3 -m vllm.entrypoints.openai.api_server \
    --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \
    --port 8080 \
    --tensor-parallel-size 1 \
    --max-num-seqs 16 \
    --max-num-batched-tokens 4096 \
    --trust-remote-code

python server.py # run on 8001

# запрос на сервер FastAPI
curl -N -X POST http://localhost:8001/stream \
     -H "Content-Type: application/json" \
     -d '{
        "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "message": "Who are you?",
        "max_tokens": 100,
        "temperature": 0.9
        }'
```

```bash
# qwen
# 0.5B
python3 -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-0.5B-Instruct \
    --port 8080 \
    --tensor-parallel-size 1 \
    --max-num-seqs 32 \
    --max-num-batched-tokens 32768 \
    --trust-remote-code

# 7B
python3 -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-7B-Instruct \
    --port 8080 \
    --tensor-parallel-size 1 \
    --max-num-seqs 16 \
    --max-num-batched-tokens 32768 \
    --trust-remote-code

# Запрос из консоли
curl http://localhost:8080/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2.5-0.5B-Instruct",
    "prompt": "Hello",
    "max_tokens": 100
  }'

# запрос на сервер FastAPI
curl -N -X POST http://localhost:8001/stream \
     -H "Content-Type: application/json" \
     -d '{
        "model": "Qwen/Qwen2.5-0.5B-Instruct",
        "message": "Who is your creator?",
        "max_tokens": 100,
        "temperature": 0.2
        }'

curl -N -X POST http://localhost:8001/stream \
     -H "Content-Type: application/json" \
     -d '{
        "model": "Qwen/Qwen2.5-0.5B-Instruct",
        "message": "How to cook apple pie?",
        "max_tokens": 100,
        "temperature": 1
        }'

curl -N -X POST http://localhost:8001/stream \
     -H "Content-Type: application/json" \
     -d '{
        "model": "Qwen/Qwen2.5-0.5B-Instruct",
        "message": "How to cook apple pie?",
        "max_tokens": 300,
        "temperature": 1
        }'

# Tests
python test.py
python stress_test.py
```
Go to Web UI and try it.