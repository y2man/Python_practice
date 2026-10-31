import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from fastapi import Depends
from database import SessionLocal
from models import Base, User, Conversation, Message
from database import engine, test_database_connection
from sqlalchemy.exc import SQLAlchemyError
from groq import Groq, APIStatusError
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator, Field,EmailStr
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()
password_hash = PasswordHash.recommended()
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = HTTPBearer()


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
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


class PromptRequest(BaseModel):
    prompt: str = Field(max_length=2000)
    conversation_id: int | None = None

    @field_validator("prompt")
    @classmethod
    def reject_blank_prompt(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Prompt cannot be empty.")
        return value
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
class RenameConversationRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty.")

        return value
def create_access_token(user_id: int):
    if not JWT_SECRET:
        raise HTTPException(
            status_code=500,
            detail="JWT secret is not configured."
        )

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid or expired authentication token.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        if not JWT_SECRET:
           raise HTTPException(
        status_code=500,
        detail="JWT secret is not configured."
            )
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )

        user_id = int(payload.get("sub"))

    except (jwt.InvalidTokenError, TypeError, ValueError):
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise credentials_exception

    return user
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


@app.post("/ask")
def ask_ai(
    request: PromptRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # 1. Find an existing conversation or create a new one
        if request.conversation_id is None:
            conversation = Conversation(user_id=current_user.id)
            db.add(conversation)
            db.flush()
            conversation.title = request.prompt[:50]

        else:
            conversation = db.query(Conversation).filter(
                Conversation.id == request.conversation_id,
                Conversation.user_id == current_user.id
            ).first()

            if conversation is None:
                raise HTTPException(
                    status_code=404,
                    detail="Conversation not found."
                )

        # 2. Retrieve the last 10 messages
        previous_messages = (
            db.query(Message)
            .filter(Message.conversation_id == conversation.id)
            .order_by(Message.id.desc())
            .limit(10)
            .all()
        )

        previous_messages.reverse()

        messages = [
            {"role": message.role, "content": message.content}
            for message in previous_messages
        ]

        # 3. Add the new user prompt to the AI context
        messages.append({
            "role": "user",
            "content": request.prompt
        })

        # 4. Send the conversation to Groq
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            max_completion_tokens=500
        )

        answer = completion.choices[0].message.content

        if not answer or not answer.strip():
            raise HTTPException(
                status_code=502,
                detail="The AI service could not generate an answer."
            )

        # 5. Save both messages in PostgreSQL
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=request.prompt
        )

        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=answer
        )

        db.add_all([user_message, assistant_message])
        db.commit()
        db.refresh(conversation)

        return {
            "conversation_id": conversation.id,
            "answer": answer
        }

    except HTTPException:
        db.rollback()
        raise

    except APIStatusError as e:
        db.rollback()
        print(f"Groq API status: {e.status_code}")

        status_code = 429 if e.status_code == 429 else 502

        raise HTTPException(
            status_code=status_code,
            detail="The AI service could not generate a response."
        )

    except Exception as e:
        db.rollback()
        print(f"Error: {type(e).__name__}: {e}")

        raise HTTPException(
            status_code=502,
            detail="The AI service could not generate a response."
        )

@app.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found."
        )

    db.delete(conversation)
    db.commit()

    return {"message": "Conversation deleted successfully."}

@app.get("/conversations")
def get_all_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conversations = (
        db.query(Conversation)
        .filter(Conversation.user_id == current_user.id)
        .order_by(Conversation.created_at.desc())
        .all()
    )

    return {
        "conversations": [
            {
                "conversation_id": conversation.id,
                "title": conversation.title,
                "created_at": conversation.created_at,
            }
            for conversation in conversations
        ]
    }
@app.patch("/conversations/{conversation_id}")
def rename_conversation(
    conversation_id: int,
    request: RenameConversationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found."
        )

    conversation.title = request.title
    db.commit()
    db.refresh(conversation)

    return {
        "message": "Conversation renamed successfully.",
        "conversation_id": conversation.id,
        "title": conversation.title
    }
@app.get("/conversations/{conversation_id}")
def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found."
        )

    return {
        "conversation_id": conversation.id,
        "title": conversation.title,
        "messages": [
            {
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at
            }
            for message in conversation.messages
        ]
    }

@app.get("/db-check")
def db_check():
    try:
        result = test_database_connection()
        return {"database_connected": result == 1}
    except (SQLAlchemyError, RuntimeError):
        return {"database_connected": False}      

        
@app.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == request.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email is already registered."
        )

    new_user = User(
        email=request.email,
        password_hash=password_hash.hash(request.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully.",
        "user_id": new_user.id,
        "email": new_user.email
    }     
        
@app.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == request.email
    ).first()

    if not user or not password_hash.verify(
        request.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }
