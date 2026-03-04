
from fastapi import FastAPI
from datetime import datetime
from Data_base.db_engine import Base,engine,SessionLocal
from Data_base.db_model import answer_text
import requests

app = FastAPI(title="ChatGPT Offline Model")

Base.metadata.create_all(bind = 'engine')

def date_time(dt:datetime):
    return dt.strftime("%d-%m-%Y %I:%M %p")

#Default Modl Endpoint.
@app.get("/")
def default():
    return {"message":"This is the ChatGPT ffline Model"}

#GPT Output Funciton
def gpt_output(input_text):

    prompt = f"{input_text}."

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model":"gemma:2b",
            "prompt": prompt,
            "stream":False,
            "temperature":0.2
        }
    )

    return response

#split funciton - For removing unwanted space from the input.
def split_input(text,max_charecter = 1500):
    return [text[i+i+max_charecter] for i in range(0,len(x),max_charecter)]