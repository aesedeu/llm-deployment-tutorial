from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from optimum.intel import OVModelForCausalLM
from transformers import GPT2Tokenizer
import torch
import numpy as np

app = FastAPI(title="OpenVINO GPT-2 Inference Server")

# Initialize model and tokenizer
MODEL_NAME = "gpt2"

print("Loading model and tokenizer...")
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
model = OVModelForCausalLM.from_pretrained(MODEL_NAME, export=True)
print("Model and tokenizer loaded successfully!")

class GenerationRequest(BaseModel):
    prompt: str
    max_length: Optional[int] = 100
    temperature: Optional[float] = 0.7
    top_k: Optional[int] = 50
    top_p: Optional[float] = 0.9
    num_return_sequences: Optional[int] = 1

class GenerationResponse(BaseModel):
    generated_texts: List[str]

@app.post("/generate", response_model=GenerationResponse)
async def generate_text(request: GenerationRequest):
    try:
        # Tokenize input
        input_ids = tokenizer.encode(request.prompt, return_tensors="pt")
        
        # Generate text
        output = model.generate(
            input_ids,
            max_length=request.max_length,
            temperature=request.temperature,
            top_k=request.top_k,
            top_p=request.top_p,
            num_return_sequences=request.num_return_sequences,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True
        )
        
        # Decode output
        generated_texts = [
            tokenizer.decode(sequence, skip_special_tokens=True)
            for sequence in output
        ]
        
        return GenerationResponse(generated_texts=generated_texts)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 