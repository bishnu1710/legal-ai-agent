# @bishnu- legal_ai_agent llm.py

import os
import time
from groq import Groq
from dotenv import load_dotenv

# LOAD ENV FILE
load_dotenv()

def call_llm(prompt: str, max_tokens: int = 600) -> str:
    try:
        time.sleep(1)

        # GET API KEY FROM .env
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            return "❌ ERROR: GROQ_API_KEY not found in .env"

        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Be concise and structured."},
                {"role": "user", "content": prompt[:5000]}  # limit tokens
            ],
            temperature=0.3,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ LLM Error: {str(e)}"