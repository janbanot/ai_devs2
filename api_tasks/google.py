import os
from dotenv import load_dotenv
from ai_devs_task import Task
from typing import Dict, Any
from openai import OpenAI

load_dotenv()
ai_devs_api_key: str = os.getenv("AI_DEVS_API_KEY", "")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

google: Task = Task(ai_devs_api_key, "google")
token: str = google.auth()
endpoint = "test_api_url"
answer_payload: Dict[str, Any] = {"answer": endpoint}
task_result: Dict[str, Any] = google.post_answer(token, answer_payload)
print(task_result)
