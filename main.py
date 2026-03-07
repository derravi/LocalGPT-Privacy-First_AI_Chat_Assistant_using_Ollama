from fastapi import FastAPI
from datetime import datetime
from Data_base.db_engine import Base, engine, SessionLocal
from Data_base.db_model import gpt_model
import requests
from schema.pydantic_model import gpt_pydantic_model

app = FastAPI(title="ChatGPT Offline Model")

Base.metadata.create_all(bind=engine)


# Format date
def date_time(dt: datetime):
    return dt.strftime("%d-%m-%Y %I:%M %p")


# GPT Output Function
def gpt_output(input_text):

    prompt = f"{input_text}"

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma:2b",
            "prompt": prompt,
            "stream": False,
            "temperature": 0.2
        }
    )

    response.raise_for_status()

    return response.json()["response"]


# Default Endpoint
@app.get("/")
def default():
    return {"message": "This is the ChatGPT Offline Model"}


# Answer Endpoint
@app.post("/answer")
def output(output: gpt_pydantic_model):

    db = SessionLocal()

    main_output = gpt_output(output.input_text)

    output_history = gpt_model(
        original_text=output.input_text,
        answer_text=main_output,
    )

    db.add(output_history)
    db.commit()
    db.refresh(output_history)
    db.close()

    return {
        "id": output_history.id,
        "final_output": output_history.answer_text,
        "date_and_time": date_time(output_history.time_stemp)
    }

#Endpoints for the view old history
@app.get("/history")
def delete_gpt_record(prompt_id:int):

    db = SessionLocal()

    data = db.query(gpt_model).all()

    db.close()

    return [{
        "id":i.id,
        "original_text":i.original_text,
        "answer_text":i.answer_text,
        "date_and_time": date_time(i.time_stemp)
        } for i in data
    ]

@app.delete()