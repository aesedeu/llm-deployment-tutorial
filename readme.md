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