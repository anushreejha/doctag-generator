# import re
# import json
# import torch
# from transformers import AutoModelForCausalLM, AutoTokenizer

# def load_model():
#     """Load the model and tokenizer."""
#     device = "cuda" if torch.cuda.is_available() else "cpu"

#     model = AutoModelForCausalLM.from_pretrained(
#         "Qwen/Qwen2-1.5B-Instruct",
#         torch_dtype="auto",
#         device_map="auto",
#         trust_remote_code=True
#     ).to(device)

#     tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-1.5B-Instruct")
#     return model, tokenizer, device

# def clean_tags(tags):
#     """Clean tags by removing unwanted symbols and converting them to lowercase."""
#     cleaned_tags = [re.sub(r'[^a-zA-Z0-9\s]', '', tag).strip().lower() for tag in tags]
#     return list(filter(None, cleaned_tags))

# def filter_tags(raw_tags):
#     """Remove quotes and return the list of cleaned tags."""
#     return clean_tags([tag.strip('"') for tag in raw_tags])

# def generate_tags(text, tokenizer, model, device, max_new_tokens=150):
#     """Generate tags from the input text."""
#     prompt = (
#         "Extract the most relevant and technical tags from the following text, "
#         "ensuring they are specific to the domain of the content:\n\n"
#         f"{text}\n\nOutput the tags as a JSON list without additional explanation."
#     )

#     messages = [
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": prompt}
#     ]
    
#     text_input = tokenizer.apply_chat_template(
#         messages,
#         tokenize=False,
#         add_generation_prompt=True
#     )

#     model_inputs = tokenizer([text_input], return_tensors="pt").to(device)

#     with torch.no_grad():  
#         generated_ids = model.generate(
#             model_inputs.input_ids,
#             max_new_tokens=max_new_tokens
#         )

#     output = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

#     try:
#         start = output.find("[")
#         end = output.find("]") + 1
#         raw_tags = json.loads(output[start:end])  
#         return filter_tags(raw_tags)
#     except json.JSONDecodeError as e:
#         print(f"JSON Error: {e}\nOutput: {output}")
#         return []

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
    ).to(device)

    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-1.5B-Instruct")
    return model, tokenizer, device

def format_tags(tags):
    """Replace spaces in each tag with hyphens."""
    return [tag.replace(" ", "-") for tag in tags]

def clean_tags(tags):
    """Clean tags by removing unwanted symbols, converting to lowercase, and formatting."""
    cleaned_tags = [re.sub(r'[^a-zA-Z0-9\s]', '', tag).strip().lower() for tag in tags]
    return format_tags(list(filter(None, cleaned_tags)))

def filter_tags(raw_tags):
    """Remove quotes and return the list of cleaned tags."""
    return clean_tags([tag.strip('"') for tag in raw_tags])

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
        return filter_tags(raw_tags)
    except json.JSONDecodeError as e:
        print(f"JSON Error: {e}\nOutput: {output}")
        return []