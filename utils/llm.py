import os
import time
from groq import Groq
from dotenv import load_dotenv

# LOAD ENV FILE
load_dotenv()

def call_llm(prompt: str) -> str:
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
                {"role": "user", "content": prompt[:2000]}  # limit tokens
            ],
            temperature=0.3,
            max_tokens=400
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ LLM Error: {str(e)}"