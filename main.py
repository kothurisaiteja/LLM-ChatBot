from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_groq import ChatGroq
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
)

# ---------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------
load_dotenv()

# ---------------------------------------------------
# Initialize LLM
# ---------------------------------------------------
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
)

# ---------------------------------------------------
# Chat Memory
# ---------------------------------------------------
chat_history = [
    SystemMessage(
        content="You are a helpful AI assistant."
    )
]

# ---------------------------------------------------
# Chat Function
# ---------------------------------------------------
def chatbot_reply(message: str) -> str:
    # Save user's message
    chat_history.append(HumanMessage(content=message))

    # Send complete conversation
    result = llm.invoke(chat_history)

    # Save AI response
    chat_history.append(AIMessage(content=result.content))

    return result.content


# ---------------------------------------------------
# FastAPI App
# ---------------------------------------------------
app = FastAPI()

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://llm-chatbot-interactive.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# Request Model
# ---------------------------------------------------
class ChatRequest(BaseModel):
    message: str


# ---------------------------------------------------
# API Endpoint
# ---------------------------------------------------
@app.post("/chat")
def chat(request: ChatRequest):
    response = chatbot_reply(request.message)
    return {"response": response}


# ---------------------------------------------------
# Home Route
# ---------------------------------------------------
@app.get("/")
def home():
    return {
        "message": "Groq Chatbot API is running!"
    }