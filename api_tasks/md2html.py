import os
from dotenv import load_dotenv
from ai_devs_task import Task
from typing import Dict, Any

load_dotenv()
ai_devs_api_key: str = os.getenv("AI_DEVS_API_KEY", "")

md2html: Task = Task(ai_devs_api_key, "md2html")
token: str = md2html.auth()
endpoint = "test_api_url"
answer_payload: Dict[str, Any] = {"answer": endpoint}
task_result: Dict[str, Any] = md2html.post_answer(token, answer_payload)
print(task_result)
