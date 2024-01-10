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
task_content: Dict[str, Any] = google.get_content(token)
print(task_content)
