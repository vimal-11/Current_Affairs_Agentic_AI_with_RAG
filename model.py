from transformers import AutoTokenizer, AutoModelForCausalLM
from db_utils import search_articles
import torch


# model_name = "mistralai/Mistral-7B-Instruct-v0.2"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(
#     model_name,
#     torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
#     device_map="auto"
# )



def build_prompt(question, context=""):
    return f"""<s>[INST] Use the following context to answer the question:

{context}

Question: {question}
Answer: [/INST]"""


# def get_answer(prompt):
#     inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
#     with torch.no_grad():
#         outputs = model.generate(
#             **inputs,
#             max_new_tokens=300,
#             temperature=0.7,
#             top_p=0.95,
#             do_sample=True
#         )
#     return tokenizer.decode(outputs[0], skip_special_tokens=True)

query = "What did Donald Trump say about protests?"
results = search_articles(query)
print(results)
