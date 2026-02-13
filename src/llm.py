from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import gc
from os import environ
from transformers.utils import is_flash_attn_2_available
def init_llm(model_name=environ["LLM_MODEL"]):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if is_flash_attn_2_available():
        model = AutoModelForCausalLM.from_pretrained(model_name,torch_dtype=torch.float16,
        attn_implementation="flash_attention_2")
    else:
        model = AutoModelForCausalLM.from_pretrained(model_name,torch_dtype=torch.float16)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if torch.cuda.is_available():
        try:
            model.to(device)
        except torch.cuda.OutOfMemoryError:
            model = AutoModelForCausalLM.from_pretrained(model_name,torch_dtype="auto")
            device = torch.device("cpu")
    return model, tokenizer, device



def analyze_dissatisfactionـcomment(comments, temperature:float=0.2, max_length=512, num_beams=5):
    model, tokenizer, device = init_llm()
    if torch.cuda.is_available():
        gc.collect()
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
    comments_text = ".\n".join(comments)
    input_text = f"""
    Analyze the following customer comment for product dissatisfaction. Identify the main reasons for dissatisfaction, the emotional tone, and any specific issues mentioned (e.g., quality, price, usability, delivery, support). Then, suggest actionable insights or recommendations the company can use to improve customer satisfaction.

    Customer Comment: “{comments_text}”

    Please structure your response as follows:

    Root Causes of Dissatisfaction: (List key issues mentioned)

    Emotional Tone: (Describe sentiment and intensity, e.g., mildly annoyed, frustrated, angry, disappointed)

    Impact Assessment: (Explain how this issue might affect customer loyalty or brand perception)

    Recommendations: (Provide clear, practical actions the company can take)

    Must respond in Persian (فارسی) clearly and professionally."""
        
    
    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.generate(
            inputs["input_ids"],
            max_new_tokens=max_length,
            num_beams=num_beams,
            early_stopping=True,
            temperature=temperature 

        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response_text = response.split("response:")[1].strip() if "response:" in response else response
    
    return response_text
