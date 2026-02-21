import requests

url = "http://127.0.0.1:5000/analyze"
data = {
    "message": "you are stupid",   # toxic message for testing
    "email": "testuser@gmail.com"
}

res = requests.post(url, json=data)
print("Response:", res.json())
