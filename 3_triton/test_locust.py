import time
from locust import HttpUser, task, between
import numpy as np

# URL вашего API
API_URL = "/predict/"
# Имя модели для использования
MODEL_NAME = "bert_model"

class ApiUser(HttpUser):
    wait_time = between(0.5, 1)  # Время ожидания между задачами (в секундах)

    # classic model inference
    @task
    def predict_classic(self):
        try:
            self.client.post(
                "/classic/",
                json={
                    "a": int(np.random.randint(1, 10, 1)[0]),
                    "b": int(np.random.randint(1, 10, 1)[0]),
                    "c": int(np.random.randint(1, 10, 1)[0]),
                },
            )
        except Exception as e:
            print(f"Error during request: {e}")

    # llm model inferencec
    @task
    def predict_llm(self):
        try:
            self.client.post(
                "/predict/",
                params={"model_name": MODEL_NAME},
                json={"text": "some text for locust inference"},
            )
        except Exception as e:
            print(f"Error during request: {e}")
