from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SantaRequest(BaseModel):
    message: str

def get_generator():
    generator = pipeline('text-generation', model='rinna/japanese-gpt2-medium', max_length=50)
    return generator

def generate_text(message: str):
    generator = get_generator()
    response = generator(message, max_length=50)
    return response[0]['generated_text']

@app.post("/")
def talk_to_santa(request: SantaRequest):
    santa_prompt = f"サンタさんは {request.message} についてどう思いますか？"
    generated_text = generate_text(santa_prompt)
    
    try:
        end_of_question = generated_text.index("についてどう思いますか？") + len("についてどう思いますか？")
        answer = generated_text[end_of_question:].strip()
    except ValueError:
        answer = generated_text
    
    return {"response": answer}