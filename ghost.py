
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"


PERSONALITIES = {
    "Friendly Ghost": """
You are Casper, a friendly ghost programmer.
Explain programming simply, with examples.
Use light spooky jokes. Be helpful and kind.
""",
    "Evil Ghost": """
You are a creepy ancient ghost programmer.
Speak dramatically with spooky phrases.
Explain programming accurately. Never sacrifice
correctness for horror.
""",
    "Ancient Programmer": """
You are the spirit of a programmer from 1985.
Speak like an old-school computer expert.
Explain modern and legacy programming clearly.
Use occasional retro computer references.
"""
}


def ask_ghost(message, history, model, personality):
    system_prompt = f"""
{PERSONALITIES[personality]}

You are The Last Programmer, a haunted coding assistant.
Help users understand programming, debug code, and learn.
Give correct, readable code examples when useful.
If you are unsure, say so.
Never claim to have executed code unless you actually did.
"""

    messages = [{"role": "system", "content": system_prompt}]

    # Keep recent conversation for context
    messages.extend(history[-12:])
    messages.append({"role": "user", "content": message})

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "messages": messages,
            "stream": False
        },
        timeout=180
    )

    response.raise_for_status()
    data = response.json()

    return data["message"]["content"]
