import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

print("Models supporting bidiGenerateContent (Live):")
for m in client.models.list():
    if "bidiGenerateContent" in m.supported_actions:
        print(f"  {m.name}")