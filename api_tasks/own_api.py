import os
import openai
from dotenv import load_dotenv
from ai_devs_task import Task
from typing import Dict, Any

load_dotenv()
ai_devs_api_key: str = os.getenv("AI_DEVS_API_KEY", "")
openai.api_key = os.getenv("OPENAI_API_KEY", "")

ownapi: Task = Task(ai_devs_api_key, "ownapi")
token: str = ownapi.auth()
task_content: Dict[str, Any] = ownapi.get_content(token)
print(task_content)
