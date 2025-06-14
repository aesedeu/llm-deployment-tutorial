from transformers import GPT2Tokenizer
from optimum.intel import OVModelForCausalLM
import argparse

def generate_text(
    prompt: str,
    model_name: str = "gpt2",
    max_length: int = 100,
    temperature: float = 0.7,
    top_k: int = 50,
    top_p: float = 0.9,
    num_return_sequences: int = 1,
):
    """
    Generate text using GPT-2 with OpenVINO optimization
    """
    print(f"Loading model {model_name}...")
    
    # Load tokenizer and model
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    # The export=True parameter converts the model to OpenVINO IR format
    model = OVModelForCausalLM.from_pretrained(model_name, export=True)
    
    print("Model loaded successfully!")
    
    # Tokenize input
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    
    print("\nGenerating text...")
    # Generate text
    output = model.generate(
        input_ids,
        max_length=max_length,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        num_return_sequences=num_return_sequences,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True
    )
    
    # Decode and print results
    print("\nGenerated texts:")
    print("---------------")
    for i, sequence in enumerate(output, 1):
        text = tokenizer.decode(sequence, skip_special_tokens=True)
        print(f"\nSequence {i}:")
        print(text)
        print("---------------")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate text using GPT-2 with OpenVINO")
    parser.add_argument("--prompt", type=str, required=True, help="Input prompt for text generation")
    parser.add_argument("--model", type=str, default="gpt2", help="Model name (default: gpt2)")
    parser.add_argument("--max-length", type=int, default=100, help="Maximum length of generated text")
    parser.add_argument("--temperature", type=float, default=0.7, help="Sampling temperature")
    parser.add_argument("--top-k", type=int, default=50, help="Top-k sampling parameter")
    parser.add_argument("--top-p", type=float, default=0.9, help="Top-p sampling parameter")
    parser.add_argument("--num-sequences", type=int, default=1, help="Number of sequences to generate")
    
    args = parser.parse_args()
    
    generate_text(
        prompt=args.prompt,
        model_name=args.model,
        max_length=args.max_length,
        temperature=args.temperature,
        top_k=args.top_k,
        top_p=args.top_p,
        num_return_sequences=args.num_sequences,
    ) 