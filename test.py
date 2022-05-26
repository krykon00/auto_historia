import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + 'd/sdasd/asdasd/30112017')
print(response.json())