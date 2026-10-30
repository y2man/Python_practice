import json
import os

from database import engine, test_database_connection
from models import Base
from sqlalchemy.exc import SQLAlchemyError
from groq import Groq, APIStatusError
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator, Field
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()


@app.on_event("startup")
def create_database_tables():
    if engine is not None:
        Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5501",
        "http://localhost:5501",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type"],
)
def save_conversations(conversations):
    with open("conversations.json","w") as file: 
        
     
        json.dump(conversations,file)
def load_conversations():
    try:
        with open("conversations.json", "r") as file:
            content = file.read().strip()

            if not content:
                return {}

            return json.loads(content)

    except FileNotFoundError:
        return {}
conversations = load_conversations()

class PromptRequest(BaseModel):
    prompt: str = Field(max_length=2000)
    conversation_id: str = Field(max_length=100)

    @field_validator("prompt", "conversation_id")
    @classmethod
    def reject_blank_values(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty or whitespace")
        return value



api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


@app.post("/ask")

def ask_ai(request: PromptRequest):
    try:
        if not api_key:
           raise HTTPException(
        status_code=401,
        detail="The Groq API key is not configured."
    )
        conversation_id = request.conversation_id
        
        if conversation_id not in conversations:
                conversations[conversation_id] = []
        

        messages = conversations[conversation_id]

        new_messages = messages + [{
            "role": "user",
            "content": request.prompt
        }]
        recent_messages = new_messages[-10:]

        
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=recent_messages,
            max_completion_tokens=500
        )
   

        answer = completion.choices[0].message.content
        
        if not answer or not answer.strip():
            raise HTTPException(
                status_code=502,
                detail="The AI service could not generate an answer.")
        
            


        conversations[conversation_id] = new_messages + [{
        "role": "assistant",
        "content": answer
    }]
        save_conversations(conversations)

        return {
            "conversation_id": conversation_id,
            "answer": answer
        }
        
        

        
    except HTTPException:
        raise
    except APIStatusError as e:
        print(f"Groq API status: {e.status_code}")

        if e.status_code == 401:
            status_code = 500
        elif e.status_code == 429:
            status_code = 429
        else:
            status_code = 502

        raise HTTPException(
            status_code=status_code,
            detail="The AI service could not generate a response."
        )
        
    except Exception as e:
        print(f"Groq error: {type(e).__name__}: {e }")
        raise HTTPException(
            status_code=502,
            detail="The AI service could not generate a response. Check the server terminal."
        )
        

@app.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: str):
    if conversation_id in conversations:
        del conversations[conversation_id]
        save_conversations(conversations)
        return {"message": "Conversation deleted"}

    raise HTTPException(
        status_code=404,
        detail="Conversation not found"
    )
    

@app.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: str):
    if conversation_id not in conversations:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    return {
        "conversation_id": conversation_id,
        "messages": conversations[conversation_id]
    }


@app.get("/db-check")
def db_check():
    try:
        result = test_database_connection()
        return {"database_connected": result == 1}
    except (SQLAlchemyError, RuntimeError):
        return {"database_connected": False}      

        
        

