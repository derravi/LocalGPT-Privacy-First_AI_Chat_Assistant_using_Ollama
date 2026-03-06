from fastapi import FastAPI
from datetime import datetime
from Data_base.db_engine import Base,engine,SessionLocal
from Data_base.db_model import gpt_model
import requests
from schema.pydantic_model import gpt_model

app = FastAPI(title="ChatGPT Offline Model")

Base.metadata.create_all(bind =engine)

#For Save the Date and Time into the History
def date_time(dt:datetime):
    return dt.strftime("%d-%m-%Y %I:%M %p")

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
    return [text[i+i+max_charecter] for i in range(0,len(text),max_charecter)]

#Default Modl Endpoint.
@app.get("/")
def default():
    return {"message":"This is the ChatGPT Offline Model"}

#Anser Endpoints
@app.get("/answer")
def output(output:gpt_model):

    db = SessionLocal()

    main_output = gpt_output(output.original_text)

    output_history = gpt_model(
        original_txt = output.original_text,
        answer_text = main_output,
    )

    db.add(output_history)
    db.commit()
    db.refresh(output_history)
    db.close()

    return {
        "id":main_output,
        "final_output":output_history,
        "date_and_time":date_time(output_history.time_stemp)
    }