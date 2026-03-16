🚀 LocalGPT – Offline AI Chat Backend

LocalGPT is a backend system that enables ChatGPT-style conversations using a locally hosted Large Language Model (LLM).

The project is built with FastAPI and integrates Gemma 2B via Ollama to generate AI responses locally.
It manages chat sessions, stores conversation history, and exposes REST APIs for interacting with the AI model.

✨ Features

🤖 Local AI responses using Gemma 2B (Ollama)
⚡ High-performance backend with FastAPI
🗄 Persistent chat storage using SQLite + SQLAlchemy
💬 Automatic chat session creation with AI-generated titles
📜 Conversation history with timestamps
🧹 APIs to retrieve or delete chat history

🧰 Tech Stack
Python
FastAPI
SQLAlchemy
Pydantic
SQLite
Ollama
Gemma 2B

▶️ Running the Project
1️⃣ Install dependencies
pip install fastapi uvicorn sqlalchemy pydantic requests
2️⃣ Pull the AI model
ollama pull gemma:2b
3️⃣ Start the FastAPI server
uvicorn main:app --reload


API docs will be available at:
 Link:- http://127.0.0.1:8000/docs

📡 API Endpoints

Create Chat Session
Creates a new chat session and generates a title using the LLM.

POST /create_session
Generate AI Response
Generates responses for prompts and stores them in the database.

POST /answer
Get Chat History

#Retrieve stored prompts and AI responses.

GET /history
Delete Specific History
DELETE /history/{history_id}
Delete All History
DELETE /delete_full_history

⚠️ Project Scope
This project currently implements only the backend system.
A frontend interface can be integrated in the future.

👨‍💻 Author:- Ravi Der