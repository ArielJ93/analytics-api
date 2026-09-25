import requests
from src.config import settings

if settings.GROQ_API_KEY == "":
    raise NotImplementedError("The API KEY is missing")

api_key = settings.GROQ_API_KEY
url = "https://api.groq.com/openai/v1/models"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

print(response.json())