from transformers import pipeline
import torch

qa_model = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    device=0 if torch.cuda.is_available() else -1
)

def generate_answer(prompt):
    output = qa_model(
        prompt,
        max_new_tokens=200,
        temperature=0.2,
        do_sample=False
    )
    return output[0]["generated_text"]