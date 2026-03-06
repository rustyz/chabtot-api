# app/llm/llm_client.py

from transformers import pipeline
import torch

# Load once globally
#qa_model = pipeline(
 #   "text2text-generation",
  #  model="google/flan-t5-base",
  #  device=0 if torch.cuda.is_available() else -1
#)
qa_model = pipeline(
    "text-generation",
    model="microsoft/phi-2",
    device=0 if torch.cuda.is_available() else -1
)


def generate_answer(question, context):

    prompt = f"""
Use the context below to answer the question in a clear complete sentence.

Context:
{context}

Question:
{question}

Answer:
"""

    output = qa_model(
        prompt,
        max_new_tokens=100,
        do_sample=False
    )

    return output[0]["generated_text"]
 #   prompt = f"""
  #  You are a professional assistant for Ideam.

   # Answer the question in a complete sentence.
    #Do NOT shorten the answer.
    #Use only the provided context.

    #Context:
    #{context}

#    Question:
 #   {question}

  #  Full Answer:
  #  """

   # response = qa_model(
    #    prompt,
     #   max_new_tokens=120,
      #  do_sample=False
    #)

    #return response[0]["generated_text"].strip()
