import os
from typing import Dict, Any
from dotenv import load_dotenv
from ai_devs_task import Task

load_dotenv()
ai_devs_api_key: str = os.getenv("AI_DEVS_API_KEY", "")

helloapi: Task = Task(ai_devs_api_key, "helloapi")

token: str = helloapi.auth()
task_content: Dict[str, Any] = helloapi.get_content(token)

cookie: str = task_content["cookie"]
answer_payload: Dict[str, str] = {"answer": cookie}

task_result: Dict[str, Any] = helloapi.post_answer(token, answer_payload)
print(task_result)
