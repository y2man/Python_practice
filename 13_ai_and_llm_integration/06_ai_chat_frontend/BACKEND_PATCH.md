# Isaac AI backend patch

Apply these changes to `main.py`. Your existing `models.py` already has `Message.id`, so no schema migration is needed.

## 1. Add request model

```python
class EditMessageRequest(BaseModel):
    message_id: int
    prompt: str = Field(min_length=1, max_length=2000)

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Prompt cannot be empty.")
        return value
```

## 2. Include message IDs in GET conversation

In the `messages` list returned by `GET /conversations/{conversation_id}`, add:

```python
"id": message.id,
```

## 3. Add regenerate and edit-and-resend endpoints

Use the endpoint implementations supplied in the accompanying conversation response. Both must verify ownership with `Conversation.user_id == current_user.id`, build the Groq context from messages preceding the target, and commit changes only after Groq returns a non-empty answer.

For edit-and-resend, delete the selected user message and all later messages, then save the edited user message and its new assistant response. For regenerate, retain the latest user message, delete later assistant output, and save the replacement answer.

## Important Stop behavior

The current browser AbortController only stops the client from waiting. It does not reliably cancel a synchronous Groq request already running on the server. Do not describe it as server-side cancellation.
