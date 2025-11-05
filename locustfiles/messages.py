import os

from faker import Faker
from locust import HttpUser, task

fake = Faker()


class ContactFailedException(Exception):
    pass


class ConversationFailedException(Exception):
    pass


class MessageFailedException(Exception):
    pass


class MessageUser(HttpUser):
    def create_contact(self):
        print("Creating Contact")
        name: str = fake.name()
        email: str = fake.email()
        payload = {"inbox_id": self.inbox_id, "name": name, "email": email}
        response = self.client.post(
            f"/api/v1/accounts/{self.account_id}/contacts",
            json=payload,
            headers=self.headers,
        )

        if response.status_code == 200:
            json_response_dict = response.json()
            return str(json_response_dict["payload"]["contact_inbox"]["source_id"])
        else:
            try:
                print("response status code is: ", response.status_code)
                print("response body is: ", response.json())
                raise ContactFailedException("Contact Creation Failed")
            except Exception as e:
                raise ContactFailedException("Contact Creation Failed") from e

    def create_conversation(self):
        print("Creating Conversation")
        payload = {"source_id": self.contact_source_id}
        response = self.client.post(
            f"/api/v1/accounts/{self.account_id}/conversations",
            json=payload,
            headers=self.headers,
        )

        if response.status_code == 200:
            json_response_dict = response.json()
            return str(json_response_dict["id"])
        else:
            try:
                print("response status code is: ", response.status_code)
                print("response body is: ", response.json())
                raise ConversationFailedException("Conversation Creation Failed")
            except Exception as e:
                raise ConversationFailedException("Conversation Creation Failed") from e

    def on_start(self):
        self.api_access_token = os.getenv("API_ACCESS_TOKEN", "99999")
        self.account_id = os.getenv("ACCOUNT_ID", "99999")
        self.inbox_id = os.getenv("INBOX_ID", "99999")
        self.headers = {
            "api_access_token": self.api_access_token,
            "Content-type": "application/json",
        }

        # Only create one new contact an conversation per run
        print("Starting Create Contact")
        self.contact_source_id = self.create_contact()
        # print("Starting Create Conversation")
        # self.conversation_id = self.create_conversation()

    @task
    def send_message(self):
        print("Sending Message")
        message_body: str = fake.sentence()
        payload = {
            "content": message_body,
            "message_type": "incoming",
            "private": False,
        }
        response = self.client.post(
            f"/api/v1/accounts/{self.account_id}/conversations/{self.conversation_id}/messages",
            json=payload,
            headers=self.headers,
        )

        if response.status_code == 200:
            print("Message sent successfully")
        else:
            print("Failed to send message")
            print("response status code is: ", response.status_code)
            print("response body is: ", response.json())
            raise MessageFailedException("Message Sending Failed")
