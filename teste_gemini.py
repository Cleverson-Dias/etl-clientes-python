from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY não encontrada")

client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model="gemini-1.0-pro",
    contents="Diga olá em português"
)

print(response.text)
