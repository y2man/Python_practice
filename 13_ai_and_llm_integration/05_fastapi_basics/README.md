# AI Conversation API

A REST API built with Python, FastAPI, and Groq that allows users to interact with an AI model and maintain conversation history.

## Features

- AI-powered responses using the Groq API
- Conversation IDs to keep chats separate
- Conversation history with recent messages included in AI requests
- Request validation using Pydantic
- JSON-based conversation persistence
- Retrieve and delete conversations
- Error handling for API failures
- Automated tests using pytest

## Technologies

- Python
- FastAPI
- Groq API
- Pydantic
- JSON
- pytest
- HTTPX

## Setup

### 1. Clone the repository

Clone this repository or download the project files.

### 2. Install dependencies

```bash
py -m pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your own Groq API key. Never commit your `.env` file or share your API key.

### 4. Run the API

```bash
py -m uvicorn main:app --reload
```

Open the interactive API documentation at:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/ask` | Send a prompt to the AI |
| GET | `/conversations/{conversation_id}` | Retrieve a conversation |
| DELETE | `/conversations/{conversation_id}` | Delete a conversation |

## Run Tests

```bash
py -m pytest -v
```

## Current Testing

The project includes automated tests for invalid prompts and requests involving nonexistent conversations.

## Future Improvements

- Expand automated test coverage
- Improve configuration and logging
- Deploy the API to a hosting service
- Add a database for conversation storage

## Learning Goals

This project was built to practice AI API integration, REST API development, request validation, error handling, persistence, and automated testing.