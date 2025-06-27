### 6. NVIDIA Triton Server (`6_triton/`)
Integration with NVIDIA Triton Inference Server:
- Model deployment using Triton server
- Support for multiple model formats (ONNX, TensorRT)
- Performance monitoring with Grafana and Prometheus
- Model optimization examples
- FastAPI integration for serving models

**Models list (`triton/models`)**:
- classic_model
- bert_model
- gpt2_model

Setup and running:
1. Move `triton/bert_trt` to `triton/models` (requires NVIDIA GPU)
2. Import Grafana dashboard from `dash-grafana-triton.json`
3. Create models in `research.ipynb` and move to `triton/models/classic_model`
4. Start the project:
```bash
# after this command be sure that all the models successfully loaded to triton (see container logs)
docker compose up -d
```

5. For TensorRT conversion:
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
6. Start FastAPI server:
```bash
python app.py
```
7. Check the availability via .ipynb file attached in the folder. There're a couple examples how to try triton via HTTP protocol.
8. Visit grafana dashboard (don't forget to create connection to Prometheus) to see metrics.
9. Try locust to see how dynamic batching works.