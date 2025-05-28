# Запуск проекта 2_http_grpc
## HTTP

## grpc
- Создаем модель в блокноте, копируем ее в `grpc_data`
- В `grpc_data` запускаем
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. model.proto
```
- Стартуем сервер
- Можно дернуть ручку из блокнота или через Postman (необходимо приложить `model.proto` файл + указать ModelService + указать Message)

# Запуск проекта 3_triton
- `triton/bert_trt` необходимо перенести в `triton/models`, модель прочитается тритоном при условии что есть GPU nvidia
- для отображения дашборда Grafana необходимо его экспортировать из файла `dash-grafana-triton.json`. Дополнительно необходимо в Grafana создать новое подключение к Prometheus
- классические модели сначала нужно создать в файле `research.ipynb` и затем переместить в `triton/models/classic_model` в директории 1 и 2
- имена ONNX-моделей должны быть только `model.onnx`
- для конвертации модели в TensorRT необходимо переместить ONNX-модель в `trtexec_workspase`, зайти в контейнер 
```bash
docker exec -it trtexec_container bash
```
В контейнере с TRT выполнить команду для конвертации ONNX -> TensorRT
```bash
trtexec \
    --onnx=model.onnx \
    --saveEngine=model.plan \
    --minShapes=input:1x3 \
    --optShapes=input:8x3 \
    --maxShapes=input:16x3 \
    --fp16 \
    --useSpinWait
```
Созданную модель переместить в `triton/models/bert_trt/1`
- Запуск FastAPI
```bash
python app.py
```
- Для запуска тестов выполнить скрипты в директории `tests`

# 4
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. file_streamer.proto
```

# 5
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto
```

# 6
```bash
python -m grpc_tools.protoc -I=proto --python_out=. --grpc_python_out=. proto/chat.proto

# запуск сервера на cuda
python server.py

# запуск сервера на macos
OMP_NUM_THREADS=1 python server.py
```

# 7
```bash
pip install "vllm[grpc]"

python3 -m vllm.entrypoints.openai.api_server \
    --model gpt2 \
    --port 8081 \
    --tensor-parallel-size 1

python3 -m vllm.entrypoints.openai.api_server \
    --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \
    --port 8080 \
    --tensor-parallel-size 1 \
    --max-num-seqs 16 \
    --max-num-batched-tokens 4096 \
    --trust-remote-code
    

curl http://localhost:8080/v1/models
curl http://localhost:8080/metrics

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. llm.proto

curl http://localhost:8080/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt2",
    "prompt": "Hello",
    "max_tokens": 100
  }'
```
```
gRPC клиент (llm_client.py)
        │
        ▼
gRPC сервер (llm_server.py → LLMService)
        │
        ▼
vLLM API сервер (localhost:8080/v1/completions, stream=True)
        │
        ▼
[ токены приходят постепенно ]
        │
        ▼
gRPC сервер читает токены и отправляет клиенту по stream
        │
        ▼
gRPC клиент печатает их в консоль по мере поступления
```

Docker image
- https://github.com/vllm-project/vllm/blob/main/docker/Dockerfile.arm