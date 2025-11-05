import os

import requests

# url = "https://experience.robert-dev.dev.avelabs.ai/app/accounts/1/contacts"
url = "http://127.0.0.1:3000/api/v1/accounts/2/contacts"

payload = {
    "inbox_id": 1,
    "name": "Alice",
    "email": "alice@acme.inc",
    "blocked": False,
    "phone_number": "+123456789",
    "avatar_url": "https://example.com/avatar.png",
    "identifier": "1234567890",
    "additional_attributes": {"type": "customer", "age": 30},
    "custom_attributes": {},
}
headers = {
    "api_access_token": os.getenv("API_ACCESS_TOKEN"),
    "Content-Type": "application/json",
}

response = requests.post(url, json=payload, headers=headers)

print("Response Status Code:", response.status_code)
print("Response Body:", response.json())
