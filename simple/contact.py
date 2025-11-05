import os

import requests

inbox_id = os.getenv("INBOX_ID", "9999999")
account_id = os.getenv("ACCOUNT_ID", "9999999")

url = f"http://experience.experience:3000/api/v1/accounts/{account_id}/contacts"

payload = {
    "inbox_id": inbox_id,
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

print(response.json())
