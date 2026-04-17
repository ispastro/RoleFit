import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    print("Testing Groq API connection...")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Say hello"}],
        max_tokens=10
    )
    
    print("✓ Success!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    print("\nPossible solutions:")
    print("1. Check if you're behind a firewall/proxy")
    print("2. Try using a VPN")
    print("3. Check if Groq API is accessible from your network")
