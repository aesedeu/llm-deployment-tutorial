https://docs.openvino.ai/2024/openvino-workflow/model-server/ovms_docs_llm_quickstart.html

wget https://raw.githubusercontent.com/openvinotoolkit/model_server/refs/heads/releases/2024/5/demos/common/export_models/export_model.py
mkdir models
python export_model.py text_generation --source_model TinyLlama/TinyLlama-1.1B-Chat-v1.0 --weight-format int8 --kv_cache_precision u8 --config_file_path models/config.json --model_repository_path models 

docker run -d --rm -p 8000:8000 -v $(pwd)/models:/models:ro openvino/model_server:2025.0 --rest_port 8000 --config_path /models/config.json

docker run -u $(id -u) -v $(pwd)/models:/models -p 8000:8000 openvino/model_server:2025.0 \ 
--model_name tinyllama --model_path /models/TinyLlama \ 
--port 8000 