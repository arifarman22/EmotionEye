import requests

url = "http://127.0.0.1:5000/chat"
data = {
    "message": "I feel really anxious and scared about my future."
}

response = requests.post(url, json=data)
print(response.json())
