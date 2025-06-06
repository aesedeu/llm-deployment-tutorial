# LLM Deployment Examples

This repository contains a collection of examples demonstrating different approaches to deploying Large Language Models (LLMs) and ML models in production. Each folder contains a specific example focusing on different deployment aspects and technologies.

## Repository Structure

### 1. Docker Basics (`1_docker/`)
Introduction to containerization for ML models:
- Basic Docker setup for ML applications
- Best practices for containerizing ML models
- Foundation for more complex deployment scenarios

### 2. HTTP and gRPC Implementation (`2_http_grpc/`)
Demonstrates two common API implementation approaches:
- HTTP server implementation for model serving
- gRPC server implementation with protobuf
- Comparison between HTTP and gRPC approaches
- Includes example client implementations and testing scripts
- Jupyter notebook for model development and testing

Running the example:
1. Generate gRPC code from protobuf:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. model.proto
```
2. Start the server (either HTTP or gRPC)
3. Test using the provided notebook or Postman (for gRPC, include the `model.proto` file and specify ModelService + Message)

### 3. NVIDIA Triton Server (`3_triton/`)
Integration with NVIDIA Triton Inference Server:
- Model deployment using Triton server
- Support for multiple model formats (ONNX, TensorRT)
- Performance monitoring with Grafana and Prometheus
- Model optimization examples
- FastAPI integration for serving models

Setup and running:
1. Move `triton/bert_trt` to `triton/models` (requires NVIDIA GPU)
2. Import Grafana dashboard from `dash-grafana-triton.json`
3. Create models in `research.ipynb` and move to `triton/models/classic_model`
4. For TensorRT conversion:
```bash
# Enter TensorRT container
docker exec -it trtexec_container bash

# Convert ONNX to TensorRT
trtexec \
    --onnx=model.onnx \
    --saveEngine=model.plan \
    --minShapes=input:1x3 \
    --optShapes=input:8x3 \
    --maxShapes=input:16x3 \
    --fp16 \
    --useSpinWait
```
5. Start FastAPI server:
```bash
python app.py
```

### 4. gRPC Server Streaming (`4_grpc_server_stream/`)
Implementation of server-side streaming with gRPC:
- Demonstrates handling large file transfers
- Server-side streaming patterns
- Protobuf definitions for streaming services

Setup:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. file_streamer.proto
```

### 5. Bidirectional gRPC Streaming (`5_grpc_bidirectional_stream/`)
Advanced gRPC streaming implementation:
- Bidirectional streaming between client and server
- Chat-like application example
- Real-time communication patterns

Setup:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto
```

### 6. LLM with gRPC (`6_llm_grpc/`)
Integration of LLMs with gRPC:
- LLM-specific gRPC service implementation
- Support for both CUDA and CPU deployments
- Optimized for machine learning model serving
- Protobuf definitions for LLM services

Setup and running:
```bash
# Generate gRPC code
python -m grpc_tools.protoc -I=proto --python_out=. --grpc_python_out=. proto/chat.proto

# Start server on CUDA
python server.py

# Start server on macOS
OMP_NUM_THREADS=1 python server.py
```

### 7. vLLM Integration (`7_vllm/`)
Implementation using vLLM for optimized LLM serving:
- vLLM API server setup
- Integration with popular LLM models (e.g., GPT-2, TinyLlama)
- Streaming completion endpoints
- Performance optimization settings
- gRPC client-server architecture for vLLM
- Web interface with Nginx reverse proxy
- Docker Compose deployment setup
- Prometheus monitoring integration

Setup and running:

1. Basic vLLM setup:
```bash
# Install vLLM with gRPC support
pip install "vllm[grpc]"

# Start vLLM server with GPT-2
python3 -m vllm.entrypoints.openai.api_server \
    --model gpt2 \
    --port 8081 \
    --tensor-parallel-size 1

# Or start with TinyLlama
python3 -m vllm.entrypoints.openai.api_server \
    --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \
    --port 8080 \
    --tensor-parallel-size 1 \
    --max-num-seqs 16 \
    --max-num-batched-tokens 4096 \
    --trust-remote-code
```

2. Docker Compose deployment:
```bash
# Start the entire stack
docker-compose up -d
```

The Docker Compose setup includes:
- Nginx reverse proxy (port 80)
- vLLM service (port 8080)
- Prometheus monitoring (port 9090)
- Grafana dashboard (port 3000)

Nginx configuration provides:
- Static web interface serving
- Reverse proxy to vLLM API
- Proper handling of streaming responses
- CORS and security headers

Web Interface Features:
- MVP chat interface
- Real-time streaming responses
- Adjustable temperature and max tokens

Testing the deployment:
```bash
# Test model availability
curl http://localhost:8080/v1/models

# Check metrics
curl http://localhost:8080/metrics

# Test completion endpoint
curl http://localhost:8080/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt2",
    "prompt": "Hello",
    "max_tokens": 100
  }'

curl http://localhost:8080/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "prompt": "Hello",
    "max_tokens": 100
  }'
```

Architecture flow:
```
gRPC client (llm_client.py)
        │
        ▼
gRPC server (llm_server.py → LLMService)
        │
        ▼
vLLM API server (localhost:8080/v1/completions, stream=True)
        │
        ▼
[ tokens arrive gradually ]
        │
        ▼
gRPC server reads tokens and sends to client via stream
        │
        ▼
gRPC client prints them to console as they arrive
```

# 8

# 9
```bash
python3 -m vllm.entrypoints.openai.api_server \
    --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \
    --port 8080 \
    --tensor-parallel-size 1 \
    --max-num-seqs 16 \
    --max-num-batched-tokens 4096 \
    --trust-remote-code

python server.py # run on 8001

curl -N -X POST http://localhost:8001/stream \
     -H "Content-Type: application/json" \
     -d '{
        "message": "Once upon a time",
        "max_tokens": 100,
        "temperature": 0.1
        }'
```

## Target Audience

This repository is designed for ML engineers who want to learn about:
- Production deployment of LLMs and ML models
- Different serving architectures (HTTP, gRPC, Triton)
- Streaming and real-time inference
- Performance optimization techniques
- Container-based deployment
- Modern API design patterns

## Prerequisites

- Basic understanding of Python and ML concepts
- Docker installed for containerization examples
- NVIDIA GPU (optional, for GPU-accelerated examples)
- Understanding of API concepts (REST, gRPC)
