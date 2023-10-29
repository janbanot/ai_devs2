import requests
import json


class Task:
    def __init__(self, ai_devs_api_key, name):
        self.ai_devs_api_key = ai_devs_api_key
        self.name = name
        self.url = "https://zadania.aidevs.pl"

    def auth(self):
        auth_url = f"{self.url}/token/{self.name}"
        data = {"apikey": self.ai_devs_api_key}
        response = requests.post(auth_url, json=data)
        response_json = json.loads(response.text)
        # TODO: add error handling
        return response_json['token']

    def get_content(self, token):
        get_content_url = f"{self.url}/task/{token}"
        response = requests.get(get_content_url)
        # TODO: add error handling
        return json.loads(response.text)

    def post_answer(self, token, answer_payload):
        answer_url = f"{self.url}/answer/{token}"
        response = requests.post(answer_url, json=answer_payload)
        # TODO: add error handling
        return json.loads(response.text)
