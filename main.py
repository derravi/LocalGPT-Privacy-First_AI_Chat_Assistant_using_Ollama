from fastapi import FastAPI
from datetime import datetime
from Data_base.db_engine import Base, engine, SessionLocal
from Data_base.db_model import gpt_model, chat_session
from schema.pydantic_model import gpt_pydantic_model
import requests
    
app = FastAPI(title="ChatGPT Offline Model")

try:

    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Error : {e}.")

# Format date
def date_time(dt: datetime):
    return dt.strftime("%d-%m-%Y %I:%M %p")


# GPT Output
def gpt_output(input_text):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma:2b",
            "prompt": input_text,
            "stream": False,
            "temperature": 0.2
        }
    )

    response.raise_for_status()

    return response.json()["response"]


# Generate Session Title
def generate_title(prompt):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma:2b",
            "prompt": f"Generate a short chat title (3-5 words): {prompt}",
            "stream": False,
            "temperature": 0.2
        }
    )

    response.raise_for_status()

    return response.json()["response"].strip()


# Default Endpoint
@app.get("/")
def default():
    return {"message": "This is the ChatGPT Offline Model"}


# Create Session
@app.post("/create_session")
def create_session(prompt: str):

    db = SessionLocal()

    auto_title = generate_title(prompt)

    session = chat_session(title=auto_title)

    db.add(session)
    db.commit()
    db.refresh(session)

    db.close()

    return {
        "session_id": session.id,
        "title": session.title
    }


# Generate Answer
@app.post("/answer")
def output(session_id: int, output: gpt_pydantic_model):

    db = SessionLocal()

    results = []

    for prompt in output.input_text:

        main_output = gpt_output(prompt)

        output_history = gpt_model(
            session_id=session_id,
            original_text=prompt,
            answer_text=main_output
        )

        db.add(output_history)
        db.commit()
        db.refresh(output_history)

        results.append({
            "id": output_history.id,
            "prompt": prompt,
            "answer": main_output,
            "date_and_time": date_time(output_history.time_stemp)
        })

    db.close()

    return {
        "total_prompts": len(results),
        "responses": results
    }


# View History with Title
@app.get("/history")
def get_history():

    db = SessionLocal()

    data = db.query(gpt_model, chat_session).join(
        chat_session,
        gpt_model.session_id == chat_session.id
    ).all()

    db.close()

    return [
        {
            "id": i.gpt_model.id,
            "title": i.chat_session.title,
            "original_text": i.gpt_model.original_text,
            "answer_text": i.gpt_model.answer_text,
            "date_and_time": date_time(i.gpt_model.time_stemp)
        }
        for i in data
    ]


# Delete single history
@app.delete("/history/{history_id}")
def delete_history(history_id: int):

    db = SessionLocal()

    data = db.query(gpt_model).filter(
        gpt_model.id == history_id
    ).first()

    if not data:
        db.close()
        return {"message": "Data not found"}

    db.delete(data)
    db.commit()

    db.close()

    return {"message": "History deleted successfully"}


# Delete full history
@app.delete("/delete_full_history")
def delete_all():

    db = SessionLocal()

    deleted = db.query(gpt_model).delete()

    db.commit()
    db.close()

    return {
        "message": "All history deleted",
        "total_deleted": deleted
    }