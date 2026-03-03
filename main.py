
from fastapi import FastAPI
from datetime import datetime
from Data_base.db_engine import Base,engine,SessionLocal
from Data_base.db_model import 

app = FastAPI(title="ChatGPT Offline Model")



@app.get("/")
def default():
    return {"message":"This is the ChatGPT ffline Model"}
