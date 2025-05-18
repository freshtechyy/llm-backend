from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import openai
import os


app = FastAPI()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can change to ["http://localhost"] if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    query : str


@app.post("/ask")
def ask_question(q: Question):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": q.query}]
        )
        answer = response.choices[0].message.content.strip()
        return {"answer": f"You asked: {q.query}. My answer: {answer}"}
    except Exception as e:
        return {"answer": f"Error: {str(e)}"}
