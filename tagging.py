import re
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def load_model():
    """Load the model and tokenizer."""
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen2-1.5B-Instruct",
        torch_dtype="auto",
        device_map="auto",  
        trust_remote_code=True
    )

    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-1.5B-Instruct")

    return model, tokenizer, device  


def generate_tags(text, tokenizer, model, device, max_new_tokens=150):
    """Generate tags from the input text."""

    prompt = (
    "Extract the most relevant and technical tags from the following text, "
    "ensuring they are specific to the domain of the content.\n\n"
    "The tags must meet the following conditions:\n"
    "- All tags should be in lowercase.\n"
    "- If a tag consists of multiple words, replace spaces with hyphens between words.\n"
    "- Tags should not contain any symbols or special characters apart from hyphens.\n\n"
    f"{text}\n\n"
    "Output the tags as a JSON list without additional explanation."
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

    with torch.no_grad():  
        generated_ids = model.generate(
            model_inputs.input_ids,
            max_new_tokens=max_new_tokens
        )

    output = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    try:
        start = output.find("[")
        end = output.find("]") + 1
        raw_tags = json.loads(output[start:end])  
        final_tags = [tag.replace("_", "-") for tag in raw_tags]
        return final_tags
    except json.JSONDecodeError as e:
        print(f"JSON Error: {e}\nOutput: {output}")
        return []