"""
Generates technical tags for text files using the Qwen-1.5B-Instruct model.
"""

import os
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import re


def load_model():
    """Load the Qwen-1.5B-Instruct model and tokenizer."""
    model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen2-1.5B-Instruct",
        torch_dtype="auto",
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-1.5B-Instruct")
    return model, tokenizer


def filter_tags(raw_tags):
    """Remove quotes and return the list of tags."""
    return [tag.strip('"') for tag in raw_tags]


def generate_tags(text, tokenizer, model, device, max_new_tokens=150):
    """Generate tags from the input text."""
    prompt = (
        "Extract the most relevant and technical tags from the following text, "
        "ensuring they are specific to the domain of the content:\n\n"
        f"{text}\n\nOutput the tags as a JSON list without additional explanation."
    )

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    
    text_input = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    model_inputs = tokenizer([text_input], return_tensors="pt").to(device)

    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=max_new_tokens
    )

    output = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    try:
        match = re.search(r'\[.*?\]', output, re.DOTALL)
        if match:
            raw_tags = json.loads(match.group(0))  
            return filter_tags(raw_tags)  
    except:
        print("Error: Failed to parse JSON.")
        print(f"Output: {output}")
        return []


def process_files(input_dir, output_dir, tokenizer, model, device):
    """Generate and save tags for all text files."""
    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".txt"):
            input_path = os.path.join(input_dir, file_name)
            with open(input_path, 'r', encoding='utf-8') as file:
                text = file.read()

            tags = generate_tags(text, tokenizer, model, device)
            save_tags(output_dir, file_name, tags)


def save_tags(output_dir, file_name, tags):
    """Save the generated tags to a JSON file."""
    output_path = os.path.join(output_dir, file_name.replace(".txt", ".json"))
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"tags": tags}, f, ensure_ascii=False, indent=4)


def main():
    input_dir = "processed_inputs"
    output_dir = "tags"
    model, tokenizer = load_model()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    process_files(input_dir, output_dir, tokenizer, model, device)


if __name__ == "__main__":
    main()
