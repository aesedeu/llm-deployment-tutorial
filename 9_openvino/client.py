import requests
import argparse
import json

def generate_text(
    prompt: str,
    max_length: int = 100,
    temperature: float = 0.7,
    top_k: int = 50,
    top_p: float = 0.9,
    num_return_sequences: int = 1,
    server_url: str = "http://localhost:8000"
):
    """
    Generate text using the OpenVINO GPT-2 server.
    
    Args:
        prompt (str): The input prompt for text generation
        max_length (int): Maximum length of generated text
        temperature (float): Sampling temperature
        top_k (int): Top-k sampling parameter
        top_p (float): Top-p sampling parameter
        num_return_sequences (int): Number of sequences to generate
        server_url (str): URL of the inference server
    """
    
    # Prepare the request
    payload = {
        "prompt": prompt,
        "max_length": max_length,
        "temperature": temperature,
        "top_k": top_k,
        "top_p": top_p,
        "num_return_sequences": num_return_sequences
    }
    
    try:
        # Send request to server
        response = requests.post(f"{server_url}/generate", json=payload)
        response.raise_for_status()
        
        # Parse and print results
        result = response.json()
        print("\nGenerated texts:")
        print("---------------")
        for i, text in enumerate(result["generated_texts"], 1):
            print(f"\nSequence {i}:")
            print(text)
            print("---------------")
            
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with server: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client for OpenVINO GPT-2 text generation")
    parser.add_argument("--prompt", type=str, required=True, help="Input prompt for text generation")
    parser.add_argument("--max-length", type=int, default=100, help="Maximum length of generated text")
    parser.add_argument("--temperature", type=float, default=0.7, help="Sampling temperature")
    parser.add_argument("--top-k", type=int, default=50, help="Top-k sampling parameter")
    parser.add_argument("--top-p", type=float, default=0.9, help="Top-p sampling parameter")
    parser.add_argument("--num-sequences", type=int, default=1, help="Number of sequences to generate")
    parser.add_argument("--server-url", type=str, default="http://localhost:8000", help="Server URL")
    
    args = parser.parse_args()
    
    generate_text(
        prompt=args.prompt,
        max_length=args.max_length,
        temperature=args.temperature,
        top_k=args.top_k,
        top_p=args.top_p,
        num_return_sequences=args.num_sequences,
        server_url=args.server_url
    ) 