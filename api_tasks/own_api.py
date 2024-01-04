import os
from dotenv import load_dotenv
from ai_devs_task import Task
from typing import Dict, Any


load_dotenv()
ai_devs_api_key: str = os.getenv("AI_DEVS_API_KEY", "")

ownapi: Task = Task(ai_devs_api_key, "ownapi")
token: str = ownapi.auth()
endpoint = "https://brightside.bieda.it/answer"
answer_payload: Dict[str, Any] = {"answer": endpoint}
task_result: Dict[str, Any] = ownapi.post_answer(token, answer_payload)
print(task_result)
