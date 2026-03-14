from fastapi import FastAPI
from datetime import datetime
from Data_base.db_engine import Base, engine, SessionLocal
from Data_base.db_model import gpt_model, chat_session
from schema.pydantic_model import gpt_pydantic_model
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ChatGPT Offline Model")

Base.metadata.create_all(bind=engine)


# Format date
def date_time(dt: datetime):
    return dt.strftime("%d-%m-%Y %I:%M %p")

try:
    # GPT Output Function
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
except Exception as e:
    print(f"Error: {e}.")

# Default Endpoint
@app.get("/")
def default():
    return {"message": "This is the ChatGPT Offline Model"}

try:

    # Create Session
    @app.post("/create_session")
    def create_session(title: str):

        db = SessionLocal()

        session = chat_session(title=title)

        db.add(session)
        db.commit()
        db.refresh(session)

        db.close()

        return {
            "session_id": session.id,
            "title": session.title
        }
except Exception as e1:
    print(f"Error : {e1}.")

try:

    # Answer Endpoint
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

except Exception as e2:
    print(f"Error : {e2}.")


try:
    # View History
    @app.get("/history")
    def get_history():

        db = SessionLocal()

        data = db.query(gpt_model).all()

        db.close()

        return [
            {
                "id": i.id,
                "original_text": i.original_text,
                "answer_text": i.answer_text,
                "date_and_time": date_time(i.time_stemp)
            }
            for i in data
        ]

except Exception as e3:
    print(f"Error : {e3}.")

try:
    # Delete single history
    @app.delete("/history/{person_history_id}")
    def delete_function(person_history_id: int):

        db = SessionLocal()

        final_output = db.query(gpt_model).filter(
            gpt_model.id == person_history_id
        ).first()

        if not final_output:
            db.close()
            return {"message": "Data not found"}

        db.delete(final_output)
        db.commit()
        db.close()

        return {
            "message": f"Output with id {person_history_id} deleted successfully"
        }

except Exception as e4:
    print(f"Error : {e4}.")

try:
    # Delete full history
    @app.delete("/delete_full_history")
    def delete_all():

        db = SessionLocal()

        deleted_data = db.query(gpt_model).delete()

        db.commit()
        db.close()

        return {
            "message": "All history deleted successfully!",
            "total_deleted": deleted_data
        }
except Exception as e5:
    print(f"Error : {e5}.")