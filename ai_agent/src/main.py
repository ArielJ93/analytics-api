from groq import Groq
from src.config import settings

if settings.GROQ_API_KEY == "":
    raise NotImplementedError("The API KEY is missing")

if settings.AI_MODEL == "":
    raise NotImplementedError("The AI Model is not implemented")

client = Groq(api_key=settings.GROQ_API_KEY)

stream = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
        "role": "user",
        "content": "Explain the importance of fast language models"
    }],
    model= settings.AI_MODEL,

    temperature=0.5,

    max_completion_tokens=1024,
    
    top_p=1,

    stop=None,

    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content, end="")