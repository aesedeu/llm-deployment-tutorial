import os
import numpy as np
import grpc
import asyncio
from transformers import BertTokenizer
import tritonclient.grpc.aio as grpcclient
from tritonclient.grpc import service_pb2, service_pb2_grpc
from tritonclient.utils import triton_to_np_dtype
# from tritonclient.http import InferenceServerClient, InferInput, InferRequestedOutput
from tritonclient.http.aio import InferenceServerClient, InferInput, InferRequestedOutput


class InferenceLLMModule:
    def __init__(self) -> None:
        """Initialize."""
        self.url = os.environ.get("TRITON_SERVER_URL", "localhost:8001")
        self.triton_client = grpcclient.InferenceServerClient(url=self.url)
        self.tokenizer = BertTokenizer.from_pretrained("ai-forever/ruBert-base")

    async def infer_text(
        self,
        text: str,
        model_name: str = "bert_model",
    ) -> dict:
        """Perform inference on the input text."""

        # Tokenize input
        enc = self.tokenizer(
            text,
            return_tensors="np",
            padding="max_length",
            truncation=True,
            max_length=512,
        )

        input_ids = enc["input_ids"].astype(np.int64)
        attention_mask = enc["attention_mask"].astype(np.int64)
        token_type_ids = enc["token_type_ids"].astype(np.int64)

        # Prepare inputs for Triton
        inputs = [
            grpcclient.InferInput("input_ids", input_ids.shape, "INT64"),
            grpcclient.InferInput("attention_mask", attention_mask.shape, "INT64"),
            grpcclient.InferInput("token_type_ids", token_type_ids.shape, "INT64"),
        ]
        inputs[0].set_data_from_numpy(input_ids)
        inputs[1].set_data_from_numpy(attention_mask)
        inputs[2].set_data_from_numpy(token_type_ids)

        # Outputs
        outputs = [grpcclient.InferRequestedOutput("pooler_output")]

        # Inference
        results = await self.triton_client.infer(
            model_name=model_name,
            inputs=inputs,
            outputs=outputs,
        )

        # Get output
        output = results.as_numpy("pooler_output")
        embedding = output[0][0]  # CLS токен — [batch, seq_len, hidden] → [hidden]

        return {
            "embedding": embedding.tolist(),
        }

    def parse_model_metadata(self, model_name: str):
        """(опционально) Получить метадату и конфиг."""
        channel = grpc.insecure_channel(self.url)
        grpc_stub = service_pb2_grpc.GRPCInferenceServiceStub(channel)
        metadata_request = service_pb2.ModelMetadataRequest(name=model_name)
        config_request = service_pb2.ModelConfigRequest(name=model_name)

        metadata_response = grpc_stub.ModelMetadata(metadata_request)
        config_response = grpc_stub.ModelConfig(config_request)

        return metadata_response, config_response

from tritonclient.http.aio import (
    InferenceServerClient,
    InferInput,
    InferRequestedOutput,
)

class InferenceLinearModel:
    def __init__(self) -> None:
        self.url = os.environ.get("TRITON_SERVER_URL", "localhost:8000")
        self.client = None

    async def init(self):
        """Асинхронная инициализация клиента Triton."""
        self.client = InferenceServerClient(url=self.url, verbose=False)

    async def infer(
        self,
        input_array: np.ndarray,
        model_name: str = "classic_model",
        model_version: str = None
    ) -> float:
        """
        Perform inference with linear regression model.

        Args:
            input_array (np.ndarray): shape (n_features,)
            model_name (str): Name of the model on Triton

        Returns:
            float: Predicted value
        """

        if self.client is None:
            await self.init()

        if input_array.ndim == 1:
            input_array = input_array.reshape(1, -1)  # shape (1, n_features)

        # Prepare Triton inputs
        inputs = [InferInput("input", input_array.shape, "FP32")]
        inputs[0].set_data_from_numpy(input_array.astype(np.float32))

        # Define requested output
        outputs = [InferRequestedOutput("variable")]

        # Run inference
        results = await self.client.infer(
            model_name=model_name,
            model_version=model_version,
            inputs=inputs,
            outputs=outputs,
        )
        output_data = results.as_numpy("variable")

        return float(output_data[0][0])  # Assuming output is shape (1, 1)

    def get_model_metadata(self, model_name: str = "linear_regression"):
        return self.client.get_model_metadata(model_name=model_name)

    def get_model_config(self, model_name: str = "linear_regression"):
        return self.client.get_model_config(model_name=model_name)
