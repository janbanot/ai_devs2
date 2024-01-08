import os
from dotenv import load_dotenv
from ai_devs_task import Task
from typing import Dict, Any

load_dotenv()
ai_devs_api_key: str = os.getenv("AI_DEVS_API_KEY", "")

optimaldb: Task = Task(ai_devs_api_key, "optimaldb")
token: str = optimaldb.auth()
task_content: Dict[str, Any] = optimaldb.get_content(token)
print(task_content)
db_url: str = task_content["database"]
