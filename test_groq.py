
import os
from groq import Groq

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing")

client = Groq(api_key=api_key)

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": "Explain an LLM API in two simple sentences."
        }
    ],
)

print(response.choices[0].message.content)
