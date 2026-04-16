import requests
import json

API_URL = "http://localhost:8000"

def test_health():
    print("Testing health endpoint...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_tailor():
    print("Testing tailor endpoint...")
    job_desc = """
    Senior Full-Stack Engineer
    - Experience with FastAPI and React
    - Build scalable APIs
    - Work with AWS
    """
    
    response = requests.post(
        f"{API_URL}/api/tailor",
        json={"job_description": job_desc}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Message: {data['message']}")
        print(f"Download URL: {data['download_url']}")
    else:
        print(f"Error: {response.text}")
    print()

if __name__ == "__main__":
    try:
        test_health()
        test_tailor()
    except Exception as e:
        print(f"Error: {e}")
