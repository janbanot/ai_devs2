import requests  # type: ignore
import json
from typing import Dict, Any


class Task:
    def __init__(self, ai_devs_api_key: str, name: str):
        self.ai_devs_api_key: str = ai_devs_api_key
        self.name: str = name
        self.url: str = "https://zadania.aidevs.pl"

    def auth(self) -> str:
        auth_url: str = f"{self.url}/token/{self.name}"
        data: Dict[str, str] = {"apikey": self.ai_devs_api_key}
        response = requests.post(auth_url, json=data)
        response_json: Dict[str, Any] = json.loads(response.text)
        # TODO: add error handling
        return response_json["token"]

    def get_content(self, token: str) -> Dict[str, Any]:
        try:
            get_content_url: str = f"{self.url}/task/{token}"
            response = requests.get(get_content_url)
            return json.loads(response.text)
        except Exception as e:
            print(f"An error occurred: {e}")
            return {}

    def post_question(self, token: str, question: Dict[str, str]) -> Dict[str, Any]:
        post_question_url: str = f"{self.url}/task/{token}"
        response = requests.post(post_question_url, data=question)
        return json.loads(response.text)

    def post_answer(self, token: str, answer_payload: Dict[str, Any]) -> Dict[str, Any]:
        answer_url: str = f"{self.url}/answer/{token}"
        response = requests.post(answer_url, json=answer_payload)
        # TODO: add error handling
        return json.loads(response.text)
