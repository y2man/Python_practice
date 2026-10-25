import os

result = {
    "choices": [
        {
            "message": {
                "content": None
            }
        }
    ]
}

reply = result.get("choices", [])[0].get("message", {}).get("content", "No answer available")