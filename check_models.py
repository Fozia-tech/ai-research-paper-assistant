import os
from dotenv import load_dotenv
from google import genai

# -------------------------
# FIX SSL ISSUES (IMPORTANT FOR WINDOWS)
# -------------------------
os.environ.pop("SSL_CERT_FILE", None)
os.environ.pop("REQUESTS_CA_BUNDLE", None)

# -------------------------
# Load API key from .env
# -------------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ GEMINI_API_KEY not found in .env file")
    exit()

# -------------------------
# Create Gemini client
# -------------------------
client = genai.Client(api_key=api_key)

# -------------------------
# List available models
# -------------------------
print("\n✅ Available Gemini Models:\n")

for m in client.models.list():
    print(m.name)